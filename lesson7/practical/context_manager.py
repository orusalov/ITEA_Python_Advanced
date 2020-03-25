import sqlite3

def beautify_dataset(description, dataset):

    names = [d[0] for d in description]

    longest_attr = [len(d[0]) for d in description]

    rows = []


    for row in dataset:
        longest_attr = list(map(lambda x,y: max(x, y), longest_attr, [len(atr) for atr in row]))

    names = list(map(lambda string, length: f'{string}{" " * (length - len(string))}', names, longest_attr))
    rows.append(' | '.join(names))
    rows.append(len(' | '.join(names)) * '-')

    for row in dataset:
        rows.append(
            ' | '.join(
                list(
                    map(
                        lambda string, length: f'{string}{" " * (length - len(string))}',
                        row,
                        longest_attr
                    )
                )
            )
        )

    return '\n'.join(rows)

class MyDBContextManager:

    def __init__(self, dbname):
        self.dbname = dbname

    def __enter__(self):
        self.conn = sqlite3.connect(self.dbname)
        return self.conn

    def __exit__(self, *args):
        self.conn.close()


def main():
    try:
        with MyDBContextManager('sqlite_my1.db') as conn:

            cursor1 = conn.cursor()
            cursor2 = conn.cursor()

            print(cursor1 == cursor2)
            print(cursor1 is cursor2)

            try:
                sql1 = "create table my_own_table(id int primary key, some_text text)"
                cursor1.execute(sql1)
            except sqlite3.DatabaseError as err:
                if err == 'table my_own_table already exists':
                    pass

            sql2 = "insert into my_own_table values(1, 'first data')"

            cursor2.execute(sql2)

            print(conn.cursor().execute('select * from my_own_table').fetchall())

    except sqlite3.DatabaseError as err:
        print(err)


if __name__ == '__main__':
    main()
