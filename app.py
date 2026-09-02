import streamlit as st
from datetime import date, timedelta
from PIL import Image
import os
import base64
import json
from typing import TypedDict, List

# Define Product and ScoredProduct Data Models
class Review(TypedDict):
    user: str
    size: str
    height: str
    rating: float
    comment: str
    date: str

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
    fabric: str
    wash_care: str
    pattern: str
    sleeve: str
    fit_summary_template: str
    fit_review_count: int
    keywords: List[str]
    image_path: str
    reviews: List[Review]

class ScoredProduct(TypedDict):
    product: Product
    score: int
    has_size: bool
    occ_match: bool
    arrives_on_time: bool

# Load 20 products dataset from JSON file
def load_products_dataset() -> List[Product]:
    json_path = "assets/kurtas_dataset.json"
    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            return json.load(f)
    return []

PRODUCTS: List[Product] = load_products_dataset()

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
        
        has_size = user_size in prod["sizes"]
        if has_size:
            score += 3

        occ_match = user_occ in prod["occasions"]
        if occ_match:
            score += 2

        arrives_on_time = prod["delivery_days"] <= days_to_event
        if arrives_on_time:
            score += 2

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

# Inject Custom CSS for Pure White Live Myntra Theme (#FFFFFF Page, #FF3F6C Pink Primary, #282C3F Text)
st.markdown("""
<style>
    /* Pure White Page Canvas */
    .stApp {
        background-color: #FFFFFF !important;
        color: #282C3F !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    /* Top Navigation Header Styling */
    .myntra-header-bar {
        background: #FFFFFF;
        border-bottom: 1px solid #EAEAEC;
        padding: 10px 20px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        margin-bottom: 20px;
    }

    .myntra-search-box {
        display: flex;
        align-items: center;
        background: #F5F5F6;
        border-radius: 4px;
        padding: 8px 14px;
        gap: 10px;
        border: 1px solid #F5F5F6;
    }

    .myntra-search-input {
        border: none;
        background: transparent;
        width: 100%;
        font-size: 14px;
        color: #282C3F;
        outline: none;
    }

    /* Product Card Surface (Pure White) */
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

    /* Top-Right Heart Overlay Badge on Image */
    .img-heart-overlay {
        position: absolute;
        top: 8px;
        right: 8px;
        background: rgba(255, 255, 255, 0.92);
        backdrop-filter: blur(4px);
        border-radius: 50%;
        width: 30px;
        height: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.12);
        z-index: 2;
    }

    /* Image Overlay Rating Badge (Bottom Left) */
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

    /* PDP Page Styling */
    .pdp-container {
        background: #FFFFFF;
        border: 1px solid #EAEAEC;
        border-radius: 6px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.04);
    }

    .pdp-spec-box {
        background: #F5F5F6;
        border-radius: 6px;
        padding: 14px;
        margin-top: 16px;
        margin-bottom: 16px;
    }

    .pdp-review-card {
        border-bottom: 1px solid #EAEAEC;
        padding: 12px 0;
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

    /* Passive AI Recommendation Banner */
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

    /* Mobile Responsiveness Rules */
    @media (max-width: 768px) {
        div[data-testid="column"] {
            min-width: 250px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# SESSION STATE INITIALIZATION
# ---------------------------------------------------------
if "current_screen" not in st.session_state:
    st.session_state.current_screen = 1  # Screen 1: Home / Catalog Store

if "pdp_product_id" not in st.session_state:
    st.session_state.pdp_product_id = None

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
# REAL LIVE MYNTRA TOP NAVBAR WITH INTERACTIVE HEADER ICONS
# ---------------------------------------------------------
cart_count = len(st.session_state.cart_items)
wishlist_count = len(st.session_state.wishlist_ids)

# Header container
with st.container():
    h_col1, h_col2, h_col3 = st.columns([3, 4, 3])
    
    with h_col1:
        if st.button("🏠 myntra", key="hdr_home", use_container_width=False):
            st.session_state.pdp_product_id = None
            st.session_state.current_screen = 1
            st.rerun()

    with h_col2:
        st.markdown(clean_html("""
        <div class="myntra-search-box">
            <span style="color:#696E79;">🔍</span>
            <input type="text" class="myntra-search-input" placeholder="Search for products, brands and more" readonly />
        </div>
        """), unsafe_allow_html=True)

    with h_col3:
        c_prof, c_wish, c_bag = st.columns(3)
        with c_prof:
            if st.button("👤 Profile", key="hdr_prof"):
                st.session_state.pdp_product_id = None
                st.session_state.current_screen = 3
                st.rerun()
        with c_wish:
            if st.button(f"❤️ Wishlist ({wishlist_count})", key="hdr_wish", type="primary" if st.session_state.current_screen == 2 else "secondary"):
                st.session_state.pdp_product_id = None
                st.session_state.current_screen = 2
                st.rerun()
        with c_bag:
            if st.button(f"🛍️ Bag ({cart_count})", key="hdr_bag", type="primary" if st.session_state.current_screen == 5 else "secondary"):
                st.session_state.pdp_product_id = None
                st.session_state.current_screen = 5
                st.rerun()

st.markdown("<hr style='border-color:#EAEAEC; margin-top:4px; margin-bottom:16px;'>", unsafe_allow_html=True)

# =========================================================
# PRODUCT DETAILS PAGE (PDP VIEW) IF AN ITEM WAS CLICKED
# =========================================================
if st.session_state.pdp_product_id is not None:
    pdp_prod = next((p for p in PRODUCTS if p["id"] == st.session_state.pdp_product_id), PRODUCTS[0])
    is_in_wishlist = pdp_prod["id"] in st.session_state.wishlist_ids
    
    if st.button("← BACK TO CATALOG", type="secondary"):
        st.session_state.pdp_product_id = None
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    pdp_col1, pdp_col2 = st.columns([1, 1])
    
    with pdp_col1:
        img_b64 = get_image_base64(pdp_prod["image_path"])
        if img_b64:
            st.markdown(f'<img src="{img_b64}" style="width:100%; max-height:480px; border-radius:6px; object-fit:cover; border:1px solid #EAEAEC;" />', unsafe_allow_html=True)
    
    with pdp_col2:
        discount_pct = int(((pdp_prod["original_price"] - pdp_prod["price"]) / pdp_prod["original_price"]) * 100)
        
        st.markdown(clean_html(f"""
        <div style="padding-left:12px;">
            <h2 style="font-size:22px; font-weight:900; color:#282C3F; margin-bottom:4px; text-transform:uppercase;">{pdp_prod['brand']}</h2>
            <p style="font-size:16px; color:#535766; margin-bottom:12px;">{pdp_prod['name']}</p>
            
            <div style="display:inline-flex; align-items:center; gap:6px; background:#F5F5F6; padding:4px 10px; border-radius:4px; margin-bottom:16px; border:1px solid #EAEAEC;">
                <span style="font-weight:800; font-size:13px;">{pdp_prod['rating']} ★</span>
                <span style="color:#7E818C;">|</span>
                <span style="font-size:13px; color:#535766;">{pdp_prod['rating_count']} Verified Ratings</span>
            </div>
            
            <hr style="border-color:#EAEAEC; margin:12px 0;">
            
            <div style="display:flex; align-items:center; gap:10px; margin-bottom:16px;">
                <span style="font-size:24px; font-weight:800; color:#282C3F;">₹{pdp_prod['price']:,}</span>
                <span style="font-size:16px; text-decoration:line-through; color:#7E818C;">MRP ₹{pdp_prod['original_price']:,}</span>
                <span style="font-size:16px; font-weight:800; color:#FF905A;">({discount_pct}% OFF)</span>
            </div>
            <p style="color:#03A685; font-size:12px; font-weight:700; margin-bottom:20px;">inclusive of all taxes</p>
        </div>
        """), unsafe_allow_html=True)

        st.markdown("### SELECT SIZE")
        selected_size = st.radio("Available Sizes:", options=pdp_prod["sizes"], horizontal=True, key="pdp_size_select")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        btn_c1, btn_c2 = st.columns(2)
        with btn_c1:
            if pdp_prod["id"] in [p["id"] for p in st.session_state.cart_items]:
                st.button("✓ IN YOUR BAG", disabled=True, use_container_width=True, type="primary")
            else:
                if st.button("🛍️ ADD TO BAG", type="primary", use_container_width=True):
                    st.session_state.cart_items.append(pdp_prod)
                    st.toast("Added to Bag! ✓", icon="🛍️")
                    st.rerun()

        with btn_c2:
            if is_in_wishlist:
                if st.button("❤️ WISHLISTED", use_container_width=True):
                    st.session_state.wishlist_ids.remove(pdp_prod["id"])
                    st.rerun()
            else:
                if st.button("♡ SAVE TO WISHLIST", use_container_width=True):
                    st.session_state.wishlist_ids.append(pdp_prod["id"])
                    st.rerun()

        st.markdown(clean_html(f"""
        <div class="pdp-spec-box">
            <h4 style="margin:0 0 10px 0; color:#282C3F;">PRODUCT SPECIFICATIONS</h4>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; font-size:13px;">
                <div><b>Fabric:</b> {pdp_prod['fabric']}</div>
                <div><b>Wash Care:</b> {pdp_prod['wash_care']}</div>
                <div><b>Pattern:</b> {pdp_prod['pattern']}</div>
                <div><b>Sleeve:</b> {pdp_prod['sleeve']}</div>
            </div>
        </div>
        """), unsafe_allow_html=True)

    st.markdown("<br><hr style='border-color:#EAEAEC;'><br>", unsafe_allow_html=True)
    st.markdown(f"### RATINGS & CUSTOMER REVIEWS ({len(pdp_prod['reviews'])} Reviews)")
    
    for rev in pdp_prod["reviews"]:
        st.markdown(clean_html(f"""
        <div class="pdp-review-card">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:4px;">
                <span style="background:#03A685; color:#FFF; font-weight:800; font-size:11px; padding:2px 6px; border-radius:3px;">{rev['rating']} ★</span>
                <span style="font-weight:700; color:#282C3F; font-size:14px;">{rev['user']}</span>
                <span style="color:#7E818C; font-size:12px;">(Height: {rev['height']} · Size: {rev['size']})</span>
            </div>
            <p style="font-size:13px; color:#535766; margin:4px 0;">"{rev['comment']}"</p>
            <div style="font-size:11px; color:#7E818C;">Verified Buyer · {rev['date']}</div>
        </div>
        """), unsafe_allow_html=True)

# =========================================================
# SCREEN 1: PRODUCT CATALOG — 20 ITEMS IN 5-COLUMN GRID
# =========================================================
elif st.session_state.current_screen == 1:
    banner_html = f"""
    <div style="background:#FFFFFF; border-radius:4px; padding:18px 24px; margin-bottom:16px; border:1px solid #EAEAEC; box-shadow:0 2px 8px rgba(0,0,0,0.03);">
    <h2 style="color:#282C3F; margin-bottom:2px; font-weight:800;">Women's Ethnic Kurta Store <span style="font-size:14px; color:#7E818C; font-weight:500;">({len(PRODUCTS)} Products)</span></h2>
    <p style="color:#FF3F6C; font-weight:800; font-size:15px; margin-bottom:4px;">UP TO 60% OFF ON FESTIVE & WEDDING COLLECTION</p>
    <p style="color:#535766; font-size:13px; margin:0;">Browse items below. Click any photo/brand name to open <b>Product Details & Reviews</b>, or click <b>❤️ Heart</b> on top right to save to Wishlist.</p>
    </div>
    """
    st.markdown(clean_html(banner_html), unsafe_allow_html=True)

    # Render 20 products in rows of 5
    for row_start in range(0, len(PRODUCTS), 5):
        row_prods = PRODUCTS[row_start:row_start + 5]
        cols = st.columns(len(row_prods))
        for idx, prod in enumerate(row_prods):
            with cols[idx]:
                is_in_wishlist = prod["id"] in st.session_state.wishlist_ids
                card_class = "product-card-white selected" if is_in_wishlist else "product-card-white"
                
                img_b64 = get_image_base64(prod["image_path"])
                
                heart_overlay_html = f"""
                <div class="img-heart-overlay">
                    {'❤️' if is_in_wishlist else '♡'}
                </div>
                """
                
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
                {heart_overlay_html}
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
                
                btn_pdp, btn_wish = st.columns([1, 1])
                with btn_pdp:
                    if st.button("VIEW DETAILS", key=f"pdp_btn_{prod['id']}", use_container_width=True):
                        st.session_state.pdp_product_id = prod["id"]
                        st.rerun()

                with btn_wish:
                    if is_in_wishlist:
                        if st.button("❤️ WISHLISTED", key=f"cat_btn_{prod['id']}", type="primary", use_container_width=True):
                            st.session_state.wishlist_ids.remove(prod["id"])
                            if prod["id"] in st.session_state.selected_ids:
                                st.session_state.selected_ids.remove(prod["id"])
                            st.rerun()
                    else:
                        if st.button("♡ WISHLIST", key=f"cat_btn_{prod['id']}", use_container_width=True):
                            st.session_state.wishlist_ids.append(prod["id"])
                            st.rerun()

        st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

    st.markdown("<br><hr style='border-color:#EAEAEC;'><br>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.session_state.wishlist_ids:
            if st.button(f"GO TO MY WISHLIST ({len(st.session_state.wishlist_ids)} Items Saved) →", type="primary", use_container_width=True):
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
        if st.button("← GO TO CATALOG STORE", use_container_width=True):
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
                    <div class="img-heart-overlay">❤️</div>
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
                    
                    btn_pdp_w, btn_sel_w = st.columns([1, 1])
                    with btn_pdp_w:
                        if st.button("DETAILS", key=f"w_pdp_{prod['id']}", use_container_width=True):
                            st.session_state.pdp_product_id = prod["id"]
                            st.rerun()

                    with btn_sel_w:
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
# SCREEN 3: BODY FIT PROFILE SETUP
# =========================================================
elif st.session_state.current_screen == 3:
    p_head_html = """
    <div style="background:#FFFFFF; border-radius:6px; padding:24px; max-width:600px; margin:0 auto; box-shadow:0 4px 14px rgba(0,0,0,0.05); border:1px solid #EAEAEC;">
    <h3 style="color:#282C3F; margin-bottom:4px; text-align:center; font-weight:800;">Body Fit Profile Setup</h3>
    <p style="color:#535766; font-size:13px; text-align:center; margin-bottom:20px;">Save your profile once to unlock body-type filtered fit intelligence & review highlights across your wishlist.</p>
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
# SCREEN 4: NATIVE MYNTRA DECISION PANEL
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
            <div class="attr-label">Fit Summary ({user_size} · {user_height})</div>
            <div class="attr-value" style="font-style: italic; color:#2B6CB0; font-size:11px;">{fit_summary}</div>
            <div class="attr-label">Review Highlights</div>
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
        st.info("Your bag is currently empty.")
        if st.button("← RETURN TO HOME", use_container_width=True):
            st.session_state.pdp_product_id = None
            st.session_state.current_screen = 1
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
