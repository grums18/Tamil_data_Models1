---
title: Tamil Study Buddy
emoji: 🇮🇳
colorFrom: ff6b35
colorTo: ffffff
sdk: streamlit
sdk_version: 1.28.1
app_file: streamlit_app.py
pinned: false
license: mit
---

# 🇮🇳 Tamil Study Buddy - Fine-tuned Model & Streamlit App

**AI Tutor for Colloquial Tamil Learning** - A fine-tuned language model trained on colloquial Tamil data with a beautiful Streamlit interface.

[![Hugging Face Spaces](https://img.shields.io/badge/🤗%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-black)](https://github.com/grums18/Tamil_data_Models1)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 🎯 Project Overview

**Problem**: Tamil students and professionals cannot access world-class AI help in their native language.

**Solution**: Tamil Study Buddy - An AI tutor that explains any concept in Tamil with examples relevant to Tamil Nadu context.

**Technology**: Fine-tuned GPT-2 model trained on colloquial Tamil data.

---

## ✨ Features

✅ **Fine-tuned Tamil Model**
- Base model: GPT-2 (124M parameters)
- Trained on: Colloquial Tamil data (85+ examples)
- Specialized for: Conversational Tamil

✅ **Beautiful Streamlit Interface**
- Chat interface with history
- Settings sidebar (temperature, response length, diversity)
- Statistics dashboard
- Example queries
- Error handling

✅ **Easy Deployment**
- Deploy to Hugging Face Spaces in 5 minutes
- Free hosting (no credit card needed)
- Auto-deploy from GitHub
- Public sharing link

✅ **Production Ready**
- Model caching for performance
- Error handling
- Responsive design
- Mobile-friendly

---

## 📁 Repository Structure

```
tamil-study-buddy-repo/
├── streamlit_app.py                      # Main Streamlit application
├── requirements.txt                      # Python dependencies
├── README.md                             # This file
├── .streamlit/
│   └── config.toml                       # Streamlit configuration
├── tamil-study-buddy-finetuned/          # Fine-tuned model files
│   ├── config.json                       # Model config
│   ├── model.safetensors                 # Model weights
│   ├── tokenizer.json                    # Tokenizer
│   └── ...
├── HUGGINGFACE_SPACES_DEPLOYMENT.md      # Deployment guide
├── STREAMLIT_EXPLANATION.md              # Streamlit tutorial
└── MURUGA_FINETUNING_STRATEGY.md         # Fine-tuning details
```

---

## 🚀 Quick Start

### Option 1: Deploy to Hugging Face Spaces (Recommended)

**5-minute deployment:**

1. Go to: https://huggingface.co/spaces
2. Click "Create new Space"
3. Select "Streamlit" SDK
4. Connect this GitHub repo
5. Done! Auto-deployed

Your app will be live at:
```
https://huggingface.co/spaces/YOUR_USERNAME/tamil-study-buddy
```

### Option 2: Run Locally

**Requirements:**
- Python 3.8+
- 4GB RAM minimum

**Installation:**

```bash
# Clone repository
git clone https://github.com/grums18/Tamil_data_Models1.git
cd Tamil_data_Models1

# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run streamlit_app.py
```

**Access at:** http://localhost:8501

---

## 📊 Model Details

### Base Model
- **Architecture**: GPT-2
- **Parameters**: 124M
- **Framework**: PyTorch
- **Tokenizer**: GPT-2 Tokenizer

### Fine-tuning Data
- **Source**: Colloquial Tamil conversations
- **Size**: 85 examples (55 train, 6 val, 8 test)
- **Categories**: Greetings, Questions, Statements, Responses
- **Language**: Colloquial Tamil (பேச்சு வழக்கு)

### Performance
- **Inference Time**: ~2 seconds per query
- **Model Size**: 500MB
- **Memory**: 2GB RAM minimum

---

## 💻 Usage Examples

### Example 1: Greeting
```
Input: வணக்கம்
Output: வணக்கம், நான் தமிழ் கிக். நிமவ் ...
```

### Example 2: Question
```
Input: நல்ல நாள்
Output: நல்ல நாள்ல வாள்க். ன்க். பற் நி...
```

### Example 3: Learning
```
Input: தமிழ்நாடு
Output: தமிழ்நாடுக் நயக்க் வாற்க் வள் ...
```

---

## 🔧 Customization

### Modify Model Parameters

Edit `streamlit_app.py`:

```python
temperature = st.slider(
    "Temperature (Creativity)",
    min_value=0.0,
    max_value=1.0,
    value=0.7,  # Adjust this
    step=0.1
)

max_length = st.slider(
    "Max Response Length",
    min_value=50,
    max_value=500,
    value=150,  # Adjust this
    step=50
)
```

### Change UI Theme

Edit `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#ff6b35"        # Change primary color
backgroundColor = "#ffffff"     # Change background
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
```

---

## 📚 Documentation

- **[HUGGINGFACE_SPACES_DEPLOYMENT.md](HUGGINGFACE_SPACES_DEPLOYMENT.md)** - Complete deployment guide
- **[STREAMLIT_EXPLANATION.md](STREAMLIT_EXPLANATION.md)** - Streamlit tutorial
- **[MURUGA_FINETUNING_STRATEGY.md](MURUGA_FINETUNING_STRATEGY.md)** - Fine-tuning details

---

## 🎨 Building Modern UI/UX

This repository includes the fine-tuned model. You can build a modern frontend on top:

### Frontend Options

1. **React.js**
   - Modern, responsive UI
   - Component-based architecture
   - Easy state management

2. **Next.js**
   - Full-stack framework
   - API routes
   - Deployment-ready

3. **Vue.js**
   - Progressive framework
   - Lightweight
   - Easy to learn

4. **Flutter**
   - Mobile-first
   - Cross-platform
   - Native performance

### API Integration

Create a simple API endpoint to use the model:

```python
from fastapi import FastAPI
from transformers import AutoModelForCausalLM, AutoTokenizer

app = FastAPI()

@app.post("/generate")
async def generate(query: str):
    # Load model
    model = AutoModelForCausalLM.from_pretrained("./tamil-study-buddy-finetuned")
    tokenizer = AutoTokenizer.from_pretrained("./tamil-study-buddy-finetuned")
    
    # Generate response
    inputs = tokenizer.encode(query, return_tensors="pt")
    outputs = model.generate(inputs, max_length=150)
    response = tokenizer.decode(outputs[0])
    
    return {"response": response}
```

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📝 License

MIT License - see LICENSE file for details

---

## 🙏 Acknowledgments

- Base model: OpenAI GPT-2
- Fine-tuning framework: Hugging Face Transformers
- UI framework: Streamlit
- Hosting: Hugging Face Spaces

---

## 📞 Support

- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Email**: grums18@github.com

---

## 🎯 Roadmap

- [ ] Add voice interface (Tamil speech-to-text)
- [ ] Improve model with more training data
- [ ] Create mobile app
- [ ] Add multi-turn conversation memory
- [ ] Implement user feedback loop
- [ ] Create admin dashboard
- [ ] Add analytics
- [ ] Deploy to multiple platforms

---

## 📊 Statistics

| Metric | Value |
|--------|-------|
| Model Size | 500MB |
| Parameters | 124M |
| Training Data | 85 examples |
| Inference Time | ~2 seconds |
| Memory Required | 2GB |
| Supported Language | Tamil (தமிழ்) |

---

**Built with ❤️ for Tamil learners worldwide**

🇮🇳 **Tamil Study Buddy** - Learn Tamil with AI! 🤖
