import streamlit as st
import openai
from dotenv import load_dotenv
import os

# Load environment
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    st.error("❌ OpenAI API key not found!")
    st.stop()

# Page setup
st.set_page_config(page_title="Amazon Listing Optimizer", page_icon="📦", layout="wide")
st.title("📦 Amazon Listing Optimizer")
st.write("Generate SEO-optimized Amazon listings with AI!")

# Input columns
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📝 Product Info")
    product_name = st.text_input("Product Name *", placeholder="Wireless Headphones")
    category = st.selectbox("Category *", ["Electronics", "Fashion", "Home", "Sports", "Beauty", "Toys", "Books", "Other"])
    keywords = st.text_area("Keywords (one per line) *", height=80, placeholder="wireless\nBluetooth\nnoise cancelling")
    description = st.text_area("Description", height=80, placeholder="Your product description...")

with col2:
    st.header("⚙️ Settings")
    marketplace = st.selectbox("Marketplace *", ["US (amazon.com)", "UK (amazon.co.uk)", "India (amazon.in)"])
    tone = st.selectbox("Tone *", ["Luxury", "Casual", "Technical", "Beauty", "Fitness", "Professional"])
    st.markdown("---")
    generate_btn = st.button("🚀 Generate Listing", use_container_width=True, type="primary")

# Main logic
if generate_btn:
    if not product_name.strip():
        st.error("❌ Enter product name")
        st.stop()
    if not keywords.strip():
        st.error("❌ Enter keywords")
        st.stop()
    
    st.markdown("---")
    st.header("📋 Generated Listing")
    
    with st.spinner("🤖 AI generating... (15-30 seconds)"):
        # Generate Title
        title_prompt = f"""Generate an SEO-optimized Amazon product title for:
Product: {product_name}
Category: {category}
Keywords: {keywords}
Tone: {tone}

Requirements:
- Under 200 characters
- Include primary keyword at start
- Include 2-3 related keywords
- Professional and compelling
- No ALL CAPS

Generate ONLY the title, nothing else."""

        try:
            title_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": title_prompt}],
                temperature=0.7,
                max_tokens=200
            )
            title = title_response.choices[0].message.content
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.stop()

        # Generate Bullets
        bullets_prompt = f"""Generate 5 compelling Amazon bullet points for:
Product: {product_name}
Category: {category}
Keywords: {keywords}
Description: {description}
Tone: {tone}

Format:
- Benefit/feature with keyword
- Key feature benefit
- Unique selling point
- Value proposition
- Call to action or warranty

Generate ONLY the 5 bullet points."""

        bullets_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": bullets_prompt}],
            temperature=0.7,
            max_tokens=500
        )
        bullets = bullets_response.choices[0].message.content

        # Generate Description
        description_prompt = f"""Generate a 1000-1500 character Amazon product description for:
Product: {product_name}
Category: {category}
Keywords: {keywords}
Current description: {description}
Tone: {tone}

Structure:
- Opening hook
- Key features & benefits (3-4 paragraphs)
- Use cases
- Quality assurance

Include relevant keywords naturally. Make it compelling and professional."""

        desc_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": description_prompt}],
            temperature=0.7,
            max_tokens=1500
        )
        product_description = desc_response.choices[0].message.content

        # Generate Backend Keywords
        keywords_prompt = f"""Generate 5 sets of backend search terms (hidden keywords) for Amazon.
Product: {product_name}
Category: {category}
Keywords: {keywords}

Requirements:
- 5 sets, each max 50 characters
- Comma-separated
- Long-tail variations
- Don't repeat main keywords
- Focus on search volume

Format as:
1. keyword1, keyword2, keyword3
2. keyword4, keyword5
etc."""

        kw_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": keywords_prompt}],
            temperature=0.7,
            max_tokens=500
        )
        backend_keywords = kw_response.choices[0].message.content

    # Display results
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Title", "📌 Bullets", "📝 Description", "🔑 Keywords"])
    
    with tab1:
        st.subheader("Optimized Title")
        st.success(f"✅ {len(title)}/200 characters")
        st.text_area("Copy this:", title, height=80, disabled=True, label_visibility="collapsed")
    
    with tab2:
        st.subheader("Bullet Points")
        st.text_area("Copy these:", bullets, height=150, disabled=True, label_visibility="collapsed")
    
    with tab3:
        st.subheader("Description")
        st.success(f"✅ {len(product_description)} characters")
        st.text_area("Copy this:", product_description, height=200, disabled=True, label_visibility="collapsed")
    
    with tab4:
        st.subheader("Backend Keywords")
        st.text_area("Copy these:", backend_keywords, height=150, disabled=True, label_visibility="collapsed")
    
    st.success("✅ Listing generated! Copy above content or use in Amazon seller account.")

st.markdown("---")
st.markdown("<div style='text-align: center; color: gray;'><small>Amazon Listing Optimizer | Powered by OpenAI</small></div>", unsafe_allow_html=True)
