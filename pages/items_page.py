from selenium.webdriver import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from pages.base_page import BasePage


class Locators:
    # Lista towarów
    ITEMS_VIEW = (By.XPATH, "//ul[@class='pure']")
    # Lista pozzycji jako LI
    ITEMS = (By.XPATH, "//li[contains(@class, 'list-item')]")
    # Link do szczegółów pozycji
    ITEM_LINK = "//li[contains(@class, 'list-item')][{0}]" \
                "/a[@class='covering-link']"
    # Opis pozycji
    ITEM_DESCRIPTION = "//li[contains(@class, 'list-item')][{0}]" \
                       "/div[@class='item-info name']" \
                       "/p[@class='emphasised product-name']"
    # Kod pozycji
    ITEM_CODE = "//li[contains(@class, 'list-item')][{0}]" \
                "/div[@class='item-info name']" \
                "/p[@class='product-code']"
    # Pole ilości
    # min 0 max 999999.9999
    # Przetestować warunki brzegowe
    # Dane testowe
    ITEM_AMOUNT = "//li[contains(@class, 'list-item')][{0}]" \
                  "/div[@class='item-info add-column flex flex-wrap']" \
                  "/div[@class='amount-section']" \
                  "/app-stepper" \
                  "/div[@role='group']" \
                  "/input"


class ItemsPage(BasePage):

    def _verify_page(self):
        # Strona z pozycjami łąduje się dłużej, ustawiam waita na 30s
        self.wait = WebDriverWait(self.driver, 30)
        try:
            # Czekam na pojawianie się listy produktów
            self.wait.until(EC.visibility_of_element_located(Locators.ITEMS_VIEW))
        except:
            return False

    def get_items_list(self):
        """
            Funkcja zwraca listę pozycji asortmenetowych.
            Ładowane są kontrolki
                1. Link do szczegółów (webelement)
                2. Nazwa (string)
                3. Kod (string)
                4. Ilość (webelement)
        :return: Lista krotek z webelemetami
        """
        # Deklaruje listę która będzie zwracana przez funckcję
        elms = []
        # Ładuje listę pozycji (webelementów)
        el = self.driver.find_elements(*Locators.ITEMS)
        # Przewijam na dół strony, żeby załadowały się wszystkie pozycje
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        for i in range(len(el)):
            # Dodaję wait na każdy element w trakcie testów nie zdążyły się załadować wszystkie
            # pozycje z listy (wolne łącze)
            self.wait.until(EC.visibility_of_element_located((By.XPATH, Locators.ITEM_LINK.format(i + 1))))
            item_link = self.driver.find_element(By.XPATH, Locators.ITEM_LINK.format(i + 1))
            self.wait.until(EC.visibility_of_element_located((By.XPATH, Locators.ITEM_DESCRIPTION.format(i + 1))))
            item_name = self.driver.find_element(By.XPATH, Locators.ITEM_DESCRIPTION.format(i + 1)).text
            self.wait.until(EC.visibility_of_element_located((By.XPATH, Locators.ITEM_CODE.format(i + 1))))
            item_code = self.driver.find_element(By.XPATH, Locators.ITEM_CODE.format(i + 1)).text
            self.wait.until(EC.visibility_of_element_located((By.XPATH, Locators.ITEM_AMOUNT.format(i + 1))))
            item_amount = self.driver.find_element(By.XPATH, Locators.ITEM_AMOUNT.format(i + 1))
            elms.append((el[i], item_link, item_name, item_code, item_amount))

        return elms

    def set_amount(self, amount_input, amount):
        """
            Ustawia pole ilość przekazaną wartości
        :param amount_input: pole input do wpisania danych
        :param amount: wartość do wpisania
        :return: funkcja nie zwraca obiektu
        """
        amount_input.send_keys(amount)

    def get_amount(self, amount_input):
        """
            Funckja zwraca wartość ze wskaznaego elementu
        :param amount_input: pole input do odczytania
        :return: wartość elementu
        """
        # Z webelementów typy input wartość odczytuje się z atrybutu
        # Nie można użyć text
        return amount_input.get_attribute("value")
