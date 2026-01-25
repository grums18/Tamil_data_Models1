# Fine-tuning Muruga Model with Colloquial Tamil Data

## Executive Summary

This document outlines a comprehensive strategy to fine-tune the existing Muruga Tamil language model with colloquial Tamil data to create a specialized conversational AI assistant. This approach combines the strengths of an existing pre-trained model with domain-specific colloquial language, resulting in a faster, cheaper, and more practical solution than training from scratch.

### Key Metrics

| Metric | Value |
|--------|-------|
| **Development Time** | 2-3 weeks |
| **Cost** | $500-1,500 |
| **Infrastructure** | Single GPU (8GB VRAM) |
| **Training Time** | 6-12 hours |
| **Data Required** | 10,000-50,000 colloquial examples |
| **Expected Improvement** | 30-50% better on conversational tasks |

---

## 1. Understanding the Muruga Model

### Model Overview

The Muruga model is a Tamil language model specifically designed for Tamil NLP tasks. It provides a solid foundation for fine-tuning with specialized data.

**Base Model Specifications:**
- **Architecture**: Transformer-based (similar to GPT-2/GPT-3)
- **Parameters**: 7B-13B (depending on variant)
- **Training Data**: General Tamil corpus (news, books, government documents)
- **Strengths**: Good at formal Tamil, structured text, general knowledge
- **Limitations**: Limited conversational ability, formal language bias

**Why Muruga for Fine-tuning:**
- ✅ Pre-trained on diverse Tamil data
- ✅ Already understands Tamil grammar and semantics
- ✅ Requires less data to fine-tune (vs. training from scratch)
- ✅ Faster convergence during training
- ✅ Lower computational requirements
- ✅ Community support and documentation

---

## 2. Colloquial Tamil Data Strategy

### What is Colloquial Tamil?

Colloquial Tamil refers to the informal, conversational form of Tamil used in everyday speech. It differs from formal/literary Tamil in several ways:

| Aspect | Formal Tamil | Colloquial Tamil |
|--------|---|---|
| **Grammar** | Strict, complex | Flexible, simplified |
| **Vocabulary** | Literary, technical | Common, practical |
| **Pronunciation** | Standard | Regional variations |
| **Structure** | Long sentences | Short, fragmented |
| **Examples** | Government documents | Social media, casual speech |

**Example:**
```
Formal: "நீங்கள் இன்று எங்கே செல்லலாம்?"
Colloquial: "நீ இன்னைக்கு எங்க போற?"
English: "Where are you going today?"
```

### Data Sources for Colloquial Tamil

#### 1. Social Media (30% of data)
- **Twitter/X Tamil posts**: 100,000+ tweets
- **Reddit r/Tamil**: 10,000+ posts
- **Facebook Tamil groups**: 50,000+ comments
- **WhatsApp conversations**: 20,000+ messages (anonymized)
- **YouTube comments**: 30,000+ comments

**Collection Method:**
```python
# Twitter API
from tweepy import Client
client = Client(bearer_token="YOUR_TOKEN")
tweets = client.search_recent_tweets(
    query="lang:ta",
    max_results=100
)

# Reddit API
import praw
reddit = praw.Reddit(client_id="ID", client_secret="SECRET")
posts = reddit.subreddit("tamil").hot(limit=1000)

# YouTube API
from youtube_transcript_api import YouTubeTranscriptApi
transcripts = YouTubeTranscriptApi.get_transcript("VIDEO_ID", languages=['ta'])
```

#### 2. Conversational Datasets (25% of data)
- **AI4Bharat Indic-Instruct**: 10,000+ instruction pairs
- **Tamil QA datasets**: 5,000+ Q&A pairs
- **Customer support conversations**: 10,000+ dialogues
- **Educational forums**: 5,000+ discussions
- **Podcast transcripts**: 50+ hours of audio

**Available Datasets:**
- ai4bharat/Indic-Instruct (HF)
- Tamil QA dataset (GitHub)
- Customer service logs (proprietary)

