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
        self.fields = [item for item in list(Fields()) if item != '']
        self.setup_tables()
        self._days = self.init_calendar()

        self._fid = self.get_max_id('food')
        self._mid = self.get_max_id('meals')
        self._did = self.get_max_id('days')

        self._fentry = {k: v for (k, v) in map(lambda x: (x, 'NA'), self.fields[1:])}
        self._mentry = {k: v for (k, v) in map(lambda x: (x, 'NA'), ['name', 'ingredients', 'serving size'])}
        self._dentry = {k: v for (k, v) in map(lambda x: (x, 'NA'), ['day', 'entry', 'serving size'])}

    def get_max_id(self, table: str):

        """
        Gets the maximum ID of the specified table and raises it by one to prepare for the passing of a new entry.
        If the table is empty or non existent returns 0 instead.
        :param table: 'food', 'fdata', 'meals' or 'days'
        :return: maxid + 1 or 0 if table empty or non existent
        """

        try:
            self.cursor.execute(f'SELECT MAX(ID) FROM {table}')
            result = self.cursor.fetchone()[0]
            if result is not None:
                return int(result) + 1

            else:
                return 0

        except sqlite3.OperationalError:
            return 0

    def load_food_data(self, file: str):

        """
        Loads the food data from a csv file and passes it into the fdata table for further usage.
        :param file: path to csvfile which contains fooddata
        :return: None
        """

        initialize(file)

    def setup_tables(self):
        """
        Tries to create the tables for food, meals and days by calling each tables init_x function.
        :return: None
        """


        try:
            self.init_food()
        except sqlite3.OperationalError:
            pass

        try:
            self.init_meals()
        except sqlite3.OperationalError:
            pass

        try:
            self.init_days()
        except sqlite3.OperationalError:
            pass

    def init_food(self):
        """
        Creates the food table in the tracknut database.
        :return: None
        """
        try:
            sql = """CREATE TABLE food ('ID' INTEGER PRIMARY KEY,
                  'Name' TEXT, 'Category' TEXT, 'Calories' REAL, 
                  'Carbohydrates' REAL, 'Total Sugar' REAL,
                  'Total Fat' REAL, 'Saturated Fats' REAL,
                  'Fiber' REAL,  'Protein' REAL, 'Salt' REAL)
                  """.replace('\n', '')
            self.cursor.execute(sql)
        except sqlite3.OperationalError:
            raise sqlite3.OperationalError('Initialization already completed')

    def init_meals(self):
        """
        Creates the meal table in the tracknut database.
        :return: None
        """

        try:
            self.cursor.execute('CREATE TABLE meals (ID INTEGER PRIMARY KEY, name, ingredients, serving size)')
        except sqlite3.OperationalError:
            raise sqlite3.OperationalError('Initialization already completed')

    def init_days(self):
        """
        Creates the days table in the tracknut database.
        :return: None
        """
        try:
            self.cursor.execute('CREATE TABLE days (ID INTEGER PRIMARY KEY, day, entry, serving size)')
        except sqlite3.OperationalError:
            raise sqlite3.OperationalError('Initialization already completed')

    def init_calendar(self):
        """
        Creates a list of days in the format 'Wkd yyyy-mm-dd' as template to pass values to the days table.
        :return: None
        """

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

    def insert_food(self, entry: list = None) -> None:

        """
        Inserts a food entry into the tracknut food database. The entry parameter is set to None by default and will
        use the private self._fentry variable to pass the value to the database. If entry is specified, it needs to
        be a list of values for each column in the food database, except the ID. By default those columns are:
        Name, Category, Calories, Carbohydrates, Total Sugar, Total Fat, Saturated Fats, Fiber, Protein, Salt
        :param entry: None (self._fentry is used) or list of values: [Name, Cat, kcal, carbs, sugar, total fat, sat.fat,
        fiber, protein, salt]
        :return: None
        """

        if not entry:
            entry = list(self._fentry.values())

        values = [self._fid] + entry
        sql = 'INSERT INTO food VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
        self.cursor.execute(sql, values)
        self.connection.commit()
        self._fid += 1
        self._fentry = {k: v for (k, v) in map(lambda x: (x, 'NA'), self.fields)}

    def insert_meal(self, name: str , ingredients: dict, serving: int | float) -> None:

        """
        Inserts a meal entry into the tracknut database. The ID is generated automatically, only name, ingredients dict
        and serving size need to be provided

        :param name: string of desired meal name
        :param ingredients: dict of ingredients from the food database. Keys are food IDs, values are amount in gram.
        :param serving: serving size in gram
        :return: None
        """

        values = [str(self._mid), name, str(ingredients), str(serving)]
        sql = f'INSERT INTO meals VALUES(?, ?, ?, ?)'
        self.cursor.execute(sql, values)
        self.connection.commit()
        self._mid += 1
        self._mentry = {k: v for (k, v) in map(lambda x: (x, 'NA'), ['name', 'ingredients', 'serving size'])}

    def insert_in_day(self, entry: list = None) -> None:
        """
        Inserts a meal or food entry into the database on the given day. Those entries are later used to generate the
        daily summary of the nutrition intake. If entry is not specified, the self._dentry variable is used.

        :param entry: None (self._dentry is used) or list of [day, entry, serving size]
        :return: None
        """
        if not entry:
            entry = self._dentry.values()

        if 'NA' in entry:
            raise ValueError('Entry is not complete')

        else:
            values = [self._did] + entry
            sql = f'INSERT INTO days VALUES (?, ?, ?, ?)'
            self.cursor.execute(sql, values)
            self._did += 1
            self._dentry = {k: v for (k, v) in map(lambda x: (x, 'NA'), ['day', 'entry', 'serving size'])}

    def go_to_day(self, day: str) -> None:

        """
        Checks the format and sets the day value of the self._dentry variable.
        Used to browse through the database for fetching and passing entries.

        :param day: Day to be set in the format Wkd yyyy-mm-dd , example: Sat 2023-07-22
        :return: None
        """

        if day in self._days:
            self._dentry['day'] = day

        else:
            raise ValueError('Day does not exist. Format of day should resemble: Sat 2023-07-22')

    def get_food(self, search: str | int ='all', strict=False) -> list | tuple:
        """
        Fetches items from the food table based on the value of the search parameter. The standard value of
        search is 'all', which fetches all the values from the database. If another string is specified, only values
        containing that string in the name are fetched. If strict is set to True,
        the string must match the name exactly. If an integer is passed, value with the unique ID of set integer is
        returned.
        :param search: 'all', string (search by name) or integer (search by ID)
        :param strict: False (string in item name) or False (string == item name)
        :return: list of tuples or tuple of item(s) matching search parameter.
        """

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

    def get_meal(self, search='all', strict=False) -> list | tuple :
        """
        Fetches items from the meals table based on the value of the search parameter. The standard value of
        search is 'all', which fetches all the items from the database. If another string is specified, only values
        containing that string in the name are fetched. If strict is set to True,
        the string must match the name exactly. If an integer is passed, value with the unique ID of set integer is
        returned.
        :param search: 'all', string (search by name) or integer (search by ID)
        :param strict: False (string in item name) or False (string == item name)
        :return: list of tuples or tuple of item(s) matching search parameter
        """
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
                result = [item for item in full if search in item[1]]
                return result

            elif strict:
                self.cursor.execute('SELECT * FROM meals')
                full = self.cursor.fetchall()
                result = [item for item in full if search == item[2]]
                return result

    def get_fdata(self, search='all', strict=False) -> list | tuple:
        """
        Fetches items from the from fooddata table based on the value of the search parameter. The standard value of
        search is 'all', which fetches all the items from the database. If another string is specified, only values
        containing that string in the name are fetched. If strict is set to True,
        the string must match the name exactly. If an integer is passed, value with the unique ID of set integer is
        returned.
        :param search: 'all', string (search by name) or integer (search by ID)
        :param strict: False (string in item name) or False (string == item name)
        :return: list of tuples or tuple of item(s) matching search parameter
        """

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

    def get_day(self, search: str ='all') -> list:
        """
        Fetches all items appended to day(s) in the days table based on the search parameter. The standard parameter
        'all' fetches all entries from the food database. If a day value is passed in the format Wkd yyyy-mm-dd only
        entries appended to that day are returned.
        :param search: 'all' or day in format 'Wkd yyy-mm-dd', example Sat 2023-07-22.
        :return: list of items appended to day(s) in days table
        """
        if search == 'all':
            self.cursor.execute('SELECT * FROM days')
            result = self.cursor.fetchall()
            return result

        if search in self._days:
            self.cursor.execute(f'SELECT * FROM days WHERE (Day = \'{search}\')')

        else:
            raise ValueError('Day is non existent or formatted wrong. Day format should be \'Sat 2023-07-22\'')

    def update_fentry(self, values: list) -> None:
        """
        Update the self._fentry variable for later passing into the database tables. The update needs to be a list of
        tuples, where the first item specifies the key and the second item specifies the value.
        Possible keys are 'Name', 'Category', 'Calories',
        'Carbohydrates', 'Total Sugar', 'Total Fat', 'Saturated Fats', 'Fiber', 'Protein', 'Salt'
        :param values: list of tuples example [('Name', 'Tofu'), ('Total Fat', 12)]
        :return: None
        """
        update = [value for value in values if value[0] in self._fentry.keys() and len(value) == 2]
        self._fentry.update(update)

    def update_mentry(self, values: list) -> None:
        """
        Update the self._mentry variable for later passing into the database tables. The update needs to be a list of
        tuples, where the first item specifies the key and the second item specifies the value. The ingredients value
        must be a dict of IDs from the food table with corresponding amounts in gram.
        Possible keys are 'name', 'ingredients', 'serving size'
        :param values: list of tuples example [('name', 'Tofu with Veggies'), ('Ingedients', {'5': 22.4, '2' : 43.2})]
        :return: None
        """

        update = [value for value in values if value[0] in self._mentry.keys() and len(value) == 2]
        self._mentry.update(update)

    def update_dentry(self, values): -> None
        """
        Update the self._mentry variable for later passing into the database tables. The update needs to be a list of
        tuples, where the first item specifies the key and the second item specifies the value. Entry specifies the ID
        of food or meal passed into the database.
        Possible keys are 'day', 'entry', 'serving size'
        :param values: list of tuples example [('day', 'Sat 2023-07-22'), ('entry', '5')]
        :return: None
        """
        update = [value for value in values if value[0] in self._dentry.keys() and len(value) == 2]
        self._dentry.update(update)
