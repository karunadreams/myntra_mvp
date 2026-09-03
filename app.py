import streamlit as st
import os
import base64
import json
from typing import TypedDict, List, Dict

# ---------------------------------------------------------
# DATASET & PRODUCT MODELS
# ---------------------------------------------------------
class Product(TypedDict):
    id: int
    brand: str
    name: str
    price: int
    original_price: int
    rating: float
    rating_count: int
    sizes_stock: Dict[str, bool]
    delivery_days: int
    fit_note: str
    keywords: List[str]
    image_path: str
    occasion: str

def load_products() -> List[Product]:
    raw_products = [
        {
            "id": 1,
            "brand": "Libas",
            "name": "Embroidered Anarkali Kurta",
            "price": 1299,
            "original_price": 2999,
            "rating": 4.1,
            "rating_count": 1280,
            "sizes_stock": {"S": True, "M": True, "L": False, "XL": True},
            "delivery_days": 2,
            "fit_note": "Runs small — order one size up · 23 matching reviews",
            "keywords": ["Runs small", "Color matches photos", "Good for petite frame"],
            "image_path": "assets/libas.jpg",
            "occasion": "🪔 Diwali 2024"
        },
        {
            "id": 2,
            "brand": "W for Woman",
            "name": "Floral Printed Kurta Set",
            "price": 2499,
            "original_price": 4999,
            "rating": 4.4,
            "rating_count": 890,
            "sizes_stock": {"S": True, "M": True, "L": True, "XL": False},
            "delivery_days": 3,
            "fit_note": "Fits true to size, soft waist fit · 42 matching reviews",
            "keywords": ["Fits true to size", "Soft cotton fabric", "Flattering silhouette"],
            "image_path": "assets/w.jpg",
            "occasion": "🪔 Diwali 2024"
        },
        {
            "id": 3,
            "brand": "Biba",
            "name": "Sequin Sharara Suit",
            "price": 3199,
            "original_price": 5999,
            "rating": 4.3,
            "rating_count": 2150,
            "sizes_stock": {"S": False, "M": True, "L": True, "XL": True},
            "delivery_days": 4,
            "fit_note": "Slightly long hemline for petite height · 18 matching reviews",
            "keywords": ["Rich festive look", "Heavy embroidery", "Pair with heels"],
            "image_path": "assets/biba.jpg",
            "occasion": "🪔 Diwali 2024"
        },
        {
            "id": 4,
            "brand": "Global Desi",
            "name": "Floral Wrap Dress",
            "price": 899,
            "original_price": 1999,
            "rating": 3.9,
            "rating_count": 640,
            "sizes_stock": {"S": True, "M": False, "L": True, "XL": True},
            "delivery_days": 2,
            "fit_note": "Flowy fit, comfortable wrap waist · 15 matching reviews",
            "keywords": ["Lightweight", "Vibrant print", "Easy breezy wear"],
            "image_path": "assets/global_desi.jpg",
            "occasion": "✨ College Fest"
        },
        {
            "id": 5,
            "brand": "Anouk",
            "name": "Printed Co-ord Set",
            "price": 1749,
            "original_price": 3499,
            "rating": 4.2,
            "rating_count": 420,
            "sizes_stock": {"S": True, "M": True, "L": True, "XL": True},
            "delivery_days": 3,
            "fit_note": "Modern relaxed fit, true to size · 31 matching reviews",
            "keywords": ["Trendy co-ord", "Breathable fabric", "Perfect for events"],
            "image_path": "assets/aurelia.jpg",
            "occasion": "✨ College Fest"
        },
        {
            "id": 6,
            "brand": "Sangria",
            "name": "Ethnic Printed Maxi Dress",
            "price": 1399,
            "original_price": 2799,
            "rating": 4.0,
            "rating_count": 510,
            "sizes_stock": {"S": True, "M": True, "L": False, "XL": True},
            "delivery_days": 3,
            "fit_note": "Flattering A-line flared cut · 19 matching reviews",
            "keywords": ["Vibrant pattern", "Elegant flare", "Soft material"],
            "image_path": "assets/libas.jpg",
            "occasion": "🪔 Diwali 2024"
        },
        {
            "id": 7,
            "brand": "Aurelia",
            "name": "Solid Straight Kurta",
            "price": 999,
            "original_price": 1999,
            "rating": 4.3,
            "rating_count": 780,
            "sizes_stock": {"S": True, "M": True, "L": True, "XL": False},
            "delivery_days": 2,
            "fit_note": "Classic straight fit, true to size · 27 matching reviews",
            "keywords": ["Office ready", "Sturdy stitch", "Clean hemline"],
            "image_path": "assets/aurelia.jpg",
            "occasion": "🪔 Diwali 2024"
        },
        {
            "id": 8,
            "brand": "Rangmanch by Pantaloons",
            "name": "Woven Anarkali",
            "price": 2199,
            "original_price": 4399,
            "rating": 4.1,
            "rating_count": 390,
            "sizes_stock": {"S": False, "M": True, "L": True, "XL": True},
            "delivery_days": 4,
            "fit_note": "Grand flare, runs slightly long · 14 matching reviews",
            "keywords": ["Festive woven", "Heavy flare", "Royal look"],
            "image_path": "assets/w.jpg",
            "occasion": "🪔 Diwali 2024"
        },
        {
            "id": 9,
            "brand": "Fabindia",
            "name": "Block Print Kurta",
            "price": 1599,
            "original_price": 2999,
            "rating": 4.5,
            "rating_count": 1420,
            "sizes_stock": {"S": True, "M": True, "L": True, "XL": True},
            "delivery_days": 2,
            "fit_note": "Pure handblock cotton, very breathable · 54 matching reviews",
            "keywords": ["Pure cotton", "Traditional block print", "Comfortable fit"],
            "image_path": "assets/biba.jpg",
            "occasion": "🪔 Diwali 2024"
        },
        {
            "id": 10,
            "brand": "Indya",
            "name": "Mirror Work Lehenga Set",
            "price": 3499,
            "original_price": 6999,
            "rating": 4.6,
            "rating_count": 910,
            "sizes_stock": {"S": True, "M": True, "L": False, "XL": True},
            "delivery_days": 3,
            "fit_note": "Stunning festive flair, slim waist cut · 38 matching reviews",
            "keywords": ["Mirror work", "Party wear", "High quality finish"],
            "image_path": "assets/global_desi.jpg",
            "occasion": "🪔 Diwali 2024"
        },
        {
            "id": 11,
            "brand": "AND",
            "name": "Solid Shift Dress",
            "price": 1299,
            "original_price": 2599,
            "rating": 3.8,
            "rating_count": 320,
            "sizes_stock": {"S": True, "M": False, "L": True, "XL": True},
            "delivery_days": 2,
            "fit_note": "Minimalist modern cut, slightly boxy · 11 matching reviews",
            "keywords": ["Sleek design", "College casual", "Easy styling"],
            "image_path": "assets/libas.jpg",
            "occasion": "✨ College Fest"
        },
        {
            "id": 12,
            "brand": "Tokyo Talkies",
            "name": "Floral Mini Dress",
            "price": 799,
            "original_price": 1599,
            "rating": 3.9,
            "rating_count": 680,
            "sizes_stock": {"S": True, "M": True, "L": True, "XL": False},
            "delivery_days": 3,
            "fit_note": "Cute mini cut, fits slim · 22 matching reviews",
            "keywords": ["Chic floral", "Short sleeve", "Youthful style"],
            "image_path": "assets/w.jpg",
            "occasion": "✨ College Fest"
        },
        {
            "id": 13,
            "brand": "Sassafras",
            "name": "Printed Wrap Dress",
            "price": 1099,
            "original_price": 2199,
            "rating": 4.0,
            "rating_count": 470,
            "sizes_stock": {"S": True, "M": True, "L": True, "XL": True},
            "delivery_days": 2,
            "fit_note": "Adjustable wrap tie waist · 17 matching reviews",
            "keywords": ["Wrap waist", "V-neckline", "Light chiffon"],
            "image_path": "assets/biba.jpg",
            "occasion": "✨ College Fest"
        },
        {
            "id": 14,
            "brand": "Nayo",
            "name": "Cotton A-Line Kurta",
            "price": 599,
            "original_price": 1299,
            "rating": 4.2,
            "rating_count": 890,
            "sizes_stock": {"S": True, "M": True, "L": True, "XL": True},
            "delivery_days": 2,
            "fit_note": "Super comfortable daily cotton · 29 matching reviews",
            "keywords": ["Budget friendly", "Soft cotton", "Everyday staple"],
            "image_path": "assets/global_desi.jpg",
            "occasion": "🪔 Diwali 2024"
        },
        {
            "id": 15,
            "brand": "Janasya",
            "name": "Paisley Print Kurta Set",
            "price": 1199,
            "original_price": 2399,
            "rating": 4.1,
            "rating_count": 530,
            "sizes_stock": {"S": False, "M": True, "L": True, "XL": True},
            "delivery_days": 3,
            "fit_note": "Rich paisley colors, true fit · 20 matching reviews",
            "keywords": ["Paisley motif", "Dupatta included", "Vibrant colors"],
            "image_path": "assets/aurelia.jpg",
            "occasion": "🪔 Diwali 2024"
        },
        {
            "id": 16,
            "brand": "Vishudh",
            "name": "Embroidered Straight Kurta",
            "price": 1499,
            "original_price": 2999,
            "rating": 4.3,
            "rating_count": 740,
            "sizes_stock": {"S": True, "M": True, "L": True, "XL": False},
            "delivery_days": 2,
            "fit_note": "Neat neckline embroidery · 33 matching reviews",
            "keywords": ["Elegant neck work", "Side slit", "Graceful silhouette"],
            "image_path": "assets/libas.jpg",
            "occasion": "🪔 Diwali 2024"
        },
        {
            "id": 17,
            "brand": "Zoella",
            "name": "Ruffle Hem Co-ord Set",
            "price": 1349,
            "original_price": 2699,
            "rating": 3.7,
            "rating_count": 210,
            "sizes_stock": {"S": True, "M": False, "L": True, "XL": True},
            "delivery_days": 3,
            "fit_note": "Trendy ruffle bottom cut · 8 matching reviews",
            "keywords": ["Ruffle hem", "Playful design", "Party ready"],
            "image_path": "assets/w.jpg",
            "occasion": "✨ College Fest"
        },
        {
            "id": 18,
            "brand": "Pannkh",
            "name": "Ethnic Flared Kurta",
            "price": 899,
            "original_price": 1799,
            "rating": 4.0,
            "rating_count": 360,
            "sizes_stock": {"S": True, "M": True, "L": True, "XL": True},
            "delivery_days": 2,
            "fit_note": "Flowy festive flared hem · 16 matching reviews",
            "keywords": ["Flared hem", "Subtle print", "Lightweight rayon"],
            "image_path": "assets/biba.jpg",
            "occasion": "🪔 Diwali 2024"
        },
        {
            "id": 19,
            "brand": "Ritu Kumar",
            "name": "Zari Border Saree",
            "price": 4999,
            "original_price": 9999,
            "rating": 4.8,
            "rating_count": 1850,
            "sizes_stock": {"S": True, "M": True, "L": True, "XL": True},
            "delivery_days": 4,
            "fit_note": "Designer luxury zari weave · 65 matching reviews",
            "keywords": ["Designer saree", "Zari border", "Premium silk blend"],
            "image_path": "assets/aurelia.jpg",
            "occasion": "🪔 Diwali 2024"
        },
        {
            "id": 20,
            "brand": "Clovia",
            "name": "Printed Loungewear Set",
            "price": 699,
            "original_price": 1399,
            "rating": 3.8,
            "rating_count": 420,
            "sizes_stock": {"S": True, "M": True, "L": False, "XL": True},
            "delivery_days": 2,
            "fit_note": "Ultra soft relaxed lounge fit · 25 matching reviews",
            "keywords": ["Super soft", "Relaxed fit", "Comfortable sleepwear"],
            "image_path": "assets/global_desi.jpg",
            "occasion": "✨ College Fest"
        }
    ]
    return raw_products

