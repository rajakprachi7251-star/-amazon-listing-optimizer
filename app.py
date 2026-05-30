import streamlit as st
import openai
from dotenv import load_dotenv
import os
from utils.prompts import (
    get_system_prompt,
    get_title_prompt,
    get_bullets_prompt,
    get_description_prompt,
    get_keywords_prompt,
    get_seo_tips_prompt
)
from utils.export import (
    validate_title,
    validate_bullets,
    validate_description,
    calculate_seo_score,
    get_timestamp
)

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Check API key
if not openai.api_key:
    st.error("❌ OpenAI API key not found! Please add it to .env file")
    st.stop()

# Page Configuration
st.set_page_config(
    page_title="Amazon Listing Optimizer",
    page_icon="📦",
    layout="wide"
)

# App Title
st.title("📦 Amazon Listing Optimizer")
st.markdown("""
    Generate SEO-optimized Amazon product listings with AI in seconds!
    """)

st.markdown("---")

# Create two columns for layout
col1, col2 = st.columns([1, 1])

# LEFT COLUMN - INPUT FORM
with col1:
    st.header("📝 Product Information")
    
    product_name = st.text_input(
        label="Product Name *",
        placeholder="Example: Wireless Bluetooth Headphones"
    )
    
    category = st.selectbox(
        label="Product Category *",
        options=[
            "Electronics",
            "Fashion & Accessories",
            "Home & Kitchen",
            "Sports & Outdoors",
            "Beauty & Personal Care",
            "Toys & Games",
            "Books",
            "Other"
        ]
    )
    
    keywords = st.text_area(
        label="Target Keywords * (one per line)",
        placeholder="wireless headphones\nBluetooth\nnoise cancelling",
        height=100
    )
    
    current_description = st.text_area(
        label="Current Product Description",
        placeholder="Describe your product...",
        height=120
    )

# RIGHT COLUMN - SETTINGS
with col2:
    st.header("⚙️ Configuration")
    
    marketplace = st.selectbox(
        label="Select Marketplace *",
        options=["US (amazon.com)", "UK (amazon.co.uk)", "India (amazon.in)"]
    )
    
    tone = st.selectbox(
        label="Listing Tone *",
        options=[
            "Luxury (Premium, high-end)",
            "Casual (Friendly, relaxed)",
            "Technical (Detailed, specs)",
            "Beauty (Aspirational)",
            "Fitness (Energetic)",
            "Professional (Formal)"
        ]
    )
    
    st.markdown("---")
    
    # Generate Button
    generate_button = st.button(
        label="🚀 Generate Listing",
        use_container_width=True,
        type="primary"
    )

