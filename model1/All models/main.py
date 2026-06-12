# =============================================================================
# LABORATÓRIO: Clone do ChatGPT com FastAPI + Modelos HuggingFace (LoRA)
# =============================================================================
# Este arquivo é o coração da aplicação. Ele:
#   1. Carrega os modelos de linguagem (base e fine-tunado com LoRA)
#   2. Expõe uma API REST via FastAPI
#   3. Serve o front-end estático (HTML/CSS/JS)
#   4. Processa mensagens do usuário e retorna respostas geradas pelos modelos
# =============================================================================

# --- Importações padrão do Python ---
import os
import logging
from typing import Optional

# --- Importações do FastAPI ---
# FastAPI: framework moderno para criação de APIs em Python
# StaticFiles: serve arquivos estáticos (HTML, CSS, JS)
# HTMLResponse: retorna respostas HTTP em HTML
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# --- Pydantic: validação de dados ---
# BaseModel: classe base para definir o "shape" dos dados que a API recebe/envia
from pydantic import BaseModel

# --- HuggingFace Transformers ---
# AutoModelForCausalLM : carrega qualquer modelo de geração de texto automaticamente
# AutoTokenizer        : carrega o tokenizador correspondente ao modelo
# pipeline             : abstração de alto nível para tarefas de NLP
from transformers import (
    AutoModelForCausalLM,
    AutoModelForSeq2SeqLM,
    AutoTokenizer
)
# --- PyTorch ---
# Biblioteca de deep learning; usada para inferência nos modelos
import torch

# =============================================================================
# CONFIGURAÇÃO DE LOGGING
# =============================================================================
# Configura o sistema de logs para exibir mensagens informativas no terminal
# Isso ajuda a acompanhar o que está acontecendo durante a execução

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# =============================================================================
# INSTÂNCIA DA APLICAÇÃO FASTAPI
# =============================================================================
# Criamos o objeto principal da aplicação.
# O título e a versão aparecem na documentação automática em /docs

app = FastAPI(
    title="ChatGPT Clone - Laboratório LLM",
    description="API para interagir com modelos de linguagem (base e fine-tunado com LoRA) Por João Vitor(Aluno da UFRN - CERES)",
    version="1.0.0",
)

# --- Middleware CORS ---
# CORS (Cross-Origin Resource Sharing) permite que o navegador faça requisições
# de uma origem diferente da API. Em laboratório, permitimos tudo ("*").
# Em produção, restrinja para domínios específicos!
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Permite qualquer origem
    allow_methods=["*"],   # Permite qualquer método HTTP (GET, POST, etc.)
    allow_headers=["*"],   # Permite qualquer cabeçalho
)

# =============================================================================
# DICIONÁRIO GLOBAL DE MODELOS
# =============================================================================
# Armazena os modelos e tokenizadores já carregados em memória.
# Usar um dicionário evita recarregar o modelo a cada requisição (muito lento!).
# Chave   → nome amigável do modelo (string)
# Valor   → dicionário com "model", "tokenizer" e "pipeline"

MODELS: dict = {}

# =============================================================================
# CARREGAMENTO DOS MODELOS
# =============================================================================
# =============================================================================
# CONFIGURAÇÃO DOS MODELOS
# =============================================================================

