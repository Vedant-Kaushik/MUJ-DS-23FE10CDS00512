import sys
import re
import importlib

class StackVM:
    def __init__(self):
        self.stack = []
        self.memory = {}
        self.functions = {}
        self.call_stack = []
        self.loop_anchors = []
        self.ip = 0

    def _resolve(self, item):
        if not isinstance(item, str): 
            return item
        if item.upper() == "TRUE": 
            return True
        if item.upper() == "FALSE": 
            return False
        if (item.startswith('"') and item.endswith('"')) or (item.startswith("'") and item.endswith("'")):
            return item[1:-1]
        if item in self.memory: 
            return self.memory[item]
        raise NameError(f"name '{item}' is not defined")

    def run(self, src):
        cleaned = re.sub(r"\((.*?)\)", "", src, flags=re.DOTALL)
        tokens = re.findall(r'"[^"]*"|\S+', cleaned.strip())
        self.ip = 0

        while self.ip < len(tokens):
            token = tokens[self.ip]
            tok_up = token.upper()

            # 1. Numbers
            if token.isdigit() or (token.startswith("-") and len(token) > 1 and token[1:].isdigit()):
                self.stack.append(int(token))

            # 2. Arithmetic (+, -, *, /, %)
            elif tok_up in ["+", "-", "*", "/", "%"]:
                b = self._resolve(self.stack.pop())
                a = self._resolve(self.stack.pop())
                if tok_up == "+": self.stack.append(a + b)
                elif tok_up == "-": self.stack.append(a - b)
                elif tok_up == "*": self.stack.append(a * b)
                elif tok_up == "/": self.stack.append(a // b if isinstance(a, int) and isinstance(b, int) else a / b)
                elif tok_up == "%": self.stack.append(a % b)

            # 3. Comparisons (==, !=, <, >, <=, >=)
            elif tok_up in ["==", "!=", "<", ">", "<=", ">="]:
                b = self._resolve(self.stack.pop())
                a = self._resolve(self.stack.pop())
                if tok_up == "==": self.stack.append(a == b)
                elif tok_up == "!=": self.stack.append(a != b)
                elif tok_up == "<": self.stack.append(a < b)
                elif tok_up == ">": self.stack.append(a > b)
                elif tok_up == "<=": self.stack.append(a <= b)
                elif tok_up == ">=": self.stack.append(a >= b)

            # 4. Variable Assignment (=)
            elif tok_up == "=":
                name = self.stack.pop().strip('"').strip("'")
                self.memory[name] = self._resolve(self.stack.pop())

            # 5. Stack Operations (DUP, DROP, SWAP)
            elif tok_up == "DUP": 
                self.stack.append(self.stack[-1])
            elif tok_up == "DROP": 
                self.stack.pop()
            elif tok_up == "SWAP": 
                self.stack[-1], self.stack[-2] = self.stack[-2], self.stack[-1]

            # 6. Loops (START ... WHILE ... REPEAT)
            elif tok_up == "START":
                self.loop_anchors.append(self.ip)
            elif tok_up == "WHILE":
                cond = self._resolve(self.stack.pop())
                if not cond:
                    if self.loop_anchors: 
                        self.loop_anchors.pop()
                    depth = 1
                    while self.ip < len(tokens) - 1 and depth > 0:
                        self.ip += 1
                        if tokens[self.ip].upper() == "START": depth += 1
                        elif tokens[self.ip].upper() == "REPEAT": depth -= 1
            elif tok_up == "REPEAT":
                if self.loop_anchors: 
                    self.ip = self.loop_anchors[-1]

            # 7. Functions (FUNC <name> ... RET)
            elif tok_up == "FUNC":
                self.ip += 1
                name = tokens[self.ip]
                self.functions[name] = self.ip + 1
                depth = 1
                while self.ip < len(tokens) - 1 and depth > 0:
                    self.ip += 1
                    if tokens[self.ip].upper() == "FUNC": depth += 1
                    elif tokens[self.ip].upper() == "RET": depth -= 1
            elif tok_up == "RET":
                frame = self.call_stack.pop()
                self.ip = frame["return_ip"]

            # 8. Printing & Imports
            elif tok_up == "PRINT":
                print(self._resolve(self.stack.pop()))
            elif tok_up == "IMPORT":
                mod = self.stack.pop().strip('"').strip("'")
                self.stack.append(importlib.import_module(mod))

            # 9. Function Calls & Identifiers
            elif token in self.functions:
                self.call_stack.append({"return_ip": self.ip, "func_name": token})
                self.ip = self.functions[token]
                continue
            else:
                self.stack.append(token)

            self.ip += 1

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "test.ai"
    try:
        with open(target, "r") as f:
            src = f.read()
    except FileNotFoundError:
        print(f"Error: Could not find '{target}'")
        sys.exit(1)

    vm = StackVM()
    vm.run(src)
