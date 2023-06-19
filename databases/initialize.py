import sqlite3
import csv

def initialize(file):
    with open(file) as csvfile:
        reader = csv.reader(csvfile, delimiter=',',quotechar='"')
        lines = [row for row in reader]
        header, body  = ', '.join(lines[:1][0]), lines [1:]

    header = header.replace('.','').replace(' ','').replace('-','')
    fdata =sqlite3.connect('food_data.db')
    cursor = fdata.cursor()

    try:
        cursor.execute(f'CREATE TABLE fooddata(ID,{header})')
    except sqlite3.OperationalError:
        pass

    cursor.execute('SELECT * FROM fooddata')
    if not cursor.fetchall():
        print('Writing into database...', end='')
        ID = 0
        for row in body:
            entry = ', '.join(['\''+ value.replace('\'','').replace('"','') + '\'' for value in row]) # Removing quotechars from entries. Example: Goat's cheese
            cursor.execute(f'INSERT INTO fooddata VALUES({ID},{entry})')
            ID += 1
            fdata.commit()

        print('done.')


initialize('food.csv')