#### 3. News & Media (20% of data)
- **News headlines**: 50,000+ articles
- **News comments**: 30,000+ reader comments
- **Magazine articles**: 10,000+ articles
- **Blog posts**: 20,000+ posts
- **Online forums**: 15,000+ discussions

**Sources:**
- Daily Thanthi (news portal)
- Dinamalar (news portal)
- BBC Tamil (news)
- Vikatan (magazine)
- Tamil blogs and forums

#### 4. Literature & Cultural Content (15% of data)
- **Classical Tamil literature**: 50+ works
- **Thirukkural with commentary**: 1,330 verses
- **Sangam literature**: 50+ poems
- **Devotional texts**: 100+ verses
- **Tamil stories**: 100+ short stories

**Sources:**
- Project Madurai (free editions)
- Shaivam.org (devotional texts)
- Tamil Digital Library
- Koyil (Divya Prabandham)

#### 5. Educational Content (10% of data)
- **School curriculum**: 50,000+ questions
- **University lectures**: 100+ transcripts
- **Educational videos**: 500+ transcripts
- **Textbooks**: 20+ books
- **Study guides**: 50+ guides

**Sources:**
- Tamil Nadu school curriculum
- University lecture notes
- Educational YouTube channels
- Open educational resources

### Data Collection Strategy

**Phase 1: Automated Collection (Week 1)**
```
- Download HF datasets: 2,000 examples
- Scrape Twitter: 5,000 tweets
- Scrape Reddit: 1,000 posts
- Scrape YouTube comments: 2,000 comments
- Total: 10,000 examples
```

**Phase 2: Manual Curation (Week 2)**
```
- Review and filter: 10,000 examples
- Remove duplicates: 2,000 removed
- Remove low quality: 1,000 removed
- Clean and normalize: 7,000 remaining
- Add annotations: 7,000 annotated
```

**Phase 3: Expansion (Week 3)**
```
- Collect additional data: 15,000 examples
- Augment existing data: 5,000 variations
- Create synthetic data: 3,000 examples
- Total: 30,000 examples
```

---

## 3. Data Preparation Pipeline

### Step 1: Data Collection

```python
import json
import pandas as pd
from pathlib import Path

class ColloquialTamilCollector:
    def __init__(self):
        self.data = []
    
    def collect_from_twitter(self, query, count=5000):
        """Collect Tamil tweets"""
        from tweepy import Client
        client = Client(bearer_token="YOUR_TOKEN")
        
        tweets = client.search_recent_tweets(
            query=f"{query} lang:ta",
            max_results=count,
            tweet_fields=['created_at', 'author_id']
        )
        
        for tweet in tweets.data:
            self.data.append({
                'text': tweet.text,
                'source': 'twitter',
                'language': 'ta'
            })
    
    def collect_from_reddit(self, subreddit='tamil', count=1000):
        """Collect Tamil Reddit posts"""
        import praw
        reddit = praw.Reddit(
            client_id="ID",
            client_secret="SECRET",
            user_agent="TamilCollector"
        )
        
        for submission in reddit.subreddit(subreddit).hot(limit=count):
            self.data.append({
                'text': submission.title + " " + submission.selftext,
                'source': 'reddit',
                'language': 'ta'
            })
    
    def collect_from_youtube_comments(self, video_ids, count=2000):
        """Collect Tamil YouTube comments"""
        from youtube_comment_downloader import YoutubeCommentDownloader
        
        downloader = YoutubeCommentDownloader()
        collected = 0
        
        for video_id in video_ids:
            comments = downloader.get_comments_from_url(
                f"https://www.youtube.com/watch?v={video_id}",
                sort_by=SORT_BY_RECENT
            )
            
            for comment in comments:
                if collected >= count:
                    break
                
                self.data.append({
                    'text': comment['text'],
                    'source': 'youtube',
                    'language': 'ta'
                })
                collected += 1
    
    def save_to_file(self, filepath):
        """Save collected data"""
        df = pd.DataFrame(self.data)
        df.to_json(filepath, orient='records', ensure_ascii=False, indent=2)
        print(f"Saved {len(self.data)} examples to {filepath}")

# Usage
collector = ColloquialTamilCollector()
collector.collect_from_twitter("தமிழ்", count=5000)
collector.collect_from_reddit("tamil", count=1000)
collector.collect_from_youtube_comments(["VIDEO_ID_1", "VIDEO_ID_2"], count=2000)
collector.save_to_file("raw_colloquial_data.json")
```

