# Architecture & Implementation Blueprint: Myntra Wishlist Decision Panel MVP

## Executive Summary

The **Myntra Wishlist Decision Panel MVP** is a high-impact, standalone Python + Streamlit web application designed to solve choice overload for occasion-driven shoppers. When users save 3–5 similar items to their wishlist for a specific event (wedding, festival, office party, etc.), they face decision friction due to the lack of an in-app comparison mechanism.

This document outlines the **end-to-end phase-wise architecture**, detailing system design, layer specifications, scoring logic, local setup, testing protocols, version control workflow, and deployment to Streamlit Community Cloud.

---

## Architecture Overview & Phase Blueprint

```
+-----------------------------------------------------------------------------------+
|                            PHASE 1: SYSTEM ARCHITECTURE                           |
|       3-Screen Workflow | Custom CSS Design System | 6-Layer Decision Engine      |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                            PHASE 2: DATA & SCORING ENGINE                         |
|         Structured Mock Products | Silent Weighted Winner Scoring Algorithm        |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                         PHASE 3: LOCAL ENVIRONMENT & MVP DEV                      |
|         Streamlit App Core | Asset Resolution | Session State Management         |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                            PHASE 4: LOCAL TESTING & QA                            |
|       Rule-Engine Testing | Selection Constraints | Mobile/Desktop Verification   |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                         PHASE 5: GIT & GITHUB WORKFLOW                            |
|           Repository Initialization | Security Check | Branch & Commit            |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                         PHASE 6: STREAMLIT CLOUD DEPLOYMENT                       |
|           Cloud Connector | Requirements Management | Live URL Verification        |
+-----------------------------------------------------------------------------------+
```

---

## Phase 1: High-Level System Architecture & Design Specification

### 1.1 Technology Stack

