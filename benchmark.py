import re
import tiktoken

with open("test.ai") as f:
    ai_raw = f.read()
with open("test.py") as f:
    py_raw = f.read()

ai_clean = re.sub(r"\(.*?\)", "", ai_raw, flags=re.DOTALL)
ai_code = "\n".join([line.strip() for line in ai_clean.split("\n") if line.strip()])
py_code = "\n".join([line.split("#")[0].rstrip() for line in py_raw.split("\n") if line.strip()])

enc = tiktoken.get_encoding("cl100k_base")
ai_tokens = len(enc.encode(ai_code))
py_tokens = len(enc.encode(py_code))

ai_attn, py_attn = ai_tokens ** 2, py_tokens ** 2
ai_kv, py_kv = ai_tokens * 64, py_tokens * 64

print("\nBenchmark:")
print(f"  Python:  {py_tokens} tokens | {py_attn} ops | {py_kv:.1f} KB KV cache")
print(f"  .ai:     {ai_tokens} tokens | {ai_attn} ops | {ai_kv:.1f} KB KV cache")

if py_tokens > ai_tokens:
    savings = ((py_tokens - ai_tokens) / py_tokens) * 100
    print(f"  -> .ai saved {savings:.1f}% tokens and VRAM\n")