### Step 2: Data Cleaning

```python
import re
import unicodedata

class ColloquialTamilCleaner:
    def __init__(self):
        self.removed_count = 0
    
    def clean_text(self, text):
        """Clean individual text"""
        # Remove URLs
        text = re.sub(r'http\S+|www\S+', '', text)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove mentions and hashtags (keep the text)
        text = re.sub(r'@\w+', '', text)
        text = re.sub(r'#(\w+)', r'\1', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Normalize Unicode
        text = unicodedata.normalize('NFC', text)
        
        # Remove control characters
        text = ''.join(ch for ch in text if unicodedata.category(ch)[0] != 'C')
        
        return text.strip()
    
    def is_valid_tamil(self, text):
        """Check if text is valid Tamil"""
        tamil_range = range(0x0B80, 0x0BFF)
        tamil_chars = sum(1 for ch in text if ord(ch) in tamil_range)
        
        # At least 70% Tamil characters
        return tamil_chars / len(text) > 0.7 if len(text) > 0 else False
    
    def is_long_enough(self, text, min_length=20):
        """Check if text is long enough"""
        return len(text) >= min_length
    
    def is_not_spam(self, text):
        """Check if text is not spam"""
        # Check for repeated characters
        if re.search(r'(.)\1{4,}', text):
            return False
        
        # Check for excessive punctuation
        punctuation_ratio = sum(1 for ch in text if ch in '!?.,;:') / len(text)
        if punctuation_ratio > 0.3:
            return False
        
        return True
    
    def process_dataset(self, input_file, output_file):
        """Process entire dataset"""
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        cleaned_data = []
        
        for item in data:
            text = item.get('text', '')
            
            # Clean text
            text = self.clean_text(text)
            
            # Validate
            if (self.is_valid_tamil(text) and 
                self.is_long_enough(text) and 
                self.is_not_spam(text)):
                
                item['text'] = text
                cleaned_data.append(item)
            else:
                self.removed_count += 1
        
        # Save cleaned data
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(cleaned_data, f, ensure_ascii=False, indent=2)
        
        print(f"Cleaned {len(cleaned_data)} examples")
        print(f"Removed {self.removed_count} examples")
        print(f"Kept {len(cleaned_data)/len(data)*100:.1f}% of original data")

# Usage
cleaner = ColloquialTamilCleaner()
cleaner.process_dataset("raw_colloquial_data.json", "cleaned_colloquial_data.json")
```

### Step 3: Data Deduplication

```python
import hashlib
from collections import defaultdict

class DataDeduplicator:
    def deduplicate(self, input_file, output_file):
        """Remove duplicate texts"""
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        seen_hashes = set()
        deduplicated = []
        
        for item in data:
            text = item.get('text', '')
            text_hash = hashlib.md5(text.encode()).hexdigest()
            
            if text_hash not in seen_hashes:
                seen_hashes.add(text_hash)
                deduplicated.append(item)
        
        # Save deduplicated data
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(deduplicated, f, ensure_ascii=False, indent=2)
        
        removed = len(data) - len(deduplicated)
        print(f"Removed {removed} duplicates")
        print(f"Kept {len(deduplicated)} unique examples")

# Usage
deduplicator = DataDeduplicator()
deduplicator.deduplicate("cleaned_colloquial_data.json", "deduplicated_colloquial_data.json")
```

### Step 4: Data Annotation (Optional but Recommended)

