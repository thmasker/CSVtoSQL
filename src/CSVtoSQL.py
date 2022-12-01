import csv
import os
import sys

INSERT_CLAUSE = "INSERT INTO {table} ({columns}) VALUES ({values});\n"
SCHEMA_CONVERSIONS = {
    'VARCHAR2': lambda x: "'" + str(x) + "'",
    'NUMBER': lambda x: x
}


def parse_argv(argv):
    if len(argv) < 4:
        sys.exit('Not enough arguments. Usage: ' + os.path.basename(__file__)
                 + ' table_name csv_file schema_file csv_delimiter')


def parse_csv(table, input_file, schema, delimiter=','):
    output_file = os.path.splitext(input_file)[0] + '.sql'

    with open(schema) as csv_schema:
        sql_schema = next(csv.DictReader(csv_schema, delimiter=delimiter))

        with open(input_file) as csv_file:
            rows = csv.DictReader(csv_file, delimiter=delimiter)

            with open(output_file, mode='w') as sql_file:
                for row in rows:
                    columns, values = [], []
                    for column in sql_schema.keys():
                        if column in row:
                            if row[column]:
                                columns.append(column)
                                values.append(SCHEMA_CONVERSIONS[sql_schema[column]](row[column]))
                        else:
                            columns.append(column)
                            values.append(sql_schema[column])

                    sql_file.write(
                        INSERT_CLAUSE.format(table=table, columns=', '.join(columns), values=', '.join(values)))


if __name__ == '__main__':
    parse_argv(sys.argv)
    parse_csv(*sys.argv[1:])
