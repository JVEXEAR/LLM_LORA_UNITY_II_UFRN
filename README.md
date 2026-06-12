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
| model3
  ├─── lora_finetuned_model.ipynb
  ├─── avaliacao_modelo_finetuned.ipynb
  ├─── lora_medium.ipynb
| model4
  ├─── lora_finetuned_model.ipynb
  ├─── avaliacao_modelo_finetuned.ipynb
  ├─── lora_medium.ipynb
```
* How to use:
```
* Create a folder with theses folders

* Inside on the folder first created, open Terminal in her folder and Type:  python -m venv . venv

* For activate the .venv:
  # Linux/macOS: source.venv/bin/activate
  # Windows(Command Prompt): .venv\Scripts\activate

* Installing Packages:
  First: put on requirements.txt = transformers datasets pypdf2 accelerate sentencepiece torch accelerate pdfplumber
  Then: !pip install -requirements.txt
```

* On .gitignore put:
```
# Python virtual environment
. venv/
venv/
env/

# Python cache files
__pycache__/
*.pyc
*.pyo
*.pyd

# Environment variable files ( sensitive data )
. env
. env.local

# IDE and editor settings
. vscode/
. idea/
*. swp

# Operating system files
.DS_Store # macOS
Thumbs.db # Windows
```

* To generate the site:
  * Preference use VS Code and install the extesion "Jupyter Notebook" and "Python".
  * After run all codes in this item: RAG_llm.ipynb -> lora_medium.ipynb -> avaliacao_modelo_finetuned.ipynb | OBS: The archive "RAG_llm.ipynb" only exist in first model because its the generate of datast_gerado_500.jsonl
  * The link of site after run is: "http://0.0.0.0:8000/" or "http://127.0.0.1:8000/".

* Images with respost each model:
<img src="Causal 1.png" alt="Model 1">
<img src="Causal 2.png" alt="Model 2" >
<img src="Seq2Seq 1.png" alt="Model 3" >
<img src="Seq2Seq 2.png" alt="Model 4" ">

* Discussion:

| Model | PPL | BLEU | ROUGUE-1 F1 | ROUGUE-2 F1 | Fatihfulness | ROUGUE L | Answer Relevance | Plan Adherende |
|-----|:--:|:-----:|:-----------:|:-----------:|:------------:|:--------:|:-----------:|:-----------:|
| Causal 1 | 344.1 | 2.090 | 0.088 | 0.042 | 0.070 | 0.169 | 0.149 | 0.495 |
| Causal 2 | 54.38 | 2.000 | 0.085 | 0.028 | 0.074 | 0.077 | 0.038 | 0.495 |
| Seq2Seq 1 | 1.880 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.495 |
| Seq2Seq 2 | 1.440 | 4.600 | 0.321 | 0.188 | 0.273 | 0.313 | 0.178 | 0.495 |

<p style="text-align: justify;">

Given these results, it is noticeable that the models were not good at generating data. In the first instance, we saw their responses through the website screenshots. The responses from the causal models were expected, since these models have the capacity to continue the responses provided by the prompts. Seq2Seq models are more expected for language translation, that is, equivalence relationships, so according to the Google Large response, it managed to give exactly the same answer, which is a sign of possible overfitting. However, in other responses, it gave answers very close to what was expected.

Therefore, the most suitable models for implementation are two models, among them, the first Causal and the second Seq2Seq. However, it is clear that their responses are unstable and have a high potential for hallucination. Therefore, it is recommended to use models with higher parameters for better effectiveness. Also on this topic, the Causal models 1 and 2 have an average response time of 5 seconds, which is a bit slow. The
Seq2Seq 1 model has an average time of 1 second, while the second one has 20 seconds, which is unacceptable.

It is important to mention that the computer used for this work was an Acer Aspire GO 15 71P, with an Intel Core I5 ​​13420H processor, 16GB of RAM, integrated Intel HD Graphics video card, and the space occupied by the project was 7.7GB. Given this information, it is clear that the strongest points are the processor and memory, which, even so, took a considerable amount of time for this project, 3 days, to generate the dataset, train the models, and generate the results.
</p>
