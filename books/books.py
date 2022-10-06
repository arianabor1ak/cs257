#Sophia Wang and Ariana Borlak
'''
    books.py
    Jeff Ondich, 21 September 2022

    For use in the "books" assignment at the beginning of Carleton's
    CS 257 Software Design class, Fall 2022.
'''

'''
user puts in: python3 books.py <file> -t searchstring sortby
'''

import csv
import sys
import booksdatasource


def main():
    if len(sys.argv) < 2:
        #raise an error: too few arguments
        raise SyntaxError('Too few arguments, type python3 books.py -h for help')
        return
    if sys.argv[1] == "-h" or sys.argv[1] == "--help":
        usage = open('usage.txt')
        print(usage.read())
        usage.close()
        return

    #try/except was inspired by code review, specifically james brink and amir al-sheikh. 
    #it seems simple enough that no google search was needed
    try:
        books_file = open(sys.argv[1])
    except:
        print(sys.argv[1], "is not a valid file, please enter a valid file")
        return

    dataSource = booksdatasource.BooksDataSource(books_file)
    if len(sys.argv) == 2:
        output = dataSource.books()
    elif sys.argv[2] == "books":
        if len(sys.argv) == 3:
            output = dataSource.books()
        elif len(sys.argv) == 4:
            output = dataSource.books(sys.argv[3])
        elif len(sys.argv) == 5:
            output = dataSource.books(sys.argv[3], sys.argv[4])
        else:
            raise SyntaxError('Wrong number of arguments')
    elif sys.argv[2] == "authors":
        if len(sys.argv) == 3:
            output = dataSource.authors()
        elif len(sys.argv) == 4:
            output = dataSource.authors(sys.argv[3])
        elif len(sys.argv) == 5:
            output = dataSource.authors(sys.argv[3], sys.argv[4])
        else:
            raise SyntaxError('Wrong number of arguments')
    elif sys.argv[2] == "years":
        if len(sys.argv) == 3:
            output = dataSource.books_between_years()
        elif len(sys.argv) == 4:
            output = dataSource.books_between_years(sys.argv[3])
        elif len(sys.argv) == 5:
            output = dataSource.books_between_years(sys.argv[3], sys.argv[4])
        else:
            raise SyntaxError('Wrong number of arguments')
    else:
        raise SyntaxError('Invalid command')
    books_file.close()

    for item in output:
        if isinstance(item, booksdatasource.Author):
            item.printAuth()
        elif isinstance(item, booksdatasource.Book):
            item.printBook()

if __name__ == "__main__":
    main()
