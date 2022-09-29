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
        bookAuthor = ""
        for author in self.authors:
            bookAuthor += author.given_name + " " + author.surname + " "
        print(self.title + ", " + self.publication_year + ", by " + bookAuthor)

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
        if type(books_csv_file_name) == str:
            self.file = open(books_csv_file_name)
        else:
            self.file = books_csv_file_name
        self.globalBookList = list()
        self.globalAuthList = list()

        #I couldn't remember how to skip commas in quotes, but I knew there was a way to do it, so I looked it up
        #Citation is https://stackoverflow.com/questions/21527057/python-parse-csv-ignoring-comma-with-double-quotes
        for line in csv.reader(self.file, quotechar = '"', delimiter = ',', skipinitialspace=True):
            lineTitle, lineYear, lineAuth = line[0], line[1], line[2]

            allAuthInfo = lineAuth.split()

            authInfoSplit = list()
            singleBookAuthList = list()


            for word in allAuthInfo:
                if word != "and":
                    authInfoSplit.append(word)

                    #then we have more than one author
                    #for all of the items in the list before and, do what's below for one author
                else:
                    #whether an author can have 2+ given names is not considered.
                    #everything after 0th index before years is considered a surname
                    lineAuthYear = authInfoSplit[len(authInfoSplit) - 1]
                    lineAuthYear = lineAuthYear.strip("()")
                    lineAuthYear = lineAuthYear.split("-")

                    i = 1
                    lineSurname = ""
                    while i <= len(authInfoSplit) -2:
                        lineSurname += authInfoSplit[i]
                        if i < len(authInfoSplit) -2:
                            lineSurname += " "
                        i += 1

                    authOb = Author(lineSurname, authInfoSplit[0], lineAuthYear[0], lineAuthYear[1]) #we have duplicate author objects
                    singleBookAuthList.append(authOb)
                    if authOb not in self.globalAuthList:
                        self.globalAuthList.append(authOb)

                    while len(authInfoSplit) > 0:
                        authInfoSplit.pop()


            #last author is skipped over, make object for them

            lineAuthYear = authInfoSplit[len(authInfoSplit) - 1]
            lineAuthYear = lineAuthYear.strip("()")
            lineAuthYear = lineAuthYear.split("-")

            i = 1
            lineSurname = ""
            while i <= len(authInfoSplit) -2:
                lineSurname += authInfoSplit[i]
                if i < len(authInfoSplit) -2:
                    lineSurname += " "
                i += 1

            authOb = Author(lineSurname, authInfoSplit[0], lineAuthYear[0], lineAuthYear[1])
            if authOb not in self.globalAuthList:
                self.globalAuthList.append(authOb)
            singleBookAuthList.append(authOb)


            bookOb = Book(lineTitle, lineYear, singleBookAuthList)

            self.globalBookList.append(bookOb)

        if type(books_csv_file_name) == str:
            self.file.close()

        pass

    def authors(self, search_text=None):
        ''' Returns a list of all the Author objects in this data source whose names contain
            (case-insensitively) the search text. If search_text is None, then this method
            returns all of the Author objects. In either case, the returned list is sorted
            by surname, breaking ties using given name (e.g. Ann Brontë comes before Charlotte Brontë).
        '''
        authResults = list()

        if search_text == None or search_text == "None":
            authResults = self.globalAuthList
            authResults.sort(key = lambda authOb: (authOb.surname, authOb.given_name))
            return authResults

        searchLower = search_text.lower()


        for author in self.globalAuthList:
            surLower = author.surname.lower()
            givenLower = author.given_name.lower()

            if searchLower in surLower or searchLower in givenLower:
                authResults.append(author)
            elif searchLower in givenLower + " " + surLower or searchLower in surLower + " " + givenLower:
                authResults.append(author)
            elif searchLower in givenLower + ", " + surLower or searchLower in surLower + ", " + givenLower:
                authResults.append(author)

        #Since I don't remember how to sort by attribute, I looked up it up and found
        #https://runestone.academy/ns/books/published/fopp/Sorting/SecondarySortOrder.html
        authResults.sort(key = lambda authOb: (authOb.surname, authOb.given_name))
        return authResults

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
        #if users search by title with apostrophe (like let's) but don't include the apostrophe, show the result anyway?
        bookResults = list()

        if search_text == None or search_text == "None":
            bookResults = self.globalBookList
            if sort_by.lower() == "year":
                bookResults.sort(key = lambda bookOb: (bookOb.publication_year, bookOb.title))
                return bookResults
            else:
                bookResults.sort(key = lambda bookOb: (bookOb.title, bookOb.publication_year))
                return bookResults
            return bookResults

        searchLower = search_text.lower()


        for book in self.globalBookList:
            titleLower = book.title.lower()
            if searchLower in titleLower:
                bookResults.append(book)


        #Since I don't remember how to sort by attribute, I looked up it up and found
        #https://runestone.academy/ns/books/published/fopp/Sorting/SecondarySortOrder.html
        if sort_by.lower() == "year":
            bookResults.sort(key = lambda bookOb: (bookOb.publication_year, bookOb.title))
            return bookResults
        else:
            bookResults.sort(key = lambda bookOb: (bookOb.title, bookOb.publication_year))
            return bookResults

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
        #check input is numbers(? if they input strings, does this matter?)

        #force users to input lesser to greater (or else no results :P)
        yearResults = list()
        if (start_year == None or start_year == "None") and (end_year == None or end_year == "None"):
            yearResults = self.globalBookList
            yearResults.sort(key = lambda bookOb: (bookOb.publication_year, bookOb.title))
            return yearResults
        for book in self.globalBookList:
            if (start_year == None or start_year == "None") and book.publication_year <= end_year:
                yearResults.append(book)
            elif (end_year == None or end_year == "None") and book.publication_year >= start_year:
                yearResults.append(book)
            elif book.publication_year >= start_year and book.publication_year <= end_year:
                yearResults.append(book)

        #Since I don't remember how to sort by attribute, I looked up it up and found
        #https://runestone.academy/ns/books/published/fopp/Sorting/SecondarySortOrder.html
        yearResults.sort(key = lambda bookOb: (bookOb.publication_year, bookOb.title))
        return yearResults

if __name__ == "__main__":
    main()

#files to be input
#change the names of variables
#handle None for books_between_years (start)
#handle None for books with
# search string but yes sorting change
#fix general style, add comments