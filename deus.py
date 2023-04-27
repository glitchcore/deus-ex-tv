import openai
import sqlite3
import random
import json
import threading
import http.server
import socketserver
import urllib
import re

import configuration
from ai_poetry import ai_poetry
from ai_describer import ai_describe


openai.api_key = configuration.api_key

def generate_poetry_thread(ai, conn, conn_mutex, event):
    TOPIC_LEN = 5
    topics = ["nothing"]
    
    while True:
        c = conn.cursor()
        conn_mutex.acquire()
        c.execute("SELECT id, request FROM user_requests WHERE processed = False")
        requests = list(c.fetchall())
        conn_mutex.release()

        for request in requests:
            topics += [ai_describe(openai, request[1])]
            topics = topics[-TOPIC_LEN:]

            poetry = ai_poetry(openai, topics)

            print("=== poetry ===")
            for line in zip(*poetry.values()):
                print(line)
            print()
            print()

            conn_mutex.acquire()
            c.execute("INSERT INTO poetry (poem, sent) VALUES (?, False)", (json.dumps(poetry),))
            conn.commit()

            # print(request[0])

            c.execute("UPDATE user_requests SET processed = True WHERE id = (?)", (request[0],))
            conn.commit()
            conn_mutex.release()

            # add random line as a topic
            topics += [random.choice(poetry["en"])]
            topics = topics[-TOPIC_LEN:]

        if len(requests) == 0:
            print("Waiting for event")
            event.wait()
            event.clear()

def get_poetry_line(conn):
    while True:
        c = conn.cursor()
        conn_mutex.acquire()
        c.execute("SELECT id, poem FROM \"poetry\" WHERE sent = False ORDER BY id LIMIT 1")
        rows = list(c.fetchall())
        conn_mutex.release()

        if len(rows) > 0:
            for line in rows[0][1].split("\n"):
                for word in line.split(" "):
                    yield word

            # conn_mutex.acquire()
            # c.execute("UPDATE \"poetry\" SET sent = True WHERE id = (?)", (rows[0][0],))
            # conn.commit()
            # conn_mutex.release()
        else:
            # select random row
            pass

if __name__ == "__main__":
    conn = sqlite3.connect(configuration.db, check_same_thread=False)
    conn_mutex = threading.Lock()

    poetry_getter = get_poetry_line(conn)

    event = threading.Event()
    poetry_thread = threading.Thread(target=generate_poetry_thread, args=(openai, conn, conn_mutex, event))
    poetry_thread.daemon = True
    poetry_thread.start()

    class SimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            
            # Write the response body
            line = next(poetry_getter)
            message = [
                line,
                line,
                line
            ]
            message = "\n".join(message)
            self.wfile.write(message.encode())
        
        def do_POST(self):
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            parsed_data = urllib.parse.parse_qs(post_data)
            if 'prompt' in parsed_data:
                param_value = parsed_data['prompt'][0]
                response = "".encode('utf-8')
                
                param_value = re.sub("[^a-zA-Zа-яА-Яა-ჰ\s]+", "", param_value)

                conn_mutex.acquire()
                c = conn.cursor()
                c.execute('''INSERT INTO user_requests (request, processed) VALUES (?, False)''', (param_value,))
                conn.commit()
                conn_mutex.release()

                event.set()
            else:
                response = b'Parameter not found'
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(response)

    # Set the port number and create the server object
    PORT = 8001
    handler = SimpleHTTPRequestHandler
    with socketserver.TCPServer(("0.0.0.0", PORT), handler) as httpd:
        print("Server listening on port", PORT)
        # Start the server and keep it running until interrupted
        httpd.serve_forever()


