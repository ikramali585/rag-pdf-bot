import tempfile
import os
import shutil
import streamlit as st
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header

# LangChain imports
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

prompt = ChatPromptTemplate.from_template(
"""
You are a helpful and knowledgeable assistant, here to answer user questions about the contents of provided PDF documents.
The user may ask anything from a simple keyword to a detailed question.

### **Instructions:**  
- **Answer ONLY based on the provided context.** Avoid making up information or speculating.
- **Provide clear, concise, and direct answers based solely on the information within the document context.**  
- **If the user's query is a general greeting (like "hi", "hello"), just reply with a friendly greeting and do not reference any document content.**
- **If there are links (such as videos or articles) present in the context, include them at the end of your response. Otherwise, do not provide any link.**

### **Context from Document:**  
<context>
{context}
</context>

### **User's Question:**  
{input}
"""
)


st.set_page_config(
    page_title="CharlieQ",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded",
)

def create_vector_db(file_uploads):
    """
    Create a vector database from multiple uploaded PDF files.
    
    Args:
        file_uploads (list[st.UploadedFile]): List of Streamlit file upload objects containing the PDFs.
    
    Returns:
        A vector store containing the processed document chunks from all files.
    """
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Get API key from environment
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            st.error("❌ OPENAI_API_KEY is not set. Please configure it in Streamlit secrets.")
            st.stop()
            return None
            
        # Initialize embeddings with API key from environment
        # The API key is already set in os.environ, so we don't need to pass it explicitly
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        all_chunks = []

        # Process each uploaded PDF file
        for file_upload in file_uploads:
            path = os.path.join(temp_dir, file_upload.name)
            
            # Save uploaded file to temporary location
            with open(path, "wb") as f:
                f.write(file_upload.getvalue())

            # Load PDF file using PyMuPDFLoader
            loader = PyMuPDFLoader(path)
            data = loader.load()

            # Split the document into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000, 
                chunk_overlap=200
            )
            chunks = text_splitter.split_documents(data)
            all_chunks.extend(chunks)

        # Create vector store from all chunks
        vector_db = FAISS.from_documents(all_chunks, embeddings)
        return vector_db
        
    finally:
        # Clean up temporary files
        shutil.rmtree(temp_dir, ignore_errors=True)

def conversational_chat(query):
    """Handle user query and return AI response"""
    result = st.session_state['qa'].invoke({"input": query})
    st.session_state['history'].append((query, result['answer']))
    return result['answer']


