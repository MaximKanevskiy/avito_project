import sqlite3

baseline_matrix_line_id = 0
discount_matrix_line_id = 1


def get_last_matrix_id(line_number):
    with open('administration_panel/last_matrix_ids.txt', 'r') as file:
        lines = file.readlines()
        try:
            return int(lines[line_number].strip())
        except IndexError:
            print(f"Error: File doesn't have line number {line_number}")
        except ValueError:
            print("Error: Can't convert line to integer")


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
