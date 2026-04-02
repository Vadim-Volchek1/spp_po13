# test_shopping.py
from unittest.mock import patch
import pytest
from shopping import Cart, apply_coupon  # COUPONS imported but unused


class TestApplyCoupon:

    @pytest.fixture
    def cart_with_items(self):
        """Fixture to create a cart with items"""
        cart = Cart()
        cart.add_item("Apple", 100)
        cart.add_item("Banana", 50)
        return cart

    # === Tests using monkeypatch ===

    def test_apply_coupon_save10_with_monkeypatch(self, cart_with_items, monkeypatch):
        """Test applying SAVE10 coupon with monkeypatch"""
        # Create test coupons dictionary
        test_coupons = {"SAVE10": 10, "HALF": 50, "TEST": 20}

        # Replace the COUPONS dictionary in shopping module
        monkeypatch.setattr("shopping.COUPONS", test_coupons)

        original_total = cart_with_items.get_total()
        apply_coupon(cart_with_items, "SAVE10")

        # Check that discount was applied
        expected_total = original_total * 0.9
        assert cart_with_items.get_total() == expected_total
        assert cart_with_items.discount == 10

    def test_apply_coupon_half_with_monkeypatch(self, cart_with_items, monkeypatch):
        """Test applying HALF coupon with monkeypatch"""
        test_coupons = {"SAVE10": 10, "HALF": 50}
        monkeypatch.setattr("shopping.COUPONS", test_coupons)

        original_total = cart_with_items.get_total()
        apply_coupon(cart_with_items, "HALF")

        # Check that 50% discount was applied
        expected_total = original_total * 0.5
        assert cart_with_items.get_total() == expected_total
        assert cart_with_items.discount == 50

    def test_apply_coupon_invalid_with_monkeypatch(self, cart_with_items, monkeypatch):
        """Test applying invalid coupon with monkeypatch"""
        test_coupons = {"SAVE10": 10, "HALF": 50}
        monkeypatch.setattr("shopping.COUPONS", test_coupons)

        with pytest.raises(ValueError, match="Invalid coupon"):
            apply_coupon(cart_with_items, "INVALID")

    # === Tests using patch.dict ===

    @patch.dict("shopping.COUPONS", {"SAVE10": 10, "HALF": 50})
    def test_apply_coupon_save10_with_patch_dict(self, cart_with_items):
        """Test applying SAVE10 coupon with patch.dict"""
        original_total = cart_with_items.get_total()
        apply_coupon(cart_with_items, "SAVE10")

        expected_total = original_total * 0.9
        assert cart_with_items.get_total() == expected_total
        assert cart_with_items.discount == 10

    @patch.dict("shopping.COUPONS", {"SAVE10": 10, "HALF": 50})
    def test_apply_coupon_half_with_patch_dict(self, cart_with_items):
        """Test applying HALF coupon with patch.dict"""
        original_total = cart_with_items.get_total()
        apply_coupon(cart_with_items, "HALF")

        expected_total = original_total * 0.5
        assert cart_with_items.get_total() == expected_total
        assert cart_with_items.discount == 50

    @patch.dict("shopping.COUPONS", {"SAVE10": 10, "HALF": 50})
    def test_apply_coupon_invalid_with_patch_dict(self, cart_with_items):
        """Test applying invalid coupon with patch.dict"""
        with pytest.raises(ValueError, match="Invalid coupon"):
            apply_coupon(cart_with_items, "INVALID")

    # === Additional tests for edge cases ===

    @patch.dict("shopping.COUPONS", {"SAVE10": 10, "HALF": 50})
    def test_apply_coupon_multiple_times(self, cart_with_items):
        """Test applying multiple coupons"""
        apply_coupon(cart_with_items, "SAVE10")
        first_total = cart_with_items.get_total()

        # Apply discount to already discounted amount
        apply_coupon(cart_with_items, "HALF")
        expected_total = first_total * 0.5

        assert cart_with_items.get_total() == expected_total
        # Last discount overwrites the previous one
        assert cart_with_items.discount == 50

    @patch.dict("shopping.COUPONS", {"SAVE10": 10, "HALF": 50, "EMPTY": 0})
    def test_apply_coupon_zero_discount(self, cart_with_items):
        """Test coupon with zero discount"""
        original_total = cart_with_items.get_total()
        apply_coupon(cart_with_items, "EMPTY")

        assert cart_with_items.get_total() == original_total
        assert cart_with_items.discount == 0

    @patch.dict("shopping.COUPONS", {"SAVE10": 10, "HALF": 50})
    def test_apply_coupon_empty_cart(self):
        """Test applying coupon to empty cart"""
        empty_cart = Cart()
        original_total = empty_cart.get_total()

        apply_coupon(empty_cart, "SAVE10")

        assert empty_cart.get_total() == original_total
        assert empty_cart.discount == 10

    def test_with_real_coupons(self, cart_with_items):
        """Test with real coupons dictionary (no mocking)"""
        original_total = cart_with_items.get_total()

        # This uses the actual COUPONS dictionary
        apply_coupon(cart_with_items, "SAVE10")

        expected_total = original_total * 0.9
        assert cart_with_items.get_total() == expected_total
        assert cart_with_items.discount == 10


