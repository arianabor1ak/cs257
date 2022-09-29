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
import booksdatasource


def main():
    books_file = open('books1.csv')
    dataSource = BooksDataSource(books_file)
    if len(sys.argv) == 1:
        output = dataSource.books()
    elif sys.argv[1] == "-h" or sys.argv[1] == "--help":
        usage = open('usage.txt')
        print(usage.read())
        usage.close()
    elif sys.argv[1] == "-t" or sys.argv[1] == "--title":
        if len(sys.arg) == 2:
            output = dataSource.books()
        elif len(sys.arg) == 3:
            output = dataSource.books(sys.argv[2])
        elif len(sys.arg) == 4:
            output = dataSource.books(sys.argv[2], sys.argv[3])
        else:
            raise SyntaxError('Wrong number of arguments')
    elif sys.argv[1] == "-a" or sys.argv[1] == "--author":
        if len(sys.arg) == 2:
            output = dataSource.books()
        elif len(sys.arg) == 3:
            output = dataSource.authors(sys.argv[2])
        elif len(sys.arg) == 4:
            output = dataSource.authors(sys.argv[2], sys.argv[3])
        else:
            raise SyntaxError('Wrong number of arguments')
    elif sys.argv[1] == "-y" or sys.argv[1] == "--year":
        if len(sys.arg) == 2:
            output = dataSource.books()
        elif len(sys.arg) == 3:
            output = dataSource.books_between_years(sys.argv[2])
        elif len(sys.arg) == 4:
            output = dataSource.books_between_years(sys.argv[2], sys.argv[3])
        else:
            raise SyntaxError('Wrong number of arguments')
    else:
        raise SyntaxError('Invalid command')
    books_file.close()

    for item in output:
        if isinstance(item, Author):
            item.printAuth()
        elif isinstance(item, Book):
            item.printBook()

main()
