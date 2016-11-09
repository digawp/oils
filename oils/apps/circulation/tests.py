from django.test import TestCase

from oils.apps.catalog import factories as cat_factories


class LoanTestCase(TestCase):
    def setUp(self):
        self.patron = Patron.objects.get()
        self.book1 = cat_factories.BookFactory()
        self.book2 = cat_factories.BookFactory()

    def test_patron_create_loan(self):
        # Arrange

        # Act
        Loan.objects.create_loan(patron, book)

        # Assert
        loans = Loan.objects.all()
        self.assertEqual(loans.count(), 1)

