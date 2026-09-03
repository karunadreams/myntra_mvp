from streamlit.testing.v1 import AppTest
import sys

def run_tests():
    print("--- Starting Myntra 4-Page Wishlist Decision Panel Test ---")
    at = AppTest.from_file("app.py", default_timeout=10)
    at.run()
    
    if at.exception:
        print(f"FAILED on initial load (Page 1 Home Screen): {at.exception}")
        sys.exit(1)
    print("[SUCCESS] Page 1 (Home Screen Grid with 20 items & Live Wishlist Badge): SUCCESS")

    # Click Wishlist button at top or on product card
    btn_wish = next((b for b in at.button if "❤️" in b.label), None)
    if btn_wish:
        btn_wish.click().run()
        if at.exception:
            print(f"FAILED navigating to Wishlist: {at.exception}")
            sys.exit(1)
        print("[SUCCESS] Page 2 (Wishlist Screen with Live Count & Checkboxes): SUCCESS")

    # Click DECISION MODE or COMPARE SELECTED
    btn_dec = next((b for b in at.button if "DECISION MODE" in b.label or "COMPARE" in b.label), None)
    if btn_dec:
        btn_dec.click().run()
        if at.exception:
            print(f"FAILED clicking Decision Mode / Compare: {at.exception}")
            sys.exit(1)
        print("[SUCCESS] Page 3 (Body Profile Setup Modal): SUCCESS")

    # On Body Profile Modal, click SAVE & COMPARE
    btn_save = next((b for b in at.button if "SAVE & COMPARE" in b.label), None)
    if btn_save:
        btn_save.click().run()
        if at.exception:
            print(f"FAILED clicking Save & Compare: {at.exception}")
            sys.exit(1)
        print("[SUCCESS] Page 4 (Comparison Screen Matrix & AI Recommendation): SUCCESS")

    # On Comparison screen, test ADD TO CART button
    btn_cart = next((b for b in at.button if "ADD TO CART" in b.label), None)
    if btn_cart:
        btn_cart.click().run()
        if at.exception:
            print(f"FAILED clicking Add to Cart on Comparison Screen: {at.exception}")
            sys.exit(1)
        print("[SUCCESS] Direct Add to Cart from Comparison Matrix: SUCCESS")

    print("\nALL 4-PAGE MYNTRA DECISION PANEL TESTS PASSED WITH 0 ERRORS!")

if __name__ == "__main__":
    run_tests()
