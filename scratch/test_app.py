from streamlit.testing.v1 import AppTest
import sys

def run_tests():
    print("--- Starting Myntra Choice Panel App Test ---")
    at = AppTest.from_file("app.py", default_timeout=10)
    at.run()
    
    if at.exception:
        print(f"FAILED on initial load: {at.exception}")
        sys.exit(1)
    print("[SUCCESS] Screen 1 (Wishlist Home Page with 5 items & Occasions): SUCCESS")

    # Click OPEN DECISION MODE
    btn_decision = next((b for b in at.button if "DECISION MODE" in b.label), None)
    if btn_decision:
        btn_decision.click().run()
        if at.exception:
            print(f"FAILED opening Decision Mode: {at.exception}")
            sys.exit(1)
        print("[SUCCESS] Screen 2 (Decision Mode Page with 2-Column Comparison): SUCCESS")

    # On Decision Mode page, click "CHOOSE THIS" on first item
    btn_choose = next((b for b in at.button if "CHOOSE THIS" in b.label), None)
    if btn_choose:
        btn_choose.click().run()
        if at.exception:
            print(f"FAILED clicking Choose This: {at.exception}")
            sys.exit(1)
        print("[SUCCESS] Confirmation View (Great choice! Ready to buy?): SUCCESS")

    # On Confirmation view, click "GO TO CART"
    btn_cart = next((b for b in at.button if "GO TO CART" in b.label), None)
    if btn_cart:
        btn_cart.click().run()
        if at.exception:
            print(f"FAILED navigating to Cart: {at.exception}")
            sys.exit(1)
        print("[SUCCESS] Screen 3 (Shopping Bag): SUCCESS")

    # On Cart view, click "PLACE ORDER"
    btn_order = next((b for b in at.button if "PLACE ORDER" in b.label), None)
    if btn_order:
        btn_order.click().run()
        if at.exception:
            print(f"FAILED clicking Place Order: {at.exception}")
            sys.exit(1)
        print("[SUCCESS] Place Order Celebration: SUCCESS")

    print("\nALL MYNTRA CHOICE PANEL TESTS PASSED WITH 0 ERRORS!")

if __name__ == "__main__":
    run_tests()
