import streamlit as st
import google.generativeai as genai
import requests
import json
import urllib.parse
import random
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import textwrap

# UI Setup
st.set_page_config(page_title="Free Viral Post Generator", layout="centered")
st.title("🚀 Free Viral Post Generator")

# Key Input
api_key = st.sidebar.text_input("🔑 Google AI Key", type="password")
story = st.text_area("Yahan story likho:", height=100)

if st.button("🪄 Magic Shuru Karo"):
    if not api_key or not story:
        st.error("Pehle Key aur Story daalo!")
    else:
        try:
            with st.spinner("🧠 AI dimaag laga raha hai..."):
                # Google Gemini Setup (gemini-pro use kiya hai jo sabse stable hai)
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-pro')
                
                # Prompt (JSON format mein)
                prompt = f"Create 1 viral post for: '{story}'. Return ONLY valid JSON: {{\"top_text\": \"...\", \"image_prompt\": \"...\", \"bottom_text\": \"...\"}}"
                
                response = model.generate_content(prompt)
                clean_json = response.text.replace("```json", "").replace("```", "").strip()
                data = json.loads(clean_json)
                
                # Image generation (POLLINATIONS AI - FREE)
                st.text("🎨 AI Photo bana raha hai...")
                encoded_prompt = urllib.parse.quote(data['image_prompt'])
                # Width/Height set hai
                img_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=850&nologo=true&seed={random.randint(1,999)}"
                img_response = requests.get(img_url)
                img = Image.open(BytesIO(img_response.content))
                
                # Design 4:5 (1080x1350)
                final = Image.new('RGB', (1080, 1350), 'white')
                draw = ImageDraw.Draw(final)
                
                # Yellow Top
                draw.rectangle([0, 0, 1080, 200], fill="#FFFF00")
                draw.text((40, 30), textwrap.fill(data['top_text'], 30), fill="black", font=ImageFont.load_default())
                
                # Image
                final.paste(img, (0, 200))
                
                # Black Bottom
                draw.rectangle([0, 1050, 1080, 1350], fill="black")
                draw.text((40, 1100), textwrap.fill(data['bottom_text'], 40), fill="white", font=ImageFont.load_default())
                
                st.image(final, use_column_width=True)
                
                buf = BytesIO()
                final.save(buf, format="PNG")
                st.download_button("📥 Download Image", buf.getvalue(), "post.png", "image/png")
        except Exception as e:
            st.error(f"Error: {e}")
