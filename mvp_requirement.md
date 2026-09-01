# Myntra Wishlist Decision Panel — MVP Requirements

## What Problem Are We Solving

Myntra has 60M+ monthly users. Users save 3–5 similar items to their wishlist for a specific occasion (wedding, festival, office party). But Myntra has no comparison tool inside the wishlist.

- 44% of users say "too many similar options" is their #1 reason for not buying
- 58% open items one by one and go back and forth — no memory, no comparison
- 28% already screenshot items and compare in their phone gallery outside the app
- 39% end up buying nothing despite genuine intent
- 89% have missed a purchase window because they couldn't decide in time

The user saves items to compare later. But Myntra never built the comparison tool. This MVP builds it.

---

## Who Is This For

**Occasion-Driven Shoppers** — women aged 22–32 who save 3–5 kurtas/dresses for a specific event and have a real deadline (the event date). They are not blocked by price. They are blocked by inability to decide between similar-looking items.

---

## What to Build

A standalone web app that simulates a Myntra wishlist comparison feature. 3 screens. 6 layers inside the core screen.

---

## The 6 Layers of the MVP (most important section — build around this)

Solution 2 is called the Decision Panel. It has exactly 6 layers. Every layer solves a specific part of the problem.

---

### Layer 1 — Select to Compare

**What the user does:** Sees their saved wishlist items. Selects 2 to 4 items. Taps "Compare."

**Why this layer exists:** 58% of users currently open items one by one and go back — they have no native way to select and compare side by side. This layer gives them that selection mechanism.

**What to show:**
- 5 mock wishlist items displayed as cards (image, brand, name, price, rating, occasion tags)
- Each card has a "Select" button
- Once 2+ items selected, "Compare Selected" button activates at the bottom
- Maximum 4 items can be selected — show a warning if user tries to select 5th

---

### Layer 2 — Side-by-Side Comparison Panel

**What the user sees:** Selected items appear as columns. Attributes appear as rows. Everything visible at once — no back and forth.

**Why this layer exists:** This is the core gap. Myntra has no compare tool. Users have to hold item details in memory while switching tabs. This panel removes that entirely.

**What to show per item column:**
- Item image (thumbnail), brand, name at the top of each column
- Row: Price — show discounted price + original price struck through + discount % badge
- Row: Rating — star rating + number of ratings
- Row: Size availability — ✅ Available in [user's size] OR ❌ Not available in [user's size] — green and red indicators
- Row: Occasion match — ✅ Great for [occasion] OR ⚠️ Not ideal for [occasion]
- Row: Delivery — exact delivery date + days remaining
- Row: Delivery vs event — 🟢 Arrives before your event OR 🔴 Arrives after your event

**Winner logic (silent scoring — user never sees the numbers):**
- +3 points if item is available in user's size
- +2 points if occasion tag matches user's selected occasion
- +2 points if delivery arrives before the event date
- +1 point if rating is 4.2 or above
- Highest total = winner. Winner column gets a pink border + "Best Match" badge at the top.

---

### Layer 3 — Fit Summary per Item

**What the user sees:** Below the comparison rows, each item column shows a one-line fit note.

**Why this layer exists:** 92% of users read reviews hoping to understand fit — but reviews are long and unfiltered. They need a quick, scannable fit verdict per item, not 200 reviews to read.

**What to show:**
- One line per item: pulled from the item's fit note field
- Examples: "Runs slightly small — size up if between sizes" / "True to size, roomy fit, works for all body types" / "Slightly boxy cut, best for layering"
- Label it clearly: "Fit Note" as a row header in the comparison table

---

### Layer 4 — Review Keywords as Chips

**What the user sees:** Below the fit note, each item shows 3–4 small keyword chips pulled from real review language.

**Why this layer exists:** Users trust reviews but can't read all of them. Surfacing the most repeated keywords gives them the signal without the scroll. This is what "Runs small · True to size · Good for petite" looks like in practice.

**What to show:**
- 3 to 4 chips per item
- Chip examples: "True to size" / "Roomy" / "Good for petite" / "Flowy fabric" / "Fades after wash" / "Color true to photo" / "Ships fast"
- Each item has its own distinct set of keywords based on the mock data
- Display as small rounded pill tags, not a list

---

### Layer 5 — One-Line Passive Recommendation