MODELOS_CONFIG = {

    # -------------------------------------------------
    # MODELOS CAUSAIS
    # -------------------------------------------------

    "jinaai/ReaderLM-v2": {
        "path": "/home/joaovitor/Documents/Faculdade/1°Semestre/Tópicos avançados em Inteligência Artificial A/Second Avaliation/model1/lora_finetuned_model01",
        "tipo": "causal",
        "tokenizer": "/home/joaovitor/Documents/Faculdade/1°Semestre/Tópicos avançados em Inteligência Artificial A/Second Avaliation/model1/tokenizer"
    },

    "LiquidAI/LFM2.5-1.2B-JP-202606": {
        "path": "/home/joaovitor/Documents/Faculdade/1°Semestre/Tópicos avançados em Inteligência Artificial A/Second Avaliation/model2/lora_finetuned_model02",
        "tipo": "causal",
        "tokenizer": "/home/joaovitor/Documents/Faculdade/1°Semestre/Tópicos avançados em Inteligência Artificial A/Second Avaliation/model2/tokenizer"
    },

    # -------------------------------------------------
    # MODELOS SEQ2SEQ
    # -------------------------------------------------

    "google/flan-t5-large": {
        "path": "/home/joaovitor/Documents/Faculdade/1°Semestre/Tópicos avançados em Inteligência Artificial A/Second Avaliation/model3/lora_finetuned_model03",
        "tipo": "seq2seq",
        "tokenizer": "/home/joaovitor/Documents/Faculdade/1°Semestre/Tópicos avançados em Inteligência Artificial A/Second Avaliation/model3/tokenizer"
    },

    "Den4ikAI/FRED-T5-XL_instructor_chitchat": {
        "path": "/home/joaovitor/Documents/Faculdade/1°Semestre/Tópicos avançados em Inteligência Artificial A/Second Avaliation/model4/lora_finetuned_model04",
        "tipo": "seq2seq",
        "tokenizer": "/home/joaovitor/Documents/Faculdade/1°Semestre/Tópicos avançados em Inteligência Artificial A/Second Avaliation/model4/tokenizer"
    }
}

# =============================================================================
# DICIONÁRIO GLOBAL
# =============================================================================


# =============================================================================
# CARREGAMENTO GENÉRICO
# =============================================================================

def carregar_modelo(
    model_path: str,
    model_type: str,
    tokenizer_path: str = None
):

    tok_path = tokenizer_path if tokenizer_path else model_path

    tokenizer = AutoTokenizer.from_pretrained(tok_path)

    if tokenizer.pad_token is None and tokenizer.eos_token is not None:
        tokenizer.pad_token = tokenizer.eos_token

    if model_type == "causal":

        model = AutoModelForCausalLM.from_pretrained(
            model_path
        )

    elif model_type == "seq2seq":

        model = AutoModelForSeq2SeqLM.from_pretrained(
            model_path
        )

    else:

        raise ValueError(
            f"Tipo de modelo inválido: {model_type}"
        )

    model.eval()

    return {
        "model": model,
        "tokenizer": tokenizer,
        "tipo": model_type
    }

# =============================================================================
# EVENTO DE INICIALIZAÇÃO DA APLICAÇÃO
# =============================================================================
# Este bloco é executado UMA VEZ quando o servidor FastAPI sobe.
# É o lugar ideal para carregar recursos pesados (modelos, conexões de banco, etc.)

@app.on_event("startup")
async def startup_event():

    global MODELS

    logger.info("=" * 60)
    logger.info("INICIANDO SERVIDOR - Carregando modelos")
    logger.info("=" * 60)

    for nome, cfg in MODELOS_CONFIG.items():

        try:

            MODELS[nome] = carregar_modelo(
                model_path=cfg["path"],
                model_type=cfg["tipo"],
                tokenizer_path=cfg.get("tokenizer")
            )

            logger.info(
                f"✓ {nome} ({cfg['tipo']}) carregado"
            )

        except Exception as e:

            logger.error(
                f"✗ Erro ao carregar {nome}: {e}"
            )

    logger.info(
        f"{len(MODELS)} modelo(s) carregado(s)"
    )

# =============================================================================
# MODELOS PYDANTIC (Schemas de Request/Response)
# =============================================================================
# Pydantic valida automaticamente os dados recebidos pela API.
# Se o JSON não bater com o schema, FastAPI retorna 422 Unprocessable Entity.

class ChatRequest(BaseModel):
    """
    Schema da requisição de chat.

    Campos:
      - modelo   : nome do modelo a usar (deve existir em MODELS)
      - mensagem : texto do usuário
      - max_tokens: máximo de tokens a gerar na resposta (padrão: 150)
      - temperatura: controla aleatoriedade (0.0 = determinístico, 1.0 = criativo)
    """
    modelo: str
    mensagem: str
    max_tokens: Optional[int] = 150
    temperatura: Optional[float] = 0.7


