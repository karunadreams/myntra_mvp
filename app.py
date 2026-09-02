import streamlit as st
from datetime import date, timedelta
from PIL import Image
import os
import base64
from typing import TypedDict, List

# Define Product and ScoredProduct Data Models
class Product(TypedDict):
    id: int
    name: str
    brand: str
    price: int
    original_price: int
    rating: float
    rating_count: int
    sizes: List[str]
    occasions: List[str]
    delivery_days: int
    fit_summary_template: str
    fit_review_count: int
    keywords: List[str]
    image_path: str

class ScoredProduct(TypedDict):
    product: Product
    score: int
    has_size: bool
    occ_match: bool
    arrives_on_time: bool

def calculate_winner_scoring(
    selected_products: List[Product],
    user_occ: str,
    user_size: str,
    days_to_event: int
) -> List[ScoredProduct]:
    """
    Silent Winner Confidence Engine Algorithm:
    Evaluates size availability, body-fit match, delivery speed, and star rating.
    Returns list of ScoredProduct sorted by (score DESC, rating DESC, price ASC).
    """
    scored_products: List[ScoredProduct] = []
    for prod in selected_products:
        score = 0
        
        # +3 pts if available in user's size
        has_size = user_size in prod["sizes"]
        if has_size:
            score += 3

        # +2 pts if occasion matches
        occ_match = user_occ in prod["occasions"]
        if occ_match:
            score += 2

        # +2 pts if delivery before event
        arrives_on_time = prod["delivery_days"] <= days_to_event
        if arrives_on_time:
            score += 2

        # +1 pt if rating >= 4.2
        if prod["rating"] >= 4.2:
            score += 1

        sp: ScoredProduct = {
            "product": prod,
            "score": score,
            "has_size": has_size,
            "occ_match": occ_match,
            "arrives_on_time": arrives_on_time
        }
        scored_products.append(sp)

    scored_products.sort(
        key=lambda x: (x["score"], x["product"]["rating"], -x["product"]["price"]),
        reverse=True
    )
    return scored_products

# Helper to clean multi-line HTML strings so no line starts with 4+ spaces (preventing Markdown code block parsing)
def clean_html(html_str: str) -> str:
    lines = [line.strip() for line in html_str.strip().split("\n") if line.strip()]
    return "\n".join(lines)

