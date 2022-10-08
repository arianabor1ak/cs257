#Sophia Wang and Ariana Borlak
'''
    booksdatasource.py
    Jeff Ondich, 21 September 2022
    For use in the "books" assignment at the beginning of Carleton's
    CS 257 Software Design class, Fall 2022.
'''

import csv
import sys

class Author:
    def __init__(self, surname='', given_name='', birth_year=None, death_year=None):
        self.surname = surname
        self.given_name = given_name
        self.birth_year = birth_year
        self.death_year = death_year

    def __eq__(self, other):
        ''' For simplicity, we're going to assume that no two authors have the same name. '''
        return self.surname == other.surname and self.given_name == other.given_name

    def printAuth(self):
        print(self.given_name + " " + self.surname + " (" + self.birth_year + "-" + self.death_year + ")")

class Book:
    def __init__(self, title='', publication_year=None, authors=[]):
        ''' Note that the self.authors instance variable is a list of
            references to Author objects. '''
        self.title = title
        self.publication_year = publication_year
        self.authors = authors

    def __eq__(self, other):
        ''' We're going to make the excessively simplifying assumption that
            no two books have the same title, so "same title" is the same
            thing as "same book". '''
        return self.title == other.title

    def printBook(self):
        book_author = ""
        if len(self.authors) == 1:
            book_author += self.authors[0].given_name + " " + self.authors[0].surname + " "
        elif len(self.authors) >= 2:
            for author in self.authors:
                book_author += author.given_name + " " + author.surname + " and "
            #I wasn't sure how to remove the last characters from a string so I used this source
            #https://stackoverflow.com/questions/1038824/how-do-i-remove-a-substring-from-the-end-of-a-string
            if book_author.endswith("and "):
                book_author = book_author[:-4]
        print(self.title + ", " + self.publication_year + ", by " + book_author)


def create_author(data_source, author_info_split, single_book_author_list):
    ''' Returns the list of authors for a single book
    '''
    #whether an author can have 2+ given names is not considered.
    #everything after 0th index before years is considered a surname
    author_years = author_info_split[len(author_info_split) - 1]
    author_years = author_years.strip("()")
    author_years = author_years.split("-")

    i = 1
    author_surname = ""
    while i <= len(author_info_split) -2:
        author_surname += author_info_split[i]
        if i < len(author_info_split) -2:
            author_surname += " "
        i += 1

    author_object = Author(author_surname, author_info_split[0], author_years[0], author_years[1])

    added_author = single_book_author_list
    added_author.append(author_object)
    if author_object not in data_source.global_author_list:
        data_source.global_author_list.append(author_object)

    return added_author


