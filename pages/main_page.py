from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from pages.items_page import ItemsPage


class Locators:
    # Nazwa firmy
    CUSTOMER_NAME = (By.XPATH, "//i[@class='ti-briefcase']/following-sibling::*")
    # Pracownik
    EMPLOYEE_NAME = (By.XPATH, "//i[@class='ti-lock']/following-sibling::*")
    # Wyglouj
    LOGOUT_BUTTON = (By.XPATH, "//i[@class='ti-power-off']")
    # Dropdown koszyk
    CART_DROPDOWN = ""
    # Lista kategorii
    CATEGORIES = (By.XPATH, "//li[@class='category-item inner-clear']")


class MainPage(BasePage):

    def _verify_page(self):
        # Zaczekaj na załadowanie wskazanych kontrolek
        super()._verify_page()
        try:
            self.wait.until(EC.visibility_of_element_located(Locators.CUSTOMER_NAME))
            self.wait.until(EC.visibility_of_element_located(Locators.EMPLOYEE_NAME))
            self.wait.until(EC.visibility_of_element_located(Locators.LOGOUT_BUTTON))
        except:
            pass

    def return_logged_customer(self):
        """
            Pobierz zalogowanego klienta
        :return: zwraca nazwę zalogowanego klienta
        """
        # Czekam aż zostanie wypełniona wartość akronimu klienta
        # W testach wartość pojawiała się po dłuższym czasie, obecność kontrolki jest sprawdzana
        # w metodzie veriry_page()
        el = self.driver.find_element(*Locators.CUSTOMER_NAME)
        return el.text

    def return_logged_employee(self):
        """
            Pobierz zalogowanego pracownika
        :return: zwraca nazwę zalogowanego pracownika
        """
        el = self.driver.find_element(*Locators.EMPLOYEE_NAME)
        return el.text

    def log_out(self):
        """
            Wyloguj z systemu
        :return:
        """
        el = self.driver.find_element(*Locators.LOGOUT_BUTTON)
        el.click()

    def get_categories(self):
        cats = self.driver.find_elements(*Locators.CATEGORIES)
        return cats

    def get_items_from_category(self, category):
        if type(category) == WebElement:
            category.click()
            return ItemsPage(self.driver)
        else:
            return self
