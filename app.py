import streamlit as st
from datetime import date, timedelta
from PIL import Image
import os
import base64
import textwrap
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

# Set page configuration
st.set_page_config(
    page_title="Myntra Wishlist & Decision Panel",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inject Custom CSS for Native Myntra App UI & Theme (Light #F5F5F6 + #FFFFFF Surface, Pink #FF3F6C Accent)
st.markdown(textwrap.dedent("""
<style>
    /* Global Container & Light Canvas Styling */
    .stApp {
        background-color: #F5F5F6;
        color: #282C3F;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }

    /* Main Viewport Mobile Constraints container */
    .myntra-viewport {
        max-width: 1200px;
        margin: 0 auto;
        padding-bottom: 70px;
    }

    /* Top App Header (Native Myntra Look) */
    .myntra-nav-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 12px 20px;
        background: #FFFFFF;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
        position: sticky;
        top: 0;
        z-index: 999;
    }

    .myntra-brand-logo {
        font-size: 20px;
        font-weight: 900;
        letter-spacing: 0.5px;
        color: #282C3F;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    
    .myntra-pink-tag {
        color: #FF3F6C;
        font-style: italic;
    }

    .myntra-header-icons {
        display: flex;
        align-items: center;
        gap: 16px;
        color: #282C3F;
        font-size: 14px;
        font-weight: 700;
    }

    .icon-badge {
        background: #FF3F6C;
        color: #FFFFFF;
        border-radius: 50%;
        padding: 2px 6px;
        font-size: 10px;
        font-weight: 800;
    }

    /* Sticky Bottom Nav Bar */
    .myntra-bottom-nav {
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

    .nav-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        font-size: 11px;
        font-weight: 700;
        color: #535766;
        cursor: pointer;
        text-decoration: none;
    }

    .nav-item.active {
        color: #FF3F6C;
    }

    /* Native Wishlist Card Surface (Light Mode) */
    .wishlist-card-native {
        background: #FFFFFF;
        border-radius: 8px;
        padding: 10px;
        border: 1px solid #EAEAEC;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
        transition: border 0.2s ease, box-shadow 0.2s ease;
        position: relative;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .wishlist-card-native.selected {
        border: 2.5px solid #FF3F6C;
        background: #FFF5F7;
    }

    .card-brand-native {
        font-size: 14px;
        font-weight: 800;
        color: #282C3F;
        text-transform: uppercase;
        margin-top: 6px;
        margin-bottom: 1px;
    }

    .card-title-native {
        font-size: 12px;
        color: #535766;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        margin-bottom: 6px;
    }

    .price-row-native {
        display: flex;
        align-items: center;
        gap: 6px;
        margin-bottom: 6px;
    }

    .price-discounted {
        font-size: 14px;
        font-weight: 800;
        color: #282C3F;
    }

    .price-original {
        font-size: 11px;
        text-decoration: line-through;
        color: #94969F;
    }

    .price-off-badge {
        font-size: 11px;
        font-weight: 700;
        color: #FF905A;
    }

    .rating-pill-native {
        display: inline-flex;
        align-items: center;
        gap: 3px;
        background: #F5F5F6;
        border-radius: 4px;
        padding: 2px 6px;
        font-size: 11px;
        font-weight: 700;
        color: #282C3F;
        margin-bottom: 8px;
    }

    /* Side-by-Side Decision Panel Styling */
    .comp-column-native {
        background: #FFFFFF;
        color: #282C3F;
        border-radius: 12px;
        padding: 14px;
        border: 1px solid #EAEAEC;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.06);
        position: relative;
    }

    .comp-column-native.winner {
        border: 2.5px solid #FF3F6C;
        box-shadow: 0 4px 20px rgba(255, 63, 108, 0.2);
    }

    .winner-badge-native {
        position: absolute;
        top: -12px;
        left: 50%;
        transform: translateX(-50%);
        background: #FF3F6C;
        color: #FFFFFF;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 0.5px;
        padding: 3px 12px;
        border-radius: 14px;
        text-transform: uppercase;
        box-shadow: 0 2px 6px rgba(255, 63, 108, 0.3);
    }

    .row-header-native {
        font-size: 11px;
        font-weight: 700;
        color: #7E818C;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 10px;
        margin-bottom: 2px;
    }

    .row-val-native {
        font-size: 12px;
        font-weight: 600;
        color: #282C3F;
    }

    .chip-native {
        display: inline-block;
        background: #F5F5F6;
        color: #3E4152;
        border-radius: 12px;
        padding: 3px 8px;
        font-size: 10px;
        font-weight: 600;
        margin: 2px;
        border: 1px solid #EAEAEC;
    }

    /* Layer 4 Passive AI Recommendation Banner (Myntra Light Theme) */
    .rec-banner-native {
        background: #FFFFFF;
        border: 1.5px solid #FF3F6C;
        border-radius: 10px;
        padding: 16px 20px;
        margin-top: 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 14px rgba(255, 63, 108, 0.1);
        text-align: center;
    }

    .rec-title-native {
        font-size: 15px;
        font-weight: 800;
        color: #282C3F;
        margin-bottom: 4px;
    }

    .rec-pink-highlight {
        color: #FF3F6C;
    }

    .rec-sub-native {
        font-size: 12px;
        color: #535766;
    }

    /* Profile Badge pill */
    .profile-pill-native {
        background: #FFF5F7;
        border: 1px solid #FF3F6C;
        border-radius: 20px;
        padding: 4px 12px;
        font-size: 12px;
        font-weight: 700;
        color: #FF3F6C;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }

    /* Native Buttons */
    .stButton > button {
        border-radius: 6px;
        font-weight: 800;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        transition: all 0.2s ease;
    }

    /* Mobile Responsiveness Rules */
    @media (max-width: 768px) {
        .myntra-nav-header {
            padding: 10px 14px;
        }
        .comp-column-native {
            padding: 10px;
        }
        div[data-testid="column"] {
            min-width: 250px !important;
        }
    }
</style>
""").strip(), unsafe_allow_html=True)

# ---------------------------------------------------------
# MOCK PRODUCT DATASET (Exact 5 items matching Myntra catalog)
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
    }
]

