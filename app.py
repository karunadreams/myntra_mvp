import streamlit as st
import os
import base64
from typing import TypedDict, List

# ---------------------------------------------------------
# DATA MODELS & DATASET DEFINITION
# ---------------------------------------------------------
class Product(TypedDict):
    id: int
    brand: str
    name: str
    occasion: str
    occasion_type: str
    price: int
    original_price: int
    rating: float
    rating_count: int
    image_path: str
    tag_bg: str
    tag_color: str

WISHLIST_PRODUCTS: List[Product] = [
    {
        "id": 1,
        "brand": "Libas",
        "name": "Embroidered Anarkali Kurta",
        "occasion": "Diwali 2024 🪔",
        "occasion_type": "diwali",
        "price": 1299,
        "original_price": 2999,
        "rating": 4.4,
        "rating_count": 1280,
        "image_path": "assets/libas.jpg",
        "tag_bg": "#FFF3E0",
        "tag_color": "#E65100"
    },
    {
        "id": 2,
        "brand": "W for Woman",
        "name": "Floral Printed Kurta Set",
        "occasion": "Diwali 2024 🪔",
        "occasion_type": "diwali",
        "price": 2499,
        "original_price": 4999,
        "rating": 4.5,
        "rating_count": 890,
        "image_path": "assets/w.jpg",
        "tag_bg": "#FFF3E0",
        "tag_color": "#E65100"
    },
    {
        "id": 3,
        "brand": "Biba",
        "name": "Sequin Sharara Suit",
        "occasion": "Diwali 2024 🪔",
        "occasion_type": "diwali",
        "price": 3199,
        "original_price": 5999,
        "rating": 4.6,
        "rating_count": 2150,
        "image_path": "assets/biba.jpg",
        "tag_bg": "#FFF3E0",
        "tag_color": "#E65100"
    },
    {
        "id": 4,
        "brand": "Global Desi",
        "name": "Floral Wrap Dress",
        "occasion": "College Fest ✨",
        "occasion_type": "college",
        "price": 899,
        "original_price": 1999,
        "rating": 4.3,
        "rating_count": 640,
        "image_path": "assets/global_desi.jpg",
        "tag_bg": "#EDE7F6",
        "tag_color": "#4A148C"
    },
    {
        "id": 5,
        "brand": "Anouk",
        "name": "Printed Co-ord Set",
        "occasion": "College Fest ✨",
        "occasion_type": "college",
        "price": 1749,
        "original_price": 3499,
        "rating": 4.2,
        "rating_count": 420,
        "image_path": "assets/aurelia.jpg",
        "tag_bg": "#EDE7F6",
        "tag_color": "#4A148C"
    }
]

# Helper to convert image file to Base64
def get_image_base64(image_path: str) -> str:
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            return f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode('utf-8')}"
    return ""

def clean_html(html_str: str) -> str:
    lines = [line.strip() for line in html_str.strip().split("\n") if line.strip()]
    return "\n".join(lines)