# === Parameterized tests ===


class TestApplyCouponParameterized:

    @pytest.fixture
    def cart_with_items(self):
        cart = Cart()
        cart.add_item("Apple", 100)
        cart.add_item("Banana", 50)
        return cart

    @patch.dict("shopping.COUPONS", {"SAVE10": 10, "HALF": 50})
    @pytest.mark.parametrize(
        "coupon_code,expected_discount,expected_multiplier",
        [
            ("SAVE10", 10, 0.9),
            ("HALF", 50, 0.5),
        ],
    )
    def test_apply_coupon_parameterized(
        self, cart_with_items, coupon_code, expected_discount, expected_multiplier
    ):
        """Parameterized test for different coupons"""
        original_total = cart_with_items.get_total()
        apply_coupon(cart_with_items, coupon_code)

        expected_total = original_total * expected_multiplier
        assert cart_with_items.get_total() == expected_total
        assert cart_with_items.discount == expected_discount

    @patch.dict("shopping.COUPONS", {"SAVE10": 10, "HALF": 50})
    @pytest.mark.parametrize("invalid_coupon", ["INVALID", "DISCOUNT20", "", None])
    def test_apply_invalid_coupons(self, cart_with_items, invalid_coupon):
        """Parameterized test for invalid coupons"""
        with pytest.raises(ValueError, match="Invalid coupon"):
            apply_coupon(cart_with_items, invalid_coupon)


# === Tests for monkeypatch with custom coupon values ===


class TestCustomCoupons:

    @pytest.fixture
    def cart_with_items(self):
        cart = Cart()
        cart.add_item("Laptop", 1000)
        cart.add_item("Mouse", 50)
        return cart

    def test_custom_coupon_with_monkeypatch(self, cart_with_items, monkeypatch):
        """Test custom coupon values with monkeypatch"""
        custom_coupons = {"SAVE20": 20, "SAVE30": 30, "SUPER_SAVE": 80}

        monkeypatch.setattr("shopping.COUPONS", custom_coupons)

        original_total = cart_with_items.get_total()
        apply_coupon(cart_with_items, "SAVE30")

        expected_total = original_total * 0.7
        assert cart_with_items.get_total() == expected_total
        assert cart_with_items.discount == 30

    @patch.dict("shopping.COUPONS", {"BLACK_FRIDAY": 70, "CYBER_MONDAY": 40})
    def test_seasonal_coupons_with_patch_dict(self, cart_with_items):
        """Test seasonal coupons with patch.dict"""
        original_total = cart_with_items.get_total()
        apply_coupon(cart_with_items, "BLACK_FRIDAY")

        expected_total = original_total * 0.3
        assert cart_with_items.get_total() == expected_total
        assert cart_with_items.discount == 70


# === Simple test without mocking ===


def test_simple_coupon_application():
    """Simple test with real coupons"""
    cart = Cart()
    cart.add_item("Test", 200)

    apply_coupon(cart, "SAVE10")
    assert cart.get_total() == 180
    assert cart.discount == 10

    # Test HALF coupon
    cart2 = Cart()
    cart2.add_item("Test", 200)
    apply_coupon(cart2, "HALF")
    assert cart2.get_total() == 100
    assert cart2.discount == 50


# Point d'entrée pour exécuter les tests
if __name__ == "__main__":
    import sys

    print("\n" + "=" * 50)
    print("Running tests...")
    print("=" * 50 + "\n")

    # Run pytest with current file
    exit_code = pytest.main([__file__, "-v", "-s", "--tb=short"])

    print("\n" + "=" * 50)
    if exit_code == 0:
        print("All tests passed!")
    else:
        print(f"Tests completed with exit code: {exit_code}")
    print("=" * 50)

    # Pause to view results
    input("\nPress Enter to exit...")

    sys.exit(exit_code)