**What the user sees:** A full-width bar at the bottom of the comparison panel with one sentence.

**Why this layer exists:** Users want permission to decide — not a chatbot, not a quiz, not typing anything. One passive line that says "this one" removes the final moment of hesitation. Isha (INT-02) converted only after a friend said "just buy it." This is that friend — built into the product.

**What to show:**
- "Based on your occasion and size, [Brand] [Item Name] is your best match."
- Sub-line: "It is available in your size, arrives before your event, and is well-rated for [occasion]."
- Auto-generated from the scoring logic — no user input needed at this step
- Dark navy background, white text, item name in Myntra pink

---

### Layer 6 — Add to Cart Directly from Comparison Screen

**What the user sees:** A clear CTA on the winning item. Not on all items — only on the best match.

**Why this layer exists:** The comparison screen is the moment of highest confidence in the entire journey. If the user has to navigate away to buy, that confidence drops. The cart button must be right here, right now.

**What to show:**
- On the winner column: "Add to Cart" button — solid Myntra pink, full width of the column
- On all other columns: "Save for Later" button — outlined, grey, secondary
- On clicking "Add to Cart": show a success toast — "Added to cart! ✓ Complete your purchase on Myntra."
- Button changes to "✓ Added" state after click (no real cart — simulate the interaction)

---

## Screen Flow Summary

**Screen 1 — Wishlist (Layer 1)**
User sees 5 saved items. Selects 2–4. Taps Compare.

**Screen 2 — Context Setup**
User picks occasion, event date, and their size. Taps Show Comparison.
(This is needed so Layers 2, 3, 5 can be personalised — size availability, occasion match, delivery vs event date all depend on these inputs.)

**Screen 3 — Decision Panel (Layers 2 + 3 + 4 + 5 + 6)**
All layers live here. Side-by-side columns. Fit note. Review chips. Recommendation bar. Add to Cart.

---

## Mock Product Data (use these 5 items exactly)

| # | Name | Brand | Price | Original | Rating | Sizes | Occasions | Delivery | Fit Note |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Embroidered Anarkali Kurta | Libas | ₹1,299 | ₹2,499 | 4.3 | S M L XL | Wedding Guest, Festival | 4 days | True to size, roomy shoulders |
| 2 | Floral Printed Straight Kurta | W | ₹999 | ₹1,799 | 4.1 | XS S M | Office Party, Casual | 3 days | Slightly slim, size up |
| 3 | Woven Design Kurta Set | Biba | ₹1,799 | ₹3,199 | 4.5 | S M L | Wedding Guest, Festival, Date Night | 5 days | True to size, roomy |
| 4 | Solid Straight Kurta | Aurelia | ₹849 | ₹1,499 | 3.9 | M L XL | Office Party, Casual | 2 days | Slightly boxy |
| 5 | Printed Wrap Kurta | Global Desi | ₹1,499 | ₹2,799 | 4.4 | XS S M L | Date Night, Casual, Festival | 3 days | True to size, flattering |

Review keywords per item:
- Libas: "True to size" · "Flowy fabric" · "Great for functions" · "Color true to photo"
- W: "Slim fit" · "Good for petite" · "Color slightly different" · "Good daily wear"
- Biba: "Roomy" · "Premium feel" · "Best for festive" · "Dupatta quality good"
- Aurelia: "Good daily wear" · "Fades after wash" · "Comfortable fabric" · "Runs large"
- Global Desi: "Very flattering" · "Great for dates" · "Fabric is silky" · "Ships fast"

---

## Design

- Background: dark navy #1A1F36
- Primary CTA: Myntra pink #FF3F6C
- Accent: Myntra orange #FF905A
- White card surfaces
- Mobile-friendly layout

---

## Deployment

- Stack: Python + Streamlit
- Deploy to: Streamlit Community Cloud
- Repo: github.com/karunadreams/myntra
- No API keys or external calls needed
- Final output: A public URL that anyone can open and test without login

---

## What NOT to Build

- No real Myntra API
- No user login or database
- No AI or Claude API calls — scoring is pure Python logic
- No real payment or cart
- No body profile or fit algorithm
- No occasion reminders or notifications

---

## Done When

A person can open the URL, select 2–3 items, set occasion + date + size, see all 6 layers working in the comparison panel, and click Add to Cart — within 60 seconds, no instructions needed.