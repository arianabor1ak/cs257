#Sophia Wang and Ariana Borlak
#!/usr/bin/env python3
'''
    books.py
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

class BooksDataSource:
    bookList = list()
    authorList = list()
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
        for line in file:
            info = line.split(",") #need to accommodate case with commas in title
            listTitle, listYear, listAuth = info[0], info[1], info[2]

            authSplit = listAuth.split()
            #don't create multiple authors for books written by same person
            #create multiple separate authors for books written by 2+ people
            listAuthYear = authSplit[len(authSplit) -1]
            listAuthYear = listAuthYear.strip("()")
            listAuthYear = listAuthYear.split("-")
        
            i = 1
            surname = ""
            while i!> len(authSplit) -2:
                surname += authSplit[i]
                i++
            auth = Author(surname, authSplit[0], listAuthYear[0], listAuthYear[1])
            
            bookOb = Book(listTitle, listYear, auth)

            bookList.append(bookOb)
            authorList.append(auth)

        pass

    def authors(self, search_text=None):
        ''' Returns a list of all the Author objects in this data source whose names contain
            (case-insensitively) the search text. If search_text is None, then this method
            returns all of the Author objects. In either case, the returned list is sorted
            by surname, breaking ties using given name (e.g. Ann Brontë comes before Charlotte Brontë).
        '''
        authResults = list()

        searchLower = search_text.lower()

        if searchLower == "":
            authResults = authorList
        for author in authorList:
            surLower = author.surname.lower()
            givenLower = author.given_name.lower()

            if searchLower in surLower or searchLower in givenLower:
                authResults.append(author)
            elif searchLower in givenLower + " " + surLower or searchLower in surLower + " " + givenLower:
                authResults.append(author)
            elif searchLower in givenLower + ", " + surLower or searchLower in surLower + ", " + givenLower:
                authResults.append(author)
        #diacritics should be considered, but that's a problem for later 
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

        searchLower = search_text.lower()

        if searchLower == "":
            bookResults = bookList

        for book in bookList:
            titleLower = book.title.lower()
            if searchLower in titleLower:
                bookResults.append(book)

        if sort_by.lower() == "year":
            bookResults.sort(key = lambda bookOb: (bookOb.publication_year, bookOb.title))
            return bookResults
        else
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
        #check input is numbers
        #force users to input lesser to greater (or else no results :P)
        yearResults = list()
        if start_year == "" and end_year == "":
            yearResults = bookList
        for book in bookList:
            if start_year == "" and book.publication_year <= end_year:
                yearResults.append(book)
            elif end_year == "" and book.publication_year >= start_year:
                yearResults.append(book)
            elif book.publication_year >= start_year and book.publication_year <= end_year:
                yearResults.append(book)

        yearResults.sort(key = lambda bookOb: (bookOb.publication_year, book0b.title))
        return yearResults

def main():
    books_file = open('books1.csv')
    dataSource = BooksDataSource(books_file)
    if len(sys.argv) == 1:
        #return all books
    elif sys.argv[1] == "-h" or sys.argv[1] == "--help":
        #return usage.txt
    elif sys.argv[1] == "-t" or sys.argv[1] == "--title":
        #sort by title
        #need to accommodate SORT capability
    elif sys.argv[1] == "-a" or sys.argv[1] == "--author":
        #sort by author
    elif sys.argv[1] == "-y" or sys.argv[1] == "--year":
        #sort by publication year


    #take in input
    #call method according to input
    books_file.close()

if __name__ == "__main__":
    main()

