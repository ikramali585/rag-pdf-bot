# Deploy to Streamlit Cloud - Quick Guide

## 🚀 Deployment Steps

### 1. Prepare Your Repository

Your code is now ready for deployment! Make sure you have:

✅ `app.py` - Your main application
✅ `requirements.txt` - Dependencies 
✅ `.gitignore` - Protects sensitive files
✅ `.streamlit/config.toml` - Streamlit configuration
✅ `README.md` - Documentation

### 2. Push to GitHub

```bash
# Initialize git repository (if not already done)
git init

# Add all files except sensitive ones
git add app.py requirements.txt README.md .gitignore .streamlit/
git add .streamlit/

# Commit
git commit -m "Ready for Streamlit deployment"

# Create a GitHub repository and push
git remote add origin https://github.com/yourusername/rag-pdf-bot.git
git push -u origin main
```

### 3. Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click **"New app"**
4. Select your repository: `rag-pdf-bot`
5. Set main file path: `app.py`
6. Branch: `main`

### 4. Configure Secrets (IMPORTANT!)

Before deploying, you **MUST** add your API keys:

1. In the Streamlit Cloud app settings, go to **Settings** → **Secrets**
2. Add the following:

```toml
OPENAI_API_KEY = "sk-your-actual-openai-key-here"
GROQ_API_KEY = "your-groq-key-if-needed"
```

3. Click **"Save"**

### 5. Deploy

Click **"Deploy"** and wait for the app to be live!

Your app will be available at:
`https://[your-app-name].streamlit.app`

## 📝 Important Notes

### Security
- ⚠️ **NEVER** commit your `.env` file or API keys
- The `.gitignore` file is set up to protect sensitive data
- Use Streamlit Cloud's Secrets feature for API keys

### Cost Management
- OpenAI API costs money based on usage
- Monitor your usage at platform.openai.com
- Consider setting usage limits in your OpenAI account

### File Upload Limits
- Streamlit Cloud has file upload size limits
- Large PDFs may take time to process
- Consider optimizing PDF file sizes before upload

## 🔧 Troubleshooting

### "Module not found" error
- Check that `requirements.txt` includes all necessary packages
- Verify package versions are compatible

### "API key not found" error
- Ensure secrets are configured in Streamlit Cloud dashboard
- Check that environment variable names match exactly

### Slow processing
- Vector database creation is computationally expensive
- Consider using smaller PDFs or increasing chunk size
- First upload may take several minutes

## 🎉 Success!

Once deployed, users can:
1. Upload PDF files
2. Ask questions about the content
3. Get AI-powered answers based on the documents

## Support

For issues:
- Check Streamlit Cloud logs in the dashboard
- Review the README.md for setup instructions
- Visit [docs.streamlit.io](https://docs.streamlit.io)

