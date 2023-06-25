# Projekt testów automatycznych Sellenium w języku Python
## Informacje o projekcie
### Autor
    Mariusz Midzio
    Nr. albumu: 59035
    email: 59035-ckp@kozminski.edu.pl
    
### Testowana strona
W trakcie testów wykorzystywana będzie strona https://demob2b-xl.comarch.pl/

### Wykorzystane wzorce:
 - [X] PageObjectPattern
 - [X] Data Driven Tests

### Scenariusze testowe
W ramach projektu zdefiniowane zostały trzy scenariusze testowe:
1. Logowanie do systemu Comarch B2B
2. Sprawdzenie wyświetlania pozycji asortymentowych oraz wprowadzanie ilości
3. Sprawdzenie poprawności dodawania pozycji do koszyka
 
Testy były przeprowadzane na różncyh przeglądarkach zależnie od konfiguaracji w pliku config.ini.


### Wnioski końcowe
W trakcie testów nasunęły się następujące wnioski:
1. Wydajność łącza internetwego wpływa na wyniki testów
2. Dobór odpowiedniego interwał dla explicit wait jest ważny dla poprawności testów
3. W przypadku testowanej strony cześć pozycji towarowych ładowanych jest dopiero po przewinięciu do końca strony
4. Kontrolka typu input wymaga innego podejścia do pobierania zawartości
5. W przypadku testowanej strony typ danych w kontrolce typu input miał wpływ na wyniki testów:

   [a]. dla danych typu int wszystkie testy przebiegały pomyślnie

   [b]. dla danych typu decimal wartości wprowadzone były błędene przez co wyniki testów nie były miarodajne
6. W przypadku testowanej strony zachowywała się ona inaczej dla testów manualnych (eksploracyjnych) a inaczej dla testów automatycznych.
