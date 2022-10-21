'''
olympics.py
Ariana Borlak
'''

import csv
import sys

def NOC_athletes():
    //do something to parse

def main():
    if len(sys.argv) < 2:
        raise SyntaxError("Not enough arguments, type python3 olympics.py -h for help")
    if sys.argv[1] == "-h" or sys.argv[1] == "--help":
        usage = open('usage.txt')
        print(usage.read())
        usage.close()
        return
        
if __name__ == "__main__":
    main()