```python
class DataAnnotator:
    def annotate_for_finetuning(self, input_file, output_file):
        """Add instruction-response pairs for fine-tuning"""
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        annotated_data = []
        
        for item in data:
            text = item.get('text', '')
            
            # Create instruction-response pairs
            # Format: {"instruction": "...", "input": "", "output": "..."}
            
            annotated_item = {
                "instruction": "பின்வரும் தமிழ் வாக்கியத்தை தொடர்ந்து எழுதுக:",
                "input": text[:len(text)//2],  # First half
                "output": text[len(text)//2:],  # Second half
                "source": item.get('source', 'unknown')
            }
            
            annotated_data.append(annotated_item)
        
        # Save annotated data
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(annotated_data, f, ensure_ascii=False, indent=2)
        
        print(f"Annotated {len(annotated_data)} examples")

# Usage
annotator = DataAnnotator()
annotator.annotate_for_finetuning("deduplicated_colloquial_data.json", "annotated_colloquial_data.json")
```

---

## 4. Fine-tuning Infrastructure Setup

### Hardware Requirements

**Minimum Configuration:**
- GPU: 8GB VRAM (NVIDIA RTX 3060 or similar)
- RAM: 16GB
- Storage: 50GB SSD
- Time: 6-12 hours for training

**Recommended Configuration:**
- GPU: 24GB VRAM (NVIDIA RTX 4090 or A100)
- RAM: 32GB
- Storage: 100GB SSD
- Time: 2-4 hours for training

**Cloud Options:**
- Google Colab Pro: $10/month (free tier available)
- AWS SageMaker: $0.50-2.00/hour
- Lambda Labs: $0.40-1.00/hour
- Hugging Face Training: $0.50-2.00/hour

### Installation

```bash
# Create virtual environment
python -m venv tamil_finetuning
source tamil_finetuning/bin/activate  # On Windows: tamil_finetuning\Scripts\activate

# Install dependencies
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install transformers datasets peft bitsandbytes accelerate wandb

# Verify installation
python -c "import torch; print(torch.cuda.is_available())"
```

### Configuration

```python
# config.py
from dataclasses import dataclass

@dataclass
class FineTuningConfig:
    # Model configuration
    model_name = "mervinpraison/tamil-large-language-model-7b-v1.0"
    output_dir = "./tamil-study-buddy-finetuned"
    
    # Training configuration
    num_train_epochs = 3
    per_device_train_batch_size = 4
    per_device_eval_batch_size = 4
    gradient_accumulation_steps = 4
    learning_rate = 2e-4
    warmup_steps = 100
    weight_decay = 0.01
    
    # LoRA configuration (for efficient fine-tuning)
    lora_r = 8
    lora_alpha = 16
    lora_dropout = 0.05
    lora_target_modules = ["q_proj", "v_proj"]
    
    # Data configuration
    train_data_path = "annotated_colloquial_data.json"
    val_split = 0.1
    max_seq_length = 512
    
    # Logging
    logging_steps = 10
    save_steps = 100
    eval_steps = 100
    save_total_limit = 3
    
    # Optimization
    fp16 = True  # Use mixed precision
    gradient_checkpointing = True
    use_cache = False
```

---

## 5. Fine-tuning Script

### Complete Fine-tuning Implementation

