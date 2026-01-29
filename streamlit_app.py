#!/usr/bin/env python3
"""
Tamil Study Buddy - Streamlit App
AI Tutor for Tamil Language Learning
"""

import streamlit as st
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import os
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Tamil Study Buddy",
    page_icon="🇮🇳",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main { padding: 2rem; }
    .header-title { color: #ff6b35; font-size: 2.5rem; font-weight: bold; text-align: center; }
    .info-box { background-color: #f0f2f6; padding: 1rem; border-radius: 0.5rem; margin: 1rem 0; }
</style>
""", unsafe_allow_html=True)

# Find model path
def find_model_path():
    """Find the model folder in various possible locations"""
    possible_paths = [
        "./tamil-study-buddy-finetuned",
        "./tamil-study-buddy-finetuned/checkpoint-63",
        "./tamil-study-buddy-finetuned/checkpoint-60",
        "/tmp/tamil-study-buddy/tamil-study-buddy-finetuned",
        "/tmp/tamil-study-buddy/tamil-study-buddy-finetuned/checkpoint-63",
        "/tmp/tamil-study-buddy/tamil-study-buddy-finetuned/checkpoint-60",
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            config_path = os.path.join(path, "config.json")
            if os.path.exists(config_path):
                return path
    
    return None

# Load model with error handling
@st.cache_resource
def load_model():
    """Load fine-tuned Tamil model"""
    try:
        # Find model path
        model_path = find_model_path()
        
        if model_path is None:
            st.error("""
            ❌ **Model Not Found**
            
            The model files are missing or incomplete. This could be because:
            - Model files weren't uploaded to the repository
            - Model files are too large for GitHub
            - Repository structure is incorrect
            
            **Solution:** Please upload the complete model folder with:
            - config.json
            - pytorch_model.bin or model.safetensors
            - tokenizer.json
            - vocab.json
            """)
            return None, None
        
        st.info(f"📦 Using model from: {model_path}")
        
        st.write("📦 Loading tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        
        st.write("📦 Loading model (this may take a minute)...")
        model = AutoModelForCausalLM.from_pretrained(model_path)
        
        st.success("✅ Model loaded successfully!")
        return model, tokenizer
        
    except Exception as e:
        st.error(f"""
        ❌ **Error Loading Model**
        
        Error details: {str(e)}
        
        **Common causes:**
        - Missing config.json file
        - Missing model weights (pytorch_model.bin)
        - Missing tokenizer files
        - Incompatible model format
        
        **Next steps:**
        1. Check that all model files are uploaded
        2. Verify model folder structure
        3. Ensure model is compatible with transformers library
        """)
        return None, None

# Initialize session
if "messages" not in st.session_state:
    st.session_state.messages = []

# Header
st.markdown('<div class="header-title">🇮🇳 Tamil Study Buddy</div>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>AI Tutor for Learning Tamil</p>")

# System info (debug)
with st.expander("ℹ️ System Information"):
    st.write(f"**Python Version:** {os.sys.version}")
    st.write(f"**PyTorch Version:** {torch.__version__}")
    st.write(f"**CUDA Available:** {torch.cuda.is_available()}")
    st.write(f"**Current Directory:** {os.getcwd()}")
    st.write(f"**Model Path:** {find_model_path()}")

# Load model
with st.spinner("Loading model..."):
    model, tokenizer = load_model()

if model is None:
    st.warning("""
    ### 📋 What to Do
    
    The model couldn't be loaded. This usually means:
    
    1. **Model files are missing** - The fine-tuned model files need to be uploaded
    2. **Wrong folder structure** - Check that all files are in the correct location
    3. **File corruption** - Try re-uploading the model files
    
    **Required files in model folder:**
    - `config.json` - Model configuration
    - `pytorch_model.bin` or `model.safetensors` - Model weights
    - `tokenizer.json` - Tokenizer configuration
    - `vocab.json` - Vocabulary file
    - `merges.txt` - Merge operations
    
    **How to fix:**
    1. Ensure all model files are uploaded to the Space
    2. Verify the folder structure matches expectations
    3. Restart the Space after uploading
    """)
else:
    # Chat display
    st.subheader("💬 Chat History")
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Input
    st.divider()
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_input(
            "Ask in Tamil:", 
            placeholder="Type your question in Tamil (தமிழ்)...",
            key="user_input"
        )
    
    with col2:
        submit = st.button("Send", use_container_width=True)
    
    if submit and user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        with st.chat_message("user"):
            st.write(user_input)
        
        with st.spinner("🤔 Thinking..."):
            try:
                inputs = tokenizer.encode(user_input, return_tensors="pt")
                
                with torch.no_grad():
                    outputs = model.generate(
                        inputs,
                        max_length=150,
                        temperature=0.7,
                        top_p=0.9,
                        do_sample=True,
                        pad_token_id=tokenizer.eos_token_id,
                    )
                
                response = tokenizer.decode(outputs[0], skip_special_tokens=True)
                
                st.session_state.messages.append({"role": "assistant", "content": response})
                
                with st.chat_message("assistant"):
                    st.write(response)
                
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error generating response: {str(e)}")
    
    # Clear button
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9rem;'>
    <p>Tamil Study Buddy - Learn Tamil with AI 🇮🇳</p>
    <p>Powered by Streamlit & Hugging Face</p>
</div>
""", unsafe_allow_html=True)