- **Core Framework**: Python 3.10+ with [Streamlit](https://streamlit.io/)
- **UI Engine**: Native Streamlit components augmented with injected custom CSS (`st.markdown(..., unsafe_allow_html=True)`)
- **State Management**: Streamlit `st.session_state` for multi-screen navigation, item selection, user context, and cart state
- **Image Delivery**: Local file resolution via `assets/` directory (`libas.jpg`, `w.jpg`, `biba.jpg`, `aurelia.jpg`, `global_desi.jpg`)

### 1.2 Design System Tokens

| Component | Token / Hex Code | Usage |
|---|---|---|
| **Primary Background** | `#1A1F36` (Dark Navy) | Main application container & headers |
| **Primary CTA** | `#FF3F6C` (Myntra Pink) | Winner border, "Add to Cart" button, badges |
| **Accent Color** | `#FF905A` (Myntra Orange) | Highlight badges, tag borders |
| **Card Surface** | `#FFFFFF` (Pure White) | Product comparison columns & wishlist cards |
| **Secondary Button** | `#F5F5F6` / `#94A3B8` | Outlined "Save for Later" CTAs |
| **Typography** | Inter, -apple-system, sans-serif | High contrast, modern aesthetic |

---

## Phase 2: The 6 Layers & Decision Engine Architecture

The decision panel consists of 6 integrated functional layers operating seamlessly across 3 distinct screens:

```
Screen 1: Wishlist Grid (Layer 1)
       │
       ▼
Screen 2: Context Setup (Occasion, Date, Size)
       │
       ▼
Screen 3: Decision Panel (Layers 2, 3, 4, 5, 6)
  ├── Layer 2: Side-by-Side Comparison Matrix & Silent Scoring Engine
  ├── Layer 3: Fit Summary per Item
  ├── Layer 4: Review Keyword Chips
  ├── Layer 5: One-Line Passive Recommendation Bar
  └── Layer 6: Instant Add to Cart CTA (Winner-focused)
```

### 2.1 Layer Specifications

#### Layer 1: Select to Compare (Wishlist Screen)
- Displays 5 mock wishlist items in an interactive card grid.
- Allows user to select 2 to 4 items.
- Enforces maximum selection cap of 4 items with warning alerts.
- Displays sticky/fixed bottom CTA: `Compare Selected (N items)` activated when $2 \le N \le 4$.

#### Layer 2: Side-by-Side Comparison Matrix
- Renders selected items as columns with aligned attribute rows:
  - **Thumbnail, Brand & Product Title**
  - **Price Row**: Discounted Price + Struck-through Original Price + Discount % Badge
  - **Rating Row**: Star Rating + Total Ratings count
  - **Size Availability**: ✅ Available in [User's Size] / ❌ Not Available
  - **Occasion Match**: ✅ Great for [Selected Occasion] / ⚠️ Not Ideal
  - **Delivery Details**: Expected Delivery Date + Days Remaining
  - **Event Deadline Status**: 🟢 Arrives before event / 🔴 Arrives after event

#### Layer 3: Fit Summary per Item
- Scannable single-line fit verdict derived from aggregated customer feedback (e.g., *"True to size, roomy shoulders"*).

#### Layer 4: Review Keyword Chips
- 3–4 rounded pill tags per product summarizing key sentiment (e.g., `True to size`, `Flowy fabric`, `Color true to photo`).

#### Layer 5: One-Line Passive Recommendation Bar
- Full-width dark navy recommendation bar summarizing the winning item:
  > *"Based on your occasion and size, **[Brand] [Item Name]** is your best match."*
  > *"Sub-line: It is available in your size, arrives before your event, and is well-rated for [Occasion]."*

#### Layer 6: Direct Add to Cart CTA
- Winning product column features prominent solid Myntra Pink `Add to Cart` CTA.
- Non-winner columns feature subtle grey `Save for Later` secondary CTAs.
- Interaction triggers state change to `✓ Added` and renders success toast (`Added to cart! ✓ Complete your purchase on Myntra.`).

---

### 2.2 Silent Winner Scoring Engine Algorithm

The decision logic operates silently behind the scenes without exposing numerical scores to the user:

$$\text{Score}(I) = S_{\text{size}}(I) + S_{\text{occasion}}(I) + S_{\text{delivery}}(I) + S_{\text{rating}}(I)$$

Where:
- $S_{\text{size}}(I) = +3$ if $U_{\text{size}} \in I.\text{sizes}$, else $0$
- $S_{\text{occasion}}(I) = +2$ if $U_{\text{occasion}} \in I.\text{occasions}$, else $0$
- $S_{\text{delivery}}(I) = +2$ if $I.\text{delivery\_days} \le U_{\text{days\_until\_event}}$, else $0$
- $S_{\text{rating}}(I) = +1$ if $I.\text{rating} \ge 4.2$, else $0$

**Winner Criteria**: Product $I^*$ with $\max(\text{Score}(I))$. Ties broken by higher star rating, then lower price.

---

## Phase 3: Project Structure & Data Schema

### 3.1 Directory Tree

```
MYNTRA_SOLUTION/
├── .streamlit/
│   └── config.toml           # Streamlit theme & layout configuration
├── assets/                   # Product image assets
│   ├── libas.jpg
│   ├── w.jpg
│   ├── biba.jpg
│   ├── aurelia.jpg
│   └── global_desi.jpg
├── app.py                    # Main Streamlit application entry point
├── architecture.md           # Phase-wise architecture & blueprint (This File)
├── mvp_requirement.md        # Feature & product requirements spec
├── README.md                 # Project documentation & setup guide
└── requirements.txt          # Python dependencies
```

### 3.2 Product Dataset Schema (5 Exact Items)

```python
PRODUCTS = [
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
        "fit_note": "True to size, roomy shoulders",
        "keywords": ["True to size", "Flowy fabric", "Great for functions", "Color true to photo"],
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
        "fit_note": "Slightly slim, size up",
        "keywords": ["Slim fit", "Good for petite", "Color slightly different", "Good daily wear"],
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
        "fit_note": "True to size, roomy",
        "keywords": ["Roomy", "Premium feel", "Best for festive", "Dupatta quality good"],
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
        "fit_note": "Slightly boxy",
        "keywords": ["Good daily wear", "Fades after wash", "Comfortable fabric", "Runs large"],
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
        "fit_note": "True to size, flattering",
        "keywords": ["Very flattering", "Great for dates", "Fabric is silky", "Ships fast"],
        "image_path": "assets/global_desi.jpg"
    }
]
```

---

## Phase 4: Step-by-Step Implementation & Local Execution

### 4.1 Dependency File (`requirements.txt`)
```text
streamlit>=1.31.0
Pillow>=10.0.0
```

### 4.2 Streamlit Configuration (`.streamlit/config.toml`)
```toml
[theme]
primaryColor = "#FF3F6C"
backgroundColor = "#1A1F36"
secondaryBackgroundColor = "#252B48"
textColor = "#FFFFFF"
font = "sans serif"

[server]
headless = true
enableCORS = false
```

### 4.3 Local Testing Workflow
1. **Initialize virtual environment**:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
2. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```
3. **Run Streamlit app locally**:
   ```powershell
   streamlit run app.py
   ```
4. **Local URL**: Application will spin up on `http://localhost:8501`.

---

## Phase 5: Verification & Quality Assurance Matrix

| Test ID | Area | Verification Step | Expected Outcome |
|---|---|---|---|
| **TC-01** | Item Selection | Click "Select" on Wishlist cards | Selection counter updates, card highlights. |
| **TC-02** | Selection Limit | Select 5th item | Toast alert: "Maximum 4 items can be compared." |
| **TC-03** | Context Form | Input Occasion = "Wedding Guest", Size = "M", Date = Event in 6 days | Context saved to `st.session_state`. |
| **TC-04** | Scoring Engine | Run Decision Panel for Libas vs Aurelia for Wedding Guest | Libas wins (+3 size, +2 occasion, +2 delivery, +1 rating = 8 pts vs 3 pts). |
| **TC-05** | UI Winner Highlight | Check column styling on Screen 3 | Winning column displays Pink Border + "BEST MATCH" badge. |
| **TC-06** | Recommendation Bar | Check Layer 5 recommendation string | Displays: "Based on your occasion and size, Libas Embroidered Anarkali Kurta is your best match." |
| **TC-07** | Add to Cart CTA | Click "Add to Cart" on Winner | Toast displays: "Added to cart!", button updates to `✓ Added`. |

---

## Phase 6: Git Workflow & Repository Management

### 6.1 Git Initialization & Pre-commit Check
Create `.gitignore` to exclude unneeded files:
```gitignore
__pycache__/
*.pyc
.venv/
.streamlit/secrets.toml
.DS_Store
```

### 6.2 Execution Commands
```powershell
# 1. Initialize Git Repository
git init

# 2. Add Remote Repository
git remote add origin https://github.com/karunadreams/myntra.git

# 3. Stage All Files
git add .

# 4. Commit MVP Codebase
git commit -m "feat: complete Myntra Wishlist Decision Panel 6-layer MVP"

# 5. Push to Main Branch
git branch -M main
git push -u origin main --force
```

---

## Phase 7: Deployment to Streamlit Community Cloud

### 7.1 Deployment Steps
1. Navigate to **[Streamlit Community Cloud](https://share.streamlit.io/)**.
2. Sign in with GitHub account (`karunadreams`).
3. Click **"New app"** -> **"Use existing repo"**.
4. Configure fields:
   - **Repository**: `karunadreams/myntra`
   - **Branch**: `main`
   - **Main file path**: `app.py`
   - **App URL**: `myntra-decision-panel.streamlit.app` (or default generated slug)
5. Click **"Deploy!"**.

### 7.2 Post-Deployment Acceptance Verification
- [x] App builds without missing module errors.
- [x] Product images render correctly from `assets/`.
- [x] 60-second end-to-end user flow operates smoothly without instructions.
- [x] Mobile responsiveness verified on phone screen sizes.
