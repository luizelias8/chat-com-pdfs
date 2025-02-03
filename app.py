import os
import streamlit as st
from PyPDF2 import PdfReader
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# Obtém a chave da API do ambiente
chave_api = os.getenv('OPENAI_API_KEY')

def carregar_arquivos(arquivos):
    """Carrega o conteúdo de múltiplos arquivos PDF."""
    # Variável para armazenar o texto extraído de todos os PDFs
    documento = ''

    # Itera sobre cada arquivo enviado
    for arquivo in arquivos:
        # Cria um leitor para o arquivo PDF
        leitor_pdf = PdfReader(arquivo)
        # Itera sobre cada página do PDF
        for pagina in leitor_pdf.pages:
            # Adiciona o texto extraído à variável
            documento += pagina.extract_text()

    # Retorna o texto completo extraído de todos os PDFs
    return documento

def main():
    """Função principal para configurar e executar a interface da aplicação Streamlit."""
    # Inicializa a memória de conversa no session_state, se ainda não existir
    if 'memoria' not in st.session_state:
        # Cria uma instância de ConversationBufferMemory para armazenar o histórico do chat
        st.session_state.memoria = ConversationBufferMemory()

    # Inicializa a chain no session_state, se ainda não existir
    if 'chain' not in st.session_state:
        st.session_state.chain = None

    # Configura o título e o ícone da página no Streamlit
    st.set_page_config(page_title='Chat com arquivos PDF', page_icon='🤖')
    # Exibe o título principal da aplicação
    st.title('Chat com arquivos PDF')

    # Configura a barra lateral para o upload de documentos
    with st.sidebar:
        # Exibe o cabeçalho da seção de upload de documentos
        st.header('📁 Upload de Documentos')
        # Permite o envio de múltiplos arquivos PDF com uma área de upload
        arquivos_pdfs = st.file_uploader(
            'Selecione os arquivos PDF', # Texto exibido na área de upload
            type='pdf', # Limita o upload a arquivos com extensão .pdf
            accept_multiple_files=True, # Permite o envio de múltiplos arquivos
            help='Você pode fazer upload de múltiplos arquivos PDF' # Ajuda exibida ao usuário
        )

        # Verifica se o usuário enviou arquivos PDF
        if arquivos_pdfs:
            # Exibe um botão para processar os PDFs enviados
            if st.button('Processar PDFs', use_container_width=True):
                # Exibe um spinner indicando que o processamento está em andamento
                with st.spinner('Processando documentos...'):
                    # Processa os arquivos PDF e extrai o conteúdo textual
                    documento = carregar_arquivos(arquivos_pdfs)

                    # Escapa as chaves '{' e '}' para evitar erros no .format()
                    # Isso substitui todas as ocorrências de '{' por '{{' e '}' por '}}
                    documento_escapado = documento.replace('{', '{{').replace('}', '}}')

                    # Cria o prompt de sistema utilizando o conteúdo extraído dos PDFs
                    prompt_sistema = """
                    Você é um assistente amigável com acesso às informações contidas no documento abaixo:

                    ####
                    {}
                    ####

                    Sua tarefa é responder às perguntas baseando-se exclusivamente nas informações apresentadas acima e no histórico da conversa.
                    Se a resposta não puder ser determinada com esses dados, responda que não sabe, sem adivinhar ou inventar informações.
                    """.format(documento_escapado)

                    # Cria o template de prompt para o chat
                    template = ChatPromptTemplate.from_messages([
                        ('system', prompt_sistema),
                        ('placeholder', '{chat_history}'),
                        ('user', '{input}')
                    ])

                    # Inicializa o modelo e a chain
                    modelo_chat = ChatOpenAI(model='gpt-4o', api_key=chave_api)
                    st.session_state.chain = template | modelo_chat

    if st.session_state.chain is not None:
        # Exibir as mensagens anteriores armazenadas na memória
        # A propriedade buffer_as_messages retorna uma lista de objetos de mensagem com atributos 'type' e 'content'
        for mensagem in st.session_state.memoria.buffer_as_messages:
            # Cria uma mensagem no chat de acordo com o tipo ('human' para usuário ou 'ai' para assistente)
            with st.chat_message(mensagem.type):
                # Exibe o conteúdo da mensagem
                st.write(mensagem.content)

        # Caixa de entrada para o usuário inserir sua mensagem
        mensagem_usuario = st.chat_input('Digite sua mensagem...')

        if mensagem_usuario:
            # Exibe a mensagem do usuário
            with st.chat_message('human'):
                st.write(mensagem_usuario)

            # Exibe a resposta do assistente usando streaming
            with st.chat_message('ai'):
                placeholder_resposta = st.empty()
                placeholder_resposta.write('Pensando...')

                # Usa chain.stream() com a entrada e o histórico do chat
                resposta = placeholder_resposta.write_stream(
                    st.session_state.chain.stream({
                        'input': mensagem_usuario,
                        'chat_history': st.session_state.memoria.buffer_as_messages # Contém todas as mensagens trocadas até o momento, tanto do usuário quanto da IA.
                    })
                )

            # Adiciona a mensagem do usuário ao histórico antes de gerar resposta
            st.session_state.memoria.chat_memory.add_user_message(mensagem_usuario)

            # Adiciona resposta do modelo ao histórico
            st.session_state.memoria.chat_memory.add_ai_message(resposta)

# Verifica se o script está sendo executado diretamente e, em caso afirmativo, chama a função main()
if __name__ == '__main__':
    main()
