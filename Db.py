from database.initialize import initialize
import sqlite3, datetime, calendar


class Db:

    '''
    Base database class for tracknut
    that will perform all the database operations.
    '''

    def __init__(self):
        self.connection = sqlite3.connect('database/food_data.db')
        self.cursor = self.connection.cursor()
        self.fid = 0
        self.mid = 0
        self.get_max_fid()
        self.get_max_mid()

    def get_max_fid(self):
        try:
            self.cursor.execute('SELECT MAX(ID) FROM food')
            result = self.cursor.fetchone()[0]
            if result is not None:
                self.fid = int(result) + 1

            else:
                self.fid = 0
        except sqlite3.OperationalError:
            self.fid = 0

    def get_max_mid(self):
        try:
            self.cursor.execute('SELECT MAX(ID) FROM meals')
            result = self.cursor.fetchone()[0]
            if result is not None:
                self.mid = int(result) + 1

            else:
                self.mid = 0
        except sqlite3.OperationalError:
            self.mid = 0

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

    def init_calendar(self):  # TODO
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
        self.cursor.execute(f'INSERT INTO food VALUES(\'{self.fid}\',{ftvstring})')
        self.connection.commit()
        self.fid += 1

    def insert_meal(self, name, ingredients: dict):
        self.cursor.execute(f'INSERT INTO meals VALUES(\'{self.mid}\',\'{name}\',\'{ingredients}\')')
        self.connection.commit()
        self.mid += 1

    def get_food(self, getid):
        self.cursor.execute(f'SELECT * FROM food WHERE(ID = {getid})')
        return self.cursor.fetchone()

    def get_meal(self, getid):
        self.cursor.execute(f'SELECT * FROM meals WHERE(ID = {getid})')
        return self.cursor.fetchone()

    def get_fdata(self, getid):
        self.cursor.execute(f'SELECT * FROM fooddata WHERE(ID = {getid})')
        return self.cursor.fetchone()
