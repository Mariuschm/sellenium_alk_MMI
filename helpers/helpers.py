def login(login_page, customer_name, employee_name, password, remember_me, accept_rules):
    """
        Metoda pomocnicza służąca do zalogowania się
    :param login_page: strona logowania
    :param customer_name: nazwa firmy lub NIP
    :param employee_name: login pracownika
    :param password: hasło pracownika
    :param remember_me: czy zaznaczyć zapamiętaj mnie
    :param accept_rules: czy akceptuje regulamin
    :return: stronę MainPage lub błąd
    """
    try:
        login_page.enter_customer_name(customer_name)
        login_page.enter_employee_name(employee_name)
        login_page.enter_password(password)
        if remember_me:
            login_page.check_remember_me()
        if accept_rules:
            login_page.check_confirm_rules()
        return login_page.click_login()
    except:
        return ""

