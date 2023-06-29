class Fields:

    def __init__(self):

        # Initialization of fields file
        try:
            open('fields', 'xt').close()
            # Insert standard fields
            with open('fields', 'wt') as file:
                file.write("""'Alpha Carotene', 'Beta Carotene', 'Beta Cryptoxanthin',
                            'Carbohydrate', 'Cholesterol', 'Choline', 'Fiber',
                            'Lutein and Zeaxanthin', 'Lycopene', 'Niacin', 'Protein',
                            'Retinol', 'Riboflavin', 'Selenium', 'Sugar Total', 'Thiamin',
                            'Water', 'Monosaturated Fat', 'Polysaturated Fat', 'Saturated Fat',
                            'Total Lipid', 'Calcium', 'Copper', 'Iron', 'Magnesium', 'Phosphorus',
                            'Potassium', 'Sodium', 'Zinc', 'Vitamin A - RAE', 'Vitamin B12', 'Vitamin B6',
                            'Vitamin C', 'Vitamin E', 'Vitamin K'"""
                           )


        except FileExistsError:
            pass

        with open('fields', 'rt') as file:
            self.fields = list(file.read())

    def add_item(self, item):
        try:
            with open('fields', 'at') as file:
                file.write(f", '{item}'")

        except: # TODO
            raise




