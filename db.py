from database.initialize import initialize
import sqlite3
import datetime
import calendar
from database.fields import Fields


class Db:

    '''
    Base database class for tracknut
    that will perform all the database operations.
    '''

    def __init__(self):
        self.connection = sqlite3.connect('database/food_data.db')
        self.cursor = self.connection.cursor()
        self._fid = self.get_max_fid()
        self._mid = self.get_max_mid()
        self.fields = Fields()

    def get_max_fid(self):
        try:
            self.cursor.execute('SELECT MAX(ID) FROM food')
            result = self.cursor.fetchone()[0]
            if result is not None:
                return int(result) + 1

            else:
                return 0

        except sqlite3.OperationalError:
            return 0

    def get_max_mid(self):
        try:
            self.cursor.execute('SELECT MAX(ID) FROM meals')
            result = self.cursor.fetchone()[0]
            if result is not None:
                return int(result) + 1

            else:
                return 0
        except sqlite3.OperationalError:
            return 0

    def initialize(self, file):
        initialize(file)

    def init_food(self, headers: list):
        try:
            fth = [header.replace('.', '').replace(' ', '').replace('-', '') for header in list(headers)]
            fthstring = ', '.join(['\'' + header.replace('\'', '').replace('"', '') + '\'' for header in fth])
            self.cursor.execute(f'CREATE TABLE food (\'ID\', {fthstring})')
        except sqlite3.OperationalError:
            raise sqlite3.OperationalError('Initialization already completed')

    def init_meals(self):
        try:
            self.cursor.execute('CREATE TABLE meals (\'ID\',\'name\',\'ingredients\'')
        except sqlite3.OperationalError:
            raise sqlite3.OperationalError('Initialization already completed')

    def init_calendar(self):
        try:
            self.cursor.execute('CREATE TABLE days (\'Day\',\'Entries\')')
        except sqlite3.OperationalError:
            self.cursor.execute('SELECT * FROM days ')
            if self.cursor.fetchall()[0]:
                raise sqlite3.OperationalError('Initialization already completed')

        start = datetime.date(2000, 1, 1)
        whead = calendar.weekheader(3).split(' ')
        for i in range(36500):
            date = str(start + datetime.timedelta(i))
            ddict = {key: value for (key, value) in
                     map(lambda x, y: (x, y), ('year', 'month', 'day'),
                     [int(item) for item in date.split('-')])
                     }
            entry = whead[calendar.weekday(**ddict)] + date
            self.cursor.execute(f'INSERT INTO days (Day) VALUES (\'{entry}\')')
        self.connection.commit()

    def insert_food(self, values: list):
        ftv = [str(value) for value in list(values)]
        ftvstring = ', '.join(['\'' + value.replace('\'', '').replace('"', '') + '\'' for value in ftv])
        self.cursor.execute(f'INSERT INTO food VALUES(\'{self._fid}\',{ftvstring})')
        self.connection.commit()
        self._fid += 1

    def insert_meal(self, name, ingredients: dict):
        self.cursor.execute(f'INSERT INTO meals VALUES(\'{self._mid}\',\'{name}\',\'{ingredients}\')')
        self.connection.commit()
        self._mid += 1

    def get_food(self, getid):

        if getid == 'all':
            self.cursor.execute('SELECT * FROM food')
            return self.cursor.fetchall()

        else:
            self.cursor.execute(f'SELECT * FROM food WHERE(ID = {getid})')
            return self.cursor.fetchone()

    def get_meal(self, getid):

        if getid == 'all':
            self.cursor.execute('SELECT * FROM meals')
            return self.cursor.fetchall()

        else:
            self.cursor.execute(f'SELECT * FROM meals WHERE(ID = {getid})')
            return self.cursor.fetchone()

    def get_fdata(self, getid):

        if getid == 'all':
            self.cursor.execute('SELECT * FROM fooddata')
            return self.cursor.fetchall()

        else:
            self.cursor.execute(f'SELECT * FROM fooddata WHERE(ID = {getid})')
            return self.cursor.fetchone()


dat = Db()
print([item for item in dat.fields])