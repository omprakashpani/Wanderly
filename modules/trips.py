from modules.db import query_all, query_one, execute

def get_trips(limit=50):
    return query_all('SELECT * FROM trips ORDER BY id DESC LIMIT %s', (limit,))

def get_trip_by_id(tid):
    return query_one('SELECT * FROM trips WHERE id=%s', (tid,))

def create_trip(title, description, image_url=None):
    return execute('INSERT INTO trips (title, description, image_url) VALUES (%s,%s,%s)', (title, description, image_url))
