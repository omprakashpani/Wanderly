from modules.db import query_all

def get_foods(limit=50):
    return query_all('SELECT * FROM foods ORDER BY id ASC LIMIT %s', (limit,))

def get_cuisines(limit=50):
    return query_all('SELECT * FROM cuisines ORDER BY id ASC LIMIT %s', (limit,))
