import sqlite3
import datetime

baseline_matrix_line_id = 0
discount_matrix_line_id = 1


def get_last_matrix_id(line_number: int):
    with open('administration_panel/last_matrix_ids.txt', 'r') as file:
        lines = file.readlines()
        try:
            return int(lines[line_number].strip())
        except IndexError:
            print(f"Error: File doesn't have line number {line_number}")
        except ValueError:
            print("Error: Can't convert line to integer")


def set_last_matrix_id(line_number: int):
    with open('administration_panel/last_matrix_ids.txt', 'r') as f:
        lines = f.readlines()
        lines[line_number] = str(int(get_last_matrix_id(line_number)) + 1)
        if line_number == 1:
            lines[line_number] += '\n'
    with open('administration_panel/last_matrix_ids.txt', 'w') as f:
        f.writelines(lines)


def get_price(category_id: int, location_id: int, matrix_type: str, matrix_id: int = None):
    price = None

    if matrix_type == 'baseline':
        if matrix_id is None:
            matrix_id = get_last_matrix_id(baseline_matrix_line_id)
        while matrix_id > 0:
            conn = sqlite3.connect(':memory:')
            c = conn.cursor()
            with open(f'administration_panel/service_pols/baseline_matrix_{matrix_id}.sql', 'r') as f:
                sql_script = f.read()
            c.executescript(sql_script)
            c.execute(f'''
        SELECT * FROM baseline_matrix_{matrix_id} WHERE microcategory_id = {category_id} AND location_id = {location_id}
                ''')
            results = c.fetchall()
            if results:
                for row in results:
                    price = row[2]
                if price is not None:
                    return int(price)
            matrix_id -= 1

    elif matrix_type == 'discount':
        if matrix_id is None:
            matrix_id = get_last_matrix_id(discount_matrix_line_id)
        while matrix_id > 0:
            conn = sqlite3.connect(':memory:')
            c = conn.cursor()
            with open(f'administration_panel/service_pols/discount_matrix_{matrix_id}.sql', 'r') as f:
                sql_script = f.read()
            c.executescript(sql_script)
            c.execute(f'''
        SELECT * FROM discount_matrix_{matrix_id} WHERE microcategory_id = {category_id} AND location_id = {location_id}
                    ''')
            results = c.fetchall()
            if results:
                for row in results:
                    price = row[2]
                if price is not None:
                    return int(price)
            matrix_id -= 1

    return None


def get_date() -> str:
    return datetime.datetime.now().strftime('%Y-%m-%d')


def set_last_change(matrix_type: str):
    with open('administration_panel/logs.txt', 'r') as f:
        lines = f.readlines()
    if matrix_type == 'baseline':
        lines[0] = get_date() + '\n'
    elif matrix_type == 'discount':
        lines[1] = get_date()
    with open('administration_panel/logs.txt', 'w') as f:
        f.writelines(lines)


def get_last_change(matrix_type: str, logs_path: str) -> str:
    with open(logs_path, 'r') as f:
        lines = f.readlines()
        if matrix_type == 'baseline':
            if lines[0] == get_date():
                return lines[0]
            else:
                set_last_change('baseline')
                return lines[0]
        elif matrix_type == 'discount':
            if lines[1] == get_date():
                return lines[1]
            else:
                set_last_change('discount')
                return lines[1]


def set_new_price(category_id: int, location_id: int, new_price: int, matrix_type: str, logs_path: str):
    with open(logs_path, 'r') as f:
        lines = f.readlines()
    if matrix_type == 'baseline':
        last_id = get_last_matrix_id(baseline_matrix_line_id)
        if get_date() == lines[0]:
            conn = sqlite3.connect(':memory:')
            c = conn.cursor()
            with open(f"administration_panel/service_pols/baseline_matrix_{last_id}.sql", "r") as file:
                sql_script = file.read()
            c.executescript(sql_script)
            c.execute(f'''
                    insert into baseline_matrix_{last_id} (microcategory_id, location_id, price)
                    values ({category_id}, {location_id}, {new_price});
                  ''')
        else:
            set_last_matrix_id(baseline_matrix_line_id)
            new_last_id = get_last_matrix_id(baseline_matrix_line_id)
            set_last_change('baseline')
            with open(f"administration_panel/service_pols/baseline_matrix_{new_last_id}.sql", "w") as file:
                file.write(f'''create table baseline_matrix_{new_last_id}(
                        microcategory_id int,
                        location_id int,
                        price int
                    );
    
                    insert into baseline_matrix_{new_last_id} (microcategory_id, location_id, price)
                    values ({category_id}, {location_id}, {new_price});'''
                           )

    if matrix_type == 'discount':
        last_id = get_last_matrix_id(baseline_matrix_line_id)
        if get_date() == lines[0]:
            conn = sqlite3.connect(':memory:')
            c = conn.cursor()
            with open(f"administration_panel/service_pols/discount_matrix_{last_id}.sql", "r") as file:
                sql_script = file.read()
            c.executescript(sql_script)
            c.execute(f'''
                    insert into discount_matrix_{last_id} (microcategory_id, location_id, price)
                    values ({category_id}, {location_id}, {new_price});
                  ''')
        else:
            set_last_matrix_id(discount_matrix_line_id)
            new_last_id = get_last_matrix_id(discount_matrix_line_id)
            set_last_change('discount')
            with open(f"administration_panel/service_pols/discount_matrix_{new_last_id}.sql", "w") as file:
                file.write(f'''create table discount_matrix_{new_last_id}(
                        microcategory_id int,
                        location_id int,
                        price int
                    );

                    insert into discount_matrix_{new_last_id} (microcategory_id, location_id, price)
                    values ({category_id}, {location_id}, {new_price});'''
                           )
