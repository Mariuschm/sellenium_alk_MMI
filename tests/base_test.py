from unittest import TestCase
from selenium import webdriver
from pages.login_page import LoginPage
from data.fake_data import FakeData
import configparser


class BaseTest(TestCase):
    """
        Klasa bazowa dla wszystkich testów niezależnie
    """

    def setUp(self):
        """
            Definuiujemy warunki wejścia do testów
            1. Otwórz przeglądarkę
            2. Wejdź na stronę https://demob2b-xl.comarch.pl/ [podstaw właściwą]
        :return:
        """
        config = configparser.ConfigParser()
        config.read('config.ini')
        browser = config.get('Config', 'browser')
        # Dodanie webdriver
        match browser.lower():
            case "firefox":
                self.driver = webdriver.Firefox()
            case "chrome":
                self.driver = webdriver.Chrome()
            case "egde":
                self.driver = webdriver.Edge()

        # Maksymalizacja okna
        self.driver.maximize_window()
        # Otwarcie strony
        self.driver.get("https://demob2b-xl.comarch.pl/")
        self.login_page = LoginPage(self.driver)
        self.fake_data = FakeData()

    def tearDown(self):
        """
            Metoda sprzątania po teście
            1. Wyloguj jeżeli zalogowany
            2. Zamknij przeglądarkę
            Dla niektórych testów koniczna będzie aktualizacja wpisów w bazie danych
        :return:
        """
        self.driver.quit()
        pass
