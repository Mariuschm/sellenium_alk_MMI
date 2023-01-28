# Pages
from pages.main_page import MainPage
# Tests
from tests.base_test import BaseTest
# Data
from data.valid_data import ValidData
# Helpers
from helpers import helpers

class LoginTests(BaseTest):
    """
        Klasa z przypadkami testowymi dla logowania
        Warunki wstępne:
        1. Otwarta przeglądarka
        2. Otwarta strona [https://demob2b-xl.comarch.pl/]

        TC101: logowanie z poprawnymi danymi
        TC102: logowanie z błędnym hasłem
        TC103: logowanie z błędną firmą
        TC104: logowanie z błędną pracownikiem
        TC105: brak akceptacji regulaminu
    """

    def setUp(self):
        # Roszerzam metodę setUp
        super().setUp()
        # Dodana flaga zalogowany
        self.logged = False
        # Dodany obiekt main_page (może przyjmować MainPage lub string)
        self.main_page = object

    def tearDown(self):
        # Nadpisuję metodę tearDown
        # Sprawdzam czy udało się zalogować
        # Jeżeli tak wylogowuję się
        if self.logged and type(self.main_page) == MainPage:
            self.main_page.log_out()
        self.driver.quit()

    def test101_valid_credential_login(self):
        """
            TC101: logowanie z poprawnymi danymi
            Firma:                  poprawna
            Pracownik:              poprawny
            Hasło:                  poprawne
            Zapamiętaj:             tak
            Akceptuj regulamin:     tak
        :return: test powiedzie się, jeżeli uda się zalgować i nazwa firmy będzie zgodna z przekazaną
        """
        try:
            self.main_page = helpers.login(self.login_page, ValidData.customer, ValidData.user_name, ValidData.password,
                                           True, True)
            if type(self.main_page) == MainPage:
                self.logged = True
                self.assertEqual(ValidData.customer.upper(), self.main_page.return_logged_customer())
            else:
                assert False
        except:
            assert False

    def test102_invalid_password(self):
        """
            TC102: logowanie z błędnym hasłem
            Firma:                  poprawna
            Pracownik:              poprawny
            Hasło:                  błędne
            Zapamiętaj:             tak
            Akceptuj regulamin:     tak
        :return: test powiedzie się, jeżeli nie uda się zalgować i pojawi się komunikat
        """
        try:
            self.main_page = helpers.login(self.login_page, ValidData.customer, ValidData.user_name,
                                           self.fake_data.fake_password, True, True)
            self.assertNotEqual("ok", self.login_page.get_login_error_message())
        except:
            assert False

    def test103_invalid_company(self):
        """
            TC103: logowanie z błędną firmą
            Firma:                  błędna
            Pracownik:              poprawny
            Hasło:                  poprawny
            Zapamiętaj:             tak
            Akceptuj regulamin:     tak
        :return: test powiedzie się, jeżeli nie uda się zalgować i pojawi się komunikat
        """
        try:
            self.main_page = helpers.login(self.login_page, self.fake_data.fake_company, ValidData.user_name,
                                           ValidData.password, True, True)
            self.assertNotEqual("ok", self.login_page.get_login_error_message())
        except:
            assert False

    def test104_invalid_employee(self):
        """
            TC104: logowanie z błędną pracownikiem
            Firma:                  poprawna
            Pracownik:              błędny
            Hasło:                  poprawny
            Zapamiętaj:             tak
            Akceptuj regulamin:     tak
        :return: test powiedzie się, jeżeli nie uda się zalgować i pojawi się komunikat
        """
        try:
            self.main_page = helpers.login(self.login_page, ValidData.customer, self.fake_data.fake_username,
                                           ValidData.password, True, True)
            self.assertNotEqual("ok", self.login_page.get_login_error_message())
        except:
            assert False

    def test105_terms_not_accepted(self):
        """
            TC105: brak akceptacji regulaminu
            Firma:                  poprawna
            Pracownik:              poprawny
            Hasło:                  poprawne
            Zapamiętaj:             tak
            Akceptuj regulamin:     nie
        :return: test powiedzie się, jeżeli nie uda się zalgować i pojawi się komunikat
        """
        try:
            self.main_page = helpers.login(self.login_page, ValidData.customer, ValidData.user_name, ValidData.password,
                                           True, False)
            self.assertNotEqual("ok", self.login_page.get_terms_not_accepted_error_message())
        except:
            assert False
