import pymysql


DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "wandely_user",          
    "password": "wander123",         
    "db": "wandely",                
    "cursorclass": pymysql.cursors.DictCursor,
    "autocommit": True
}

def get_db():
    """Get a new database connection"""
    return pymysql.connect(**DB_CONFIG)

def query_one(sql, params=None):
    """Fetch a single record"""
    with get_db().cursor() as cur:
        cur.execute(sql, params)
        return cur.fetchone()

def query_all(sql, params=None):
    """Fetch all records"""
    with get_db().cursor() as cur:
        cur.execute(sql, params)
        return cur.fetchall()

def execute(sql, params=None):
    """Execute INSERT, UPDATE, DELETE"""
    with get_db().cursor() as cur:
        cur.execute(sql, params)

def close_db():
    """Close DB connection (handled automatically here)"""
    pass