# ---------------------------------------------------------
# SESSION STATE INITIALIZATION
# ---------------------------------------------------------
if "current_screen" not in st.session_state:
    st.session_state.current_screen = 1  # Default to Home (Screen 1)

if "selected_ids" not in st.session_state:
    st.session_state.selected_ids = [1, 3]  # Pre-select 2 items for seamless test

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
# TOP NATIVE MYNTRA APP HEADER
# ---------------------------------------------------------
cart_count = len(st.session_state.cart_items)
wishlist_count = len(PRODUCTS)

st.markdown(textwrap.dedent(f"""
<div class="myntra-nav-header">
    <div class="myntra-brand-logo">
        <span style="color:#FF3F6C; font-weight:900;">myntra</span>
        <span style="font-size:12px; font-weight:600; color:#535766;">| WISHLIST DECISION PANEL</span>
    </div>
    <div class="myntra-header-icons">
        <span>🔍</span>
        <span>❤️ <span class="icon-badge">{wishlist_count}</span></span>
        <span>🛍️ <span class="icon-badge">{cart_count}</span></span>
    </div>
</div>
""").strip(), unsafe_allow_html=True)

# ---------------------------------------------------------
# SCREEN NAVIGATION CONTROLLER (5 Native Screens)
# ---------------------------------------------------------
# Navigation Bar Tabs
nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns(5)
with nav_col1:
    if st.button("🏠 Home", use_container_width=True, type="primary" if st.session_state.current_screen == 1 else "secondary"):
        st.session_state.current_screen = 1
        st.rerun()
