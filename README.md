# 🛍️ Myntra Wishlist Decision Panel — MVP

A high-impact, standalone Python + Streamlit web application that simulates a **Wishlist Comparison & Decision Tool** for Myntra's occasion-driven shoppers.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.34%2B-FF4B4B.svg)](https://streamlit.io/)
[![Deployment](https://img.shields.io/badge/Deploy-Streamlit%20Cloud-brightgreen.svg)](https://share.streamlit.io/)

---

## 🎯 What Problem Does This Solve?

Myntra has 60M+ monthly active users. Users save 3–5 similar items to their wishlist for specific events (weddings, festivals, office parties), but face severe **choice overload**:
- **44%** of users abandon purchases due to "too many similar options".
- **58%** open items one by one in separate tabs without side-by-side comparison memory.
- **39%** buy nothing despite strong purchasing intent.

This MVP builds the missing **Decision Panel** inside Myntra's wishlist workflow.

---

## ⚡ The 6 Core Layers

1. **Layer 1: Select to Compare** — Wishlist grid with 2–4 item interactive selection bounds.
2. **Layer 2: Side-by-Side Comparison Panel** — Synchronized matrix comparing price, rating, size match, occasion fit, and delivery deadlines.
3. **Layer 3: Fit Summary per Item** — Single-line aggregated fit verdict per product.
4. **Layer 4: Review Keyword Chips** — Sentiment pill tags derived from customer review data.
5. **Layer 5: One-Line Passive Recommendation Bar** — Automated verdict bar recommending the top-scoring product.
6. **Layer 6: Instant Add to Cart CTA** — Primary CTA on the winning product with instant toast feedback.

---

## 📂 Project Structure

```
MYNTRA_SOLUTION/
├── .streamlit/
│   └── config.toml           # Myntra Dark Navy theme styling tokens
├── assets/                   # High-res product images
│   ├── libas.jpg
│   ├── w.jpg
│   ├── biba.jpg
│   ├── aurelia.jpg
│   └── global_desi.jpg
├── app.py                    # Core Streamlit app & silent scoring engine
├── architecture.md           # End-to-end phase-wise architecture spec
├── mvp_requirement.md        # Product requirements document
├── README.md                 # Project documentation (This File)
├── requirements.txt          # Python dependencies
└── .gitignore                # Git environment exclusions
```

---

## 🚀 Quick Start (Local Setup)

### 1. Clone or Download Repository
```bash
git clone https://github.com/karunadreams/myntra.git
cd myntra
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Streamlit Application
```bash
python -m streamlit run app.py
```

Open your browser at `http://localhost:8501`.

---

## 🏆 Silent Winner Scoring Engine

$$\text{Score}(I) = S_{\text{size}}(I) + S_{\text{occasion}}(I) + S_{\text{delivery}}(I) + S_{\text{rating}}(I)$$

- **+3 pts**: User size available (`XS`, `S`, `M`, `L`, `XL`)
- **+2 pts**: Occasion tag match (`Wedding Guest`, `Festival`, `Office Party`, `Date Night`, `Casual`)
- **+2 pts**: Delivery on or before event date
- **+1 pt**: Rating $\ge 4.2$

**Tie-breaking**: Highest Score $\rightarrow$ Highest Rating $\rightarrow$ Lowest Price.

---

## 🌐 Deploy to Streamlit Community Cloud

1. Push repo to GitHub (`github.com/karunadreams/myntra`).
2. Log into [Streamlit Community Cloud](https://share.streamlit.io/).
3. Click **"New App"** $\rightarrow$ Select `karunadreams/myntra` $\rightarrow$ Main file path: `app.py`.
4. Click **"Deploy!"**.
