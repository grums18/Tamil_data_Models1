#!/usr/bin/env python3
"""
Tamil Study Buddy - Streamlit App (Optimized for HF Spaces)
Fine-tuned Tamil Language Model with Chat Interface
"""

import streamlit as st
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import time
from datetime import datetime
import os
import sys

# Page configuration
st.set_page_config(
    page_title="Tamil Study Buddy",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stChatMessage {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .header-title {
        color: #ff6b35;
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
    }
    .stat-box {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
    }
    .error-box {
        background-color: #ffebee;
        border-left: 4px solid #f44336;
        padding: 1rem;
        border-radius: 4px;
    }
    .success-box {
        background-color: #e8f5e9;
        border-left: 4px solid #4caf50;
        padding: 1rem;
        border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)

# Load model (cached for performance)
@st.cache_resource
def load_model():
    """Load fine-tuned Tamil model"""
    try:
        # Try multiple possible paths
        possible_paths = [
            "./tamil-study-buddy-finetuned",
            "/app/tamil-study-buddy-finetuned",
            "tamil-study-buddy-finetuned",
        ]
        
        model_path = None
        for path in possible_paths:
            if os.path.exists(path):
                model_path = path
                st.write(f"✅ Found model at: {path}")
                break
        
        if model_path is None:
            st.error("❌ Model directory not found. Checked paths:")
            for path in possible_paths:
                st.write(f"  - {path}")
            return None, None
        
        st.write(f"📦 Loading model from: {model_path}")
        
        # Load tokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        st.write("✅ Tokenizer loaded")
        
        # Load model with optimization
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.float32,
            device_map="auto" if torch.cuda.is_available() else None
        )
        st.write("✅ Model loaded successfully")
        
        return model, tokenizer
        
    except Exception as e:
        st.error(f"❌ Error loading model: {str(e)}")
        st.error(f"Error type: {type(e).__name__}")
        import traceback
        st.error(traceback.format_exc())
        return None, None

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "query_count" not in st.session_state:
    st.session_state.query_count = 0

if "start_time" not in st.session_state:
    st.session_state.start_time = datetime.now()

if "model_loaded" not in st.session_state:
    st.session_state.model_loaded = False

# Header
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown('<div class="header-title">🇮🇳 Tamil Study Buddy</div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666;'>AI Tutor for Colloquial Tamil Learning</p>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("⚙️ Settings")
    
    # Model settings
    st.subheader("Model Parameters")
    temperature = st.slider(
        "Temperature (Creativity)",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="Higher = more creative, Lower = more focused"
    )
    
    max_length = st.slider(
        "Max Response Length",
        min_value=50,
        max_value=500,
        value=150,
        step=50
    )
    
    top_p = st.slider(
        "Top P (Diversity)",
        min_value=0.0,
        max_value=1.0,
        value=0.9,
        step=0.1
    )
    
    # Statistics
    st.subheader("📊 Statistics")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Queries", st.session_state.query_count)
    
    with col2:
        uptime = datetime.now() - st.session_state.start_time
        minutes = int(uptime.total_seconds() / 60)
        st.metric("Uptime", f"{minutes}m")
    
    # Example queries
    st.subheader("💡 Example Queries")
    examples = [
        "வணக்கம்",
        "நல்ல நாள்",
        "தமிழ்நாடு",
        "பள்ளி",
        "எப்படி இருக்கீங்க",
    ]
    
    for example in examples:
        if st.button(f"📝 {example}", key=example):
            st.session_state.query_input = example
    
    # System info
    st.divider()
    st.subheader("ℹ️ System Info")
    st.write(f"**Python**: {sys.version.split()[0]}")
    st.write(f"**PyTorch**: {torch.__version__}")
    st.write(f"**CUDA Available**: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        st.write(f"**GPU**: {torch.cuda.get_device_name(0)}")
    
    # About
    st.divider()
    st.subheader("ℹ️ About")
    st.markdown("""
    **Tamil Study Buddy** is an AI-powered tutor trained on colloquial Tamil data.
    
    - 🤖 Fine-tuned model
    - 🇮🇳 Understands Tamil
    - 💬 Conversational responses
    - 📚 Educational focus
    """)

# Main content
st.subheader("💬 Chat with Tamil Study Buddy")

# Load model with status
with st.spinner("🔄 Loading model... (This may take 1-2 minutes on first run)"):
    model, tokenizer = load_model()
    st.session_state.model_loaded = model is not None and tokenizer is not None

if model is None or tokenizer is None:
    st.markdown("""
    <div class="error-box">
    <h3>❌ Model Loading Failed</h3>
    <p>The model could not be loaded. This might be because:</p>
    <ul>
        <li>The model files are still being downloaded</li>
        <li>There's not enough memory available</li>
        <li>The model path is incorrect</li>
    </ul>
    <p><strong>Please wait a few moments and refresh the page.</strong></p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="success-box">
    <h3>✅ Model Ready</h3>
    <p>The model has loaded successfully. You can now chat!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat history display
    st.subheader("Chat History")
    
    if len(st.session_state.messages) == 0:
        st.info("💬 No messages yet. Start by typing something in Tamil!")
    else:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
    
    # Input area
    st.divider()
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_input(
            "Ask me something in Tamil:",
            placeholder="Type your question in Tamil...",
            key="user_input"
        )
    
    with col2:
        submit_button = st.button("Send", use_container_width=True)
    
    # Process input
    if submit_button and user_input:
        # Add user message
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })
        
        st.session_state.query_count += 1
        
        # Display user message
        with st.chat_message("user"):
            st.write(user_input)
        
        # Generate response
        with st.spinner("🤔 Thinking..."):
            try:
                # Tokenize
                inputs = tokenizer.encode(user_input, return_tensors="pt")
                
                # Generate
                with torch.no_grad():
                    outputs = model.generate(
                        inputs,
                        max_length=max_length,
                        temperature=temperature,
                        top_p=top_p,
                        do_sample=True,
                        pad_token_id=tokenizer.eos_token_id,
                        num_return_sequences=1
                    )
                
                # Decode
                response = tokenizer.decode(outputs[0], skip_special_tokens=True)
                
                # Add assistant message
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response
                })
                
                # Display assistant message
                with st.chat_message("assistant"):
                    st.write(response)
                
                # Rerun to update UI
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error generating response: {str(e)}")
                st.error(f"Error type: {type(e).__name__}")
                import traceback
                st.error(traceback.format_exc())
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.session_state.query_count = 0
        st.rerun()

# Footer
st.divider()
st.markdown("""
<p style='text-align: center; color: #999; font-size: 0.8rem;'>
    Tamil Study Buddy v1.0 | Fine-tuned with Colloquial Tamil Data | Powered by Streamlit & Hugging Face
</p>
""", unsafe_allow_html=True)
