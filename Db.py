from database.initialize import initialize
import sqlite3

class Db():

    '''
    Base Database Class for tracknut
    that will perform all the operations
    '''

    def __init__(self):
        self.connection = sqlite3.connect('database/food_data.db')
        self.cursor = self.connection.cursor()
        self.get_max_fid()


    def get_max_fid(self):
        self.cursor.execute('SELECT MAX(ID) FROM food')
        result = self.cursor.fetchone()[0]
        if result is not None:
            self.fid = int(result) + 1

        else:
            self.fid = 0


    def initialize(self, file):
        initialize(file)

    def init_foodtable(self, headers:list):
        try:
            self.fth = [header.replace('.', '').replace(' ', '').replace('-', '') for header in list(headers)]
            self.fthstring = ', '.join(['\'' + header.replace('\'', '').replace('"', '') + '\'' for header in self.fth])
            self.cursor.execute(f'CREATE TABLE food (\'ID\', {self.fthstring})')
        except sqlite3.OperationalError:
            raise sqlite3.OperationalError('Initialization already completed')


    def insert_food(self, values:list):
        self.ftv = [str(value) for value in list(values)]
        self.ftvstring = ', '.join(['\'' + value.replace('\'', '').replace('"', '') + '\'' for value in self.ftv])
        self.cursor.execute(f'INSERT INTO food VALUES(\'{self.fid}\',{self.ftvstring})')
        self.connection.commit()
        self.fid += 1

    def init_meals(self):
        self.cursor.execute(f'CREATE TABLE meals (ID, meal')

    def init_calendar(self): # TODO
        pass












