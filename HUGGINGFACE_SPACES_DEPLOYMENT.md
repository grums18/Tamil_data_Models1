# 🚀 Deploy Tamil Study Buddy to Hugging Face Spaces

## What is Hugging Face Spaces?

Hugging Face Spaces is a **FREE hosting platform** for AI applications. Perfect for deploying Streamlit apps!

**Benefits:**
- ✅ Free hosting (no credit card needed)
- ✅ Automatic deployment from GitHub
- ✅ GPU support (optional, paid)
- ✅ Easy integration with HF models
- ✅ Public sharing with one link
- ✅ Custom domain support

---

## Step-by-Step Deployment

### Step 1: Create GitHub Repository

```bash
# Create new repo on GitHub
# Go to: https://github.com/new
# Name: tamil-study-buddy
# Description: AI Tutor for Colloquial Tamil Learning
# Make it PUBLIC
```

### Step 2: Prepare Project Files

Your GitHub repo should have this structure:

```
tamil-study-buddy/
├── streamlit_app.py              # Main Streamlit app
├── requirements.txt              # Python dependencies
├── .streamlit/
│   └── config.toml              # Streamlit config
├── README.md                     # Documentation
└── tamil-study-buddy-finetuned/  # Fine-tuned model files
    ├── config.json
    ├── model.safetensors
    ├── tokenizer.json
    └── ...
```

### Step 3: Create README.md

```markdown
# Tamil Study Buddy 🇮🇳

AI Tutor for Colloquial Tamil Learning

## Features
- 🤖 Fine-tuned Tamil language model
- 💬 Chat interface
- 📚 Colloquial Tamil support
- ⚡ Fast responses

## How to Use
1. Ask a question in Tamil
2. Get instant response
3. Learn from examples

## Local Setup
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Model
- Base: GPT-2
- Fine-tuned on: Colloquial Tamil data
- Parameters: 124M

## License
MIT
```

### Step 4: Push to GitHub

```bash
# Initialize git
cd tamil-study-buddy
git init
git add .
git commit -m "Initial commit: Tamil Study Buddy with fine-tuned model"

# Add remote
git remote add origin https://github.com/YOUR_USERNAME/tamil-study-buddy.git

# Push
git branch -M main
git push -u origin main
```

### Step 5: Create Hugging Face Space

**Option A: Using Web Interface (Easiest)**

1. Go to: https://huggingface.co/spaces
2. Click "Create new Space"
3. Fill in details:
   - **Name**: tamil-study-buddy
   - **License**: MIT
   - **Space SDK**: Streamlit
   - **Visibility**: Public
4. Click "Create Space"

**Option B: Using CLI**

```bash
pip install huggingface-hub
huggingface-cli login  # Enter your HF token

huggingface-cli repo create tamil-study-buddy \
    --type space \
    --space-sdk streamlit
```

### Step 6: Connect GitHub to Hugging Face

1. Go to your HF Space settings
2. Click "Linked Repository"
3. Connect your GitHub repo: `YOUR_USERNAME/tamil-study-buddy`
4. Enable "Sync with GitHub"

**Now every GitHub push auto-deploys to HF!** 🎉

### Step 7: Add Model Files

The fine-tuned model files need to be in your repo. You have two options:

**Option A: Git LFS (Recommended for large files)**

```bash
# Install git-lfs
brew install git-lfs  # macOS
apt-get install git-lfs  # Linux
choco install git-lfs  # Windows

# Track model files
git lfs install
git lfs track "*.safetensors"
git lfs track "*.bin"

# Add and push
git add .gitattributes
git add tamil-study-buddy-finetuned/
git commit -m "Add fine-tuned model"
git push
```

**Option B: Upload to Hugging Face Hub**

```bash
# Upload model to HF Hub
from huggingface_hub import upload_folder

upload_folder(
    folder_path="./tamil-study-buddy-finetuned",
    repo_id="YOUR_USERNAME/tamil-study-buddy-model",
    repo_type="model"
)

# Update streamlit_app.py to load from HF Hub
model_path = "YOUR_USERNAME/tamil-study-buddy-model"
model = AutoModelForCausalLM.from_pretrained(model_path)
```

### Step 8: Configure Secrets (if needed)

If your app needs API keys:

1. Go to Space settings
2. Click "Repository secrets"
3. Add your secrets (e.g., API keys)
4. Access in code: `os.environ.get("SECRET_NAME")`

### Step 9: Test Your Space

1. Wait for deployment (usually 2-5 minutes)
2. Click "App" tab
3. Test the interface
4. Share the link!

---

## Deployment Checklist

- [ ] GitHub repo created and public
- [ ] All files committed and pushed
- [ ] Model files included (via Git LFS or HF Hub)
- [ ] requirements.txt has all dependencies
- [ ] streamlit_app.py works locally
- [ ] README.md is complete
- [ ] HF Space created
- [ ] GitHub connected to HF Space
- [ ] Space deployed successfully
- [ ] App loads without errors
- [ ] Chat interface works
- [ ] Model generates responses

---

## Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'transformers'"
**Solution**: Add to requirements.txt
```
transformers==4.35.2
torch==2.1.1
```

### Problem: "Model not found"
**Solution**: Use full HF Hub path
```python
model_path = "YOUR_USERNAME/tamil-study-buddy-model"
model = AutoModelForCausalLM.from_pretrained(model_path)
```

### Problem: "Out of memory"
**Solution**: Use smaller model or enable GPU in Space settings

### Problem: "Deployment failed"
**Solution**: Check Space logs for errors

---

## Performance Tips

1. **Cache model loading**
   ```python
   @st.cache_resource
   def load_model():
       return AutoModelForCausalLM.from_pretrained("model")
   ```

2. **Optimize model size**
   - Use quantization
   - Use smaller base model
   - Use ONNX format

3. **Enable GPU** (paid)
   - Go to Space settings
   - Select GPU hardware
   - Faster inference

---

## Sharing Your Space

Once deployed, share the link:
- **Public URL**: `https://huggingface.co/spaces/YOUR_USERNAME/tamil-study-buddy`
- **Embed in website**: Use iframe
- **Share on social media**: Direct link
- **Add to portfolio**: Link in GitHub

---

## Next Steps

1. ✅ Deploy to HF Spaces
2. ⏳ Gather user feedback
3. ⏳ Improve model based on feedback
4. ⏳ Add more features (voice, etc.)
5. ⏳ Create mobile app
6. ⏳ Scale to production

---

## Resources

- Hugging Face Spaces: https://huggingface.co/spaces
- Streamlit Docs: https://docs.streamlit.io
- Transformers Docs: https://huggingface.co/docs/transformers
- Git LFS: https://git-lfs.com

---

**Your Tamil Study Buddy is ready to be shared with the world!** 🚀
