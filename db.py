import sqlite3
import datetime
import calendar
from database.fields import Fields
from database.initialize import initialize


class Db:

    """
    Base database class for tracknut
    that will perform all the database operations.
    """

    def __init__(self):
        self.connection = sqlite3.connect('database/food_data.db')
        self.cursor = self.connection.cursor()
        self.fields = list(Fields())
        self.setup_tables()
        self._days = self.init_calendar()

        self._fid = self.get_max_fid()
        self._mid = self.get_max_mid()

        self._fentry = {k: v for (k, v) in map(lambda x: (x, 'NA'), self.fields)}
        self._mentry = {k: v for (k, v) in map(lambda x: (x, 'NA'), ['name', 'ingredients', 'serving size'])}
        self._dentry = {k: v for (k, v) in map(lambda x: (x, 'NA'), ['day', 'meals', 'foods'])}

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

    def load_food_data(self, file):

        initialize(file)

    def setup_tables(self):

        try:
            self.init_food()
        except sqlite3.OperationalError:
            pass

        try:
            self.init_meals()
        except sqlite3.OperationalError:
            pass

    def init_food(self):

        try:
            fth = ','.join(['\'' + item + '\'' for item in self.fields]).replace(' ', '')
            sql = "CREATE TABLE food ('ID' INTEGER PRIMARY KEY," + fth + ")"
            self.cursor.execute(sql)
        except sqlite3.OperationalError:
            raise sqlite3.OperationalError('Initialization already completed')

    def init_meals(self):

        try:  # TODO change SQL declaration
            self.cursor.execute('CREATE TABLE meals (ID INTEGER PRIMARY KEY, name, ingredients, serving size)')
        except sqlite3.OperationalError:
            raise sqlite3.OperationalError('Initialization already completed')

    def init_calendar(self):

        dlist = []
        start = datetime.date(2000, 1, 1)
        whead = calendar.weekheader(3).split(' ')
        for i in range(36500):
            date = str(start + datetime.timedelta(i))
            ddict = {key: value for (key, value) in
                     map(lambda x, y: (x, y), ('year', 'month', 'day'),
                     [int(item) for item in date.split('-')])
                     }
            entry = whead[calendar.weekday(**ddict)] + ' ' + date
            dlist.append(entry)

        return dlist

    def insert_food(self, entry=None):

        if not entry:
            entry = self._fentry

        ftv = entry.values()
        ftvstring = ', '.join(['\'' + str(item) + '\'' for item in ftv])
        self.cursor.execute(f'INSERT INTO food VALUES(\'{self._fid}\',{ftvstring})')
        self.connection.commit()
        self._fid += 1
        self._fentry = {k: v for (k, v) in map(lambda x: (x, 'NA'), self.fields)}

    def insert_meal(self, name, ingredients: dict):

        self.cursor.execute(f'INSERT INTO meals VALUES(\'{self._mid}\',\'{name}\',\'{ingredients}\')')
        self.connection.commit()
        self._mid += 1
        self._mentry = {k: v for (k, v) in map(lambda x: (x, 'NA'), ['name', 'ingredients', 'serving size'])}

    def go_to_day(self, day: str):

        if day in self._days:
            self._dentry['day'] = day

        else:
            raise ValueError('Day does not exist. Format of day should resemble: Sat 2023-07-22')

    def get_food(self, search='all', strict=False):

        if search == 'all':
            self.cursor.execute('SELECT * FROM food')
            result = self.cursor.fetchall()
            return result

        elif type(search) == int:
            self.cursor.execute(f'SELECT * FROM food WHERE(ID = {search})')
            result = self.cursor.fetchone()
            result = {k: v for (k, v) in map(lambda x, y: (x, y), self.fields, result)}
            return result

        elif type(search) == str:
            if not strict:
                self.cursor.execute('SELECT * FROM food')
                full = self.cursor.fetchall()
                result = [item for item in full if search in item[2]]
                return result

            elif strict:
                self.cursor.execute('SELECT * FROM food')
                full = self.cursor.fetchall()
                result = [item for item in full if search == item[2]]
                return result

    def get_meal(self, search='all', strict=False):

        if search == 'all':
            self.cursor.execute('SELECT * FROM meals')
            return self.cursor.fetchall()

        elif type(search) == int:
            self.cursor.execute(f'SELECT * FROM meals WHERE(ID = {search})')
            return self.cursor.fetchone()

        elif type(search) == str:

            if not strict:
                self.cursor.execute('SELECT * FROM meals')
                full = self.cursor.fetchall()
                result = [item for item in full if search in item[2]]
                return result

            elif strict:
                self.cursor.execute('SELECT * FROM meals')
                full = self.cursor.fetchall()
                result = [item for item in full if search == item[2]]
                return result

    def get_fdata(self, search='all', strict=False):

        if search == 'all':
            self.cursor.execute('SELECT * FROM fooddata')
            return self.cursor.fetchall()

        elif type(search) == int:
            self.cursor.execute(f'SELECT * FROM fooddata WHERE(ID = {search})')
            result = self.cursor.fetchone()
            result = {k: v for (k, v) in map(lambda x, y: (x, y), ['ID'] + self.fields, result)}
            return result

        elif type(search) == str:

            if not strict:
                self.cursor.execute('SELECT * FROM fooddata')
                full = self.cursor.fetchall()
                result = [{k: v for (k, v) in map(lambda x, y: (x, y), ['ID'] + self.fields, item)} for item in full]
                return result

            elif strict:
                self.cursor.execute('SELECT * FROM fooddata')
                full = self.cursor.fetchall()
                result = [item for item in full if search == item[2]]
                return result

    def update_fentry(self, values):
        update = [value for value in values if value[0] in self._fentry.keys() and len(value) == 2]
        self._fentry.update(update)

    def update_mentry(self, values):
        update = [value for value in values if value[0] in self._mentry.keys() and len(value) == 2]
        self._mentry.update(update)

    def update_dentry(self, values):
        update = [value for value in values if value[0] in self._dentry.keys() and len(value) == 2]
        self._dentry.update(update)


