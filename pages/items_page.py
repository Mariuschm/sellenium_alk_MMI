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

        # Zwracama listę linków
        elms = []
        el = self.driver.find_elements(*Locators.ITEMS)
        for i in range(len(el)):
            item_link = self.driver.find_element(By.XPATH, Locators.ITEM_LINK.format(i+1))
            item_name = self.driver.find_element(By.XPATH, Locators.ITEM_DESCRIPTION.format(i+1)).text
            item_code = self.driver.find_element(By.XPATH, Locators.ITEM_CODE.format(i+1)).text
            item_amount = self.driver.find_element(By.XPATH, Locators.ITEM_AMOUNT.format(i+1))
            elms.append((el[i], item_link, item_name,item_code, item_amount))

        return elms
