import random

def db_get_user_requests(conn, conn_mutex):
    conn_mutex.acquire()

    try:
        c = conn.cursor()
        c.execute("SELECT id, request FROM user_requests WHERE processed = False")
        requests = list(c.fetchall())
    except Exception:
        requests = []
    finally:
        conn_mutex.release()

    return requests

def db_set_poetry(conn, conn_mutex, poetry, request_id):
    conn_mutex.acquire()
    
    try:
        c = conn.cursor()
        c.execute("INSERT INTO poetry (poem, sent) VALUES (?, False)", (poetry,))
        conn.commit()

        c.execute("UPDATE user_requests SET processed = True WHERE id = (?)", (request_id,))
        conn.commit()
    finally:
        conn_mutex.release()

def db_get_last_poetry(conn, conn_mutex):
    conn_mutex.acquire()

    try:
        c = conn.cursor()
        c.execute("SELECT id, poem FROM \"poetry\" WHERE sent = False ORDER BY id LIMIT 1")
        rows = list(c.fetchall())
    except Exception:
        rows = []
    finally:
        conn_mutex.release()

    return rows

def db_get_random_poetry(conn, conn_mutex):
    conn_mutex.acquire()
    try:
        c = conn.cursor()
        c.execute("SELECT id FROM \"poetry\"")
        ids = list(c.fetchall())
        poetry_id = random.choice(ids)[0]
        c.execute("SELECT poem FROM \"poetry\" WHERE id = (?) LIMIT 1", (poetry_id,))
        poetry = list(c.fetchall())[0][0]
    except Exception:
        poetry = []
    finally:
        conn_mutex.release()

    return poetry

def db_set_poetry_sent(conn, conn_mutex, poetry_id):
    conn_mutex.acquire()

    try:
        c = conn.cursor()
        c.execute("UPDATE \"poetry\" SET sent = True WHERE id = (?)", (poetry_id,))
        conn.commit()
    finally:
        conn_mutex.release()

def db_post_user_request(conn, conn_mutex, user_request):
    conn_mutex.acquire()
    try:
        c = conn.cursor()
        c.execute('''INSERT INTO user_requests (request, processed) VALUES (?, False)''', (user_request,))
        conn.commit()
    finally:
        conn_mutex.release()
