import random

import pandas


class Generator:
    def generate(self):
        raise NotImplementedError


class FloatGenerator(Generator):
    def __init__(self, min, max):
        self.min = min
        self.max = max

    def generate(self):
        return random.uniform(self.min, self.max)


class IntGenerator(Generator):
    def __init__(self, min, max):
        self.min = min
        self.max = max

    def generate(self):
        return random.randint(self.min, self.max)


class ChoiceGenerator(Generator):
    def __init__(self, choices):
        self.choices = choices

    def generate(self):
        return random.choice(self.choices)


def generate_more_data(df: pandas.DataFrame, rows_to_generate=100):
    generators = dict()
    columns = list(df.columns)
    for col_name, col_type in zip(columns, df.dtypes):
        if col_type == "float64":
            min_value, max_value = df[col_name].min(), df[col_name].max()
            generators[col_name] = FloatGenerator(min_value, max_value)
        elif col_type == "int64":
            min_value, max_value = df[col_name].min(), df[col_name].max()
            generators[col_name] = IntGenerator(min_value, max_value)
        elif col_type == "object":
            unique_values = df[col_name].unique()
            generators[col_name] = ChoiceGenerator(unique_values)
        else:
            raise Exception("Unsupported type " + col_type)

    new_data = []
    for _ in range(rows_to_generate):
        row = tuple(generators[col_name].generate() for col_name in columns)
        new_data.append(row)

    new_df = pandas.DataFrame(columns=columns, data=new_data)
    return df.append(new_df, ignore_index=True)
