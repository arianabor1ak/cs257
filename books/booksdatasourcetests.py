'''
   booksdatasourcetest.py
   Jeff Ondich, 24 September 2021
'''

from booksdatasource import Author, Book, BooksDataSource
import unittest

class BooksDataSourceTester(unittest.TestCase):
    def setUp(self):
        self.data_source = BooksDataSource('books1.csv')

    def tearDown(self):
        pass

    def test_all_books(self):
        tiny_data_source = BooksDataSource('tinybooks.csv')
        books = tiny_data_source.books()
        self.assertTrue(len(books) == 3)
        self.assertTrue(books[0].title == 'Emma')
        self.assertTrue(books[1].title == 'Neverwhere')
        self.assertTrue(books[2].title == 'Omoo')
    
    #tests for author
    def test_all_authors(self):
        tiny_data_source = BooksDataSource('tinybooks.csv')
        books = tiny_data_source.books()
        self.assertTrue(len(books) == 3)
        self.assertTrue(books[0].title == 'Emma')
        self.assertTrue(books[1].title == 'Neverwhere')
        self.assertTrue(books[2].title == 'Omoo')

    def test_unique_author(self):
        authors = self.data_source.authors('Pratchett')
        self.assertTrue(len(authors) == 1)
        self.assertTrue(authors[0] == Author('Pratchett', 'Terry'))

    def test_multiple_author(self):
        authors = self.data_source.authors('Brontë')
        self.assertTrue(len(authors) == 3)
        self.assertTrue(authors[0] == Author('Brontë', 'Ann') and authors[1] == Author('Brontë', 'Charlotte') and authors[2] == Author('Brontë', 'Emily'))

    def test_no_author(self):
        authors=self.data_source.authors('asdfkjl;')
        self.assertTrue(len(authors) == 0)

#figure out what to do in terms of testing for no string/print all authors
#all case insensitive results show up
#books testing: putting in gibberish for sortby still gives you default sorting/no type error
#books testing: zero books, one book, two+ books, all books, check sorting (btwn 2/all)
#booksbetween testing: if start year > end year, return nothing; zero, one, two, all, checking none for both start and
#check that book results are returned in sorted order by pub year

if __name__ == '__main__':
    unittest.main()

