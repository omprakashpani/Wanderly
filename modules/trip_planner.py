from modules.db import query_all, execute

def save_plan(user_id, trip_name, start_date, end_date, monasteries_csv, preferences):
    return execute('INSERT INTO trip_planner (user_id, trip_name, start_date, end_date, monasteries_selected, preferences, created_at) VALUES (%s,%s,%s,%s,%s,%s,NOW())',
                   (user_id, trip_name, start_date, end_date, monasteries_csv, preferences))

def recent_plans(user_id, limit=20):
    return query_all('SELECT * FROM trip_planner WHERE user_id=%s ORDER BY created_at DESC LIMIT %s', (user_id, limit))
