class Fields:

    def __init__(self):

        # Initialization of fields file
        try:
            open('fields', 'xt').close()
            # Insert standard fields
            with open('fields', 'wt') as file:
                stdfields = [item + ', \n' for item in ['Alpha Carotene', 'Beta Carotene', 'Beta Cryptoxanthin',
                                                        'Carbohydrate', 'Cholesterol', 'Choline', 'Fiber',
                                                        'Lutein and Zeaxanthin', 'Lycopene', 'Niacin', 'Protein',
                                                        'Retinol', 'Riboflavin', 'Selenium', 'Sugar Total', 'Thiamin',
                                                        'Water', 'Monosaturated Fat', 'Polysaturated Fat',
                                                        'Saturated Fat', 'Total Lipid', 'Calcium', 'Copper', 'Iron',
                                                        'Magnesium', 'Phosphorus', 'Potassium', 'Sodium', 'Zinc',
                                                        'Vitamin A - RAE', 'Vitamin B12', 'Vitamin B6',
                                                        'Vitamin C', 'Vitamin E', 'Vitamin K']]
                file.writelines(stdfields)

        except FileExistsError:
            pass

        with open('fields', 'rt') as file:
            self.fields = list(file.read().split(', \n'))

    def add_item(self, item):

        if item not in self.fields:
            try:
                with open('fields', 'at') as file:
                    file.write(f'{item}, \n')

                with open('fields', 'rt') as file:
                    self.fields = list(file.read().split(', \n'))

            except:  # TODO
                raise

        else:
            raise ValueError('Item already exists in fields.')

    def __str__(self):
        return str(self.fields)
