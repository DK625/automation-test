from selenium.webdriver.common.by import By


class LoginPageLocators:
    EMAIL_INPUT = (By.CSS_SELECTOR, "input.MuiInputBase-input[type='text']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input.MuiInputBase-input[type='password']")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button.MuiButton-contained[type='submit']")


class HomePageLocators:
    CART_ICON = (By.CSS_SELECTOR, ".iconify--flowbite")
    BACKDROP = (By.CSS_SELECTOR, ".MuiBackdrop-root")
    PHONE_TAB = (By.CSS_SELECTOR, ".MuiButtonBase-root:nth-child(4)")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, ".MuiGrid-root:nth-child(4) .MuiButtonBase-root:nth-child(1)")
    CART_BADGE = (By.CSS_SELECTOR, ".MuiBadge-badge")


class CartPageLocators:
    QUANTITY_INPUT = (By.CSS_SELECTOR, "input[type='number'].MuiInputBase-input")
    INCREASE_BUTTON = (By.CSS_SELECTOR, ".css-1nwk2ar > button:last-child")
    DECREASE_BUTTON = (By.CSS_SELECTOR, ".css-1nwk2ar > button:first-of-type")
    PRODUCT_NAME = (By.CSS_SELECTOR, "p.MuiTypography-root.MuiTypography-body1 > a")
    DELETE_BUTTON = (By.CSS_SELECTOR, ".MuiBox-root.css-1gca1vy .MuiButtonBase-root")
    TOTAL_AMOUNT = (By.CSS_SELECTOR, ".MuiTypography-root.MuiTypography-body1.css-c78xqc-MuiTypography-root")
