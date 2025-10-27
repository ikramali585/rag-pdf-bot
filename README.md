# Charlie Bot - RAG PDF Chatbot

A Streamlit-based RAG (Retrieval-Augmented Generation) chatbot that answers questions from uploaded PDF documents using OpenAI and LangChain.

## Features

- 📄 Upload multiple PDF files
- 🤖 AI-powered question answering
- 🔍 Semantic search using vector embeddings
- 💬 Interactive chat interface
- 🚀 Ready for Streamlit Cloud deployment

## Prerequisites

- Python 3.8+
- OpenAI API key
- Streamlit account (for cloud deployment)

## Local Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd rag-pdf-bot
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   GROQ_API_KEY=your_groq_api_key_here  # Optional, not currently used
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

## Deployment to Streamlit Cloud

1. **Push your code to GitHub**
   - Create a GitHub repository
   - Push your code to the repository

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account
   - Click "New app"
   - Select your repository and branch
   - Set the main file path as `app.py`

3. **Add Secrets**
   - In your Streamlit Cloud dashboard, go to "Settings" → "Secrets"
   - Add your environment variables:
   ```toml
   OPENAI_API_KEY = "your_openai_api_key_here"
   GROQ_API_KEY = "your_groq_api_key_here"
   ```

4. **Deploy**
   - Click "Deploy"
   - Your app will be live at `https://your-app-name.streamlit.app`

## Important Notes

- **Security**: Never commit API keys or `.env` files to the repository
- **API Costs**: This app uses OpenAI API which incurs costs based on usage
- **File Size**: Large PDF files may take longer to process
- **Vector Store**: The app creates a FAISS vector store for efficient document retrieval

## Troubleshooting

- If you get module import errors, ensure all packages are installed: `pip install -r requirements.txt`
- If the app doesn't load PDFs, check that PyMuPDF is properly installed
- For Streamlit Cloud deployment issues, check the logs in the Streamlit Cloud dashboard

## License

This project is licensed under the MIT License.