# Function to call OpenAI
def call_openai(prompt, max_tokens=1000):
    """Call OpenAI API"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": get_system_prompt()
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    
    except Exception as e:
        error_msg = str(e)
        if "authentication" in error_msg.lower():
            st.error("❌ Invalid OpenAI API key")
        elif "rate" in error_msg.lower():
            st.error("⏳ Rate limit reached. Wait a moment and try again")
        else:
            st.error(f"❌ Error: {error_msg}")
        return None
    except openai.error.RateLimitError:
        st.error("⏳ Rate limit reached. Wait 1 minute and try again")
        return None
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        return None

# MAIN LOGIC
if generate_button:
    # Validate inputs
    if not product_name.strip():
        st.error("❌ Please enter a product name")
        st.stop()
    
    if not keywords.strip():
        st.error("❌ Please enter at least one keyword")
        st.stop()
    
    # Generate content
    st.markdown("---")
    
    with st.spinner("🤖 AI is generating your listing... (10-30 seconds)"):
        title_prompt = get_title_prompt(product_name, category, keywords, tone)
        title = call_openai(title_prompt, max_tokens=200)
        
        if not title:
            st.stop()
        
        bullets_prompt = get_bullets_prompt(product_name, category, keywords, current_description, tone)
        bullets = call_openai(bullets_prompt, max_tokens=500)
        
        description_prompt = get_description_prompt(product_name, category, keywords, current_description, tone)
        description = call_openai(description_prompt, max_tokens=1500)
        
        keywords_prompt = get_keywords_prompt(product_name, category, keywords, current_description)
        backend_keywords = call_openai(keywords_prompt, max_tokens=500)
        
        seo_tips_prompt = get_seo_tips_prompt(product_name, title, bullets, description)
        seo_tips = call_openai(seo_tips_prompt, max_tokens=800)
    
    if not title:
        st.error("Failed to generate listing")
        st.stop()
    
    # DISPLAY RESULTS
    st.header("📋 Generated Listing")
    
    # SEO Score
    seo_score = calculate_seo_score(title, bullets, description)
    col_score1, col_score2, col_score3 = st.columns(3)
    with col_score1:
        st.metric("SEO Score", f"{seo_score}/100")
    with col_score2:
        st.metric("Title Length", f"{len(title)}/200")
    with col_score3:
        st.metric("Description Length", f"{len(description)}/2000")
    
    st.markdown("---")
    
    # Tabs for content
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["🎯 Title", "📌 Bullets", "📝 Description", "🔑 Keywords", "💡 SEO Tips"]
    )
    
    # TAB 1: TITLE
    with tab1:
        st.subheader("Optimized Amazon Title")
        is_valid_title, title_msg = validate_title(title)
        if is_valid_title:
            st.success(title_msg)
        else:
            st.warning(title_msg)
        
        st.text_area(
            label="Copy this title:",
            value=title,
            height=60,
            disabled=True,
            label_visibility="collapsed"
        )
    
    # TAB 2: BULLET POINTS
    with tab2:
        st.subheader("5 SEO Optimized Bullet Points")
        is_valid_bullets, bullets_msg = validate_bullets(bullets)
        if is_valid_bullets:
            st.success(bullets_msg)
        else:
            st.warning(bullets_msg)
        
        st.text_area(
            label="Copy these bullet points:",
            value=bullets,
            height=180,
            disabled=True,
            label_visibility="collapsed"
        )
    
    # TAB 3: DESCRIPTION
    with tab3:
        st.subheader("Product Description")
        is_valid_desc, desc_msg = validate_description(description)
        if is_valid_desc:
            st.success(desc_msg)
        else:
            st.warning(desc_msg)
        
        st.text_area(
            label="Copy this description:",
            value=description,
            height=250,
            disabled=True,
            label_visibility="collapsed"
        )
    
    # TAB 4: BACKEND KEYWORDS
    with tab4:
        st.subheader("Backend Search Terms (Hidden Keywords)")
        st.info("These keywords help Amazon find your product but buyers won't see them.")
        
        st.text_area(
            label="Copy backend keywords:",
            value=backend_keywords,
            height=150,
            disabled=True,
            label_visibility="collapsed"
        )
    
    # TAB 5: SEO TIPS
    with tab5:
        st.subheader("SEO Analysis & Optimization Tips")
        if seo_tips:
            st.markdown(seo_tips)
    
    # Export Section
    st.markdown("---")
    st.header("💾 Export Listing")
    
    # Create downloadable text file
    text_content = f"""AMAZON LISTING OPTIMIZATION
Generated: {get_timestamp()}

{'='*60}
PRODUCT: {product_name}
{'='*60}

TITLE ({len(title)} characters)
-------------------------------------------
{title}

BULLET POINTS
-------------------------------------------
{bullets}

DESCRIPTION ({len(description)} characters)
-------------------------------------------
{description}

BACKEND KEYWORDS
-------------------------------------------
{backend_keywords}

SEO TIPS
-------------------------------------------
{seo_tips}

{'='*60}
Generated with Amazon Listing Optimizer
"""
    
    st.download_button(
        label="📄 Download as TXT",
        data=text_content,
        file_name=f"listing_{get_timestamp()}.txt",
        mime="text/plain",
        use_container_width=True
    )
    
    st.success("✅ Listing generated successfully! Download or copy above.")

# DEFAULT STATE
else:
    st.markdown("---")
    st.header("📋 Generated Listing")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["🎯 Title", "📌 Bullets", "📝 Description", "🔑 Keywords", "💡 SEO Tips"]
    )
    
    with tab1:
        st.info("⏳ Fill in product info and click 'Generate Listing'")
    
    with tab2:
        st.info("⏳ Fill in product info and click 'Generate Listing'")
    
    with tab3:
        st.info("⏳ Fill in product info and click 'Generate Listing'")
    
    with tab4:
        st.info("⏳ Fill in product info and click 'Generate Listing'")
    
    with tab5:
        st.info("⏳ Fill in product info and click 'Generate Listing'")
    
    # Help section
    st.markdown("---")
    st.header("🎓 How to Use")
    st.markdown("""
    1. **Fill in product information** (name, category, keywords, description)
    2. **Choose settings** (marketplace, tone)
    3. **Click "Generate Listing"** button
    4. **Wait 15-30 seconds** for AI to create content
    5. **Copy or download** the results
    """)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: gray;'>
    <small>Amazon Listing Optimizer v1.0 | Powered by OpenAI</small>
    </div>
    """, unsafe_allow_html=True)
