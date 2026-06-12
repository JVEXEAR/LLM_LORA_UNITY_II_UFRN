# LLM_LORA_UNITY_II_UFRN
Second avaliation about LLM, by teacher PhD Thommas Kevin Sales Flores.
* Structury of Project:

```
| .gitignore
| README.md
│ requirements.txt
| All models
  ├─── Main.py
  ├─── static
    ├─── index.html
| model1
  ├─── lora_finetuned_model.ipynb
  ├─── avaliacao_modelo_finetuned.ipynb
  ├─── lora_medium.ipynb
  ├─── RAG_llm.ipynb
| model2
  ├─── lora_finetuned_model.ipynb
  ├─── avaliacao_modelo_finetuned.ipynb
  ├─── lora_medium.ipynb
  ├─── RAG_llm.ipynb
| model3
  ├─── lora_finetuned_model.ipynb
  ├─── avaliacao_modelo_finetuned.ipynb
  ├─── lora_medium.ipynb
  ├─── RAG_llm.ipynb
| model4
  ├─── lora_finetuned_model.ipynb
  ├─── avaliacao_modelo_finetuned.ipynb
  ├─── lora_medium.ipynb
  ├─── RAG_llm.ipynb
```
* How to use:
```
* Create a folder with theses folders

* Inside on the folder first created, open Terminal in her folder and Type:  python -m venv . venv

* For activate the .venv:
  # Linux / macOS: source . venv / bin / activate
  # Windows(Command Prompt): . venv \ Scripts \ activate

* Installing Packages:
  First: put on requirements.txt = transformers datasets pypdf2 accelerate sentencepiece torch accelerate pdfplumber
  Then: !pip install -requirements.txt

* On .gitignore put:

# Python virtual environment
. venv /
venv /
env /

# Python cache files
__pycache__ /
*. pyc
*. pyo
*. pyd

# Environment variable files ( sensitive data )
. env
. env . local

# IDE and editor settings
. vscode /
. idea /
*. swp

# Operating system files
. DS_Store # macOS
Thumbs . db # Windows
```

