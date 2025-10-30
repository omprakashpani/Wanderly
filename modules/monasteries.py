from modules.db import query_all, query_one

def get_monasteries(limit=None):
    if limit:
        return query_all('SELECT * FROM monasteries ORDER BY name ASC LIMIT %s', (limit,))
    return query_all('SELECT * FROM monasteries ORDER BY name ASC')

def get_monastery(mid):
    return query_one('SELECT * FROM monasteries WHERE id=%s', (mid,))
