"""
Prompt Engineering Module
Contains all AI prompts for Amazon listing generation
"""

def get_system_prompt():
    """
    System prompt - tells AI what role to play
    """
    return """You are an expert Amazon product listing optimizer with 10+ years 
of experience in e-commerce SEO and conversion rate optimization.

Your expertise includes:
- Amazon A9 search algorithm optimization
- Keyword placement strategies
- Psychological copywriting for conversions
- Amazon TOS compliance
- Multi-marketplace best practices

You understand:
- Buyers search behavior on Amazon
- What makes listings rank high
- How to write compelling, honest descriptions
- Character limits and formatting rules

Your goal: Generate high-converting, SEO-optimized Amazon listings 
that follow Amazon best practices and increase sales."""


def get_title_prompt(product_name, category, keywords, tone):
    """
    Generate optimized Amazon product title
    Amazon title limit: 200 characters
    """
    return f"""Generate an SEO-optimized Amazon product title for:

Product: {product_name}
Category: {category}
Target Keywords: {keywords}
Tone: {tone}

Requirements:
1. Must be under 200 characters (Amazon limit)
2. Include primary keyword at the beginning
3. Include 2-3 related keywords naturally
4. Create urgency/value proposition
5. Be compelling and professional
6. Follow {tone} tone
7. No all CAPS words
8. No misleading claims

Generate ONLY the title, nothing else.
Example format: "Premium Wireless Noise Cancelling Headphones with 40hr Battery"
"""


def get_bullets_prompt(product_name, category, keywords, description, tone):
    """
    Generate 5 optimized bullet points
    Amazon bullet limit: 5 points, 1000 characters total
    """
    return f"""Generate 5 compelling Amazon bullet points for:

Product: {product_name}
Category: {category}
Keywords: {keywords}
Description: {description}
Tone: {tone}

Requirements for each bullet point:
1. Start with a benefit or key feature
2. Include relevant keywords naturally
3. Be scannable (short and punchy)
4. 100-150 characters each
5. Highlight unique selling points
6. Use numbers/metrics where possible
7. Follow {tone} tone
8. No duplicate information

Format:
- First benefit with keyword
- Second feature benefit
- Third unique selling point
- Fourth value proposition
- Fifth call to action or warranty

Generate ONLY the 5 bullet points.
"""


def get_description_prompt(product_name, category, keywords, current_description, tone):
    """
    Generate detailed product description
    """
    return f"""Generate a compelling Amazon product description for:

Product: {product_name}
Category: {category}
Keywords: {keywords}
Current Description: {current_description}
Tone: {tone}

Requirements:
1. 1000-1500 characters
2. Start with hook (why customer needs this)
3. Include 3-5 key features
4. Include benefits (not just features)
5. Address customer pain points
6. Include social proof if applicable
7. Natural keyword placement
8. Follow {tone} tone
9. End with clear call-to-action
10. Use short paragraphs for readability

Structure:
- Opening hook (1-2 sentences)
- Key features & benefits (3-4 paragraphs)
- Use cases / How it helps
- Quality assurance / Warranty
- Call to action

Generate ONLY the description.
"""


def get_keywords_prompt(product_name, category, keywords, description):
    """
    Generate backend search terms
    Amazon backend keywords: up to 250 bytes per field, 5 fields
    """
    return f"""Generate backend search terms (also called search keywords) for Amazon.

Product: {product_name}
Category: {category}
Keywords: {keywords}
Description: {description}

Requirements:
1. Generate 5 sets of backend keywords
2. Each set max 50 characters
3. Don't repeat keywords already in title/bullets
4. Include long-tail keywords
5. Include synonym variations
6. Include common misspellings
7. Focus on search volume keywords
8. Comma-separated within each set
9. Avoid trademarked terms

Backend Keywords are HIDDEN from customers - for search optimization only.

Format your response as:
1. keyword1, keyword2, keyword3
2. keyword4, keyword5, keyword6
etc.

Generate ONLY the 5 sets of backend keywords.
"""


def get_seo_tips_prompt(product_name, title_text, bullets_text, description_text):
    """
    Generate SEO suggestions and tips
    """
    return f"""Analyze this Amazon listing and provide SEO improvement suggestions.

Product: {product_name}
Title: {title_text}
Bullets: {bullets_text}
Description: {description_text}

Provide:
1. Keyword density analysis (are keywords repeated too much/too little?)
2. Title optimization suggestions
3. Bullet point strengths & weaknesses
4. Description flow and clarity
5. Missing important keywords
6. Competitive advantages highlighted
7. Potential compliance issues
8. Overall SEO score (1-10)

Format as clear, actionable advice.
Keep response concise and practical.
"""


def get_full_prompt(product_name, category, keywords, description, marketplace, tone):
    """
    Generate complete listing in one go
    """
    marketplace_info = {
        "US (amazon.com)": "US market - USD pricing, English US",
        "UK (amazon.co.uk)": "UK market - GBP pricing, English UK",
        "India (amazon.in)": "India market - INR pricing, English India"
    }
    
    return f"""Generate a complete Amazon product listing.

PRODUCT DETAILS:
- Name: {product_name}
- Category: {category}
- Keywords: {keywords}
- Description: {description}
- Marketplace: {marketplace_info.get(marketplace, marketplace)}
- Tone: {tone}

GENERATE (in this exact order):

1. TITLE (max 200 characters):
[optimized title]

2. BULLET POINTS (5 points, max 1000 chars total):
[5 bullet points]

3. DESCRIPTION (1000-1500 characters):
[detailed description]

4. BACKEND KEYWORDS (5 sets, comma-separated):
[5 sets of backend keywords]

5. SEO TIPS:
[3-5 actionable optimization tips]

---
Follow all Amazon best practices and requirements for {marketplace}.
Optimize for conversions while maintaining honesty and compliance.
Use {tone} tone throughout.
"""
