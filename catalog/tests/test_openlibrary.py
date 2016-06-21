from ..openlibrary import *
import unittest

class TestOpenLibraryRequest(unittest.TestCase):

    def test_isbn_search(self):
        isbn = '9780465050659'
        result = search_by_isbn(isbn)
        self.assertIn('identifiers', result)

    def test_bibkey_search(self):
        bibkey = ('isbn', '9780465050659')
        result = search(bibkey)
        self.assertIn('identifiers', result)

    def test_search_bulk(self):
        bibkeys = [('isbn', '9780465050659'), ('lccn', '62019420')]
        result = search_bulk(bibkeys)
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), len(bibkeys))


if __name__ == '__main__':
    unittest.main()


