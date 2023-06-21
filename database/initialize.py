import sqlite3
import csv


def initialize(file):
    '''
    Initializes the database for the preset food data table and the internal tables for ingredients and meals.

    :param file: CSV File provided for the preset food data table
    :return: None
    '''
    # Open CSV-File for reading standard food table data
    with open(file) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        lines = [row for row in reader]
        header, body = ', '.join(lines[:1][0]), lines[1:]

    # Removing unsupported characters for sqlite table headers:
    header = header.replace('.', '').replace(' ', '').replace('-', '')
    fdata = sqlite3.connect('database/food_data.db')
    cursor = fdata.cursor()

    # Create preset food data table, if not created
    try:
        cursor.execute(f'CREATE TABLE fooddata(ID,{header})')
    except sqlite3.OperationalError:
        pass

    # Test if table has content, if not fill with data
    cursor.execute('SELECT * FROM fooddata')
    if not cursor.fetchall():
        print('Writing into database...', end='')
        uniqid = 0
        for row in body:
            # Removing quotechars from entries. Example: Goat's cheese
            entry = ', '.join(['\'' + value.replace('\'', '').replace('"', '') + '\'' for value in row])
            cursor.execute(f'INSERT INTO fooddata VALUES({uniqid},{entry})')
            uniqid += 1
            fdata.commit()

        print('done.')

    fdata.close()