# Chat com Arquivos PDF

Este projeto permite interagir com documentos PDF através de um chatbot utilizando Streamlit e OpenAI. Ele processa arquivos PDF carregados pelo usuário e responde a perguntas baseando-se exclusivamente no conteúdo extraído dos documentos.

## 🚀 Funcionalidades

- Upload de múltiplos arquivos PDF
- Extração de texto dos documentos enviados
- Chat interativo com memória de conversação
- Respostas baseadas no conteúdo dos PDFs carregados

## 🛠 Tecnologias Utilizadas

- Python
- Streamlit
- LangChain
- OpenAI API (GPT-4o)
- PyPDFLoader

## 📌 Pré-requisitos

Antes de executar o projeto, certifique-se de ter instalado:

- Python 3.8+
- Uma chave de API da OpenAI, definida na variável de ambiente `OPENAI_API_KEY`

## 📥 Instalação

1. Clone este repositório:

    ```
    git clone https://github.com/luizelias8/chat-com-pdfs.git
    cd chat-com-pdfs
    ```

2. Crie um ambiente virtual e ative-o:

    ```
    python -m venv venv
    source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
    ```

3. Instale as dependências:
    ```
    pip install -r requirements.txt
    ```

4. Configure sua chave de API:
    ```
    export OPENAI_API_KEY='sua-chave-aqui'  # No Windows, use `set OPENAI_API_KEY=sua-chave-aqui`
    ```

## ▶️ Como Usar

1. Execute a aplicação:

    ```
    streamlit run app.py
    ```

2. Acesse a aplicação no navegador no endereço indicado pelo Streamlit.

3. Faça upload dos arquivos PDF na barra lateral.

4. Digite suas perguntas no chat e obtenha respostas baseadas no conteúdo dos documentos.

## 💡 Sugestões ou problemas?

Sinta-se à vontade para abrir uma issue ou contribuir com melhorias!
