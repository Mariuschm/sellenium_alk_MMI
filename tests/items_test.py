from pages.items_page import ItemsPage
from pages.main_page import MainPage
from helpers import helpers
from tests.base_test import BaseTest
from data.valid_data import ValidData


class ItemsTest(BaseTest):
    """
        Klasa z przypadkami testowymi dla listy produktów
        Warunki wstępne:
        1. Otwarta przeglądarka
        2. Otwarta strona [https://demob2b-xl.comarch.pl/]
        3. Zaloguj się poprawnymi danymi

        TC201:  sprawdź czy załadowała się lista kategorii
        TC202:  sprawdź czy załaduje się lista towarów dla kategorii
        TC203:  sprawdzenie ilości poniżej 0
        TC204:  sprawdzenie iloścci powyżej maksimum
        TC205:  sprawdzenie ilości losowej
    """

    def setUp(self):
        super().setUp()
        self.main_page = helpers.login(self.login_page,
                                       ValidData.customer,
                                       ValidData.user_name,
                                       ValidData.password,
                                       True,
                                       True)

    def test201_categories_loaded(self):
        """
            TC201: sprawadzenie czy załadowała sie lista kategorii

        :return: test powiedzie się, jeżeli  zostanie załadowana conajmniej jedna kategoria
        """
        if type(self.main_page) == MainPage:
            self.assertNotEqual(0, len(self.main_page.get_categories()))

    def test202_items_loaded(self):
        """
             TC201:  sprawdź czy załadowała się lista kategorii
             1. Kliknij w pierwszą kategorię
             2. Sprawdź czy załadowała się lista
        :return: test powiedzie się, jeżeli zostanie wyświetlony conajmniej jeden towar
        """
        if type(self.main_page) == MainPage:
            categories = self.main_page.get_categories()
            if len(categories)>0:
                # Jest lista kategorii, mogę kontynuować test
                # Kategorie są typu web_element
                page = self.main_page.get_items_from_category(categories[0])
                if type(page) == ItemsPage:
                    # Jeżeli załadowała się strona ItemsPage idę dalej
                    self.assertGreater(len(page.get_items_list()), 2)
                else:
                    # Jeżeli nie załadowała się strona ItemsPage zwróć False
                    return False
            else:
                # Jeżeli nie załadowano kategorii testu nie da się dalej przeprowadzić
                # przez co test jest nie zaliczony
                assert False


