from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.main_page import BasePage
from pages.main_page import MainPage


class Locators:
    """
    Lokatory na stronie logowania
    """
    # Pole firma na oknie logowania
    CUSTOMER_INPUT = (By.ID, "customerName-field")
    # Pole pracownik na oknie logowania
    EMPLOYEE_INPUT = (By.ID, "userName-field")
    # Pole hasło na oknie logowania
    PASSWORD_INPUT = (By.XPATH, "//input[@type='password']")
    # Label zapamiętaj mnie (nie działa obsługa inputa)
    REMEMBER_ME = (By.XPATH, "//app-checkbox[@name='rememberMe']")
    # Checkbox zapoznałem się z regulaminem
    TERMS_CONFIRMATION = (By.XPATH, "//span[@class='vmiddle']")
    # Przycisk zaloguj
    LOGIN_BUTTON = (By.XPATH, "//button[@class='action primary-action']")
    # Ostrzeżenie o błędnym haśle/loginie
    ERROR_MESSAGE_LOGIN = (By.XPATH, "//div[@class='danger text-center']")
    # Ostrzeżenie o braku akceptacji regulaminu
    TERMS_NOT_ACCEPTED_MESSAGE = (By.XPATH, "//small[@class='validation-error danger']")


class LoginPage(BasePage):

    def _verify_page(self):
        """
            Weryfikacja załadowania okna logowowania
            Po uruchomieniu powinny załadować się wszystkie wymagane kontrolki
            CUSTOMER_INPUT
            EMPLOYEE_INPUT
            PASSWORD_INPUT
            REMEMBER_ME
            TERMS_CONFIRMATION
         """
        super()._verify_page()
        try:

            self.wait.until(EC.visibility_of_element_located(Locators.CUSTOMER_INPUT))
            self.wait.until(EC.visibility_of_element_located(Locators.EMPLOYEE_INPUT))
            self.wait.until(EC.visibility_of_element_located(Locators.PASSWORD_INPUT))
            self.wait.until(EC.visibility_of_element_located(Locators.REMEMBER_ME))
            self.wait.until(EC.visibility_of_element_located(Locators.TERMS_CONFIRMATION))
        except:
            raise RuntimeError("Nie udało się załadować kontrolek!")

    def enter_customer_name(self, customer_name):
        """
            Uzupełnia pole Firma
        :param customer_name: krótka nazwa firmy lub NIP
        :return:
        """
        el = self.driver.find_element(*Locators.CUSTOMER_INPUT)
        el.send_keys(customer_name)

    def enter_employee_name(self, employee_name):
        """
            Uzupełnia pole pracownik
            UWAGA!
            Pracownik musi być przypisany do firmy po stronie ERP
        :param employee_name: krótka nazwa firmy lub NIP
        :return:
        """
        el = self.driver.find_element(*Locators.EMPLOYEE_INPUT)
        el.send_keys(employee_name)

    def enter_password(self, password):
        """
            Uzupełnia pole hasło
        :param enter_password: hasło pracownika
        :return:
        """
        el = self.driver.find_element(*Locators.PASSWORD_INPUT)
        el.send_keys(password)

    def check_confirm_rules(self):
        el = self.driver.find_element(*Locators.TERMS_CONFIRMATION)
        el.click()

    def check_remember_me(self):
        """
            Zaznacza check zapamiętaj mnie. Kliknięcie na lable
            (opcjonalny)
        :return:
        """
        el = self.driver.find_element(*Locators.REMEMBER_ME)
        el.click()

    def click_login(self):
        """
            Klika przycsik zaloguj i próbuje zalogować z podanymi danymi
        :return: MainPage lub string: "Nie udało się załadować strony"
        """
        el = self.driver.find_element(*Locators.LOGIN_BUTTON)
        el.click()
        try:
            mp = MainPage(self.driver)
        except:
            mp = "Nie udało się załadować strony"
        return mp

    def get_login_error_message(self):
        """
            Odszukuje komunikat o błędzie logowania i pobiera jego treść.
            Jeżeli brak komunikatu zwraca "ok"
        :return: komunikat błędu lub ok
        """
        try:
            self.wait.until(EC.visibility_of_element_located(Locators.ERROR_MESSAGE_LOGIN))
            el = self.driver.find_element(*Locators.ERROR_MESSAGE_LOGIN)
            return el.text
        except:
            return "ok"

    def get_terms_not_accepted_error_message(self):
        """
            Odszukuje komunikat o błędzie logowania i pobiera jego treść.
            Jeżeli brak komunikatu zwraca "ok"
        :return: komunikat błędu lub ok
        """
        try:
            self.wait.until(EC.visibility_of_element_located(Locators.TERMS_NOT_ACCEPTED_MESSAGE))
            el = self.driver.find_element(*Locators.TERMS_NOT_ACCEPTED_MESSAGE)
            return el.text
        except:
            return "ok"
