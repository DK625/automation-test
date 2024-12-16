import pytest
from page_objects.login_page import LoginPage
from page_objects.home_page import HomePage
from page_objects.cart_page import CartPage


@pytest.mark.usefixtures("driver")
class TestCart:
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Setup for each test case"""
        self.login_page = LoginPage(driver)
        self.home_page = HomePage(driver)
        self.cart_page = CartPage(driver)

    def test_add_product_to_cart(self, driver):
        # Login
        driver.get("http://localhost:3000/home")
        self.login_page.login("doanthuyduong2103@gmail.com", "Thanhthuy2103@")

        # Add products to cart
        initial_count = 0
        self.home_page.select_phones_tab()
        self.home_page.add_product_to_cart()

        updated_count = self.home_page.get_cart_count()
        assert updated_count == initial_count + 1

        # Verify cart contents
        self.home_page.open_cart()
        product_info = self.cart_page.get_product_info()
        assert product_info["name"] == "iPhone 15 Pro Max"
        self.home_page.close_cart()

        # Add another product
        self.home_page.add_product_to_cart(product_index=5)  # Samsung product
        final_count = self.home_page.get_cart_count()
        assert final_count == initial_count + 2

    def test_increase_quantity(self, driver):
        driver.get("http://localhost:3000/my-cart")

        initial_value = self.cart_page.get_quantity()
        self.cart_page.increase_quantity(10)
        self.cart_page.decrease_quantity(5)

        final_value = self.cart_page.get_quantity()
        assert final_value == initial_value + 5

    def test_product_info_display(self, driver):
        # Open cart and get product details
        self.home_page.open_cart()
        cart_product_info = self.cart_page.get_product_info()

        # Navigate to product page and get details
        self.cart_page.navigate_to_product_page()
        product_page_info = self.cart_page.get_product_info()

        # Verify information matches
        assert cart_product_info["name"] == product_page_info["name"], "Product name mismatch"
        assert cart_product_info["price"] == product_page_info["price"], "Price mismatch"
        assert cart_product_info["quantity"] == product_page_info["quantity"], "Quantity mismatch"

    def test_cart_total_calculation(self, driver):
        driver.get("http://localhost:3000/my-cart")

        # Select all products
        self.cart_page.select_all_products()

        # Get product details
        products = self.cart_page.get_all_products_info()

        # Calculate expected total
        expected_total = sum(
            product["price"] * product["quantity"]
            for product in products
        )

        # Get actual total from UI
        actual_total = self.cart_page.get_total_amount()

        # Verify total
        assert actual_total == expected_total, (
            f"Total mismatch. Expected: {expected_total:,} VND, "
            f"Got: {actual_total:,} VND"
        )

    def test_delete_product(self, driver):
        driver.get("http://localhost:3000/my-cart")

        # Get initial product count and first product name
        initial_products = self.cart_page.get_all_products_info()
        product_to_delete = initial_products[0]["name"]

        # Delete first product
        self.cart_page.delete_product(index=0)

        # Verify product was deleted
        remaining_products = self.cart_page.get_all_products_info()
        remaining_names = [product["name"] for product in remaining_products]

        assert len(remaining_products) == len(initial_products) - 1, (
            "Product count did not decrease after deletion"
        )
        assert product_to_delete not in remaining_names, (
            f"Product '{product_to_delete}' still exists after deletion"
        )

    @pytest.mark.parametrize("quantity", [1, 5, 10])
    def test_quantity_limits(self, driver, quantity):
        """Test various quantity scenarios"""
        driver.get("http://localhost:3000/my-cart")

        self.cart_page.set_quantity(quantity)
        actual_quantity = self.cart_page.get_quantity()

        assert actual_quantity == quantity, (
            f"Quantity not set correctly. Expected: {quantity}, "
            f"Got: {actual_quantity}"
        )

    def test_cart_persistence(self, driver):
        """Test if cart items persist after page reload"""
        # Get initial cart state
        initial_products = self.cart_page.get_all_products_info()

        # Reload page
        driver.refresh()

        # Get cart state after reload
        final_products = self.cart_page.get_all_products_info()

        # Verify cart contents remain the same
        assert len(initial_products) == len(final_products), (
            "Number of products changed after page reload"
        )

        for initial, final in zip(initial_products, final_products):
            assert initial["name"] == final["name"], "Product name changed"
            assert initial["price"] == final["price"], "Price changed"
            assert initial["quantity"] == final["quantity"], "Quantity changed"