# ---------------------------------------------------------
# PAGE CONFIG & CSS INJECTION (Mobile Container max 480px)
# ---------------------------------------------------------
st.set_page_config(
    page_title="Myntra Wishlist — Decision Mode",
    page_icon="🛍️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    /* Global Page Background */
    .stApp {
        background-color: #F4F4F6 !important;
        color: #282C3F !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    /* Mobile First Centered App Container (Max Width 480px) */
    .block-container {
        max-width: 480px !important;
        padding-top: 10px !important;
        padding-bottom: 75px !important;
        padding-left: 14px !important;
        padding-right: 14px !important;
        margin: 0 auto !important;
        background-color: #FFFFFF !important;
        min-height: 100vh;
        box-shadow: 0 0 24px rgba(0, 0, 0, 0.08);
        border-radius: 8px;
    }

    /* Hide Streamlit Header & Footer */
    header, footer { visibility: hidden !important; }

    /* Top Navbar Bar */
    .top-navbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 8px 0 12px 0;
        border-bottom: 1px solid #EAEAEC;
        margin-bottom: 12px;
    }

    .top-nav-title {
        font-size: 18px;
        font-weight: 800;
        color: #282C3F;
    }

    .top-nav-sub {
        font-size: 11px;
        color: #7E818C;
        margin-top: 2px;
    }

    /* Primary CTA Button (#FF3F6C Pink) */
    .stButton > button {
        border-radius: 6px !important;
        font-weight: 800 !important;
        letter-spacing: 0.3px !important;
        text-transform: uppercase !important;
        transition: all 0.2s ease !important;
        font-size: 12px !important;
    }

    button[kind="primary"] {
        background-color: #FF3F6C !important;
        color: #FFFFFF !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(255, 63, 108, 0.25) !important;
    }

    button[kind="primary"]:hover {
        background-color: #E6355F !important;
        box-shadow: 0 6px 16px rgba(255, 63, 108, 0.35) !important;
    }

    /* Decision CTA Banner */
    .decision-cta-box {
        background: linear-gradient(135deg, #FFF0F4 0%, #FFE4EC 100%);
        border: 1.5px solid #FF3F6C;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 18px;
        box-shadow: 0 4px 12px rgba(255, 63, 108, 0.12);
        text-align: center;
    }

    .decision-cta-title {
        font-size: 16px;
        font-weight: 900;
        color: #282C3F;
        margin-bottom: 4px;
    }

    .decision-cta-sub {
        font-size: 12px;
        color: #535766;
        margin-bottom: 12px;
    }

    /* Section Header Banners */
    .section-header-box {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 10px 14px;
        border-radius: 8px;
        margin-top: 18px;
        margin-bottom: 12px;
        font-weight: 800;
        font-size: 13px;
    }

    .section-header-box.diwali {
        background: #FFF3E0;
        color: #E65100;
        border-left: 4px solid #FF9800;
    }

    .section-header-box.college {
        background: #EDE7F6;
        color: #4A148C;
        border-left: 4px solid #7E57C2;
    }

    /* Wishlist Product Card */
    .wishlist-card {
        background: #FFFFFF;
        border: 1px solid #EAEAEC;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        position: relative;
    }

    .wishlist-thumb {
        width: 82px;
        height: 82px;
        border-radius: 8px;
        object-fit: cover;
        border: 1px solid #F0F0F0;
        flex-shrink: 0;
    }

    .wishlist-info {
        flex-grow: 1;
        overflow: hidden;
    }

    .brand-name {
        font-size: 13px;
        font-weight: 900;
        color: #282C3F;
        text-transform: uppercase;
        margin-bottom: 2px;
    }

    .prod-name {
        font-size: 12px;
        color: #535766;
        margin-bottom: 4px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .pill-tag {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 10px;
        font-weight: 700;
        margin-bottom: 4px;
    }

    .price-wrap {
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .price-current {
        font-size: 14px;
        font-weight: 800;
        color: #282C3F;
    }

    .price-mrp {
        font-size: 11px;
        text-decoration: line-through;
        color: #7E818C;
    }

    .heart-icon {
        color: #FF3F6C;
        font-size: 18px;
        padding: 4px;
    }

    /* Decision Mode Grid Card */
    .decision-card {
        background: #FFFFFF;
        border: 1px solid #EAEAEC;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 100%;
    }

    .decision-thumb {
        width: 100%;
        height: 150px;
        border-radius: 6px;
        object-fit: cover;
        margin-bottom: 8px;
    }

    /* Urgency Banner */
    .urgency-banner {
        background: #FFF0F4;
        border: 1.5px solid #FF3F6C;
        color: #FF3F6C;
        padding: 10px 14px;
        border-radius: 8px;
        font-weight: 800;
        font-size: 13px;
        text-align: center;
        margin-bottom: 16px;
    }

    /* Sticky Bottom Nav Bar */
    .bottom-nav-bar {
        position: fixed;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 100%;
        max-width: 480px;
        background: #FFFFFF;
        border-top: 1px solid #EAEAEC;
        display: flex;
        justify-content: space-around;
        padding: 8px 0;
        z-index: 9999;
        box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.06);
    }

    .nav-btn {
        display: flex;
        flex-direction: column;
        align-items: center;
        font-size: 10px;
        font-weight: 700;
        color: #696E79;
        position: relative;
        text-decoration: none;
        cursor: pointer;
    }

    .nav-btn.active {
        color: #FF3F6C;
    }

    .nav-badge {
        position: absolute;
        top: -4px;
        right: -8px;
        background: #FF3F6C;
        color: #FFFFFF;
        font-size: 9px;
        font-weight: 800;
        border-radius: 10px;
        padding: 1px 5px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# SESSION STATE INITIALIZATION
# ---------------------------------------------------------
if "current_screen" not in st.session_state:
    st.session_state.current_screen = "wishlist"  # "wishlist", "decision", "confirmation", "cart"

if "wishlist_items" not in st.session_state:
    st.session_state.wishlist_items = WISHLIST_PRODUCTS.copy()

if "chosen_product" not in st.session_state:
    st.session_state.chosen_product = None

if "cart_items" not in st.session_state:
    st.session_state.cart_items = []

if "decision_occasion" not in st.session_state:
    st.session_state.decision_occasion = "Diwali 2024 🪔"

logo_b64 = get_image_base64("assets/myntra_logo.jpg")

# ---------------------------------------------------------
# TOP NAVBAR HEADER
# ---------------------------------------------------------
with st.container():
    h_col1, h_col2 = st.columns([1, 4])
    with h_col1:
        if logo_b64:
            st.markdown(f'<img src="{logo_b64}" style="height:36px; object-fit:contain; border-radius:4px; margin-top:4px;" />', unsafe_allow_html=True)
        else:
            st.markdown("<h3 style='color:#FF3F6C; margin:0; font-weight:900;'>MYNTRA</h3>", unsafe_allow_html=True)
    with h_col2:
        st.markdown(clean_html("""
        <div style="text-align:right;">
            <div class="top-nav-title">My Wishlist</div>
            <div class="top-nav-sub">5 items saved · 12 days left for Diwali</div>
        </div>
        """), unsafe_allow_html=True)

st.markdown("<hr style='border-color:#EAEAEC; margin-top:6px; margin-bottom:14px;'>", unsafe_allow_html=True)

# =========================================================
# SCREEN 1: WISHLIST HOME PAGE
# =========================================================
if st.session_state.current_screen == "wishlist":
    
    # Prominent Decision Mode CTA Box
    st.markdown(clean_html("""
    <div class="decision-cta-box">
        <div class="decision-cta-title">🎯 Hard to Choose What to Buy?</div>
        <div class="decision-cta-sub">Compare wishlisted items side-by-side & pick your Diwali outfit!</div>
    </div>
    """), unsafe_allow_html=True)

    if st.button("🚀 OPEN DECISION MODE (5 ITEMS)", type="primary", use_container_width=True):
        st.session_state.current_screen = "decision"
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Occasion Section 1: Diwali 2024 🪔
    diwali_items = [item for item in WISHLIST_PRODUCTS if item["occasion_type"] == "diwali"]
    st.markdown(clean_html(f"""
    <div class="section-header-box diwali">
        <span>🪔 Diwali 2024 ({len(diwali_items)} Items)</span>
        <span style="font-size:11px; font-weight:700;">12 days left</span>
    </div>
    """), unsafe_allow_html=True)

    for item in diwali_items:
        img_b64 = get_image_base64(item["image_path"])
        img_html = f'<img src="{img_b64}" class="wishlist-thumb" />' if img_b64 else ''
        discount_pct = int(((item["original_price"] - item["price"]) / item["original_price"]) * 100)
        
        card_html = f"""
        <div class="wishlist-card">
            {img_html}
            <div class="wishlist-info">
                <div class="brand-name">{item['brand']}</div>
                <div class="prod-name">{item['name']}</div>
                <div><span class="pill-tag" style="background:{item['tag_bg']}; color:{item['tag_color']};">{item['occasion']}</span></div>
                <div class="price-wrap">
                    <span class="price-current">₹{item['price']:,}</span>
                    <span class="price-mrp">₹{item['original_price']:,}</span>
                    <span style="font-size:11px; font-weight:800; color:#FF905A;">({discount_pct}% OFF)</span>
                </div>
            </div>
            <div class="heart-icon">❤️</div>
        </div>
        """
        st.markdown(clean_html(card_html), unsafe_allow_html=True)

    # Occasion Section 2: College Fest ✨
    college_items = [item for item in WISHLIST_PRODUCTS if item["occasion_type"] == "college"]
    st.markdown(clean_html(f"""
    <div class="section-header-box college">
        <span>✨ College Fest ({len(college_items)} Items)</span>
        <span style="font-size:11px; font-weight:700;">Upcoming</span>
    </div>
    """), unsafe_allow_html=True)

    for item in college_items:
        img_b64 = get_image_base64(item["image_path"])
        img_html = f'<img src="{img_b64}" class="wishlist-thumb" />' if img_b64 else ''
        discount_pct = int(((item["original_price"] - item["price"]) / item["original_price"]) * 100)
        
        card_html = f"""
        <div class="wishlist-card">
            {img_html}
            <div class="wishlist-info">
                <div class="brand-name">{item['brand']}</div>
                <div class="prod-name">{item['name']}</div>
                <div><span class="pill-tag" style="background:{item['tag_bg']}; color:{item['tag_color']};">{item['occasion']}</span></div>
                <div class="price-wrap">
                    <span class="price-current">₹{item['price']:,}</span>
                    <span class="price-mrp">₹{item['original_price']:,}</span>
                    <span style="font-size:11px; font-weight:800; color:#FF905A;">({discount_pct}% OFF)</span>
                </div>
            </div>
            <div class="heart-icon">❤️</div>
        </div>
        """
        st.markdown(clean_html(card_html), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("✨ START DECISION MODE COMPARISON", type="primary", use_container_width=True):
        st.session_state.current_screen = "decision"
        st.rerun()

# =========================================================
# SCREEN 2: DECISION MODE PAGE (/decision)
# =========================================================
elif st.session_state.current_screen == "decision":
    
    col_back, col_title = st.columns([1, 3])
    with col_back:
        if st.button("← BACK", use_container_width=True):
            st.session_state.current_screen = "wishlist"
            st.rerun()
    with col_title:
        st.markdown("<div style='font-size:16px; font-weight:900; color:#282C3F; text-align:right;'>🎯 DECISION MODE</div>", unsafe_allow_html=True)

    # Urgency Banner
    st.markdown(clean_html("""
    <div class="urgency-banner">
        ⚡ Diwali is in 12 days — time to decide & order!
    </div>
    """), unsafe_allow_html=True)

    # Occasion Filter Selector
    selected_occ = st.radio(
        "Select Occasion Group:",
        options=["Diwali 2024 🪔 (3 Items)", "College Fest ✨ (2 Items)", "All Wishlist Items (5)"],
        horizontal=True,
        key="dec_occ_select"
    )

    if "Diwali" in selected_occ:
        filtered_products = [item for item in WISHLIST_PRODUCTS if item["occasion_type"] == "diwali"]
    elif "College" in selected_occ:
        filtered_products = [item for item in WISHLIST_PRODUCTS if item["occasion_type"] == "college"]
    else:
        filtered_products = WISHLIST_PRODUCTS

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:13px; font-weight:800; color:#535766; margin-bottom:10px;'>SIDE-BY-SIDE COMPARISON:</div>", unsafe_allow_html=True)

    # Side-by-Side 2 Column Grid for Decision Mode Comparison
    for row_start in range(0, len(filtered_products), 2):
        row_prods = filtered_products[row_start:row_start + 2]
        cols = st.columns(len(row_prods))
        
        for idx, item in enumerate(row_prods):
            with cols[idx]:
                img_b64 = get_image_base64(item["image_path"])
                img_html = f'<img src="{img_b64}" class="decision-thumb" />' if img_b64 else ''
                discount_pct = int(((item["original_price"] - item["price"]) / item["original_price"]) * 100)

                card_html = f"""
                <div class="decision-card">
                    <div>
                        {img_html}
                        <div class="brand-name">{item['brand']}</div>
                        <div class="prod-name">{item['name']}</div>
                        <div style="margin:4px 0;"><span class="pill-tag" style="background:{item['tag_bg']}; color:{item['tag_color']};">{item['occasion']}</span></div>
                        <div class="price-wrap" style="justify-content:center; margin-bottom:8px;">
                            <span class="price-current">₹{item['price']:,}</span>
                            <span class="price-mrp">₹{item['original_price']:,}</span>
                        </div>
                    </div>
                </div>
                """
                st.markdown(clean_html(card_html), unsafe_allow_html=True)
                st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)
                
                if st.button("CHOOSE THIS", key=f"choose_{item['id']}", type="primary", use_container_width=True):
                    st.session_state.chosen_product = item
                    st.session_state.current_screen = "confirmation"
                    st.rerun()

        st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)

# =========================================================
# CONFIRMATION MODAL / SCREEN (After "Choose This")
# =========================================================
elif st.session_state.current_screen == "confirmation":
    chosen = st.session_state.chosen_product
    if chosen:
        st.balloons()
        
        st.markdown(clean_html("""
        <div style="background:#FFF5F7; border:2px solid #FF3F6C; border-radius:12px; padding:20px; text-align:center; margin-bottom:20px;">
            <div style="font-size:24px; margin-bottom:6px;">🎉</div>
            <div style="font-size:18px; font-weight:900; color:#FF3F6C; margin-bottom:4px;">GREAT CHOICE! READY TO BUY?</div>
            <div style="font-size:13px; color:#535766;">You picked the perfect outfit for your occasion.</div>
        </div>
        """), unsafe_allow_html=True)

        img_b64 = get_image_base64(chosen["image_path"])
        img_html = f'<img src="{img_b64}" style="width:100%; height:240px; border-radius:8px; object-fit:cover; margin-bottom:12px;" />' if img_b64 else ''
        discount_pct = int(((chosen["original_price"] - chosen["price"]) / chosen["original_price"]) * 100)

        card_html = f"""
        <div style="background:#FFFFFF; border:1px solid #EAEAEC; border-radius:10px; padding:16px; margin-bottom:20px; box-shadow:0 4px 12px rgba(0,0,0,0.06);">
            {img_html}
            <div style="font-size:16px; font-weight:900; color:#282C3F; text-transform:uppercase;">{chosen['brand']}</div>
            <div style="font-size:14px; color:#535766; margin-bottom:8px;">{chosen['name']}</div>
            <div style="margin-bottom:12px;"><span class="pill-tag" style="background:{chosen['tag_bg']}; color:{chosen['tag_color']}; font-size:11px;">{chosen['occasion']}</span></div>
            <div style="display:flex; align-items:center; gap:8px;">
                <span style="font-size:20px; font-weight:900; color:#282C3F;">₹{chosen['price']:,}</span>
                <span style="font-size:14px; text-decoration:line-through; color:#7E818C;">₹{chosen['original_price']:,}</span>
                <span style="font-size:14px; font-weight:800; color:#FF905A;">({discount_pct}% OFF)</span>
            </div>
        </div>
        """
        st.markdown(clean_html(card_html), unsafe_allow_html=True)

        st.markdown("### SELECT YOUR SIZE:")
        selected_size = st.radio("Size", options=["S", "M", "L", "XL"], index=1, horizontal=True, key="conf_size")
        st.markdown("<br>", unsafe_allow_html=True)

        btn_c1, btn_c2 = st.columns(2)
        with btn_c1:
            if st.button("🛍️ GO TO CART", type="primary", use_container_width=True):
                if chosen not in st.session_state.cart_items:
                    st.session_state.cart_items.append(chosen)
                st.session_state.current_screen = "cart"
                st.rerun()
        with btn_c2:
            if st.button("← KEEP BROWSING", use_container_width=True):
                st.session_state.current_screen = "decision"
                st.rerun()

# =========================================================
# SCREEN 3: CART / BAG PAGE
# =========================================================
elif st.session_state.current_screen == "cart":
    st.markdown("<h3 style='color:#282C3F; font-weight:900; margin-bottom:14px;'>SHOPPING BAG</h3>", unsafe_allow_html=True)

    if not st.session_state.cart_items:
        st.info("Your shopping bag is empty.")
        if st.button("← RETURN TO WISHLIST", use_container_width=True):
            st.session_state.current_screen = "wishlist"
            st.rerun()
    else:
        for item in st.session_state.cart_items:
            img_b64 = get_image_base64(item["image_path"])
            img_html = f'<img src="{img_b64}" style="width:65px; height:80px; border-radius:6px; object-fit:cover;" />' if img_b64 else ''
            discount_pct = int(((item["original_price"] - item["price"]) / item["original_price"]) * 100)

            bag_html = f"""
            <div style="background:#FFFFFF; border-radius:8px; padding:12px; margin-bottom:12px; display:flex; gap:12px; border:1px solid #EAEAEC;">
                {img_html}
                <div>
                    <div style="font-weight:900; font-size:14px; color:#282C3F; text-transform:uppercase;">{item['brand']}</div>
                    <div style="font-size:12px; color:#535766; margin-bottom:4px;">{item['name']}</div>
                    <div style="font-size:11px; color:#535766;">Qty: <b>1</b> · Size: <b>M</b></div>
                    <div style="margin-top:4px;">
                        <span style="font-weight:800; font-size:14px; color:#282C3F;">₹{item['price']:,}</span>
                        <span style="font-size:11px; text-decoration:line-through; color:#7E818C; margin-left:6px;">₹{item['original_price']:,}</span>
                    </div>
                </div>
            </div>
            """
            st.markdown(clean_html(bag_html), unsafe_allow_html=True)

        mrp_total = sum(i["original_price"] for i in st.session_state.cart_items)
        subtotal = sum(i["price"] for i in st.session_state.cart_items)
        discount_total = mrp_total - subtotal

        summary_html = f"""
        <div style="background:#FFFFFF; border-radius:8px; padding:14px; border:1px solid #EAEAEC; margin-top:16px;">
            <div style="font-weight:800; font-size:11px; color:#7E818C; text-transform:uppercase; margin-bottom:10px;">PRICE DETAILS ({len(st.session_state.cart_items)} Items)</div>
            <div style="display:flex; justify-content:space-between; font-size:13px; margin-bottom:6px; color:#282C3F;">
                <span>Total MRP</span>
                <span>₹{mrp_total:,}</span>
            </div>
            <div style="display:flex; justify-content:space-between; font-size:13px; margin-bottom:6px; color:#03A685;">
                <span>Discount on MRP</span>
                <span>-₹{discount_total:,}</span>
            </div>
            <div style="display:flex; justify-content:space-between; font-size:13px; margin-bottom:6px; color:#282C3F;">
                <span>Convenience Fee</span>
                <span style="color:#03A685; font-weight:700;">FREE</span>
            </div>
            <hr style="border-color:#EAEAEC; margin:10px 0;">
            <div style="display:flex; justify-content:space-between; font-size:15px; font-weight:900; color:#282C3F; margin-bottom:14px;">
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
# STICKY BOTTOM NAVIGATION BAR (Mobile Style)
# ---------------------------------------------------------
cart_count = len(st.session_state.cart_items)
wishlist_count = len(WISHLIST_PRODUCTS)

bottom_nav_html = f"""
<div class="bottom-nav-bar">
    <div class="nav-btn {'active' if st.session_state.current_screen == 'wishlist' else ''}">
        <span style="font-size:16px;">🏠</span>
        <span>Home</span>
    </div>
    <div class="nav-btn">
        <span style="font-size:16px;">📂</span>
        <span>Categories</span>
    </div>
    <div class="nav-btn {'active' if st.session_state.current_screen in ['wishlist', 'decision'] else ''}">
        <span style="font-size:16px;">❤️</span>
        <span>Wishlist</span>
        <span class="nav-badge">{wishlist_count}</span>
    </div>
    <div class="nav-btn {'active' if st.session_state.current_screen == 'cart' else ''}">
        <span style="font-size:16px;">🛍️</span>
        <span>Bag</span>
        {'<span class="nav-badge">' + str(cart_count) + '</span>' if cart_count > 0 else ''}
    </div>
    <div class="nav-btn">
        <span style="font-size:16px;">👤</span>
        <span>Profile</span>
    </div>
</div>
"""
st.markdown(clean_html(bottom_nav_html), unsafe_allow_html=True)
