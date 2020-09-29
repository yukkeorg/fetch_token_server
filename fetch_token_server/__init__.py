import queue
import threading
from http.server import HTTPStatus, HTTPServer, BaseHTTPRequestHandler

__version__ = "0.1.0"


def serve_fetch_token_server(host="localhost", port=8888):
    q = queue.Queue(1)

    class fetchTokenRequestHandler(BaseHTTPRequestHandler):
        server_version = "FetchTokenServer/" + __version__

        def do_GET(self):
            self.send_response(HTTPStatus.OK)
            self.end_headers()

            q.put("http://{}:{}{}".format(host, port, self.path))

            # prevent deadlock
            threading.Thread(target=self.server.shutdown, daemon=True).start()

    with HTTPServer((host, port), fetchTokenRequestHandler) as httpd:
        httpd.serve_forever()

    return None if q.empty() else q.get()
