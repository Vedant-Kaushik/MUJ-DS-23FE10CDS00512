# MUJ-DS-23FE10CDS00512

**Name**: Vedant Kaushik
**Registration Number**: 23FE10CDS00512
**Branch**: Data Science (DS)
**Batch**: F
**GitHub Username**: Vedant-Kaushik
**Project Title**: .ai StackVM - AI-Native Programming Language for LLM Hardware Efficiency

## Project Overview
This repository contains the deliverables for the capstone project. Our project introduces `.ai`, a Postfix StackVM programming language designed to replace Python AST for LLM code generation. By eliminating syntax overhead (parentheses, colons, indentation), `.ai` achieves:
- ~14% reduction in Token Generation
- ~26% reduction in Attention FLOPs (N^2)
- Lower KV Cache VRAM footprint during inference

## Deliverables
- `code/`: Contains the StackVM engine (`main.py`), LangChain code generator (`write.py`), hardware benchmark (`benchmark.py`), and VS Code syntax extension.
- `resources/`: Contains architectural schematics and VRAM benchmark blueprints.
- `presentations/`: Contains the presentation script and speaking notes.
- `capstone/`: Contains final documentation and installation guide.

## Installation & Usage
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Generate .ai code
python3 code/write.py

# 3. Execute StackVM
python3 code/main.py test.ai

# 4. Run hardware efficiency benchmark
python3 code/benchmark.py
```