```python
# finetune.py
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from datasets import load_dataset, Dataset
from peft import get_peft_model, LoraConfig, TaskType
import json
from config import FineTuningConfig

class TamilModelFineTuner:
    def __init__(self, config):
        self.config = config
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Using device: {self.device}")
    
    def load_data(self):
        """Load and prepare dataset"""
        print("Loading dataset...")
        
        # Load from JSON file
        with open(self.config.train_data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Create Hugging Face dataset
        dataset = Dataset.from_dict({
            'text': [item.get('output', '') for item in data]
        })
        
        # Split into train/val
        split_dataset = dataset.train_test_split(
            test_size=self.config.val_split,
            seed=42
        )
        
        print(f"Training examples: {len(split_dataset['train'])}")
        print(f"Validation examples: {len(split_dataset['test'])}")
        
        return split_dataset
    
    def load_model_and_tokenizer(self):
        """Load model and tokenizer"""
        print(f"Loading model: {self.config.model_name}")
        
        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.config.model_name,
            trust_remote_code=True
        )
        
        # Set pad token
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        # Load model
        model = AutoModelForCausalLM.from_pretrained(
            self.config.model_name,
            torch_dtype=torch.float16 if self.config.fp16 else torch.float32,
            device_map="auto",
            trust_remote_code=True
        )
        
        # Apply LoRA for efficient fine-tuning
        lora_config = LoraConfig(
            r=self.config.lora_r,
            lora_alpha=self.config.lora_alpha,
            target_modules=self.config.lora_target_modules,
            lora_dropout=self.config.lora_dropout,
            bias="none",
            task_type=TaskType.CAUSAL_LM
        )
        
        model = get_peft_model(model, lora_config)
        model.print_trainable_parameters()
        
        return model
    
    def tokenize_function(self, examples):
        """Tokenize examples"""
        return self.tokenizer(
            examples['text'],
            truncation=True,
            max_length=self.config.max_seq_length,
            padding='max_length'
        )
    
    def prepare_dataset(self, dataset):
        """Prepare dataset for training"""
        print("Tokenizing dataset...")
        
        tokenized_dataset = dataset.map(
            self.tokenize_function,
            batched=True,
            remove_columns=['text']
        )
        
        return tokenized_dataset
    
    def train(self):
        """Execute fine-tuning"""
        # Load data
        dataset = self.load_data()
        
        # Load model
        model = self.load_model_and_tokenizer()
        
        # Prepare dataset
        tokenized_dataset = self.prepare_dataset(dataset)
        
        # Training arguments
        training_args = TrainingArguments(
            output_dir=self.config.output_dir,
            num_train_epochs=self.config.num_train_epochs,
            per_device_train_batch_size=self.config.per_device_train_batch_size,
            per_device_eval_batch_size=self.config.per_device_eval_batch_size,
            gradient_accumulation_steps=self.config.gradient_accumulation_steps,
            learning_rate=self.config.learning_rate,
            warmup_steps=self.config.warmup_steps,
            weight_decay=self.config.weight_decay,
            logging_steps=self.config.logging_steps,
            save_steps=self.config.save_steps,
            eval_steps=self.config.eval_steps,
            save_total_limit=self.config.save_total_limit,
            fp16=self.config.fp16 and torch.cuda.is_available(),
            gradient_checkpointing=self.config.gradient_checkpointing,
            report_to=["wandb"],
            logging_dir='./logs',
            evaluation_strategy="steps",
            save_strategy="steps",
            load_best_model_at_end=True,
        )
        
        # Data collator
        data_collator = DataCollatorForLanguageModeling(
            self.tokenizer,
            mlm=False
        )
        
        # Trainer
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=tokenized_dataset['train'],
            eval_dataset=tokenized_dataset['test'],
            data_collator=data_collator,
        )
        
        # Train
        print("Starting training...")
        trainer.train()
        
        # Save model
        print(f"Saving model to {self.config.output_dir}")
        model.save_pretrained(self.config.output_dir)
        self.tokenizer.save_pretrained(self.config.output_dir)
        
        return trainer

# Usage
if __name__ == "__main__":
    config = FineTuningConfig()
    finetuner = TamilModelFineTuner(config)
    trainer = finetuner.train()
```

---

## 6. Evaluation and Testing

### Evaluation Metrics

```python
from rouge_score import rouge_scorer
from nltk.translate.bleu_score import sentence_bleu
import numpy as np

class ModelEvaluator:
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer
    
    def generate_response(self, prompt, max_length=100):
        """Generate response from model"""
        inputs = self.tokenizer.encode(prompt, return_tensors="pt")
        outputs = self.model.generate(
            inputs,
            max_length=max_length,
            temperature=0.7,
            top_p=0.9,
            do_sample=True
        )
        return self.tokenizer.decode(outputs[0])
    
    def evaluate_perplexity(self, test_dataset):
        """Calculate perplexity"""
        total_loss = 0
        total_tokens = 0
        
        with torch.no_grad():
            for batch in test_dataset:
                outputs = self.model(**batch)
                loss = outputs.loss
                total_loss += loss.item() * batch['input_ids'].shape[0]
                total_tokens += batch['input_ids'].shape[0]
        
        perplexity = np.exp(total_loss / total_tokens)
        return perplexity
    
    def evaluate_rouge(self, references, predictions):
        """Calculate ROUGE scores"""
        scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)
        scores = {'rouge1': [], 'rougeL': []}
        
        for ref, pred in zip(references, predictions):
            score = scorer.score(ref, pred)
            scores['rouge1'].append(score['rouge1'].fmeasure)
            scores['rougeL'].append(score['rougeL'].fmeasure)
        
        return {
            'rouge1': np.mean(scores['rouge1']),
            'rougeL': np.mean(scores['rougeL'])
        }
    
    def evaluate_bleu(self, references, predictions):
        """Calculate BLEU scores"""
        bleu_scores = []
        
        for ref, pred in zip(references, predictions):
            ref_tokens = ref.split()
            pred_tokens = pred.split()
            bleu = sentence_bleu([ref_tokens], pred_tokens)
            bleu_scores.append(bleu)
        
        return np.mean(bleu_scores)
```

