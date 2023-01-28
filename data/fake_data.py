from faker import Faker


class FakeData:

    def __init__(self):
        fake = Faker("pl-Pl")
        self.fake_password = fake.password(12)
        self.fake_company = fake.company()
        self.fake_username = fake.user_name()
        self.fake_tax_id = fake.company_vat()
        self.fake_text = fake.text(5)
