#!/usr/bin/env python3
"""
Tamil Study Buddy - Minimal Streamlit App
Simplified version to work on HF Spaces
"""

import streamlit as st
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from datetime import datetime

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
</style>
""", unsafe_allow_html=True)

# Load model
@st.cache_resource
def load_model():
    """Load fine-tuned Tamil model"""
    try:
        model_path = "./tamil-study-buddy-finetuned"
        
        st.write("📦 Loading tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        
        st.write("📦 Loading model...")
        model = AutoModelForCausalLM.from_pretrained(model_path)
        
        st.write("✅ Model loaded successfully!")
        return model, tokenizer
        
    except Exception as e:
        st.error(f"❌ Error: {e}")
        return None, None

# Initialize session
if "messages" not in st.session_state:
    st.session_state.messages = []

# Header
st.markdown('<div class="header-title">🇮🇳 Tamil Study Buddy</div>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>AI Tutor for Tamil</p>")

# Load model
with st.spinner("Loading model..."):
    model, tokenizer = load_model()

if model is None:
    st.error("Failed to load model")
else:
    # Chat display
    st.subheader("Chat History")
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Input
    st.divider()
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_input("Ask in Tamil:", placeholder="Type in Tamil...")
    
    with col2:
        submit = st.button("Send")
    
    if submit and user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        with st.chat_message("user"):
            st.write(user_input)
        
        with st.spinner("Thinking..."):
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
                st.error(f"Error: {e}")
    
    if st.button("Clear"):
        st.session_state.messages = []
        st.rerun()