---

## 7. Deployment Strategy

### Step 1: Push to Hugging Face

```bash
# Login to Hugging Face
huggingface-cli login

# Create model repository
huggingface-cli repo create tamil-study-buddy-finetuned --type model

# Push model
cd ./tamil-study-buddy-finetuned
git init
git add .
git commit -m "Fine-tuned Muruga model with colloquial Tamil data"
git remote add origin https://huggingface.co/grums18/tamil-study-buddy-finetuned
git push -u origin main
```

### Step 2: Create Streamlit App

```python
# app.py
import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

st.set_page_config(page_title="Tamil Study Buddy", layout="wide")

@st.cache_resource
def load_model():
    model_name = "grums18/tamil-study-buddy-finetuned"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16,
        device_map="auto"
    )
    return model, tokenizer

st.title("🇮🇳 Tamil Study Buddy")
st.write("AI Tutor that explains concepts in colloquial Tamil")

model, tokenizer = load_model()

# User input
user_query = st.text_area("உங்கள் கேள்வியை கேட்கவும்:", placeholder="எ.கா., தமிழ் பற்றி சொல்லு")

if st.button("பதிலளி"):
    if user_query:
        with st.spinner("சிந்திக்கிறேன்..."):
            inputs = tokenizer.encode(user_query, return_tensors="pt")
            outputs = model.generate(
                inputs,
                max_length=200,
                temperature=0.7,
                top_p=0.9,
                do_sample=True
            )
            response = tokenizer.decode(outputs[0])
            st.write(response)
```

---

## 8. Timeline and Milestones

### Week 1: Data Collection and Preparation
- Day 1-2: Collect colloquial Tamil data from various sources
- Day 3-4: Clean and deduplicate data
- Day 5: Annotate data for fine-tuning
- Day 6-7: Prepare training/validation splits

### Week 2: Fine-tuning
- Day 1-2: Set up infrastructure and dependencies
- Day 3-5: Execute fine-tuning (6-12 hours)
- Day 6: Evaluate model performance
- Day 7: Iterate and optimize

### Week 3: Deployment
- Day 1-2: Push model to Hugging Face
- Day 3-4: Create Streamlit app
- Day 5-6: Test and gather feedback
- Day 7: Document and prepare for production

---

## 9. Cost Analysis

| Component | Cost |
|-----------|------|
| **GPU Infrastructure** | $100-300 (or free with Colab) |
| **Data Collection** | $0 (automated) |
| **API Keys** | $0-50 (Twitter, Reddit) |
| **Hugging Face Hosting** | $0 (free tier) |
| **Total** | $100-350 |

---

## 10. Success Criteria

- ✅ Model generates coherent Tamil responses
- ✅ Responses are in colloquial Tamil (not formal)
- ✅ Perplexity < 50 on test set
- ✅ ROUGE-L score > 0.3
- ✅ Inference time < 2 seconds
- ✅ User satisfaction > 4/5 stars

---

## References

1. Hugging Face Model Hub: https://huggingface.co/models
2. Transformers Documentation: https://huggingface.co/docs/transformers
3. PEFT (Parameter-Efficient Fine-Tuning): https://github.com/huggingface/peft
4. Tamil NLP Resources: https://github.com/anandsimmy/Tamil-NLP
5. Colloquial Tamil Studies: https://www.researchgate.net/publication/Tamil_Colloquial_Language
