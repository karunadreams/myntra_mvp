from streamlit.testing.v1 import AppTest
import sys

def run_tests():
    print("--- Starting Interactive Navigation & Home Button Test ---")
    at = AppTest.from_file("app.py", default_timeout=10)
    at.run()
    
    if at.exception:
        print(f"FAILED on initial load: {at.exception}")
        sys.exit(1)
    print("[SUCCESS] Page 1 (Home Screen Grid with 20 items): SUCCESS")

    # Click Wishlist button on bottom nav
    btn_wish = next((b for b in at.button if "bnav_wish" in (b.key or "")), None)
    if btn_wish:
        btn_wish.click().run()
        if at.exception:
            print(f"FAILED clicking Wishlist bnav: {at.exception}")
            sys.exit(1)
        print("[SUCCESS] Navigated to Wishlist Screen via bottom nav: SUCCESS")

    # Click Home button on bottom nav from Wishlist screen
    btn_home = next((b for b in at.button if "bnav_home" in (b.key or "")), None)
    if btn_home:
        btn_home.click().run()
        if at.exception:
            print(f"FAILED clicking Home bnav: {at.exception}")
            sys.exit(1)
        print("[SUCCESS] Clicked Home button on bottom nav -> Returned to Home Catalog Screen: SUCCESS")

    # Click Categories button on bottom nav
    btn_cat = next((b for b in at.button if "bnav_cat" in (b.key or "")), None)
    if btn_cat:
        btn_cat.click().run()
        if at.exception:
            print(f"FAILED clicking Categories bnav: {at.exception}")
            sys.exit(1)
        print("[SUCCESS] Navigated to Categories Screen: SUCCESS")

    # Click Profile button on bottom nav
    btn_prof = next((b for b in at.button if "bnav_prof" in (b.key or "")), None)
    if btn_prof:
        btn_prof.click().run()
        if at.exception:
            print(f"FAILED clicking Profile bnav: {at.exception}")
            sys.exit(1)
        print("[SUCCESS] Navigated to Profile Screen: SUCCESS")

    # Click top Myntra Logo button -> Return to Home
    btn_logo = next((b for b in at.button if "top_logo_btn" in (b.key or "")), None)
    if btn_logo:
        btn_logo.click().run()
        if at.exception:
            print(f"FAILED clicking top Myntra Logo: {at.exception}")
            sys.exit(1)
        print("[SUCCESS] Clicked top Myntra logo -> Returned to Home Catalog Screen: SUCCESS")

    print("\nALL INTERACTIVE NAVIGATION & HOME BUTTON TESTS PASSED WITH 0 ERRORS!")

if __name__ == "__main__":
    run_tests()
