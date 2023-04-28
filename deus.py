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
from deus_db import *


openai.api_key = configuration.api_key

    
def generate_poetry_thread(ai, conn, conn_mutex, event):
    TOPIC_LEN = 5
    topics = ["nothing"]
    
    while True:
        requests = db_get_user_requests(conn, conn_mutex)
        for request in requests:
            topics += [ai_describe(openai, request[1])]
            topics = topics[-TOPIC_LEN:]

            print(topics)

            poetry = ai_poetry(openai, topics)

            print("=== poetry ===")
            for line in zip(*poetry.values()):
                print(line)
            print()
            print()

            db_set_poetry(conn, conn_mutex, json.dumps(poetry), request[0])

            # add random line as a topic
            topics += [random.choice(poetry["en"])]
            topics = topics[-TOPIC_LEN:]

        if len(requests) == 0:
            print("Waiting for event")
            event.wait()
            event.clear()

def word_getter(poem):
    print("new getter")
    for line in zip(*poem.values()):
        print(line)
        lang_words = [lang.split(" ") for lang in line]
        l = max([len(x) for x in lang_words])

        for i in range(l):
            p = i / l
            yield "\n".join([x[int(p * len(x) + 0.1)] for x in lang_words])

def get_poetry_line(conn, conn_mutex):
    while True:
        rows = db_get_last_poetry(conn, conn_mutex)

        if len(rows) > 0:
            words = word_getter(json.loads(rows[0][1]))
            try:
                while True:
                    yield next(words)
            except StopIteration:
                print("stop")
                pass

            db_set_poetry_sent(conn, conn_mutex, rows[0][0])
        else:
            # select random row
            print("select random row")
            words = db_get_random_poetry(conn, conn_mutex)
            words = word_getter(json.loads(words))

        try:
            while True:
                yield next(words)
        except StopIteration:
            print("stop")
            pass

def get_server(conn, conn_mutex):
    poetry_getter = get_poetry_line(conn, conn_mutex)

    class SimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/':
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                
                # Write the response body
                message = next(poetry_getter)
                self.wfile.write(message.encode())
            else:
                self.send_response(404)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                
                # Write the response body
                message = ""
                self.wfile.write(message.encode())

    # Set the port number and create the server object
    PORT = 8001
    handler = SimpleHTTPRequestHandler
    with socketserver.TCPServer(("0.0.0.0", PORT), handler) as httpd:
        print("Server listening on port", PORT)
        # Start the server and keep it running until interrupted
        try:
            httpd.serve_forever()
        finally:
            httpd.server_close()

if __name__ == "__main__":
    conn = sqlite3.connect(configuration.db, check_same_thread=False)
    conn_mutex = threading.Lock()

    event = threading.Event()
    poetry_thread = threading.Thread(target=generate_poetry_thread, args=(openai, conn, conn_mutex, event))
    poetry_thread.daemon = True
    poetry_thread.start()

    get_thread = threading.Thread(target=get_server, args=(conn, conn_mutex))
    get_thread.daemon = True
    get_thread.start()

    class SimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
        def do_POST(self):
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            parsed_data = urllib.parse.parse_qs(post_data)
            if 'prompt' in parsed_data:
                param_value = parsed_data['prompt'][0]
                response = "".encode('utf-8')
                
                param_value = re.sub("[^a-zA-Zа-яА-Яა-ჰ\s]+", "", param_value)

                db_post_user_request(conn, conn_mutex, param_value)

                event.set()
            else:
                response = b'Parameter not found'
            
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write("".encode())

    # Set the port number and create the server object
    PORT = 8002
    handler = SimpleHTTPRequestHandler
    with socketserver.TCPServer(("0.0.0.0", PORT), handler) as httpd:
        print("Server listening on port", PORT)
        # Start the server and keep it running until interrupted
        try:
            httpd.serve_forever()
        finally:
            httpd.server_close()