class ChatResponse(BaseModel):
    """
    Schema da resposta de chat.

    Campos:
      - resposta : texto gerado pelo modelo
      - modelo   : qual modelo foi usado
      - tokens_gerados: quantidade de tokens na resposta
    """
    resposta: str
    modelo: str
    tokens_gerados: int


# =============================================================================
# ENDPOINTS DA API
# =============================================================================

@app.get("/modelos", response_class=JSONResponse)
async def listar_modelos():

    return {
        "modelos": [
            {
                "id": nome,
                "nome": nome,
                "tipo": dados["tipo"]
            }
            for nome, dados in MODELS.items()
        ]
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):

    if request.modelo not in MODELS:
        raise HTTPException(
            status_code=404,
            detail=f"Modelo '{request.modelo}' não encontrado."
        )

    if not request.mensagem.strip():
        raise HTTPException(
            status_code=400,
            detail="A mensagem não pode ser vazia."
        )

    logger.info(
        f"[CHAT] Modelo='{request.modelo}' | "
        f"Mensagem='{request.mensagem[:50]}...'"
    )

    try:

        tokenizer = MODELS[request.modelo]["tokenizer"]
        model = MODELS[request.modelo]["model"]
        tipo = MODELS[request.modelo]["tipo"]

        inputs = tokenizer(
            request.mensagem,
            return_tensors="pt",
            truncation=True
        )

        with torch.no_grad():

            outputs = model.generate(
                **inputs,
                max_new_tokens=request.max_tokens,
                do_sample=True,
                temperature=request.temperatura,
                top_p=0.9,
                pad_token_id=tokenizer.pad_token_id
            )

        texto_completo = tokenizer.decode(
            outputs[0],
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False
        ).strip()

        if tipo == "causal":

            if texto_completo.startswith(
                request.mensagem
            ):
                resposta = texto_completo[
                    len(request.mensagem):
                ].strip()
            else:
                resposta = texto_completo

        else:

            resposta = texto_completo

        if not resposta:

            resposta = (
                "[O modelo não gerou texto adicional. "
                "Tente aumentar max_tokens.]"
            )

        tokens_gerados = len(
            tokenizer.encode(resposta)
        )

        logger.info(
            f"✓ Resposta gerada: "
            f"{tokens_gerados} tokens"
        )

        return ChatResponse(
            resposta=resposta,
            modelo=request.modelo,
            tokens_gerados=tokens_gerados
        )

    except Exception as e:

        logger.error(
            f"Erro na geração: {str(e)}"
        )

        raise HTTPException(
            status_code=500,
            detail=f"Erro ao gerar resposta: {str(e)}"
        )

@app.get("/health")
async def health_check():
    """
    GET /health

    Endpoint de verificação de saúde do servidor.
    Retorna quais modelos estão carregados e prontos para uso.
    Útil para monitoramento e debugging em laboratório.
    """
    return {
        "status": "ok",
        "modelos_carregados": list(MODELS.keys()),
        "quantidade": len(MODELS)
    }


# =============================================================================
# SERVIR O FRONT-END (HTML/CSS/JS)
# =============================================================================
# Monta o diretório "static" para servir arquivos estáticos.
# O index.html será acessível em http://localhost:8000/

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def root():
    """
    GET /

    Serve a página principal do chat.
    Lê o arquivo HTML do diretório static/ e retorna seu conteúdo.
    """
    html_path = os.path.join("static", "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


# =============================================================================
# PONTO DE ENTRADA (execução direta)
# =============================================================================
# Este bloco só executa quando rodamos `python main.py` diretamente.
# Em produção, usa-se `uvicorn main:app` para melhor controle.

if __name__ == "__main__":
    import uvicorn

    # uvicorn: servidor ASGI de alta performance para aplicações FastAPI/Starlette
    # host="0.0.0.0"  → aceita conexões de qualquer IP (necessário em laboratório)
    # port=8000       → porta padrão da aplicação
    # reload=True     → reinicia automaticamente ao salvar alterações no código
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Desative em produção!
    )
