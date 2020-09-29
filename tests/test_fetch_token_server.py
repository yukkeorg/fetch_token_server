import pytest
import time
from threading import Thread
from urllib.request import urlopen

from fetch_token_server import serve_fetch_token_server


def test_fetch_token_server():
    request_url = "http://localhost:8888/?state=ABCDEFG&token=ABCabc123"

    def request_thread():
        time.sleep(1)
        urlopen(request_url)

    Thread(target=request_thread, daemon=True).start()

    redirect_url = serve_fetch_token_server()

    assert redirect_url == request_url
