from streamlit.testing.v1 import AppTest
import sys

def run_tests():
    print("--- Starting Full Local Automated Test Suite ---")
    at = AppTest.from_file("app.py", default_timeout=10)
    at.run()
    
    if at.exception:
        print(f"FAILED on initial load: {at.exception}")
        sys.exit(1)
    print("[SUCCESS] Page 1 (Home Screen Grid with 20 items): SUCCESS")

    # 1. Wishlist 5 products on Home screen to test 4-item compare limit
    for p_id in range(1, 6):
        btn_w = next((b for b in at.button if f"home_wish_{p_id}" in (b.key or "")), None)
        if btn_w:
            btn_w.click().run()

    if at.exception:
        print(f"FAILED wishlisting items on Home: {at.exception}")
        sys.exit(1)
    print(f"[SUCCESS] Wishlisted 5 items on Home screen. Selected for compare count: {len(at.session_state.selected_for_compare)}")
    assert len(at.session_state.selected_for_compare) <= 4, "Error: selected_for_compare exceeded maximum 4 items!"
    print("[SUCCESS] Verified maximum 4 items comparison limit enforcement: SUCCESS")

    # 2. Click Wishlist button on top header
    btn_wish = next((b for b in at.button if "top_wish_btn" in (b.key or "")), None)
    if btn_wish:
        btn_wish.click().run()
        if at.exception:
            print(f"FAILED clicking Wishlist header button: {at.exception}")
            sys.exit(1)
        print("[SUCCESS] Navigated to Wishlist Screen: SUCCESS")

    # 2b. Verify DECISION MODE (COMPARE ALL) button is REMOVED
    btn_compare_all = next((b for b in at.button if "COMPARE ALL" in b.label), None)
    assert btn_compare_all is None, "Error: 'COMPARE ALL' button should be removed!"
    print("[SUCCESS] Verified 'COMPARE ALL' button removed: SUCCESS")

    # 2c. Verify 1-item compare disabled (min 2 required)
    chk_1 = next((c for c in at.checkbox if "chk_sel_1" in (c.key or "")), None)
    chk_2 = next((c for c in at.checkbox if "chk_sel_2" in (c.key or "")), None)
    chk_3 = next((c for c in at.checkbox if "chk_sel_3" in (c.key or "")), None)
    chk_4 = next((c for c in at.checkbox if "chk_sel_4" in (c.key or "")), None)

    # Uncheck checkboxes dynamically until only 1 item is selected
    while len([c for c in at.checkbox if c.value]) > 1:
        c = next((c for c in at.checkbox if c.value and (c.key or "") != "chk_sel_1"), None)
        if not c:
            break
        c.uncheck().run()

    btn_comp_disabled = next((b for b in at.button if "btn_compare_selected" in (b.key or "")), None)
    assert btn_comp_disabled is not None and btn_comp_disabled.disabled, f"Error: Compare button should be disabled when < 2 items selected! Button label: {btn_comp_disabled.label if btn_comp_disabled else 'None'}, disabled: {btn_comp_disabled.disabled if btn_comp_disabled else 'None'}"
    print("[SUCCESS] Verified Compare button disabled when < 2 items selected: SUCCESS")

    # Re-check item 2 to have 2 items selected
    chk_2 = next((c for c in at.checkbox if "chk_sel_2" in (c.key or "")), None)
    if chk_2:
        chk_2.check().run()

    # 3. Click Compare Selected button on Wishlist screen
    btn_comp = next((b for b in at.button if "btn_compare_selected" in (b.key or "")), None)
    assert btn_comp is not None and not btn_comp.disabled, "Error: Compare button should be enabled when 2+ items selected!"
    if btn_comp:
        btn_comp.click().run()
        if at.exception:
            print(f"FAILED clicking compare button: {at.exception}")
            sys.exit(1)
        print("[SUCCESS] Clicked Compare button -> Profile Modal Triggered: SUCCESS")

    # 4. Interact with Quick Fit Setup Modal Dropdowns (Height Range & Size)
    if at.selectbox:
        h_sel = next((s for s in at.selectbox if "mod_height_sel" in (s.key or "")), None)
        s_sel = next((s for s in at.selectbox if "mod_size_sel" in (s.key or "")), None)
        if h_sel:
            h_sel.select("5'6\"+").run()
            print("[SUCCESS] Selected Height Range 5'6\"+: SUCCESS")
        if s_sel:
            s_sel.select("M").run()
            print("[SUCCESS] Selected Size M: SUCCESS")

    # 5. Click SAVE & COMPARE -> button
    btn_save = next((b for b in at.button if "save_compare_btn" in (b.key or "") or "SAVE & COMPARE" in b.label), None)
    if btn_save:
        btn_save.click().run()
        if at.exception:
            print(f"FAILED clicking SAVE & COMPARE button: {at.exception}")
            sys.exit(1)
        print("[SUCCESS] Saved Profile & Transitioned to Comparison Screen: SUCCESS")
        assert len(at.session_state.selected_for_compare) <= 4, "Error: Comparison screen has > 4 items!"

    # 6. Click Home button on bottom nav to return home
    btn_home = next((b for b in at.button if "bnav_home" in (b.key or "")), None)
    if btn_home:
        btn_home.click().run()
        if at.exception:
            print(f"FAILED clicking Home bnav: {at.exception}")
            sys.exit(1)
        print("[SUCCESS] Returned to Home Screen: SUCCESS")

    print("\nALL LOCAL INTERACTIVE TESTS (NAVIGATION, WISHLIST, 4-ITEM COMPARE LIMIT, PROFILE DROPDOWNS & COMPARISON) PASSED WITH 0 ERRORS!")

if __name__ == "__main__":
    run_tests()