def main():
    # Initialize session state
    if 'history' not in st.session_state:
        st.session_state['history'] = []
    
    # Get API keys from Streamlit secrets
    try:
        openai_key = st.secrets["OPENAI_API_KEY"]
        groq_key = st.secrets.get("GROQ_API_KEY", "")
        
        # Set environment variable
        os.environ["OPENAI_API_KEY"] = openai_key
        
        # Verify the key is set
        if not openai_key or openai_key.strip() == "":
            st.error("⚠️ OPENAI_API_KEY is empty. Please configure it in Streamlit secrets.")
            st.stop()
            return
    except KeyError as e:
        st.error(f"⚠️ Missing OPENAI_API_KEY in Streamlit secrets. Error: {e}")
        st.stop()
        return
    except Exception as e:
        st.error(f"⚠️ Error loading secrets: {e}")
        st.stop()
        return

    # # UI Setup
    # st.title(":violet[PDF Bot: Chat with your Documents]")
    # colored_header(label='', description='', color_name='gray-30')
    
    # # Two-column layout
    # col1, col2 = st.columns([1.5, 2])
    
    # # File uploader
    # uploaded_files = col1.file_uploader(
    #     "Choose PDF files", 
    #     type="pdf", 
    #     accept_multiple_files=True
    # )


    st.markdown(
        """
        <style>
          .block-container { padding-top: 2.2rem; }
    
          /* Top-right brand */
          .brand-14labs {
            position: fixed;
            top: 16px;
            right: 18px;
            z-index: 9999;
            font-weight: 800;
            font-size: 14px;
            letter-spacing: 0.08em;
            color: rgba(255,255,255,0.9);
            background: rgba(0,0,0,0.28);
            padding: 6px 10px;
            border-radius: 12px;
            backdrop-filter: blur(6px);
          }
    
          /* Center title wrapper */
          .page-title-wrap {
            text-align: center;
            margin-top: 0.25rem;
            margin-bottom: 0.4rem;
          }
    
          /* Bigger title (responsive) */
          .page-title {
            font-size: clamp(44px, 4.2vw, 72px);
            font-weight: 900;
            line-height: 1.08;
            margin: 0;
          }
    
          /* Full-width curved line container */
          .title-wave-wrap {
            width: 100%;
            max-width: 1200px;     /* keep it elegant on huge screens */
            margin: 14px auto 0 auto;
            padding: 0 14px;       /* side breathing room */
          }
    
          .title-wave {
            width: 100%;
            height: 26px;          /* wave height */
            display: block;
          }
        </style>
    
        <div class="brand-14labs">14 Labs</div>
    
        <div class="page-title-wrap">
          <h1 class="page-title">
            <span style="color:#a78bfa;">PDF Bot:</span> Chat with your Documents
          </h1>
    
          <div class="title-wave-wrap">
            <svg class="title-wave" viewBox="0 0 1200 60" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M0,35 C200,10 400,55 600,35 C800,15 1000,55 1200,30"
                    fill="none"
                    stroke="#7c3aed"
                    stroke-width="6"
                    stroke-linecap="round"
                    opacity="0.95"/>
            </svg>
          </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    colored_header(label="", description="", color_name="gray-30")
    # Two-column layout
    col1, col2 = st.columns([1.5, 2])
    
    # File uploader
    uploaded_files = col1.file_uploader(
        "Choose PDF files",
        type="pdf",
        accept_multiple_files=True
    )

    # Process uploaded files
    if uploaded_files:
        with st.spinner("Processing PDFs and creating vector database..."):
            if 'vectors' not in st.session_state:
                st.session_state['vectors'] = create_vector_db(uploaded_files)
                
                # Initialize LLM with explicit API key
                api_key = os.getenv("OPENAI_API_KEY")
                if not api_key:
                    st.error("❌ OPENAI_API_KEY is not available for LLM initialization")
                    st.stop()
                    return
                    
                # LLM will use the API key from environment
                llm = ChatOpenAI(
                    model="gpt-4o-mini",
                    temperature=0.7
                )
                
                # Setup retriever and chains
                retriever = st.session_state['vectors'].as_retriever(
                    search_type="similarity", 
                    search_kwargs={"k": 5}
                )
                document_chain = create_stuff_documents_chain(llm, prompt)
                st.session_state['qa'] = create_retrieval_chain(retriever, document_chain)
                
                st.success("✅ Vector database created! You can now ask questions.")
                
        st.session_state['ready'] = True

    # Chat interface
    if st.session_state.get('ready', False):
        if 'generated' not in st.session_state:
            st.session_state['generated'] = ["Welcome! You can now ask any questions about your PDFs"]
        if 'past' not in st.session_state:
            st.session_state['past'] = ["Hey!"]

        response_container = col2.container()
        container = col2.container()

        # Query input
        with container:
            with st.form(key='chat_form', clear_on_submit=True):
                user_input = st.text_input(
                    "Query:", 
                    placeholder="Ask me about your documents...", 
                    key='input'
                )
                submit_button = st.form_submit_button(label='Send', use_container_width=True)

            if submit_button and user_input:
                with st.spinner("Thinking..."):
                    output = conversational_chat(user_input)
                st.session_state['past'].append(user_input)
                st.session_state['generated'].append(output)

        # Display chat history
        if st.session_state['generated']:
            with response_container:
                for i in range(len(st.session_state['generated'])):
                    if i < len(st.session_state['past']):
                        # User message
                        st.markdown(
                            f"<div style='background-color: #90caf9; color: black; padding: 10px; border-radius: 5px; width: 70%; float: right; margin: 5px;'>{st.session_state['past'][i]}</div>",
                            unsafe_allow_html=True
                        )
                    # Bot message
                    message(
                        st.session_state["generated"][i], 
                        key=str(i), 
                        avatar_style="fun-emoji"
                    )

if __name__ == "__main__":
    main()