# Set page configuration
st.set_page_config(
    page_title="Myntra — Wishlist Decision Panel",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inject Custom CSS for Exact Pixel-Accurate Live Myntra Desktop & Mobile UI/UX Design System
st.markdown("""
<style>
    /* Pure White Page Canvas */
    .stApp {
        background-color: #FFFFFF !important;
        color: #282C3F !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    /* Desktop Sticky Header */
    .myntra-desktop-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 14px 40px;
        background: #FFFFFF;
        box-shadow: 0 4px 12px 0 rgba(0, 0, 0, 0.05);
        position: sticky;
        top: 0;
        z-index: 999;
        border-bottom: 1px solid #EAEAEC;
    }

    .header-brand-section {
        display: flex;
        align-items: center;
        gap: 36px;
    }

    .myntra-logo-wrap {
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .cat-nav-links {
        display: flex;
        align-items: center;
        gap: 28px;
        font-size: 14px;
        font-weight: 700;
        color: #282C3F;
        letter-spacing: 0.3px;
        text-transform: uppercase;
    }

    .cat-item {
        cursor: pointer;
        padding-bottom: 2px;
    }

    .cat-item:hover {
        border-bottom: 2px solid #FF3F6C;
    }

    .cat-badge-new {
        font-size: 9px;
        color: #FF3F6C;
        font-weight: 800;
        vertical-align: super;
    }

    /* Desktop Search Box */
    .desktop-search-bar {
        display: flex;
        align-items: center;
        background: #F5F5F6;
        border-radius: 4px;
        padding: 10px 16px;
        width: 420px;
        gap: 10px;
        border: 1px solid #F5F5F6;
    }

    .desktop-search-input {
        border: none;
        background: transparent;
        width: 100%;
        font-size: 14px;
        color: #282C3F;
        outline: none;
    }

    .desktop-actions-right {
        display: flex;
        align-items: center;
        gap: 28px;
    }

    .action-nav-box {
        display: flex;
        flex-direction: column;
        align-items: center;
        font-size: 12px;
        font-weight: 700;
        color: #282C3F;
        cursor: pointer;
        position: relative;
    }

    .badge-pink-count {
        position: absolute;
        top: -4px;
        right: -8px;
        background: #FF3F6C;
        color: #FFFFFF;
        border-radius: 50%;
        width: 16px;
        height: 16px;
        font-size: 10px;
        font-weight: 800;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    /* Mobile Header & Pincode Bar */
    .myntra-mobile-header {
        display: none;
        flex-direction: column;
        background: #FFFFFF;
        border-bottom: 1px solid #EAEAEC;
        position: sticky;
        top: 0;
        z-index: 999;
    }

    .mobile-header-top {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 10px 16px;
    }

    .mobile-pincode-bar {
        background: #F4F4F8;
        padding: 6px 16px;
        font-size: 12px;
        color: #282C3F;
        display: flex;
        align-items: center;
        justify-content: space-between;
        font-weight: 600;
    }

    .mobile-search-row {
        padding: 8px 16px;
    }

    /* Promo Banners */
    .ticket-promo-banner {
        background: linear-gradient(135deg, #FF5722, #FF905A);
        color: #FFFFFF;
        border-radius: 8px;
        padding: 16px 24px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(255, 87, 34, 0.2);
    }

    .hero-banner-brands {
        background: linear-gradient(135deg, #1E88E5, #00ACC1);
        color: #FFFFFF;
        border-radius: 8px;
        padding: 28px 32px;
        margin-bottom: 20px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 4px 14px rgba(30, 136, 229, 0.25);
    }

    .bank-strip-bar {
        background: #FFF8F6;
        border: 1px solid #FFD0C5;
        border-radius: 6px;
        padding: 10px 16px;
        font-size: 13px;
        font-weight: 700;
        color: #FF3F6C;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 24px;
    }

    /* Category Pill Circle Stories */
    .cat-circle-wrap {
        display: flex;
        gap: 16px;
        overflow-x: auto;
        padding-bottom: 12px;
        margin-bottom: 24px;
    }

    .cat-circle-card {
        display: flex;
        flex-direction: column;
        align-items: center;
        min-width: 80px;
        cursor: pointer;
    }

    .cat-circle-img {
        width: 70px;
        height: 70px;
        border-radius: 50%;
        object-fit: cover;
        border: 2px solid #FF3F6C;
        padding: 2px;
        margin-bottom: 6px;
    }

    .cat-circle-title {
        font-size: 11px;
        font-weight: 800;
        color: #282C3F;
        text-align: center;
        text-transform: uppercase;
    }

    /* Product Cards */
    .product-card-white {
        background: #FFFFFF;
        border: 1px solid #EAEAEC;
        border-radius: 4px;
        padding: 10px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        position: relative;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .product-card-white:hover {
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
    }

    .product-card-white.selected {
        border: 2.5px solid #FF3F6C;
        background: #FFF5F7;
    }

    /* Image Overlay Rating Badge */
    .img-rating-badge {
        position: absolute;
        bottom: 8px;
        left: 8px;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(4px);
        border-radius: 2px;
        padding: 2px 6px;
        font-size: 11px;
        font-weight: 700;
        color: #282C3F;
        display: inline-flex;
        align-items: center;
        gap: 3px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
    }

    .star-icon-green {
        color: #03A685;
        font-size: 12px;
    }

    .card-brand-name {
        font-size: 15px;
        font-weight: 800;
        color: #282C3F;
        text-transform: uppercase;
        margin-top: 8px;
        margin-bottom: 2px;
    }

    .card-title-text {
        font-size: 13px;
        color: #535766;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        margin-bottom: 8px;
    }

    .price-wrap {
        display: flex;
        align-items: center;
        gap: 6px;
        margin-bottom: 8px;
    }

    .price-current {
        font-size: 15px;
        font-weight: 800;
        color: #282C3F;
    }

    .price-mrp {
        font-size: 12px;
        text-decoration: line-through;
        color: #7E818C;
    }

    .price-off {
        font-size: 12px;
        font-weight: 700;
        color: #FF905A;
    }

    /* Decision Panel Column Surface */
    .decision-card-white {
        background: #FFFFFF;
        border: 1px solid #EAEAEC;
        border-radius: 6px;
        padding: 14px;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.05);
        position: relative;
    }

    .decision-card-white.winner {
        border: 2.5px solid #FF3F6C;
        box-shadow: 0 4px 20px rgba(255, 63, 108, 0.25);
    }

    .winner-flag-badge {
        position: absolute;
        top: -12px;
        left: 50%;
        transform: translateX(-50%);
        background: #FF3F6C;
        color: #FFFFFF;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 0.6px;
        padding: 4px 14px;
        border-radius: 12px;
        text-transform: uppercase;
        box-shadow: 0 2px 6px rgba(255, 63, 108, 0.35);
    }

    .attr-label {
        font-size: 11px;
        font-weight: 700;
        color: #7E818C;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 10px;
        margin-bottom: 2px;
    }

    .attr-value {
        font-size: 13px;
        font-weight: 600;
        color: #282C3F;
    }

    .keyword-pill {
        display: inline-block;
        background: #F5F5F6;
        color: #3E4152;
        border-radius: 12px;
        padding: 3px 9px;
        font-size: 11px;
        font-weight: 600;
        margin: 2px;
        border: 1px solid #EAEAEC;
    }

    /* Layer 4 Passive AI Recommendation Banner */
    .rec-banner-white {
        background: #FFFFFF;
        border: 1.5px solid #FF3F6C;
        border-radius: 8px;
        padding: 18px 24px;
        margin-top: 24px;
        margin-bottom: 20px;
        text-align: center;
        box-shadow: 0 4px 14px rgba(255, 63, 108, 0.12);
    }

    .rec-title-bold {
        font-size: 16px;
        font-weight: 800;
        color: #282C3F;
        margin-bottom: 4px;
    }

    .text-pink {
        color: #FF3F6C;
    }

    .rec-subtitle {
        font-size: 13px;
        color: #535766;
    }

    /* Sticky Bottom Nav Bar */
    .myntra-bottom-bar {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: #FFFFFF;
        border-top: 1px solid #EAEAEC;
        display: flex;
        justify-content: space-around;
        padding: 8px 0;
        z-index: 1000;
        box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.05);
    }

    .bottom-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        font-size: 11px;
        font-weight: 700;
        color: #696E79;
        cursor: pointer;
        text-decoration: none;
    }

    .bottom-item.active {
        color: #FF3F6C;
    }

    /* Primary & Secondary Buttons Styling */
    .stButton > button {
        border-radius: 4px;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        transition: all 0.2s ease;
    }

    /* Responsive Mobile Layout Rules */
    @media (max-width: 768px) {
        .myntra-desktop-header {
            display: none;
        }
        .myntra-mobile-header {
            display: flex;
        }
        div[data-testid="column"] {
            min-width: 250px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# EXPANDED 15 MYNTRA PRODUCT TEST DATASET
# ---------------------------------------------------------
PRODUCTS: List[Product] = [
    {
        "id": 1,
        "name": "Embroidered Anarkali Kurta",
        "brand": "Libas",
        "price": 1299,
        "original_price": 2499,
        "rating": 4.3,
        "rating_count": 1240,
        "sizes": ["S", "M", "L", "XL"],
        "occasions": ["Wedding Guest", "Festival"],
        "delivery_days": 4,
        "fit_summary_template": "True to size, roomy shoulders",
        "fit_review_count": 34,
        "keywords": ["Fits true to size", "Color matches photos", "Good for functions"],
        "image_path": "assets/libas.jpg"
    },
    {
        "id": 2,
        "name": "Floral Printed Straight Kurta",
        "brand": "W",
        "price": 999,
        "original_price": 1799,
        "rating": 4.1,
        "rating_count": 850,
        "sizes": ["XS", "S", "M"],
        "occasions": ["Office Party", "Casual"],
        "delivery_days": 3,
        "fit_summary_template": "Runs slightly small, order one size up",
        "fit_review_count": 19,
        "keywords": ["Runs small", "Good for petite frame", "Color matches photos"],
        "image_path": "assets/w.jpg"
    },
    {
        "id": 3,
        "name": "Woven Design Kurta Set",
        "brand": "Biba",
        "price": 1799,
        "original_price": 3199,
        "rating": 4.5,
        "rating_count": 2100,
        "sizes": ["S", "M", "L"],
        "occasions": ["Wedding Guest", "Festival", "Date Night"],
        "delivery_days": 5,
        "fit_summary_template": "Fits true to size, premium flowy fit",
        "fit_review_count": 48,
        "keywords": ["Fits true to size", "Premium feel", "Best for festive"],
        "image_path": "assets/biba.jpg"
    },
    {
        "id": 4,
        "name": "Solid Straight Kurta",
        "brand": "Aurelia",
        "price": 849,
        "original_price": 1499,
        "rating": 3.9,
        "rating_count": 620,
        "sizes": ["M", "L", "XL"],
        "occasions": ["Office Party", "Casual"],
        "delivery_days": 2,
        "fit_summary_template": "Slightly boxy cut, runs large",
        "fit_review_count": 14,
        "keywords": ["Runs large", "Comfortable fabric", "Good daily wear"],
        "image_path": "assets/aurelia.jpg"
    },
    {
        "id": 5,
        "name": "Printed Wrap Kurta",
        "brand": "Global Desi",
        "price": 1499,
        "original_price": 2799,
        "rating": 4.4,
        "rating_count": 1580,
        "sizes": ["XS", "S", "M", "L"],
        "occasions": ["Date Night", "Casual", "Festival"],
        "delivery_days": 3,
        "fit_summary_template": "Fits true to size, highly flattering",
        "fit_review_count": 29,
        "keywords": ["Fits true to size", "Very flattering", "Silky fabric"],
        "image_path": "assets/global_desi.jpg"
    },
    {
        "id": 6,
        "name": "Chanderi Silk Ethnic Kurta",
        "brand": "Sangria",
        "price": 1599,
        "original_price": 3499,
        "rating": 4.6,
        "rating_count": 940,
        "sizes": ["S", "M", "L", "XL"],
        "occasions": ["Wedding Guest", "Festival"],
        "delivery_days": 3,
        "fit_summary_template": "True to size, royal shine",
        "fit_review_count": 26,
        "keywords": ["Royal shine", "Fits true to size", "Perfect for sangeet"],
        "image_path": "assets/libas.jpg"
    },
    {
        "id": 7,
        "name": "Bandhani Print Silk Blend Kurta",
        "brand": "Indo Era",
        "price": 1399,
        "original_price": 2999,
        "rating": 4.2,
        "rating_count": 1120,
        "sizes": ["XS", "S", "M", "L"],
        "occasions": ["Festival", "Casual"],
        "delivery_days": 4,
        "fit_summary_template": "Comfortable chest fit, lightweight",
        "fit_review_count": 21,
        "keywords": ["Lightweight silk", "Vibrant colors", "True to size"],
        "image_path": "assets/w.jpg"
    },
    {
        "id": 8,
        "name": "Foil Printed Straight Kurta",
        "brand": "Anouk",
        "price": 799,
        "original_price": 1599,
        "rating": 4.0,
        "rating_count": 780,
        "sizes": ["S", "M", "L"],
        "occasions": ["Office Party", "Casual"],
        "delivery_days": 2,
        "fit_summary_template": "Slim waist fit, size up if broad",
        "fit_review_count": 15,
        "keywords": ["Slim waist", "Budget friendly", "Good workwear"],
        "image_path": "assets/aurelia.jpg"
    },
    {
        "id": 9,
        "name": "Mirror Work Georgette Kurta",
        "brand": "Kalini",
        "price": 1899,
        "original_price": 3999,
        "rating": 4.7,
        "rating_count": 2450,
        "sizes": ["S", "M", "L", "XL"],
        "occasions": ["Wedding Guest", "Festival"],
        "delivery_days": 3,
        "fit_summary_template": "Flattering flow, true to size",
        "fit_review_count": 52,
        "keywords": ["Stunning mirror work", "Heavy festive look", "Comfortable lining"],
        "image_path": "assets/biba.jpg"
    },
    {
        "id": 10,
        "name": "Festive Metallic Print Kurta",
        "brand": "Ahalyaa",
        "price": 1649,
        "original_price": 3299,
        "rating": 4.3,
        "rating_count": 1310,
        "sizes": ["S", "M", "L"],
        "occasions": ["Festival", "Date Night"],
        "delivery_days": 4,
        "fit_summary_template": "Roomy fit, soft inner lining",
        "fit_review_count": 31,
        "keywords": ["Metallic shine", "Soft fabric", "Runs slightly large"],
        "image_path": "assets/global_desi.jpg"
    },
    {
        "id": 11,
        "name": "Embroidered A-Line Silk Kurta",
        "brand": "Varanga",
        "price": 2199,
        "original_price": 4599,
        "rating": 4.5,
        "rating_count": 1890,
        "sizes": ["S", "M", "L", "XL"],
        "occasions": ["Wedding Guest", "Festival"],
        "delivery_days": 4,
        "fit_summary_template": "True to size, regal flare",
        "fit_review_count": 41,
        "keywords": ["Regal flare", "High quality threadwork", "Fits perfectly"],
        "image_path": "assets/libas.jpg"
    },
    {
        "id": 12,
        "name": "Silk Blend Straight Kurta",
        "brand": "Mitera",
        "price": 1099,
        "original_price": 2199,
        "rating": 4.2,
        "rating_count": 890,
        "sizes": ["XS", "S", "M"],
        "occasions": ["Office Party", "Casual"],
        "delivery_days": 3,
        "fit_summary_template": "Straight tailored cut, true to size",
        "fit_review_count": 18,
        "keywords": ["Clean tailored look", "Great fabric", "Comfortable collar"],
        "image_path": "assets/w.jpg"
    },
    {
        "id": 13,
        "name": "Poly Silk Flared Kurta",
        "brand": "Janasya",
        "price": 1149,
        "original_price": 2399,
        "rating": 4.1,
        "rating_count": 960,
        "sizes": ["S", "M", "L"],
        "occasions": ["Casual", "Festival"],
        "delivery_days": 3,
        "fit_summary_template": "Flowy flare, snug bust fit",
        "fit_review_count": 22,
        "keywords": ["Flowy silhouette", "Vibrant prints", "Wrinkle free"],
        "image_path": "assets/global_desi.jpg"
    },
    {
        "id": 14,
        "name": "Luxury Zari Embroidered Kurta Set",
        "brand": "Wishful by W",
        "price": 2999,
        "original_price": 5999,
        "rating": 4.8,
        "rating_count": 3100,
        "sizes": ["S", "M", "L", "XL"],
        "occasions": ["Wedding Guest", "Festival"],
        "delivery_days": 5,
        "fit_summary_template": "Couture fit, premium silk texture",
        "fit_review_count": 64,
        "keywords": ["Couture quality", "Rich zari work", "Top wedding choice"],
        "image_path": "assets/biba.jpg"
    },
    {
        "id": 15,
        "name": "Jashn Collection Silk Kurta Set",
        "brand": "House of Pataudi",
        "price": 2499,
        "original_price": 4999,
        "rating": 4.6,
        "rating_count": 2280,
        "sizes": ["S", "M", "L"],
        "occasions": ["Wedding Guest", "Festival", "Date Night"],
        "delivery_days": 4,
        "fit_summary_template": "Royal tailoring, true to size",
        "fit_review_count": 55,
        "keywords": ["Royal aesthetic", "Premium dupatta", "True to size"],
        "image_path": "assets/libas.jpg"
    }
]

# ---------------------------------------------------------
# SESSION STATE INITIALIZATION
# ---------------------------------------------------------
if "current_screen" not in st.session_state:
    st.session_state.current_screen = 1

if "wishlist_ids" not in st.session_state:
    st.session_state.wishlist_ids = [1, 3, 6, 9, 14]

if "selected_ids" not in st.session_state:
    st.session_state.selected_ids = [3, 14]

if "body_profile" not in st.session_state:
    st.session_state.body_profile = {
        "height": "5'3\" - 5'5\"",
        "size": "S",
        "occasion": "Wedding Guest",
        "event_date": date.today() + timedelta(days=5)
    }

if "cart_items" not in st.session_state:
    st.session_state.cart_items = []

# Helper to convert image to Base64
def get_image_base64(image_path: str) -> str:
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            return f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode('utf-8')}"
    return ""

# ---------------------------------------------------------
# REAL LIVE MYNTRA TOP NAVBAR (DESKTOP & MOBILE ADAPTIVE)
# ---------------------------------------------------------
cart_count = len(st.session_state.cart_items)
wishlist_count = len(st.session_state.wishlist_ids)

logo_b64 = get_image_base64("assets/myntra_logo.jpg")
logo_img_html = f'<img src="{logo_b64}" style="height:36px; object-fit:contain; border-radius:4px;" />' if logo_b64 else '<span class="logo-pink">myntra</span>'

# Desktop Header HTML
desktop_header_html = f"""
<div class="myntra-desktop-header">
<div class="header-brand-section">
<div class="myntra-logo-wrap">
{logo_img_html}
<span style="font-size:12px; font-weight:700; color:#535766; margin-left:4px; border-left:1px solid #EAEAEC; padding-left:8px;">DECISION PANEL</span>
</div>
<div class="cat-nav-links">
<span class="cat-item">MEN</span>
<span class="cat-item">WOMEN</span>
<span class="cat-item">KIDS</span>
<span class="cat-item">HOME</span>
<span class="cat-item">BEAUTY</span>
<span class="cat-item">GENZ</span>
<span class="cat-item">STUDIO <span class="cat-badge-new">NEW</span></span>
</div>
</div>
<div class="desktop-search-bar">
<span style="color:#696E79;">🔍</span>
<input type="text" class="desktop-search-input" placeholder="Search for products, brands and more" readonly />
</div>
<div class="desktop-actions-right">
<div class="action-nav-box">
<span>👤</span>
<span>Profile</span>
</div>
<div class="action-nav-box">
<span>❤️</span>
<span>Wishlist</span>
<span class="badge-pink-count">{wishlist_count}</span>
</div>
<div class="action-nav-box">
<span>🛍️</span>
<span>Bag</span>
<span class="badge-pink-count">{cart_count}</span>
</div>
</div>
</div>
"""

# Mobile Header HTML
mobile_header_html = f"""
<div class="myntra-mobile-header">
<div class="mobile-header-top">
<div style="display:flex; align-items:center; gap:12px;">
<span style="font-size:20px; font-weight:800; cursor:pointer;">≡</span>
{logo_img_html}
</div>
<div style="display:flex; align-items:center; gap:16px;">
<span style="font-size:16px; cursor:pointer;">➕</span>
<span style="font-size:16px; cursor:pointer; position:relative;">❤️<span class="badge-pink-count" style="top:-6px; right:-8px;">{wishlist_count}</span></span>
<span style="font-size:16px; cursor:pointer; position:relative;">🛍️<span class="badge-pink-count" style="top:-6px; right:-8px;">{cart_count}</span></span>
</div>
</div>
<div class="mobile-pincode-bar">
<span>📍 <b>Select Delivery Location</b> (110092)</span>
<span>⌄</span>
</div>
<div class="mobile-search-row">
<div class="desktop-search-bar" style="width:100%;">
<span>🔍</span>
<input type="text" class="desktop-search-input" placeholder="Search for products, brands and more" readonly />
</div>
</div>
</div>
"""

st.markdown(clean_html(desktop_header_html), unsafe_allow_html=True)
st.markdown(clean_html(mobile_header_html), unsafe_allow_html=True)

# Navigation Bar Controllers
nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns(5)
with nav_col1:
    if st.button("🛍️ Catalog Feed", use_container_width=True, type="primary" if st.session_state.current_screen == 1 else "secondary"):
        st.session_state.current_screen = 1
        st.rerun()
with nav_col2:
    if st.button(f"❤️ Wishlist ({wishlist_count})", use_container_width=True, type="primary" if st.session_state.current_screen == 2 else "secondary"):
        st.session_state.current_screen = 2
        st.rerun()
with nav_col3:
    if st.button("👤 Profile", use_container_width=True, type="primary" if st.session_state.current_screen == 3 else "secondary"):
        st.session_state.current_screen = 3
        st.rerun()
with nav_col4:
    if st.button("⚖️ Decision Panel", use_container_width=True, type="primary" if st.session_state.current_screen == 4 else "secondary"):
        st.session_state.current_screen = 4
        st.rerun()
with nav_col5:
    if st.button(f"🛍️ Bag ({cart_count})", use_container_width=True, type="primary" if st.session_state.current_screen == 5 else "secondary"):
        st.session_state.current_screen = 5
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# =========================================================
# SCREEN 1: PRODUCT CATALOG & REAL PROMO BANNERS
# =========================================================
if st.session_state.current_screen == 1:
    # Promo Ticket Banner
    ticket_html = """
    <div class="ticket-promo-banner">
    <div>
    <h3 style="margin:0; font-size:22px; font-weight:900;">FLAT ₹300 OFF</h3>
    <p style="margin:2px 0 0 0; font-size:13px;">On Your 1st Purchase Via Myntra App!</p>
    </div>
    <div style="background:#FFFFFF; color:#FF5722; font-weight:800; font-size:13px; padding:6px 14px; border-radius:4px;">
    CODE: MYNTRA300
    </div>
    </div>
    """
    st.markdown(clean_html(ticket_html), unsafe_allow_html=True)

    # Hero Big Brands Bash Banner
    hero_banner_html = """
    <div class="hero-banner-brands">
    <div style="display:flex; justify-content:space-between; align-items:center;">
    <div>
    <span style="background:#FF3F6C; color:#FFFFFF; font-size:11px; font-weight:800; padding:3px 10px; border-radius:12px; text-transform:uppercase;">BIG BRANDS BASH • LIVE NOW</span>
    <h1 style="margin:8px 0 4px 0; font-size:32px; font-weight:900;">50 - 80% OFF</h1>
    <p style="margin:0; font-size:16px; font-weight:500;">Irresistible Brands, Best Prices for Festive & Wedding Season</p>
    </div>
    <div style="display:flex; gap:12px;">
    <span style="background:rgba(255,255,255,0.25); backdrop-filter:blur(4px); padding:8px 18px; border-radius:20px; font-weight:700; font-size:14px; cursor:pointer;">Him ❯</span>
    <span style="background:#FFFFFF; color:#1E88E5; padding:8px 18px; border-radius:20px; font-weight:800; font-size:14px; cursor:pointer;">Her ❯</span>
    </div>
    </div>
    </div>
    """
    st.markdown(clean_html(hero_banner_html), unsafe_allow_html=True)

    # Bank Offer Strip
    bank_html = """
    <div class="bank-strip-bar">
    <span>🏦 <b>RBL BANK / HSBC BANK</b> | Get 10% Instant Discount* on credit card transactions</span>
    <span>T&C Apply ❯</span>
    </div>
    """
    st.markdown(clean_html(bank_html), unsafe_allow_html=True)

    # Category Circle Stories (Horizontal Scroll)
    libas_b64 = get_image_base64("assets/libas.jpg")
    biba_b64 = get_image_base64("assets/biba.jpg")
    w_b64 = get_image_base64("assets/w.jpg")
    aurelia_b64 = get_image_base64("assets/aurelia.jpg")
    gdesi_b64 = get_image_base64("assets/global_desi.jpg")

    stories_html = f"""
    <div class="cat-circle-wrap">
    <div class="cat-circle-card">
    <img src="{libas_b64}" class="cat-circle-img" />
    <span class="cat-circle-title">Kurta Sets</span>
    </div>
    <div class="cat-circle-card">
    <img src="{biba_b64}" class="cat-circle-img" />
    <span class="cat-circle-title">Dresses</span>
    </div>
    <div class="cat-circle-card">
    <img src="{w_b64}" class="cat-circle-img" />
    <span class="cat-circle-title">Kurtas</span>
    </div>
    <div class="cat-circle-card">
    <img src="{aurelia_b64}" class="cat-circle-img" />
    <span class="cat-circle-title">Shirts</span>
    </div>
    <div class="cat-circle-card">
    <img src="{gdesi_b64}" class="cat-circle-img" />
    <span class="cat-circle-title">Casual Shoes</span>
    </div>
    </div>
    """
    st.markdown(clean_html(stories_html), unsafe_allow_html=True)

    # Catalog Grid
    st.markdown("<h3 style='color:#282C3F; font-weight:800; margin-bottom:14px;'>WOMEN'S ETHNIC COLLECTION</h3>", unsafe_allow_html=True)

    for row_start in range(0, len(PRODUCTS), 5):
        row_prods = PRODUCTS[row_start:row_start + 5]
        cols = st.columns(len(row_prods))
        for idx, prod in enumerate(row_prods):
            with cols[idx]:
                is_in_wishlist = prod["id"] in st.session_state.wishlist_ids
                card_class = "product-card-white selected" if is_in_wishlist else "product-card-white"
                
                img_b64 = get_image_base64(prod["image_path"])
                
                rating_overlay_html = f"""
                <div class="img-rating-badge">
                <span>{prod['rating']}</span>
                <span class="star-icon-green">★</span>
                <span>|</span>
                <span>{prod['rating_count']}</span>
                </div>
                """
                
                img_container_html = f"""
                <div style="position:relative; width:100%; height:200px; margin-bottom:8px;">
                <img src="{img_b64}" style="width:100%; height:200px; border-radius:4px; object-fit:cover;" />
                {rating_overlay_html}
                </div>
                """ if img_b64 else ''
                
                discount_pct = int(((prod["original_price"] - prod["price"]) / prod["original_price"]) * 100)
                
                card_html = f"""
                <div class="{card_class}">
                {img_container_html}
                <div class="card-brand-name">{prod['brand']}</div>
                <div class="card-title-text">{prod['name']}</div>
                <div class="price-wrap">
                <span class="price-current">₹{prod['price']:,}</span>
                <span class="price-mrp">₹{prod['original_price']:,}</span>
                <span class="price-off">({discount_pct}% OFF)</span>
                </div>
                </div>
                """
                st.markdown(clean_html(card_html), unsafe_allow_html=True)
                
                st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)
                
                if is_in_wishlist:
                    if st.button("❤️ WISHLISTED", key=f"cat_btn_{prod['id']}", type="primary", use_container_width=True):
                        st.session_state.wishlist_ids.remove(prod["id"])
                        if prod["id"] in st.session_state.selected_ids:
                            st.session_state.selected_ids.remove(prod["id"])
                        st.rerun()
                else:
                    if st.button("♡ SAVE TO WISHLIST", key=f"cat_btn_{prod['id']}", use_container_width=True):
                        st.session_state.wishlist_ids.append(prod["id"])
                        st.rerun()

        st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

    st.markdown("<br><hr style='border-color:#EAEAEC;'><br>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.session_state.wishlist_ids:
            if st.button(f"GO TO WISHLIST ({len(st.session_state.wishlist_ids)} Items Saved) →", type="primary", use_container_width=True):
                st.session_state.current_screen = 2
                st.rerun()
        else:
            st.button("WISHLIST IS EMPTY — SAVE ITEMS ABOVE", disabled=True, use_container_width=True)

# =========================================================
# SCREEN 2: NATIVE MYNTRA WISHLIST PAGE (Compare Selection)
# =========================================================
elif st.session_state.current_screen == 2:
    wishlist_products = [p for p in PRODUCTS if p["id"] in st.session_state.wishlist_ids]

    w_head_html = f"""
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
    <h3 style="margin:0; color:#282C3F; font-weight:800;">MY WISHLIST <span style="font-size:14px; color:#7E818C; font-weight:500;">({len(wishlist_products)} Items)</span></h3>
    <span style="font-size:12px; color:#FF3F6C; font-weight:700;">Select 2 to 4 items to Compare</span>
    </div>
    """
    st.markdown(clean_html(w_head_html), unsafe_allow_html=True)

    if not wishlist_products:
        st.info("Your wishlist is currently empty. Go back to the Catalog Feed and save items!")
        if st.button("← GO TO CATALOG FEED", use_container_width=True):
            st.session_state.current_screen = 1
            st.rerun()
    else:
        for row_start in range(0, len(wishlist_products), 5):
            row_prods = wishlist_products[row_start:row_start + 5]
            cols = st.columns(len(row_prods))
            for idx, prod in enumerate(row_prods):
                with cols[idx]:
                    is_selected = prod["id"] in st.session_state.selected_ids
                    card_class = "product-card-white selected" if is_selected else "product-card-white"
                    
                    img_b64 = get_image_base64(prod["image_path"])
                    
                    rating_overlay_html = f"""
                    <div class="img-rating-badge">
                    <span>{prod['rating']}</span>
                    <span class="star-icon-green">★</span>
                    <span>|</span>
                    <span>{prod['rating_count']}</span>
                    </div>
                    """
                    
                    img_container_html = f"""
                    <div style="position:relative; width:100%; height:200px; margin-bottom:8px;">
                    <img src="{img_b64}" style="width:100%; height:200px; border-radius:4px; object-fit:cover;" />
                    {rating_overlay_html}
                    </div>
                    """ if img_b64 else ''
                    
                    discount_pct = int(((prod["original_price"] - prod["price"]) / prod["original_price"]) * 100)
                    
                    w_card_html = f"""
                    <div class="{card_class}">
                    {img_container_html}
                    <div class="card-brand-name">{prod['brand']}</div>
                    <div class="card-title-text">{prod['name']}</div>
                    <div class="price-wrap">
                    <span class="price-current">₹{prod['price']:,}</span>
                    <span class="price-mrp">₹{prod['original_price']:,}</span>
                    <span class="price-off">({discount_pct}% OFF)</span>
                    </div>
                    </div>
                    """
                    st.markdown(clean_html(w_card_html), unsafe_allow_html=True)
                    
                    st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)
                    
                    if is_selected:
                        if st.button("✓ SELECTED", key=f"w_btn_{prod['id']}", type="primary", use_container_width=True):
                            st.session_state.selected_ids.remove(prod["id"])
                            st.rerun()
                    else:
                        if st.button("+ COMPARE", key=f"w_btn_{prod['id']}", use_container_width=True):
                            if len(st.session_state.selected_ids) >= 4:
                                st.warning("⚠️ Maximum 4 items can be selected for comparison.")
                            else:
                                st.session_state.selected_ids.append(prod["id"])
                                st.rerun()

            st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

        st.markdown("<br><hr style='border-color:#EAEAEC;'><br>", unsafe_allow_html=True)

        sel_count = len(st.session_state.selected_ids)
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            if 2 <= sel_count <= 4:
                if st.button(f"COMPARE SELECTED ({sel_count} ITEMS) →", type="primary", use_container_width=True):
                    st.session_state.current_screen = 3
                    st.rerun()
            else:
                st.button(f"SELECT AT LEAST 2 ITEMS TO COMPARE ({sel_count}/4)", disabled=True, use_container_width=True)

# =========================================================
# SCREEN 3: LAYER 6 — BODY PROFILE SETUP
# =========================================================
elif st.session_state.current_screen == 3:
    p_head_html = """
    <div style="background:#FFFFFF; border-radius:6px; padding:24px; max-width:600px; margin:0 auto; box-shadow:0 4px 14px rgba(0,0,0,0.05); border:1px solid #EAEAEC;">
    <h3 style="color:#282C3F; margin-bottom:4px; text-align:center; font-weight:800;">Layer 6: One-Time Body Profile Setup</h3>
    <p style="color:#535766; font-size:13px; text-align:center; margin-bottom:20px;">Save your profile once to unlock body-type filtered fit intelligence & keywords across your entire wishlist.</p>
    </div>
    """
    st.markdown(clean_html(p_head_html), unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 👤 Body Fit Profile")
        user_height = st.selectbox(
            "1. Select Your Height Range:",
            options=["5'0\" - 5'2\"", "5'3\" - 5'5\"", "5'6\" - 5'8\"", "5'9\"+"],
            index=1,
            key="input_height"
        )
        user_size = st.radio(
            "2. Select Your Usual Size:",
            options=["XS", "S", "M", "L", "XL"],
            index=1,
            horizontal=True,
            key="input_size"
        )

        st.markdown("<br>### 📅 Occasion Details", unsafe_allow_html=True)
        user_occ = st.selectbox(
            "3. What is your occasion?",
            options=["Wedding Guest", "Festival", "Office Party", "Date Night", "Casual"],
            index=0,
            key="input_occasion"
        )
        date_preset = st.selectbox(
            "4. When is your event?",
            options=["In 5 days (Recommended)", "In 3 days", "In 1 week", "In 2 weeks"],
            index=0,
            key="input_date_preset"
        )

        if date_preset == "In 3 days":
            selected_event_date = date.today() + timedelta(days=3)
        elif date_preset == "In 5 days (Recommended)":
            selected_event_date = date.today() + timedelta(days=5)
        elif date_preset == "In 1 week":
            selected_event_date = date.today() + timedelta(days=7)
        else:
            selected_event_date = date.today() + timedelta(days=14)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("SAVE PROFILE & OPEN DECISION PANEL →", type="primary", use_container_width=True):
            st.session_state.body_profile = {
                "height": user_height,
                "size": user_size,
                "occasion": user_occ,
                "event_date": selected_event_date
            }
            st.session_state.current_screen = 4
            st.rerun()

# =========================================================
# SCREEN 4: NATIVE MYNTRA DECISION PANEL (LAYERS 1-5)
# =========================================================
elif st.session_state.current_screen == 4:
    selected_products: List[Product] = [p for p in PRODUCTS if p["id"] in st.session_state.selected_ids]
    profile = st.session_state.body_profile
    user_height = profile["height"]
    user_size = profile["size"]
    user_occ = profile["occasion"]
    event_date = profile["event_date"]
    days_to_event = (event_date - date.today()).days

    scored_products = calculate_winner_scoring(selected_products, user_occ, user_size, days_to_event)
    winner_item: Product = scored_products[0]["product"]

    h_col1, h_col2 = st.columns([3, 1])
    with h_col1:
        st.markdown("<h3 style='margin:0; color:#282C3F; font-weight:800;'>WISHLIST DECISION PANEL</h3>", unsafe_allow_html=True)
        d_badge_html = f"""
        <div style="background:#FFF5F7; border:1px solid #FF3F6C; border-radius:20px; padding:4px 12px; font-size:12px; font-weight:700; color:#FF3F6C; display:inline-flex; align-items:center; gap:6px; margin-top:6px;">
        <span>👤 Body Filter: <b>{user_size} · {user_height}</b></span>
        <span>|</span>
        <span>Occasion: <b>{user_occ}</b></span>
        </div>
        """
        st.markdown(clean_html(d_badge_html), unsafe_allow_html=True)
    with h_col2:
        if st.button("⚙️ EDIT PROFILE", use_container_width=True):
            st.session_state.current_screen = 3
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    num_items = len(selected_products)
    comp_cols = st.columns(num_items)

    for idx, item_data in enumerate(scored_products):
        prod = item_data["product"]
        is_winner = (prod["id"] == winner_item["id"])
        
        with comp_cols[idx]:
            col_class = "decision-card-white winner" if is_winner else "decision-card-white"
            winner_html = '<div class="winner-flag-badge">★ HIGHEST CONFIDENCE MATCH</div>' if is_winner else ''

            img_b64 = get_image_base64(prod["image_path"])
            img_html = f'<img src="{img_b64}" style="width:100%; border-radius:4px; margin-bottom:8px; object-fit:cover; height:180px;" />' if img_b64 else ''
            discount_pct = int(((prod["original_price"] - prod["price"]) / prod["original_price"]) * 100)
            
            size_str = f"<span style='color:#03A685; font-weight:700;'>🟢 Available in {user_size}</span>" if item_data['has_size'] else f"<span style='color:#FF3F6C; font-weight:700;'>🔴 Out of Stock in {user_size}</span>"
            del_str = f"Delivers in {prod['delivery_days']} days ({'🟢 Arrives before event' if item_data['arrives_on_time'] else '🔴 Arrives after event'})"
            
            fit_summary = f"\"People your size ({user_size} · {user_height}) say: {prod['fit_summary_template']} · {prod['fit_review_count']} matching reviews.\""
            chips_html = "".join([f'<span class="keyword-pill">{kw}</span>' for kw in prod['keywords']])

            column_card_html = f"""
            <div class="{col_class}">
            {winner_html}
            <div style="margin-top: 8px;"></div>
            {img_html}
            <div class="card-brand-name">{prod['brand']}</div>
            <div class="card-title-text">{prod['name']}</div>
            <div class="attr-label">Price</div>
            <div class="price-wrap">
            <span class="price-current">₹{prod['price']:,}</span>
            <span class="price-mrp">₹{prod['original_price']:,}</span>
            <span class="price-off">({discount_pct}% OFF)</span>
            </div>
            <div class="attr-label">Average Rating</div>
            <div class="attr-value">★ {prod['rating']} ({prod['rating_count']:,} reviews)</div>
            <div class="attr-label">Size Availability ({user_size})</div>
            <div class="attr-value">{size_str}</div>
            <div class="attr-label">Estimated Delivery</div>
            <div class="attr-value">{del_str}</div>
            <div class="attr-label">Layer 2: Fit Summary ({user_size} · {user_height})</div>
            <div class="attr-value" style="font-style: italic; color:#2B6CB0; font-size:11px;">{fit_summary}</div>
            <div class="attr-label">Layer 3: Review Keywords</div>
            <div style="margin-bottom: 8px;">{chips_html}</div>
            </div>
            """

            st.markdown(clean_html(column_card_html), unsafe_allow_html=True)
            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

            if is_winner:
                if prod["id"] in [p["id"] for p in st.session_state.cart_items]:
                    st.button("✓ IN YOUR BAG", key=f"c_btn_{prod['id']}", type="primary", disabled=True, use_container_width=True)
                else:
                    if st.button("ADD TO BAG", key=f"c_btn_{prod['id']}", type="primary", use_container_width=True):
                        st.session_state.cart_items.append(prod)
                        st.toast("Added to Bag! ✓ Complete your purchase on Myntra.", icon="🛍️")
                        st.rerun()
            else:
                st.button("SAVE TO WISHLIST", key=f"s_btn_{prod['id']}", use_container_width=True)

    rec_bar_html = f"""
    <div class="rec-banner-white">
    <div class="rec-title-bold">
    Based on ratings and fit reviews from people your size (<span class="text-pink">{user_size} · {user_height}</span>), <span class="text-pink">{winner_item['brand']} {winner_item['name']}</span> has the highest confidence score.
    </div>
    <div class="rec-subtitle">
    4.5★ rating, 48 body-matched fit reviews, guaranteed size availability, and delivery before your event date.
    </div>
    </div>
    """
    st.markdown(clean_html(rec_bar_html), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("VIEW BAG & CHECKOUT →", type="primary", use_container_width=True):
        st.session_state.current_screen = 5
        st.rerun()

# =========================================================
# SCREEN 5: REAL MYNTRA BAG / CART PAGE
# =========================================================
elif st.session_state.current_screen == 5:
    st.markdown("<h3 style='color:#282C3F; font-weight:800;'>SHOPPING BAG</h3>", unsafe_allow_html=True)

    if not st.session_state.cart_items:
        st.info("Your bag is currently empty. Add items from the Decision Panel!")
        if st.button("← RETURN TO DECISION PANEL", use_container_width=True):
            st.session_state.current_screen = 4
            st.rerun()
    else:
        col1, col2 = st.columns([2, 1])
        with col1:
            for item in st.session_state.cart_items:
                img_b64 = get_image_base64(item["image_path"])
                img_html = f'<img src="{img_b64}" style="width:70px; height:90px; border-radius:4px; object-fit:cover;" />' if img_b64 else ''
                discount_pct = int(((item["original_price"] - item["price"]) / item["original_price"]) * 100)

                bag_item_html = f"""
                <div style="background:#FFFFFF; border-radius:4px; padding:14px; margin-bottom:12px; display:flex; gap:14px; border:1px solid #EAEAEC;">
                {img_html}
                <div>
                <div style="font-weight:800; font-size:14px; color:#282C3F;">{item['brand']}</div>
                <div style="font-size:12px; color:#535766; margin-bottom:6px;">{item['name']}</div>
                <div style="font-size:12px; color:#535766;">Size: <b>{st.session_state.body_profile['size']}</b> | Qty: <b>1</b></div>
                <div style="margin-top:6px;">
                <span style="font-weight:700; font-size:14px; color:#282C3F;">₹{item['price']:,}</span>
                <span style="font-size:11px; text-decoration:line-through; color:#7E818C; margin-left:6px;">₹{item['original_price']:,}</span>
                <span style="font-size:11px; font-weight:700; color:#FF905A; margin-left:6px;">({discount_pct}% OFF)</span>
                </div>
                </div>
                </div>
                """
                st.markdown(clean_html(bag_item_html), unsafe_allow_html=True)

        with col2:
            subtotal = sum(i["price"] for i in st.session_state.cart_items)
            mrp_total = sum(i["original_price"] for i in st.session_state.cart_items)
            discount_total = mrp_total - subtotal

            price_summary_html = f"""
            <div style="background:#FFFFFF; border-radius:4px; padding:16px; border:1px solid #EAEAEC;">
            <div style="font-weight:800; font-size:12px; color:#7E818C; text-transform:uppercase; margin-bottom:12px;">PRICE DETAILS ({len(st.session_state.cart_items)} Items)</div>
            <div style="display:flex; justify-content:space-between; font-size:13px; margin-bottom:8px; color:#282C3F;">
            <span>Total MRP</span>
            <span>₹{mrp_total:,}</span>
            </div>
            <div style="display:flex; justify-content:space-between; font-size:13px; margin-bottom:8px; color:#03A685;">
            <span>Discount on MRP</span>
            <span>-₹{discount_total:,}</span>
            </div>
            <div style="display:flex; justify-content:space-between; font-size:13px; margin-bottom:8px; color:#282C3F;">
            <span>Convenience Fee</span>
            <span style="color:#03A685; font-weight:700;">FREE</span>
            </div>
            <hr style="border-color:#EAEAEC; margin:12px 0;">
            <div style="display:flex; justify-content:space-between; font-size:15px; font-weight:800; color:#282C3F; margin-bottom:16px;">
            <span>Total Amount</span>
            <span>₹{subtotal:,}</span>
            </div>
            </div>
            """
            st.markdown(clean_html(price_summary_html), unsafe_allow_html=True)

            st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
            if st.button("PLACE ORDER", type="primary", use_container_width=True):
                st.balloons()
                st.success("Order Placed Successfully! 🎉 Thank you for shopping on Myntra.")

# ---------------------------------------------------------
# STICKY BOTTOM NAV BAR (Real Myntra Look)
# ---------------------------------------------------------
bottom_nav_html = """
<div class="myntra-bottom-bar">
<div class="bottom-item">🏠<br>Home</div>
<div class="bottom-item">📂<br>Categories</div>
<div class="bottom-item">🎬<br>Studio</div>
<div class="bottom-item active">❤️<br>Wishlist</div>
<div class="bottom-item">👤<br>Profile</div>
</div>
"""
st.markdown(clean_html(bottom_nav_html), unsafe_allow_html=True)
