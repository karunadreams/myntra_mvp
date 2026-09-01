import streamlit as st
from datetime import date, timedelta
from PIL import Image
import os
import base64
import textwrap
from typing import TypedDict, List

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

    # Sort to determine winner (Highest score DESC, rating DESC, price ASC -> -price DESC)
    scored_products.sort(
        key=lambda x: (x["score"], x["product"]["rating"], -x["product"]["price"]),
        reverse=True
    )
    return scored_products

# Set page configuration
st.set_page_config(
    page_title="Myntra Wishlist Decision Panel",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inject Custom CSS for Myntra Dark Navy Theme & High-End Aesthetics
st.markdown(textwrap.dedent("""
<style>
    /* Global Container Styling */
    .stApp {
        background-color: #1A1F36;
        color: #FFFFFF;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    /* Header Bar */
    .myntra-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 12px 24px;
        background: #111528;
        border-bottom: 2px solid #FF3F6C;
        margin-bottom: 24px;
        border-radius: 0 0 12px 12px;
    }
    
    .myntra-logo {
        font-size: 24px;
        font-weight: 800;
        letter-spacing: 1px;
        color: #FF3F6C;
    }
    
    .myntra-tagline {
        font-size: 14px;
        color: #94A3B8;
        font-weight: 500;
    }

    /* Step Indicator Progress Bar */
    .step-tracker {
        display: flex;
        justify-content: center;
        gap: 32px;
        margin-bottom: 28px;
    }
    
    .step-item {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 14px;
        font-weight: 600;
        color: #64748B;
    }
    
    .step-item.active {
        color: #FF3F6C;
    }

    .step-number {
        width: 28px;
        height: 28px;
        border-radius: 50%;
        background: #252B48;
        color: #FFFFFF;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 13px;
        font-weight: 700;
    }

    .step-item.active .step-number {
        background: #FF3F6C;
    }

    /* Product Card Surface (Screen 1) */
    .wishlist-card {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 14px;
        color: #1A1F36;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
        transition: transform 0.2s ease, border 0.2s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .wishlist-card.selected {
        border: 3px solid #FF3F6C;
        background: #FFF5F7;
    }

    .card-brand {
        font-size: 16px;
        font-weight: 800;
        color: #1A1F36;
        margin-bottom: 2px;
    }

    .card-title {
        font-size: 13px;
        color: #4A5568;
        font-weight: 500;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        margin-bottom: 8px;
    }

    .price-row {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 6px;
    }

    .discount-price {
        font-size: 16px;
        font-weight: 800;
        color: #1A1F36;
    }

    .original-price {
        font-size: 12px;
        text-decoration: line-through;
        color: #A0AEC0;
    }

    .discount-badge {
        font-size: 11px;
        font-weight: 700;
        color: #FF905A;
        background: #FFF5F0;
        padding: 2px 6px;
        border-radius: 4px;
    }

    .rating-badge {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        background: #EDF2F7;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 700;
        color: #2D3748;
        margin-bottom: 10px;
    }

    /* Comparison Table Styling (Screen 3) */
    .comp-column {
        background: #FFFFFF;
        color: #1A1F36;
        border-radius: 14px;
        padding: 16px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        border: 2px solid #E2E8F0;
        position: relative;
    }

    .comp-column.winner {
        border: 3.5px solid #FF3F6C;
        box-shadow: 0 0 25px rgba(255, 63, 108, 0.35);
        background: #FFFFFF;
    }

    .winner-badge {
        position: absolute;
        top: -14px;
        left: 50%;
        transform: translateX(-50%);
        background: linear-gradient(135deg, #FF3F6C, #FF905A);
        color: #FFFFFF;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 0.8px;
        padding: 4px 14px;
        border-radius: 20px;
        text-transform: uppercase;
        box-shadow: 0 4px 10px rgba(255, 63, 108, 0.4);
    }

    .row-header {
        font-size: 11px;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 12px;
        margin-bottom: 3px;
    }

    .row-value {
        font-size: 13px;
        font-weight: 600;
        color: #1A1F36;
    }

    .chip {
        display: inline-block;
        background: #F1F5F9;
        color: #334155;
        border-radius: 14px;
        padding: 3px 9px;
        font-size: 11px;
        font-weight: 600;
        margin: 2px;
    }

    /* Layer 4 Passive Recommendation Bar */
    .recommendation-bar {
        background: #111528;
        border: 2px solid #FF3F6C;
        border-radius: 12px;
        padding: 20px 24px;
        margin-top: 32px;
        margin-bottom: 24px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(255, 63, 108, 0.2);
    }

    .rec-title {
        font-size: 18px;
        font-weight: 800;
        color: #FFFFFF;
        margin-bottom: 6px;
    }

    .rec-item-name {
        color: #FF3F6C;
    }

    .rec-subtitle {
        font-size: 14px;
        color: #CBD5E1;
        font-weight: 400;
    }

    /* Profile Badge Banner */
    .profile-badge {
        background: #252B48;
        border: 1px solid #FF3F6C;
        border-radius: 8px;
        padding: 8px 16px;
        display: inline-flex;
        align-items: center;
        gap: 10px;
        font-size: 13px;
        font-weight: 600;
        color: #FFFFFF;
    }

    /* Custom Buttons */
    .stButton > button {
        border-radius: 8px;
        font-weight: 700;
        transition: all 0.2s ease;
    }
</style>
""").strip(), unsafe_allow_html=True)

# ---------------------------------------------------------
# MOCK PRODUCT DATASET (Exact 5 items with Body Profile Fit Data)
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
    st.session_state.current_screen = 1

if "selected_ids" not in st.session_state:
    st.session_state.selected_ids = []

# LAYER 6: Permanent One-Time Body Profile Setup
if "body_profile" not in st.session_state:
    st.session_state.body_profile = {
        "height": "5'3\" - 5'5\"",
        "size": "S",
        "occasion": "Wedding Guest",
        "event_date": date.today() + timedelta(days=6)
    }

if "cart_added_id" not in st.session_state:
    st.session_state.cart_added_id = None

# Helper to convert image to Base64 for inline HTML embedding
def get_image_base64(image_path: str) -> str:
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            return f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode('utf-8')}"
    return ""