with nav_col2:
    if st.button("❤️ Wishlist", use_container_width=True, type="primary" if st.session_state.current_screen == 2 else "secondary"):
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
# SCREEN 1: MYNTRA APP HOME PAGE
# =========================================================
if st.session_state.current_screen == 1:
    st.markdown(textwrap.dedent("""
    <div style="background:#FFFFFF; border-radius:10px; padding:20px; text-align:center; box-shadow:0 2px 10px rgba(0,0,0,0.05);">
        <h2 style="color:#282C3F; margin-bottom:4px;">Festive & Occasion Store</h2>
        <p style="color:#FF3F6C; font-weight:700; margin-bottom:16px;">UP TO 60% OFF ON FESTIVE KURTAS & ANARKALIS</p>
        <p style="color:#535766; font-size:14px;">You have <b>5 items saved in your Wishlist</b> for your upcoming event.</p>
    </div>
    """).strip(), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.button("❤️ GO TO MY WISHLIST (5 Items Saved) →", type="primary", use_container_width=True):
            st.session_state.current_screen = 2
            st.rerun()

# =========================================================
# SCREEN 2: NATIVE MYNTRA WISHLIST PAGE
# =========================================================
elif st.session_state.current_screen == 2:
    st.markdown(textwrap.dedent(f"""
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
        <h3 style="margin:0; color:#282C3F;">MY WISHLIST <span style="font-size:14px; color:#94969F;">({len(PRODUCTS)} Items)</span></h3>
        <span style="font-size:12px; color:#FF3F6C; font-weight:700;">Select 2-4 items to Compare</span>
    </div>
    """).strip(), unsafe_allow_html=True)

    cols = st.columns(5)
    for idx, prod in enumerate(PRODUCTS):
        with cols[idx]:
            is_selected = prod["id"] in st.session_state.selected_ids
            card_class = "wishlist-card-native selected" if is_selected else "wishlist-card-native"
            
            img_b64 = get_image_base64(prod["image_path"])
            img_html = f'<img src="{img_b64}" style="width:100%; border-radius:6px; margin-bottom:8px; object-fit:cover; height:200px;" />' if img_b64 else ''
            discount_pct = int(((prod["original_price"] - prod["price"]) / prod["original_price"]) * 100)
            
            # Native Wishlist Card HTML
            st.markdown(textwrap.dedent(f"""
            <div class="{card_class}">
                {img_html}
                <div class="card-brand-native">{prod['brand']}</div>
                <div class="card-title-native">{prod['name']}</div>
                <div class="price-row-native">
                    <span class="price-discounted">₹{prod['price']:,}</span>
                    <span class="price-original">₹{prod['original_price']:,}</span>
                    <span class="price-off-badge">({discount_pct}% OFF)</span>
                </div>
                <div class="rating-pill-native">★ {prod['rating']} | {prod['rating_count']}</div>
            </div>
            """).strip(), unsafe_allow_html=True)
            
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

    st.markdown("<br><hr style='border-color:#EAEAEC;'><br>", unsafe_allow_html=True)

    # Sticky Myntra Pink Compare CTA
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
    st.markdown(textwrap.dedent("""
    <div style="background:#FFFFFF; border-radius:10px; padding:24px; max-width:600px; margin:0 auto; box-shadow:0 4px 14px rgba(0,0,0,0.06);">
        <h3 style="color:#282C3F; margin-bottom:4px; text-align:center;">Layer 6: One-Time Body Profile Setup</h3>
        <p style="color:#535766; font-size:13px; text-align:center; margin-bottom:20px;">Save your profile once to unlock body-type filtered fit intelligence & keywords across your entire wishlist.</p>
    </div>
    """).strip(), unsafe_allow_html=True)

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
        st.markdown(f"<h3 style='margin:0; color:#282C3F;'>WISHLIST DECISION PANEL</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="profile-pill-native" style="margin-top:6px;">
            <span>👤 Body Filter: <b>{user_size} · {user_height}</b></span>
            <span>|</span>
            <span>Occasion: <b>{user_occ}</b></span>
        </div>
        """, unsafe_allow_html=True)
    with h_col2:
        if st.button("⚙️ EDIT PROFILE", use_container_width=True):
            st.session_state.current_screen = 3
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Side-by-Side Columns Matrix
    num_items = len(selected_products)
    comp_cols = st.columns(num_items)

    for idx, item_data in enumerate(scored_products):
        prod = item_data["product"]
        is_winner = (prod["id"] == winner_item["id"])
        
        with comp_cols[idx]:
            col_class = "comp-column-native winner" if is_winner else "comp-column-native"
            winner_html = '<div class="winner-badge-native">★ HIGHEST CONFIDENCE MATCH</div>' if is_winner else ''

            img_b64 = get_image_base64(prod["image_path"])
            img_html = f'<img src="{img_b64}" style="width:100%; border-radius:6px; margin-bottom:10px; object-fit:cover; height:180px;" />' if img_b64 else ''
            discount_pct = int(((prod["original_price"] - prod["price"]) / prod["original_price"]) * 100)
            
            size_str = f"<span style='color:#03A685; font-weight:700;'>🟢 Available in {user_size}</span>" if item_data['has_size'] else f"<span style='color:#FF3F6C; font-weight:700;'>🔴 Out of Stock in {user_size}</span>"
            del_str = f"Delivers in {prod['delivery_days']} days ({'🟢 Arrives before event' if item_data['arrives_on_time'] else '🔴 Arrives after event'})"
            
            fit_summary = f"\"People your size ({user_size} · {user_height}) say: {prod['fit_summary_template']} · {prod['fit_review_count']} matching reviews.\""
            chips_html = "".join([f'<span class="chip-native">{kw}</span>' for kw in prod['keywords']])

            column_card_html = textwrap.dedent(f"""
            <div class="{col_class}">
            {winner_html}
            <div style="margin-top: 8px;"></div>
            {img_html}
            <div class="card-brand-native">{prod['brand']}</div>
            <div class="card-title-native">{prod['name']}</div>
            
            <div class="row-header-native">Price</div>
            <div class="price-row-native">
            <span class="price-discounted">₹{prod['price']:,}</span>
            <span class="price-original">₹{prod['original_price']:,}</span>
            <span class="price-off-badge">({discount_pct}% OFF)</span>
            </div>
            
            <div class="row-header-native">Average Rating</div>
            <div class="row-val-native">★ {prod['rating']} ({prod['rating_count']:,} reviews)</div>
            
            <div class="row-header-native">Size Availability ({user_size})</div>
            <div class="row-val-native">{size_str}</div>
            
            <div class="row-header-native">Estimated Delivery</div>
            <div class="row-val-native">{del_str}</div>
            
            <div class="row-header-native">Layer 2: Fit Summary ({user_size} · {user_height})</div>
            <div class="row-val-native" style="font-style: italic; color:#2B6CB0; font-size:11px;">{fit_summary}</div>
            
            <div class="row-header-native">Layer 3: Review Keywords</div>
            <div style="margin-bottom: 8px;">{chips_html}</div>
            </div>
            """).strip()

            st.markdown(column_card_html, unsafe_allow_html=True)
            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

            # Layer 5: Direct Add to Cart CTA
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

    # Layer 4: One-Line AI Recommendation Banner
    rec_bar_html = textwrap.dedent(f"""
    <div class="rec-banner-native">
        <div class="rec-title-native">
            Based on ratings and fit reviews from people your size (<span class="rec-pink-highlight">{user_size} · {user_height}</span>), <span class="rec-pink-highlight">{winner_item['brand']} {winner_item['name']}</span> has the highest confidence score.
        </div>
        <div class="rec-sub-native">
            4.5★ rating, 48 body-matched fit reviews, guaranteed size availability, and delivery before your event date.
        </div>
    </div>
    """).strip()
    
    st.markdown(rec_bar_html, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("VIEW BAG & CHECKOUT →", type="primary", use_container_width=True):
        st.session_state.current_screen = 5
        st.rerun()

# =========================================================
# SCREEN 5: NATIVE MYNTRA CART / BAG PAGE
# =========================================================
elif st.session_state.current_screen == 5:
    st.markdown("<h3 style='color:#282C3F;'>SHOPPING BAG</h3>", unsafe_allow_html=True)

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

                st.markdown(textwrap.dedent(f"""
                <div style="background:#FFFFFF; border-radius:8px; padding:12px; margin-bottom:12px; display:flex; gap:14px; border:1px solid #EAEAEC;">
                    {img_html}
                    <div>
                        <div style="font-weight:800; font-size:14px; color:#282C3F;">{item['brand']}</div>
                        <div style="font-size:12px; color:#535766; margin-bottom:6px;">{item['name']}</div>
                        <div style="font-size:12px; color:#535766;">Size: <b>{st.session_state.body_profile['size']}</b> | Qty: <b>1</b></div>
                        <div style="margin-top:6px;">
                            <span style="font-weight:800; font-size:14px; color:#282C3F;">₹{item['price']:,}</span>
                            <span style="font-size:11px; text-decoration:line-through; color:#94969F; margin-left:6px;">₹{item['original_price']:,}</span>
                            <span style="font-size:11px; font-weight:700; color:#FF905A; margin-left:6px;">({discount_pct}% OFF)</span>
                        </div>
                    </div>
                </div>
                """).strip(), unsafe_allow_html=True)

        with col2:
            subtotal = sum(i["price"] for i in st.session_state.cart_items)
            mrp_total = sum(i["original_price"] for i in st.session_state.cart_items)
            discount_total = mrp_total - subtotal

            st.markdown(textwrap.dedent(f"""
            <div style="background:#FFFFFF; border-radius:8px; padding:16px; border:1px solid #EAEAEC;">
                <div style="font-weight:800; font-size:13px; color:#7E818C; text-transform:uppercase; margin-bottom:12px;">PRICE DETAILS ({len(st.session_state.cart_items)} Items)</div>
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
            """).strip(), unsafe_allow_html=True)

            st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
            if st.button("PLACE ORDER", type="primary", use_container_width=True):
                st.balloons()
                st.success("Order Placed Successfully! 🎉 Thank you for shopping on Myntra.")

# ---------------------------------------------------------
# STICKY BOTTOM NAV BAR (Real Myntra Look)
# ---------------------------------------------------------
st.markdown(textwrap.dedent("""
<div class="myntra-bottom-nav">
    <div class="nav-item">🏠<br>Home</div>
    <div class="nav-item">📂<br>Categories</div>
    <div class="nav-item">🎬<br>Studio</div>
    <div class="nav-item active">❤️<br>Wishlist</div>
    <div class="nav-item">👤<br>Profile</div>
</div>
""").strip(), unsafe_allow_html=True)
