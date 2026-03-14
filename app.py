import streamlit as st
import google.generativeai as genai
import requests
import json
import urllib.parse
import os
import random
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import textwrap

# --- API KEY ---
# Maine key yahan daal di hai, ab error nahi aayega
API_KEY = "AIzaSyDw2IM4S8e6_SmlRJcf67ZgVMyhjuMR8DQ"

st.set_page_config(page_title="Viral Post Generator", layout="wide")
st.title("🚀 AI Viral Post Generator")

def get_font():
    try: return ImageFont.truetype("arial.ttf", 50)
    except: return ImageFont.load_default()

story = st.text_area("Yahan apni story/facts daalo:", height=150)
num_posts = st.slider("Kitni Post?", 1, 10, 3)

if st.button("🪄 Magic Shuru Karo"):
    if not story:
        st.error("Pehle story daalo!")
    else:
        try:
            genai.configure(api_key=API_KEY)
            model = genai.GenerativeModel('gemini-1.5-pro')
            # Prompt fix: double {{ }} for JSON safety
            prompt = f"Create {num_posts} viral post concepts for: {story}. Return result as a raw JSON list of objects with these keys: {{'top_text': '...', 'image_prompt': '...', 'bottom_text': '...'}}"
            
            response = model.generate_content(prompt)
            clean_text = response.text.replace("```json", "").replace("```", "").strip()
            data = json.loads(clean_text)
            
            for item in data:
                img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(item['image_prompt'])}?width=1080&height=850&nologo=true&seed={random.randint(1,999)}"
                img = Image.open(BytesIO(requests.get(img_url).content))
                
                final = Image.new('RGB', (1080, 1350), 'white')
                d = ImageDraw.Draw(final)
                d.rectangle([0, 0, 1080, 200], fill="#FFFF00")
                d.text((50, 50), textwrap.fill(item['top_text'], 20), fill="black", font=get_font())
                final.paste(img, (0, 200))
                d.rectangle([0, 1050, 1080, 1350], fill="black")
                d.text((50, 1100), textwrap.fill(item['bottom_text'], 30), fill="white", font=get_font())
                
                st.image(final)
        except Exception as e:
            st.error(f"Error: {e}")