PRODUCTS: List[Product] = load_products()

def get_image_base64(image_path: str) -> str:
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            return f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode('utf-8')}"
    return ""

def clean_html(html_str: str) -> str:
    lines = [line.strip() for line in html_str.strip().split("\n") if line.strip()]
    return "\n".join(lines)

# ---------------------------------------------------------
# PAGE CONFIG & MOBILE-FIRST CSS (430px MAX WIDTH)
# ---------------------------------------------------------
st.set_page_config(
    page_title="Myntra Wishlist — Decision Mode",
    page_icon="🛍️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    /* Canvas */
    .stApp {
        background-color: #F5F5F6 !important;
        color: #282C3F !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    /* Mobile Container 430px */
    .block-container {
        max-width: 430px !important;
        padding-top: 6px !important;
        padding-bottom: 85px !important;
        padding-left: 12px !important;
        padding-right: 12px !important;
        margin: 0 auto !important;
        background-color: #FFFFFF !important;
        min-height: 100vh;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border-radius: 12px;
    }

    header, footer { visibility: hidden !important; }

    /* Top Logo Bar */
    .top-logo-img {
        height: 32px;
        object-fit: contain;
    }

    /* Pink Banner Chip */
    .pink-banner-chip {
        background: #FFF0F4;
        border: 1px solid #FF3F6C;
        color: #FF3F6C;
        font-weight: 700;
        font-size: 12px;
        padding: 8px 12px;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 6px;
    }

    .section-title {
        font-size: 16px;
        font-weight: 800;
        color: #282C3F;
        margin-bottom: 12px;
    }

    /* Product Grid Card (Home Screen) */
    .grid-card {
        background: #FFFFFF;
        border: 1px solid #EAEAEC;
        border-radius: 12px;
        overflow: hidden;
        margin-bottom: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        position: relative;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 100%;
    }

    .grid-img-wrap {
        position: relative;
        width: 100%;
        height: 160px;
    }

    .grid-img {
        width: 100%;
        height: 160px;
        object-fit: cover;
    }

    .grid-card-body {
        padding: 8px;
    }

    .card-brand {
        font-size: 12px;
        font-weight: 800;
        color: #282C3F;
        text-transform: uppercase;
        margin-bottom: 2px;
    }

    .card-title {
        font-size: 11px;
        color: #696B79;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        margin-bottom: 4px;
    }

    .card-price-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 4px;
    }

    .card-price {
        font-size: 13px;
        font-weight: 800;
        color: #282C3F;
    }

    .card-rating {
        font-size: 11px;
        font-weight: 700;
        color: #03A685;
    }

    .occasion-pill {
        display: inline-block;
        background: #F5F5F6;
        color: #535766;
        font-size: 9px;
        font-weight: 700;
        padding: 2px 6px;
        border-radius: 10px;
        margin-top: 2px;
    }

    /* Wishlist Card */
    .wishlist-row-card {
        background: #FFFFFF;
        border: 1px solid #EAEAEC;
        border-radius: 12px;
        padding: 10px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 10px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
    }

    .wishlist-thumb {
        width: 90px;
        height: 110px;
        border-radius: 8px;
        object-fit: cover;
        flex-shrink: 0;
    }

    .wishlist-details {
        flex-grow: 1;
        overflow: hidden;
    }

    /* General Buttons */
    .stButton > button {
        border-radius: 6px !important;
        font-weight: 800 !important;
        letter-spacing: 0.3px !important;
        text-transform: uppercase !important;
        font-size: 12px !important;
        height: 38px !important;
    }

    button[kind="primary"] {
        background-color: #FF3F6C !important;
        color: #FFFFFF !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(255, 63, 108, 0.25) !important;
    }

    button[kind="primary"]:hover {
        background-color: #E6355F !important;
    }

    /* Interactive Bottom Navigation Buttons */
    button[key*="bnav_"] {
        font-size: 10px !important;
        font-weight: 800 !important;
        padding: 4px 0 !important;
        height: 48px !important;
        min-height: 48px !important;
        line-height: 1.2 !important;
        white-space: pre-line !important;
        border-radius: 8px !important;
    }

    /* Comparison Matrix */
    .comp-col-card {
        background: #FFFFFF;
        border: 1px solid #EAEAEC;
        border-radius: 10px;
        padding: 8px;
        margin-bottom: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        font-size: 11px;
    }

    .stock-pill {
        display: inline-block;
        padding: 1px 5px;
        border-radius: 4px;
        font-size: 10px;
        font-weight: 700;
        margin: 1px;
    }

    .stock-green { background: #E6F4EA; color: #137333; }
    .stock-red { background: #FCE8E6; color: #C5221F; }

    .fit-box {
        background: #F0F4F9;
        border-radius: 6px;
        padding: 8px;
        margin-top: 8px;
        margin-bottom: 8px;
        font-size: 10.5px;
        color: #1A73E8;
        font-style: italic;
    }

    .kw-pill {
        display: inline-block;
        background: #F5F5F6;
        color: #535766;
        font-size: 9.5px;
        padding: 2px 6px;
        border-radius: 8px;
        margin: 1px;
    }

    .rec-banner {
        background: #FFF0F4;
        border: 1px solid #FF3F6C;
        color: #282C3F;
        border-radius: 8px;
        padding: 10px 12px;
        margin-top: 14px;
        margin-bottom: 14px;
        font-size: 12px;
        font-weight: 700;
        text-align: center;
    }

    /* Always Fixed Sticky Bottom Navigation Bar (Never disappears on scroll) */
    div[data-testid="stHorizontalBlock"]:has(button[key*="bnav_"]) {
        position: fixed !important;
        bottom: 0 !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: 100% !important;
        max-width: 430px !important;
        background: #FFFFFF !important;
        border-top: 1px solid #EAEAEC !important;
        padding: 6px 8px 10px 8px !important;
        z-index: 999999 !important;
        box-shadow: 0 -4px 16px rgba(0, 0, 0, 0.08) !important;
        margin: 0 !important;
    }

    div[data-testid="column"]:has(button[key*="bnav_"]) {
        padding: 0 2px !important;
    }

    button[key*="bnav_"] {
        font-size: 10px !important;
        font-weight: 800 !important;
        padding: 2px 0 !important;
        height: 44px !important;
        min-height: 44px !important;
        line-height: 1.2 !important;
        white-space: nowrap !important;
        border-radius: 8px !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# SESSION STATE INITIALIZATION
# ---------------------------------------------------------
if "current_screen" not in st.session_state:
    st.session_state.current_screen = "home"  # "home", "wishlist", "comparison", "categories", "profile", "cart"

if "wishlist_ids" not in st.session_state:
    st.session_state.wishlist_ids = [1, 2, 3, 4, 5]

if "selected_for_compare" not in st.session_state:
    st.session_state.selected_for_compare = [1, 2, 3, 4, 5]

if "cart_ids" not in st.session_state:
    st.session_state.cart_ids = []

if "body_profile" not in st.session_state:
    st.session_state.body_profile = {
        "height": "5'3\"–5'5\"",
        "size": "S",
        "is_saved": False
    }

if "show_profile_modal" not in st.session_state:
    st.session_state.show_profile_modal = False

if "mod_height_sel" not in st.session_state:
    st.session_state.mod_height_sel = "5'3\"–5'5\""
if "mod_size_sel" not in st.session_state:
    st.session_state.mod_size_sel = "S"

for prod in PRODUCTS:
    key_name = f"chk_sel_{prod['id']}"
    if key_name not in st.session_state:
        st.session_state[key_name] = prod["id"] in st.session_state.selected_for_compare

logo_b64 = get_image_base64("assets/myntra_logo.jpg")

# Helper to toggle item selection for comparison
def toggle_compare_item(prod_id: int):
    if prod_id in st.session_state.selected_for_compare:
        st.session_state.selected_for_compare.remove(prod_id)
    else:
        st.session_state.selected_for_compare.append(prod_id)

# Helper to toggle wishlist status on heart click
def toggle_wishlist(prod_id: int):
    if prod_id in st.session_state.wishlist_ids:
        st.session_state.wishlist_ids.remove(prod_id)
        if prod_id in st.session_state.selected_for_compare:
            st.session_state.selected_for_compare.remove(prod_id)
    else:
        st.session_state.wishlist_ids.append(prod_id)
        if prod_id not in st.session_state.selected_for_compare:
            st.session_state.selected_for_compare.append(prod_id)

# ---------------------------------------------------------
# INTERACTIVE TOP NAVBAR HEADER
# ---------------------------------------------------------
wishlist_cnt = len(st.session_state.wishlist_ids)
cart_cnt = len(st.session_state.cart_ids)

with st.container():
    h_col1, h_col2 = st.columns([1, 1])
    with h_col1:
        if st.button("🛍️ MYNTRA", key="top_logo_btn", type="primary" if st.session_state.current_screen == "home" else "secondary"):
            st.session_state.show_profile_modal = False
            st.session_state.current_screen = "home"
            st.rerun()
            
    with h_col2:
        btn_c1, btn_c2, btn_c3 = st.columns(3)
        with btn_c1:
            st.markdown("<div style='text-align:center; font-size:16px;'>🔍</div>", unsafe_allow_html=True)
        with btn_c2:
            if st.button(f"❤️ {wishlist_cnt}", key="top_wish_btn", type="primary" if st.session_state.current_screen == "wishlist" else "secondary"):
                st.session_state.show_profile_modal = False
                st.session_state.current_screen = "wishlist"
                st.rerun()
        with btn_c3:
            if st.button(f"🛍️ {cart_cnt}", key="top_bag_btn", type="primary" if st.session_state.current_screen == "cart" else "secondary"):
                st.session_state.show_profile_modal = False
                st.session_state.current_screen = "cart"
                st.rerun()

st.markdown("<hr style='border-color:#EAEAEC; margin-top:4px; margin-bottom:10px;'>", unsafe_allow_html=True)

# =========================================================
# PAGE 1: HOME SCREEN (Catalog Grid of 20 Products)
# =========================================================
if st.session_state.current_screen == "home":
    
    st.markdown(clean_html("""
    <div class="pink-banner-chip">
        <span>🪔 Diwali picks · Shop before stock runs out</span>
    </div>
    """), unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Trending Kurtas & Sets</div>", unsafe_allow_html=True)

    for i in range(0, len(PRODUCTS), 2):
        row_prods = PRODUCTS[i:i+2]
        cols = st.columns(len(row_prods))
        
        for idx, prod in enumerate(row_prods):
            with cols[idx]:
                is_wishlisted = prod["id"] in st.session_state.wishlist_ids
                img_b64 = get_image_base64(prod["image_path"])
                img_tag = f'<img src="{img_b64}" class="grid-img" />' if img_b64 else ''
                
                card_html = f"""
                <div class="grid-card">
                    <div class="grid-img-wrap">
                        {img_tag}
                    </div>
                    <div class="grid-card-body">
                        <div class="card-brand">{prod['brand']}</div>
                        <div class="card-title">{prod['name']}</div>
                        <div class="card-price-row">
                            <span class="card-price">₹{prod['price']:,}</span>
                            <span class="card-rating">⭐ {prod['rating']}</span>
                        </div>
                        <span class="occasion-pill">{prod['occasion']}</span>
                    </div>
                </div>
                """
                st.markdown(clean_html(card_html), unsafe_allow_html=True)
                
                heart_label = "❤️ WISHLISTED" if is_wishlisted else "♡ WISHLIST"
                if st.button(heart_label, key=f"home_heart_{prod['id']}", type="primary" if is_wishlisted else "secondary", use_container_width=True):
                    toggle_wishlist(prod["id"])
                    st.rerun()

        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

# =========================================================
# PAGE 2: WISHLIST SCREEN
# =========================================================
elif st.session_state.current_screen == "wishlist":
    
    st.markdown(f"<div class='section-title' style='margin-bottom:2px;'>My Wishlist</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size:12px; color:#696B79; margin-bottom:12px;'>{len(st.session_state.wishlist_ids)} items saved</div>", unsafe_allow_html=True)

    st.markdown(clean_html(f"""
    <div class="pink-banner-chip">
        <span>You have {len(st.session_state.wishlist_ids)} items saved for Diwali 2024 · 12 days left</span>
    </div>
    """), unsafe_allow_html=True)

    if st.button("🚀 DECISION MODE (COMPARE ALL)", type="primary", use_container_width=True):
        st.session_state.selected_for_compare = st.session_state.wishlist_ids.copy()
        if not st.session_state.body_profile["is_saved"]:
            st.session_state.show_profile_modal = True
        else:
            st.session_state.current_screen = "comparison"
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    wishlist_prods = [p for p in PRODUCTS if p["id"] in st.session_state.wishlist_ids]

    if not wishlist_prods:
        st.info("Your wishlist is empty. Click Home at the bottom or ♡ on products to add items!")
        if st.button("🏠 RETURN TO HOME SCREEN", type="primary", use_container_width=True):
            st.session_state.current_screen = "home"
            st.rerun()
    else:
        for prod in wishlist_prods:
            is_selected = prod["id"] in st.session_state.selected_for_compare
            
            c_chk, c_card = st.columns([1, 6])
            
            with c_chk:
                st.markdown("<div style='height:36px;'></div>", unsafe_allow_html=True)
                st.checkbox(
                    f"Select {prod['brand']} {prod['name']}",
                    value=is_selected,
                    key=f"chk_sel_{prod['id']}",
                    on_change=toggle_compare_item,
                    args=(prod["id"],),
                    label_visibility="collapsed"
                )

            with c_card:
                img_b64 = get_image_base64(prod["image_path"])
                img_html = f'<img src="{img_b64}" class="wishlist-thumb" />' if img_b64 else ''
                
                row_html = f"""
                <div class="wishlist-row-card">
                    {img_html}
                    <div class="wishlist-details">
                        <div class="card-brand">{prod['brand']}</div>
                        <div class="card-title">{prod['name']}</div>
                        <span class="occasion-pill">{prod['occasion']}</span>
                        <div class="card-price-row" style="margin-top:4px;">
                            <span class="card-price">₹{prod['price']:,}</span>
                            <span class="card-rating">⭐ {prod['rating']}</span>
                        </div>
                    </div>
                </div>
                """
                st.markdown(clean_html(row_html), unsafe_allow_html=True)
                
                c_del1, c_del2 = st.columns([3, 1])
                with c_del2:
                    if st.button("❤️ REMOVE", key=f"w_rem_{prod['id']}", use_container_width=True):
                        toggle_wishlist(prod["id"])
                        st.rerun()

            st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)

    sel_count = len(st.session_state.selected_for_compare)
    if sel_count >= 2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button(f"COMPARE SELECTED ({sel_count}) →", type="primary", use_container_width=True):
            if not st.session_state.body_profile["is_saved"]:
                st.session_state.show_profile_modal = True
            else:
                st.session_state.current_screen = "comparison"
            st.rerun()

# =========================================================
# PAGE 3: BODY PROFILE SETUP MODAL
# =========================================================
if st.session_state.show_profile_modal:
    st.markdown("""
    <div style="background: #FFF5F7; border: 2px solid #FF3F6C; border-radius: 12px; padding: 16px; margin-bottom: 20px;">
        <h4 style="margin: 0 0 4px 0; color: #282C3F; font-weight: 800;">⚡ Quick Fit Setup</h4>
        <p style="margin: 0; font-size: 12px; color: #696B79;">Takes 30 seconds. Never asked again.</p>
    </div>
    """, unsafe_allow_html=True)

    prof_h = st.selectbox(
        "1. Select Height Range:",
        options=["5'0\"–5'2\"", "5'3\"–5'5\"", "5'6\"+"],
        index=1,
        key="mod_height_sel"
    )

    prof_s = st.selectbox(
        "2. Select Usual Size:",
        options=["XS", "S", "M", "L", "XL"],
        index=1,
        key="mod_size_sel"
    )

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("SAVE & COMPARE →", type="primary", use_container_width=True):
        st.session_state.body_profile = {
            "height": prof_h,
            "size": prof_s,
            "is_saved": True
        }
        st.session_state.show_profile_modal = False
        st.session_state.current_screen = "comparison"
        st.rerun()

# =========================================================
# PAGE 4: COMPARISON SCREEN
# =========================================================
elif st.session_state.current_screen == "comparison" and not st.session_state.show_profile_modal:
    
    col_back, col_chip = st.columns([1, 3])
    with col_back:
        if st.button("← BACK", use_container_width=True):
            st.session_state.current_screen = "wishlist"
            st.rerun()
    with col_chip:
        prof = st.session_state.body_profile
        if st.button(f"👤 Fit: {prof['size']} · {prof['height']} · EDIT", key="edit_prof_btn", use_container_width=True):
            st.session_state.show_profile_modal = True
            st.rerun()

    st.markdown("<div class='section-title' style='margin-top:8px;'>Comparison Matrix</div>", unsafe_allow_html=True)

    comp_prods = [p for p in PRODUCTS if p["id"] in st.session_state.selected_for_compare]

    if not comp_prods:
        st.warning("No items selected for comparison. Please select 2 or more items from Wishlist!")
        if st.button("← GO TO WISHLIST"):
            st.session_state.current_screen = "wishlist"
            st.rerun()
    else:
        winner_item = max(comp_prods, key=lambda x: x["rating"])
        num_items = len(comp_prods)
        comp_cols = st.columns(num_items)

        for idx, prod in enumerate(comp_prods):
            user_size = st.session_state.body_profile["size"]
            user_height = st.session_state.body_profile["height"]

            with comp_cols[idx]:
                img_b64 = get_image_base64(prod["image_path"])
                img_html = f'<img src="{img_b64}" style="width:100%; height:120px; border-radius:6px; object-fit:cover; margin-bottom:6px;" />' if img_b64 else ''
                
                stock_htmls = []
                for s, avail in prod["sizes_stock"].items():
                    cls = "stock-green" if avail else "stock-red"
                    symbol = "🟢" if avail else "🔴"
                    stock_htmls.append(f'<span class="stock-pill {cls}">{s}{symbol}</span>')
                stock_row = "".join(stock_htmls)

                kw_htmls = "".join([f'<span class="kw-pill">{kw}</span>' for kw in prod["keywords"]])

                col_card_html = f"""
                <div class="comp-col-card">
                    {img_html}
                    <div style="font-weight:800; text-transform:uppercase; color:#282C3F;">{prod['brand']}</div>
                    <div style="color:#696B79; font-size:10px; margin-bottom:4px;">{prod['name']}</div>
                    <div style="font-weight:800; color:#282C3F;">₹{prod['price']:,}</div>
                    <div style="color:#03A685; font-weight:700; margin-bottom:4px;">⭐ {prod['rating']}</div>
                    <div style="margin-bottom:4px;">{stock_row}</div>
                    <div style="font-size:10px; color:#535766; margin-bottom:6px;">🚚 Arrives in {prod['delivery_days']} days</div>
                    <div class="fit-box">"People your size ({user_size} · {user_height}) say: {prod['fit_note']}"</div>
                    <div style="margin-bottom:8px;">{kw_htmls}</div>
                </div>
                """
                st.markdown(clean_html(col_card_html), unsafe_allow_html=True)
                
                if prod["id"] in st.session_state.cart_ids:
                    st.button("✓ IN BAG", key=f"cart_btn_{prod['id']}", disabled=True, use_container_width=True)
                else:
                    if st.button("ADD TO CART", key=f"cart_btn_{prod['id']}", type="primary", use_container_width=True):
                        st.session_state.cart_ids.append(prod["id"])
                        st.toast(f"Added {prod['brand']} {prod['name']} to Bag! 🛍️")
                        st.rerun()

        st.markdown(clean_html(f"""
        <div class="rec-banner">
            ✨ Based on ratings and fit reviews from people your size ({user_size} · {user_height}), <b>{winner_item['brand']} {winner_item['name']}</b> (⭐{winner_item['rating']}) has the highest confidence score.
        </div>
        """), unsafe_allow_html=True)

# =========================================================
# CATEGORIES SCREEN (Interactive Category Explorer)
# =========================================================
elif st.session_state.current_screen == "categories":
    st.markdown("<div class='section-title'>Explore Categories</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:12px; color:#696B79; margin-bottom:14px;'>Find ethnic wear & festive outfits</div>", unsafe_allow_html=True)

    cat_list = [
        {"name": "Kurtas & Kurta Sets", "desc": "Diwali & Festive Collection · 20 Products", "icon": "🪔"},
        {"name": "Anarkali & Sharara Suits", "desc": "Royal Silk & Sequin Embroidered", "icon": "✨"},
        {"name": "College Fest Dresses", "desc": "Floral Wrap & Co-ord Sets", "icon": "👗"},
        {"name": "Silk Sarees & Lehengas", "desc": "Zari Border & Mirror Work", "icon": "🥻"},
        {"name": "Loungewear & Casuals", "desc": "Soft Cotton Everyday Wear", "icon": "👚"}
    ]

    for cat in cat_list:
        st.markdown(clean_html(f"""
        <div style="background:#FFFFFF; border:1px solid #EAEAEC; border-radius:10px; padding:12px; margin-bottom:10px; display:flex; align-items:center; gap:12px; box-shadow:0 2px 6px rgba(0,0,0,0.04);">
            <div style="font-size:24px;">{cat['icon']}</div>
            <div>
                <div style="font-weight:800; font-size:14px; color:#282C3F;">{cat['name']}</div>
                <div style="font-size:11px; color:#696B79;">{cat['desc']}</div>
            </div>
        </div>
        """), unsafe_allow_html=True)
        if st.button(f"BROWSE {cat['name'].upper()}", key=f"cat_btn_{cat['name']}", type="primary", use_container_width=True):
            st.session_state.current_screen = "home"
            st.rerun()
        st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)

# =========================================================
# PROFILE SCREEN (Interactive Body Fit Profile Settings)
# =========================================================
elif st.session_state.current_screen == "profile":
    st.markdown("<div class='section-title'>User Fit Profile & Settings</div>", unsafe_allow_html=True)
    
    prof = st.session_state.body_profile
    st.markdown(clean_html(f"""
    <div style="background:#FFF5F7; border:1px solid #FF3F6C; border-radius:12px; padding:14px; margin-bottom:16px;">
        <div style="font-weight:900; font-size:14px; color:#FF3F6C; margin-bottom:4px;">👤 YOUR SAVED FIT PROFILE</div>
        <div style="font-size:13px; color:#282C3F;">Usual Size: <b>{prof['size']}</b> | Height: <b>{prof['height']}</b></div>
        <div style="font-size:11px; color:#696B79; margin-top:4px;">Used for AI Fit Intelligence & size stock matching across all 20 items.</div>
    </div>
    """), unsafe_allow_html=True)

    if st.button("⚙️ EDIT FIT PROFILE", type="primary", use_container_width=True):
        st.session_state.show_profile_modal = True
        st.rerun()

    st.markdown("<br><hr style='border-color:#EAEAEC;'><br>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:13px; font-weight:800; color:#282C3F;'>WISHLIST SUMMARY</div>", unsafe_allow_html=True)
    st.write(f"• Total Saved Items: **{len(st.session_state.wishlist_ids)}**")
    st.write(f"• Items in Shopping Bag: **{len(st.session_state.cart_ids)}**")

    if st.button("🏠 RETURN TO HOME CATALOG", use_container_width=True):
        st.session_state.current_screen = "home"
        st.rerun()

# =========================================================
# SHOPPING BAG / CART SCREEN
# =========================================================
elif st.session_state.current_screen == "cart":
    st.markdown("<div class='section-title'>Shopping Bag</div>", unsafe_allow_html=True)

    cart_prods = [p for p in PRODUCTS if p["id"] in st.session_state.cart_ids]

    if not cart_prods:
        st.info("Your shopping bag is empty.")
        if st.button("🏠 BROWSE 20 PRODUCTS ON HOME", type="primary", use_container_width=True):
            st.session_state.current_screen = "home"
            st.rerun()
    else:
        for item in cart_prods:
            img_b64 = get_image_base64(item["image_path"])
            img_html = f'<img src="{img_b64}" style="width:65px; height:80px; border-radius:6px; object-fit:cover;" />' if img_b64 else ''
            discount_pct = int(((item["original_price"] - item["price"]) / item["original_price"]) * 100)

            bag_html = f"""
            <div style="background:#FFFFFF; border-radius:8px; padding:10px; margin-bottom:10px; display:flex; gap:10px; border:1px solid #EAEAEC;">
                {img_html}
                <div>
                    <div style="font-weight:800; font-size:13px; color:#282C3F; text-transform:uppercase;">{item['brand']}</div>
                    <div style="font-size:11px; color:#696B79; margin-bottom:4px;">{item['name']}</div>
                    <div style="font-size:11px; color:#282C3F;">Qty: <b>1</b> · Size: <b>{st.session_state.body_profile['size']}</b></div>
                    <div style="margin-top:4px;">
                        <span style="font-weight:800; font-size:13px; color:#282C3F;">₹{item['price']:,}</span>
                        <span style="font-size:10px; text-decoration:line-through; color:#7E818C; margin-left:4px;">₹{item['original_price']:,}</span>
                    </div>
                </div>
            </div>
            """
            st.markdown(clean_html(bag_html), unsafe_allow_html=True)

        mrp_total = sum(i["original_price"] for i in cart_prods)
        subtotal = sum(i["price"] for i in cart_prods)
        discount_total = mrp_total - subtotal

        summary_html = f"""
        <div style="background:#FFFFFF; border-radius:8px; padding:12px; border:1px solid #EAEAEC; margin-top:12px;">
            <div style="font-weight:800; font-size:11px; color:#7E818C; text-transform:uppercase; margin-bottom:8px;">PRICE DETAILS ({len(cart_prods)} Items)</div>
            <div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:4px; color:#282C3F;">
                <span>Total MRP</span>
                <span>₹{mrp_total:,}</span>
            </div>
            <div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:4px; color:#03A685;">
                <span>Discount on MRP</span>
                <span>-₹{discount_total:,}</span>
            </div>
            <div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:4px; color:#282C3F;">
                <span>Convenience Fee</span>
                <span style="color:#03A685; font-weight:700;">FREE</span>
            </div>
            <hr style="border-color:#EAEAEC; margin:8px 0;">
            <div style="display:flex; justify-content:space-between; font-size:14px; font-weight:800; color:#282C3F; margin-bottom:10px;">
                <span>Total Amount</span>
                <span>₹{subtotal:,}</span>
            </div>
        </div>
        """
        st.markdown(clean_html(summary_html), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("PLACE ORDER", type="primary", use_container_width=True):
            st.balloons()
            st.success("🎉 Order Placed Successfully! Thank you for shopping on Myntra.")

# ---------------------------------------------------------
# ALWAYS FIXED STICKY BOTTOM NAVIGATION BAR
# ---------------------------------------------------------
wishlist_count = len(st.session_state.wishlist_ids)
cart_count = len(st.session_state.cart_ids)

with st.container():
    b_col1, b_col2, b_col3, b_col4, b_col5 = st.columns(5)
    
    with b_col1:
        if st.button("🏠 Home", key="bnav_home", type="primary" if st.session_state.current_screen == "home" else "secondary", use_container_width=True):
            st.session_state.show_profile_modal = False
            st.session_state.current_screen = "home"
            st.rerun()
            
    with b_col2:
        if st.button("📂 Category", key="bnav_cat", type="primary" if st.session_state.current_screen == "categories" else "secondary", use_container_width=True):
            st.session_state.show_profile_modal = False
            st.session_state.current_screen = "categories"
            st.rerun()
            
    with b_col3:
        w_lbl = f"❤️ Wishlist ({wishlist_count})" if wishlist_count > 0 else "❤️ Wishlist"
        if st.button(w_lbl, key="bnav_wish", type="primary" if st.session_state.current_screen == "wishlist" else "secondary", use_container_width=True):
            st.session_state.show_profile_modal = False
            st.session_state.current_screen = "wishlist"
            st.rerun()
            
    with b_col4:
        c_lbl = f"🛍️ Bag ({cart_count})" if cart_count > 0 else "🛍️ Bag"
        if st.button(c_lbl, key="bnav_bag", type="primary" if st.session_state.current_screen == "cart" else "secondary", use_container_width=True):
            st.session_state.show_profile_modal = False
            st.session_state.current_screen = "cart"
            st.rerun()
            
    with b_col5:
        if st.button("👤 Profile", key="bnav_prof", type="primary" if st.session_state.current_screen == "profile" else "secondary", use_container_width=True):
            st.session_state.show_profile_modal = False
            st.session_state.current_screen = "profile"
            st.rerun()