# ---------------------------------------------------------
# TOP APP HEADER
# ---------------------------------------------------------
st.markdown(textwrap.dedent("""
<div class="myntra-header">
    <div class="myntra-logo">MYNTRA <span style="font-size:14px; font-weight:600; color:#FF905A;">WISHLIST DECISION PANEL</span></div>
    <div class="myntra-tagline">Solution 2 — 6-Layer Decision Engine</div>
</div>
""").strip(), unsafe_allow_html=True)

# Step Progress Bar
s1_active = "active" if st.session_state.current_screen == 1 else ""
s2_active = "active" if st.session_state.current_screen == 2 else ""
s3_active = "active" if st.session_state.current_screen == 3 else ""

st.markdown(textwrap.dedent(f"""
<div class="step-tracker">
    <div class="step-item {s1_active}">
        <div class="step-number">1</div> Select Items (Layer 1)
    </div>
    <div class="step-item {s2_active}">
        <div class="step-number">2</div> Body Profile Setup (Layer 6)
    </div>
    <div class="step-item {s3_active}">
        <div class="step-number">3</div> Decision Panel (Layers 1-5)
    </div>
</div>
""").strip(), unsafe_allow_html=True)

# ---------------------------------------------------------
# SCREEN 1: WISHLIST SELECTION (LAYER 1)
# ---------------------------------------------------------
if st.session_state.current_screen == 1:
    st.markdown("<h2 style='text-align:center; margin-bottom: 4px;'>Wishlist Comparison (Layer 1)</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#94A3B8; margin-bottom: 24px;'>Select <b>2 to 4 wishlisted items</b> to compare side-by-side on one screen without screenshot workarounds.</p>", unsafe_allow_html=True)

    cols = st.columns(5)
    for idx, prod in enumerate(PRODUCTS):
        with cols[idx]:
            is_selected = prod["id"] in st.session_state.selected_ids
            card_class = "wishlist-card selected" if is_selected else "wishlist-card"
            
            img_b64 = get_image_base64(prod["image_path"])
            img_html = f'<img src="{img_b64}" style="width:100%; border-radius:8px; margin-bottom:10px; object-fit:cover; height:200px;" />' if img_b64 else ''
            
            discount_pct = int(((prod["original_price"] - prod["price"]) / prod["original_price"]) * 100)
            
            # Unified Card HTML Surface
            st.markdown(textwrap.dedent(f"""
            <div class="{card_class}">
                {img_html}
                <div class="card-brand">{prod['brand']}</div>
                <div class="card-title">{prod['name']}</div>
                <div class="price-row">
                    <span class="discount-price">₹{prod['price']:,}</span>
                    <span class="original-price">₹{prod['original_price']:,}</span>
                    <span class="discount-badge">{discount_pct}% OFF</span>
                </div>
                <div class="rating-badge">★ {prod['rating']} ({prod['rating_count']})</div>
            </div>
            """).strip(), unsafe_allow_html=True)
            
            st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
            
            # Layer 1 Selection Checkbox / Toggle Logic
            if is_selected:
                if st.button(f"✓ Selected", key=f"btn_{prod['id']}", type="primary", use_container_width=True):
                    st.session_state.selected_ids.remove(prod["id"])
                    st.rerun()
            else:
                if st.button(f"+ Select to Compare", key=f"btn_{prod['id']}", use_container_width=True):
                    if len(st.session_state.selected_ids) >= 4:
                        st.warning("⚠️ Maximum 4 items can be selected for comparison.")
                    else:
                        st.session_state.selected_ids.append(prod["id"])
                        st.rerun()

    st.markdown("<br><hr style='border-color:#252B48;'><br>", unsafe_allow_html=True)

    # Bottom Action Button
    sel_count = len(st.session_state.selected_ids)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if 2 <= sel_count <= 4:
            if st.button(f"Compare Selected ({sel_count} Items) →", type="primary", use_container_width=True):
                st.session_state.current_screen = 2
                st.rerun()
        else:
            st.button(f"Select at least 2 items to compare ({sel_count}/4 selected)", disabled=True, use_container_width=True)

