class Fields:

    def __init__(self):

        # Initialization of fields file
        try:
            open('database/fields', 'xt').close()
            # Insert standard fields
            with open('database/fields', 'wt') as file:
                stdfields = [item + ', \n' for item in ['Category','Name','Nutrient Databank Number',
                                                        'Alpha Carotene', 'Beta Carotene', 'Beta Cryptoxanthin',
                                                        'Carbohydrate', 'Cholesterol', 'Choline', 'Fiber',
                                                        'Lutein and Zeaxanthin', 'Lycopene', 'Niacin', 'Protein',
                                                        'Retinol', 'Riboflavin', 'Selenium', 'Sugar Total', 'Thiamin',
                                                        'Water', 'Monosaturated Fat', 'Polysaturated Fat',
                                                        'Saturated Fat', 'Total Lipid', 'Calcium', 'Copper', 'Iron',
                                                        'Magnesium', 'Phosphorus', 'Potassium', 'Sodium', 'Zinc',
                                                        'Vitamin A', 'Vitamin B12', 'Vitamin B6',
                                                        'Vitamin C', 'Vitamin E', 'Vitamin K']]
                file.writelines(stdfields)

        except FileExistsError:
            pass

        with open('database/fields', 'rt') as file:
            self.fields = list(file.read().split(', \n'))

            self._itercurr = 0
            self._iterend = len(self.fields)

    def add_item(self, item: str) -> None :
        '''
        Adds an item to the list of fields for the user-defined food catalog.
        :param item: Item to be added
        :return: None
        '''

        if item not in self.fields:
            try:
                with open('database/fields', 'at') as file:
                    file.write(f'{item}, \n')

                with open('database/fields', 'rt') as file:
                    self.fields = list(file.read().split(', \n'))

            except:  # TODO
                raise

        else:
            raise ValueError('Item already exists in fields.')

    def __str__(self):
        return str(self.fields)

    def __iter__(self):
        while self._itercurr < self._iterend:
            yield self.fields[self._itercurr]
            self._itercurr += 1

    def __next__(self):
        if self._itercurr > self._iterend:
            self._itercurr = 0
            raise StopIteration

        else:
            self._itercurr += 1
