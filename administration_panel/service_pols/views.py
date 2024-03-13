from django.http import JsonResponse
import json
import sqlite3

user_skid = [2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 2900, 3000, 3100, 3200, 3300, 3400, 3500, 3600, 3700, 3800, 3900, 4000, 4100, 4200]

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

def logic_main(microcategory_id, location_id, user_id): #доделать построение и ретюрн json с нужными данными (смотреть в методичке) + функцию выявления скидки
    global user_skid
    
    with open('путь к файлу', 'r') as file:
        id_mat_base = file.readline().strip()
        id_mat_dis = file.readline()[1].split()[0]
    
    if user_id not in user_skid:
        return logic_base(microcategory_id, location_id, user_id, id_mat_base)
    else:
        return logic_skid(microcategory_id, location_id, user_id, id_mat_dis)

def logic_base(microcategory_id, location_id, user_id, id_mat_base):
    pri = ''
    conn = sqlite3.connect(':memory:')
    c = conn.cursor()
    with open(f'baseline_matrix_{id_mat_base}.sql', 'r') as f:
        sql_script = f.read()
    c.executescript(sql_script)
    c.execute(f'''
        SELECT * FROM baseline_matrix_{id_mat_base} WHERE microcategory_id = {microcategory_id} AND location_id = {location_id}
    ''')
    results = c.fetchall()
    for row in results:
        pri = row[2]
    if pri == '':
        logic_base(microcategory_id, location_id, user_id, id_mat_base-1)
    else:
        json_otv = {
            'prise': pri,
            'location_id': location_id,
            'microcategory_id': microcategory_id,
            'matrix_id': id_mat_base,
            'user_segment_id': user_id
        }
        return json_otv

def logic_skid(microcategory_id, location_id, user_id, id_mat_base, id_mat_dis): #выявление, есть ли скидка
    if id_mat_dis == 0:
        logic_base(microcategory_id, location_id, user_id, id_mat_base)
    else:
        pri = ''
        conn = sqlite3.connect(':memory:')
        c = conn.cursor()
        with open('discount_matrix_{id_mat_dis}.sql', 'r') as f:
            sql_script = f.read()
        c.executescript(sql_script)
        c.execute(f'''
            SELECT * FROM discount_matrix_{id_mat_dis} WHERE microcategory_id = {microcategory_id} AND location_id = {location_id}
        ''')
        results = c.fetchall()
        for row in results:
            pri = str(row[2])
        if pri == '':    
            logic_skid(microcategory_id, location_id, user_id, id_mat_dis-1)
        else:
            json_otv = {
                'prise': pri,
                'location_id': location_id,
                'microcategory_id': microcategory_id,
                'matrix_id': id_mat_dis,
                'user_segment_id': user_id
            }
            return json_otv