class BooksDataSource:
    def __init__(self, books_csv_file_name):
        ''' The books CSV file format looks like this:
                title,publication_year,author_description
            For example:
                All Clear,2010,Connie Willis (1945-)
                "Right Ho, Jeeves",1934,Pelham Grenville Wodehouse (1881-1975)
            This __init__ method parses the specified CSV file and creates
            suitable instance variables for the BooksDataSource object containing
            a collection of Author objects and a collection of Book objects.
        '''

        #command line is handled differently than testing, so this covers both:
        if type(books_csv_file_name) == str:
            self.file = open(books_csv_file_name)
        else:
            self.file = books_csv_file_name
        self.global_book_list = list()
        self.global_author_list = list()

        #I couldn't remember how to skip commas in quotes, but I knew there was a way to do it, so I looked it up
        #Citation is https://stackoverflow.com/questions/21527057/python-parse-csv-ignoring-comma-with-double-quotes
        for line in csv.reader(self.file, quotechar = '"', delimiter = ',', skipinitialspace=True):
            line_title, line_year, line_authors = line[0], line[1], line[2]
            all_author_info = line_authors.split()

            author_info_split = list()
            single_book_author_list = list()

            for word in all_author_info:
                if word != "and":
                    author_info_split.append(word)

                else:
                    single_book_author_list = create_author(self, author_info_split, single_book_author_list)
                    while len(author_info_split) > 0:
                        author_info_split.pop()

            #last author is skipped over, make object for them
            single_book_author_list = create_author(self, author_info_split, single_book_author_list)

            book_object = Book(line_title, line_year, single_book_author_list)

            #print(book_object.printBook())

            self.global_book_list.append(book_object)

        if type(books_csv_file_name) == str:
            self.file.close()

    def authors(self, search_text=None):
        ''' Returns a list of all the Author objects in this data source whose names contain
            (case-insensitively) the search text. If search_text is None, then this method
            returns all of the Author objects. In either case, the returned list is sorted
            by surname, breaking ties using given name (e.g. Ann Brontë comes before Charlotte Brontë).
        '''
        author_results = list()

        if search_text == None or search_text == "None":
            author_results = self.global_author_list
            author_results.sort(key = lambda author_object: (author_object.surname, author_object.given_name))
            return author_results

        search_lower = search_text.lower()


        for author in self.global_author_list:
            surname_lower = author.surname.lower()
            given_lower = author.given_name.lower()

            if search_lower in surname_lower or search_lower in given_lower:
                author_results.append(author)
            elif search_lower in given_lower + " " + surname_lower or search_lower in surname_lower + " " + given_lower:
                author_results.append(author)
            elif search_lower in given_lower + ", " + surname_lower or search_lower in surname_lower + ", " + given_lower:
                author_results.append(author)

        #Since I don't remember how to sort by attribute, I looked up it up and found
        #https://runestone.academy/ns/books/published/fopp/Sorting/SecondarySortOrder.html
        author_results.sort(key = lambda author_object: (author_object.surname, author_object.given_name))
        return author_results

    def books(self, search_text=None, sort_by='title'):
        ''' Returns a list of all the Book objects in this data source whose
            titles contain (case-insensitively) search_text. If search_text is None,
            then this method returns all of the books objects.
            The list of books is sorted in an order depending on the sort_by parameter:
                'year' -- sorts by publication_year, breaking ties with (case-insenstive) title
                'title' -- sorts by (case-insensitive) title, breaking ties with publication_year
                default -- same as 'title' (that is, if sort_by is anything other than 'year'
                            or 'title', just do the same thing you would do for 'title')
        '''
        #we choose to force users to keep track of diacritics and apostrophes or other punctuation
        book_results = list()

        if search_text == None or search_text == "None":
            book_results = self.global_book_list
            if sort_by.lower() == "-y" or sort_by.lower() == "--year":
                book_results.sort(key = lambda book_object: (book_object.publication_year, book_object.title))
                return book_results
            else:
                book_results.sort(key = lambda book_object: (book_object.title, book_object.publication_year))
                return book_results
            return book_results

        search_lower = search_text.lower()


        for book in self.global_book_list:
            title_lower = book.title.lower()
            if search_lower in title_lower:
                book_results.append(book)


        #Since I don't remember how to sort by attribute, I looked up it up and found
        #https://runestone.academy/ns/books/published/fopp/Sorting/SecondarySortOrder.html
        if sort_by.lower() == "year":
            book_results.sort(key = lambda book_object: (book_object.publication_year, book_object.title))
            return book_results
        else:
            book_results.sort(key = lambda book_object: (book_object.title, book_object.publication_year))
            return book_results

    def books_between_years(self, start_year=None, end_year=None):
        ''' Returns a list of all the Book objects in this data source whose publication
            years are between start_year and end_year, inclusive. The list is sorted
            by publication year, breaking ties by title (e.g. Neverwhere 1996 should
            come before Thief of Time 1996).
            If start_year is None, then any book published before or during end_year
            should be included. If end_year is None, then any book published after or
            during start_year should be included. If both are None, then all books
            should be included.
        '''


        #we choose to force users to input lesser to greater or else no results
        year_results = list()
        if (start_year == None or start_year == "None") and (end_year == None or end_year == "None"):
            year_results = self.global_book_list
            year_results.sort(key = lambda book_object: (book_object.publication_year, book_object.title))
            return year_results
        for book in self.global_book_list:
            if (start_year == None or start_year == "None") and book.publication_year <= end_year:
                year_results.append(book)
            elif (end_year == None or end_year == "None") and book.publication_year >= start_year:
                year_results.append(book)
            elif book.publication_year >= start_year and book.publication_year <= end_year:
                year_results.append(book)

        #Since I don't remember how to sort by attribute, I looked up it up and found
        #https://runestone.academy/ns/books/published/fopp/Sorting/SecondarySortOrder.html
        year_results.sort(key = lambda book_object: (book_object.publication_year, book_object.title))
        return year_results

if __name__ == "__main__":
    main()