# ---------------------------------------------------------
# SCREEN 2: LAYER 6 — ONE-TIME BODY PROFILE SETUP
# ---------------------------------------------------------
elif st.session_state.current_screen == 2:
    st.markdown("<h2 style='text-align:center;'>Layer 6: One-Time Body Profile Setup</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#94A3B8; margin-bottom: 24px;'>A 30-second setup saved permanently to unlock body-type filtered fit intelligence & keywords across your entire wishlist.</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("body_profile_form"):
            st.markdown("### 👤 Body Profile Information")
            
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

            st.markdown("<br>### 📅 Event Details")
            
            user_occ = st.selectbox(
                "3. What is your occasion?",
                options=["Wedding Guest", "Festival", "Office Party", "Date Night", "Casual"],
                index=0,
                key="input_occasion"
            )
            
            user_date = st.date_input(
                "4. When is your event?",
                value=st.session_state.body_profile["event_date"],
                min_value=date.today(),
                key="input_date"
            )

            st.markdown("<br>", unsafe_allow_html=True)
            submit = st.form_submit_button("Save Profile & Unlock Decision Panel →", type="primary", use_container_width=True)
            
            if submit:
                st.session_state.body_profile = {
                    "height": st.session_state.input_height,
                    "size": st.session_state.input_size,
                    "occasion": st.session_state.input_occasion,
                    "event_date": st.session_state.input_date
                }
                st.session_state.current_screen = 3
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("← Back to Selection", use_container_width=True):
            st.session_state.current_screen = 1
            st.rerun()

# ---------------------------------------------------------
# SCREEN 3: DECISION PANEL (LAYERS 1, 2, 3, 4, 5)
# ---------------------------------------------------------
elif st.session_state.current_screen == 3:
    # Selected Products Subset
    selected_products: List[Product] = [p for p in PRODUCTS if p["id"] in st.session_state.selected_ids]
    
    profile = st.session_state.body_profile
    user_height = profile["height"]
    user_size = profile["size"]
    user_occ = profile["occasion"]
    event_date = profile["event_date"]
    days_to_event = (event_date - date.today()).days

    # ---------------------------------------------------------
    # SILENT CONFIDENCE ENGINE SCORING
    # ---------------------------------------------------------
    scored_products = calculate_winner_scoring(selected_products, user_occ, user_size, days_to_event)
    winner_item: Product = scored_products[0]["product"]

    # Header with Body Profile Badge & Navigation Actions
    h_col1, h_col2 = st.columns([3, 1])
    with h_col1:
        st.markdown(f"<h2>Wishlist Decision Panel</h2>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="profile-badge">
            <span>👤 Body Profile Filter: <b>{user_size} · {user_height}</b></span>
            <span style="color:#FF905A;">|</span>
            <span>Occasion: <b>{user_occ}</b></span>
        </div>
        """, unsafe_allow_html=True)
    with h_col2:
        if st.button("⚙️ Edit Profile / Items", use_container_width=True):
            st.session_state.current_screen = 1
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # LAYER 1, 2, 3 & 5: SIDE-BY-SIDE COMPARISON MATRIX COLUMNS
    # ---------------------------------------------------------
    num_items = len(selected_products)
    comp_cols = st.columns(num_items)

    for idx, item_data in enumerate(scored_products):
        prod = item_data["product"]
        is_winner = (prod["id"] == winner_item["id"])
        
        with comp_cols[idx]:
            # Winner column styling highlight
            col_class = "comp-column winner" if is_winner else "comp-column"
            winner_html = '<div class="winner-badge">★ HIGHEST CONFIDENCE SCORE</div>' if is_winner else ''

            img_b64 = get_image_base64(prod["image_path"])
            img_html = f'<img src="{img_b64}" style="width:100%; border-radius:8px; margin-bottom:12px; object-fit:cover; height:180px;" />' if img_b64 else ''
            
            discount_pct = int(((prod["original_price"] - prod["price"]) / prod["original_price"]) * 100)
            
            size_str = f"🟢 Available in {user_size}" if item_data['has_size'] else f"🔴 Not available in {user_size}"
            del_str = f"Delivers in {prod['delivery_days']} days ({'🟢 Arrives before event' if item_data['arrives_on_time'] else '🔴 Arrives after event'})"
            
            # Layer 2: Fit Intelligence from Body-Type Filtered Reviews
            fit_summary = f"\"People your size ({user_size} · {user_height}) say: {prod['fit_summary_template']} · {prod['fit_review_count']} matching reviews.\""
            
            # Layer 3: Review Intelligence Keywords (3 extracted keywords)
            chips_html = "".join([f'<span class="chip">{kw}</span>' for kw in prod['keywords']])

            # Unified Column HTML Card (dedented to column 0 to prevent markdown code block parsing)
            column_card_html = textwrap.dedent(f"""
            <div class="{col_class}">
            {winner_html}
            <div style="margin-top: 10px;"></div>
            {img_html}
            <div class="card-brand">{prod['brand']}</div>
            <div class="card-title">{prod['name']}</div>
            
            <!-- LAYER 1: COMPARISON ATTRIBUTES -->
            <div class="row-header">Price</div>
            <div class="price-row">
            <span class="discount-price">₹{prod['price']:,}</span>
            <span class="original-price">₹{prod['original_price']:,}</span>
            <span class="discount-badge">{discount_pct}% OFF</span>
            </div>
            
            <div class="row-header">Average Rating</div>
            <div class="row-value">★ {prod['rating']} ({prod['rating_count']:,} reviews)</div>
            
            <div class="row-header">Size Availability</div>
            <div class="row-value">{size_str}</div>
            
            <div class="row-header">Estimated Delivery</div>
            <div class="row-value">{del_str}</div>
            
            <!-- LAYER 2: FIT INTELLIGENCE (FILTERED REVIEWS) -->
            <div class="row-header">Layer 2: Fit Intelligence (Body Filtered)</div>
            <div class="row-value" style="font-style: italic; color: #2B6CB0; font-size:12px;">{fit_summary}</div>
            
            <!-- LAYER 3: REVIEW INTELLIGENCE KEYWORDS -->
            <div class="row-header">Layer 3: Review Keywords ({user_size} · {user_height})</div>
            <div style="margin-bottom: 12px;">{chips_html}</div>
            </div>
            """).strip()

            st.markdown(column_card_html, unsafe_allow_html=True)

            st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

            # LAYER 5: DIRECT ADD TO CART FROM COMPARISON SCREEN
            if is_winner:
                if st.session_state.cart_added_id == prod["id"]:
                    st.button("✓ Added to Cart", key=f"cart_{prod['id']}", type="primary", disabled=True, use_container_width=True)
                else:
                    if st.button("🛒 Add to Cart", key=f"cart_{prod['id']}", type="primary", use_container_width=True):
                        st.session_state.cart_added_id = prod["id"]
                        st.toast("Added to cart! ✓ Complete your purchase on Myntra.", icon="🛒")
                        st.rerun()
            else:
                st.button("Save for Later", key=f"save_{prod['id']}", use_container_width=True)

    # ---------------------------------------------------------
    # LAYER 4: ONE-LINE AI RECOMMENDATION (PASSIVE)
    # ---------------------------------------------------------
    rec_bar_html = textwrap.dedent(f"""
    <div class="recommendation-bar">
        <div class="rec-title">
            Based on ratings and fit reviews from people your size (<span style="color:#FF905A;">{user_size} · {user_height}</span>), <span class="rec-item-name">{winner_item['brand']} {winner_item['name']}</span> has the highest confidence score.
        </div>
        <div class="rec-subtitle">
            No typing or chatbot needed — 4.5★ average rating, 48 body-matched fit reviews, and guaranteed size availability.
        </div>
    </div>
    """).strip()
    
    st.markdown(rec_bar_html, unsafe_allow_html=True)
