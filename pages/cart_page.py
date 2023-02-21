from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from pages.base_page import BasePage


class Locators:
    # Selektory
    CART_ITEMS = (By.XPATH, "//div[@class='trow']")
    CART_SELECTOR = (By.XPATH, "//trigger[@class='user-cart many-currencies']")
    CART_LIST = (By.XPATH, "//ul[@class='inner-carts-container']//li")
    CONFIRM_REMOVE = (By.XPATH, "//div[@class='modal-content mauto']//button[1]")
    # Stringi
    ITEM_CODE = "(//div[@class='product-desc'])[{0}]/span[@class='product-code']"
    ITEM_AMOUNT = "(//div[@class='tcell quantity-col with-stepper without-covering-link'])" \
                  "[{0}]//input[@type='tel']"
    CART_ID = "//li[contains(@class, 'cart-container')][{0}]//div[@class='cart-item']//span[@class='name-value']"
    CART_REMOVE = "//li[contains(@class, 'cart-container')][1]//div[@class='options']//button"


class CartPage(BasePage):

    def _verify_page(self):
        # Strona z pozycjami łąduje się dłużej, ustawiam waita na 15s
        self.wait = WebDriverWait(self.driver, 15)
        # Czekam na pojawianie się listy pozycji koszyka
        self.wait.until(EC.visibility_of_element_located(Locators.CART_ITEMS))

    def get_cart_items(self):
        """
            Funkcja zwraca listę krotek z pozycjami koszyka
        :return: Lista krotek
        """
        # Deklaruje listę która będzie zwracana przez funckcję
        elms = []
        # Ładuje listę pozycji koszyka (webelementów)
        el = self.driver.find_elements(*Locators.CART_ITEMS)
        for i in range(len(el)):
            # Kod produktu
            item_code = self.driver.find_element(By.XPATH, Locators.ITEM_CODE.format(i + 1)).text
            # Ilość produktu
            item_amount = self.driver.find_element(By.XPATH, Locators.ITEM_AMOUNT.format(i + 1)).get_attribute("value")
            elms.append((el[i], item_code, item_amount))
        return elms

    def remove_cart(self, cart_id):
        """
            Usuwa koszyk w wskazanym ID
        :param cart_id: Id koszyka do usunięca
        :return:
        """
        self.wait.until(EC.visibility_of_element_located(Locators.CART_SELECTOR))
        self.driver.find_element(*Locators.CART_SELECTOR).click()
        # Załaduj listę koszyków
        carts = []
        carts_we = self.driver.find_elements(*Locators.CART_LIST)
        for i in range(len(carts_we)):
            # Numer (nazwa) koszyka [int]
            cart_id_text = self.driver.find_element(By.XPATH, Locators.CART_ID.format(i + 1)).text
            # Przycisk usuwania koszyka [webelement]
            remove_button = self.driver.find_element(By.XPATH, Locators.CART_REMOVE.format(i + 1))
            carts.append((carts_we[i], cart_id_text, remove_button))
        # Wyszuka konkrenty przycis dla danego koszyka
        remove_cart_button = [c[2] for c in carts if c[1] == cart_id][0]
        if type(remove_cart_button) == WebElement:
            # Klikam usuń koszyk
            remove_cart_button.click()
            # Potwierdzam usunięcie koszyka
            self.driver.find_element(*Locators.CONFIRM_REMOVE).click()
