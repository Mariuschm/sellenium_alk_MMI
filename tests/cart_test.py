from tests.base_test import BaseTest
from pages.cart_page import CartPage
from pages.items_page import ItemsPage
from data.valid_data import ValidData
from helpers import helpers
from ddt import ddt, data, unpack
import csv


def get_data_from_csv(filename):
    """
        Zwraca zwartość pliku CSC
    :param filename: plik
    :return: lista wierszy
    """
    rows = []
    # Strona kodowa umożliwiając obsługę polskich znaków
    data_file = open(filename, "r", encoding="utf-8")
    # Dodany separator średnik
    reader = csv.reader(data_file, delimiter=";")
    for row in reader:
        rows.append(row)
    return rows


@ddt
class CartTest(BaseTest):
    """
    Klasa z przypadkami testowymi dla sprawdzania dodwania do koszyka
    Warunki wstępne:
    1. Otwarta przeglądarka
    2. Otwarta strona [https://demob2b-xl.comarch.pl/]
    3. Zaloguj się poprawnymi danymi

    TC301:  Dodaj pozycję do koszyka i sprawdź zgodność pozycji z plikiem (nie walidowane są wartości)
    """

    def setUp(self):
        super().setUp()
        # Logowanie
        self.main_page = helpers.login(self.login_page,
                                       ValidData.customer,
                                       ValidData.user_name,
                                       ValidData.password,
                                       True,
                                       True)
        self.cart_page = ""
        self.cart_id = 0

    def tearDown(self):
        # Nadpisuję tearDown
        # Kasuję koszyk stowrzony w ramach danej sesji
        if type(self.cart_page) == CartPage and self.cart_id != 0:
            self.cart_page.remove_cart(self.cart_id)
        # Wylogowuję się
        self.main_page.log_out()
        self.driver.quit()

    @data(*get_data_from_csv("..\\data\\valid_items.csv"))
    @unpack
    def test301_valid_data(self, category, item_code, amount):
        """
            TC301:   Dodaj pozycję do koszyka i sprawdź zgodność pozycji z plikiem (nie walidowane są wartości)
            Warunki wstępne:
                1. Otwarta przeglądarka
                2. Otwarta strona [https://demob2b-xl.comarch.pl/]
                3. Zaloguj się poprawnymi danymi
            pyt
        :return: test powiedzie się jeżeli dodano produkt w poprawnej ilości
        """
        # Plik powinien zawierać kolumny: kategoria, kod, ilość
        # Krok 1 Ładuję kategorię
        cats = self.main_page.get_categories_with_names()
        # Krok 2 Szukam kategorii z pliku
        cat = [cats_list[0] for cats_list in cats if cats_list[1] == category][0]
        # Krok 3 Pobieram towary z kategorii
        page = self.main_page.get_items_from_category(cat)
        # Powinna się załadować lista towarów
        if type(page) == ItemsPage:  # Zwrócona strona typu ItemsPage
            # Krok 4 Szukam towaru na liście
            items = page.get_items_list()
            item = [items_list for items_list in items if items_list[3] == item_code]
            # asercja czy to jest item
            # Ustaw ilość i dodaj do koszyka
            if len(item) == 0:
                assert False
                return
            page.set_amount(item[0][4], amount)
            # Dodaj do koszyka, poczekaj na stronę
            ret = page.add_to_cart(item[0][5])
            self.cart_id = ret[0]
            self.cart_page = ret[1]
            # Jeżeli załadowano stronę koszyka jest ok
            if type(self.cart_page) == CartPage:
                cart_items = self.cart_page.get_cart_items()
                cart_item = [cart_it[1] for cart_it in cart_items
                             if cart_it[1] == item_code and cart_it[2] == amount][0]
                self.assertEqual(cart_item, item_code)
            else:
                assert False
        else:
            assert False
