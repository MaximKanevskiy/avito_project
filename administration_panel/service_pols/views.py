from django.http import JsonResponse
import json
import sqlite3

user_skid = [2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 2900, 3000, 3100, 3200, 3300, 3400, 3500, 3600, 3700, 3800,
             3900, 4000, 4100, 4200]


def main(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

        kat_id = data.get('microcategory_id')
        loc_id = data.get('location_id')
        us_id = data.get('user_id')

        return JsonResponse(logic_main(kat_id, loc_id, us_id))
    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)


def logic_main(microcategory_id, location_id, user_id):  # доделать построение и ретюрн json с нужными данными
    # (смотреть в методичке) + функцию выявления скидки
    global user_skid
    if user_id not in user_skid:
        return logic_base(microcategory_id, location_id, user_id)
    else:
        return logic_skid(microcategory_id, location_id, user_id)


def logic_base(microcategory_id, location_id, user_id):
    pri = ''
    conn = sqlite3.connect(':memory:')
    c = conn.cursor()
    with open('baseline_matrix_3.sql', 'r') as f:
        sql_script = f.read()
    c.executescript(sql_script)
    c.execute(f'''
        SELECT * FROM baseline_matrix_3 WHERE microcategory_id = {microcategory_id} AND location_id = {location_id}
    ''')
    results = c.fetchall()
    for row in results:
        pri = row[2]
    json_otv = {
        'prise': pri,
        'location_id': location_id,
        'microcategory_id': microcategory_id,
        'matrix_id': 'base_3',
        'user_segment_id': user_id
    }
    return json_otv


def logic_skid(microcategory_id, location_id, user_id):  # выявление, есть ли скидка
    pri = ''
    conn = sqlite3.connect(':memory:')
    c = conn.cursor()
    with open('discount_matrix_3.sql', 'r') as f:
        sql_script = f.read()
    c.executescript(sql_script)
    c.execute(f'''
        SELECT * FROM discount_matrix_3 WHERE microcategory_id = {microcategory_id} AND location_id = {location_id}
    ''')
    results = c.fetchall()
    for row in results:
        pri = str(row[2])
    if pri == '':
        print('не нашли в 3')
        pri = ''
        conn = sqlite3.connect(':memory:')
        c = conn.cursor()
        with open('discount_matrix_2.sql', 'r') as f:
            sql_script = f.read()
        c.executescript(sql_script)
        c.execute(f'''
            SELECT * FROM discount_matrix_2 WHERE microcategory_id = {microcategory_id} AND location_id = {location_id}
        ''')
        results = c.fetchall()
        for row in results:
            pri = str(row[2])
        if pri == '':
            print('не нашли в 2')
            pri = ''
            conn = sqlite3.connect(':memory:')
            c = conn.cursor()
            with open('discount_matrix_1.sql', 'r') as f:
                sql_script = f.read()
            c.executescript(sql_script)
            c.execute(f'''
                SELECT * FROM discount_matrix_1 WHERE microcategory_id = {microcategory_id} AND location_id = {location_id}
            ''')
            results = c.fetchall()
            for row in results:
                pri = str(row[2])
            if pri == '':
                print('не нашли в 1')
                logic_base(microcategory_id, location_id, user_id)
            else:
                json_otv = {
                    'prise': pri,
                    'location_id': location_id,
                    'microcategory_id': microcategory_id,
                    'matrix_id': 'dis_1',
                    'user_segment_id': user_id
                }
        else:
            json_otv = {
                'prise': pri,
                'location_id': location_id,
                'microcategory_id': microcategory_id,
                'matrix_id': 'dis_2',
                'user_segment_id': user_id
            }
    else:
        json_otv = {
            'prise': pri,
            'location_id': location_id,
            'microcategory_id': microcategory_id,
            'matrix_id': 'dis_3',
            'user_segment_id': user_id
        }
    return json_otv
