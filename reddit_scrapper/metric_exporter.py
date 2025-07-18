from prometheus_client import CollectorRegistry, multiprocess, make_wsgi_app
from wsgiref.simple_server import make_server
import time


def start_exporter_server(port=8000):
    registry = CollectorRegistry()
    multiprocess.MultiProcessCollector(registry)

    try:
        app = make_wsgi_app(registry)
        server = make_server("", port, app)
        server.serve_forever()
    except Exception as e:
        print(f"Error starting exporter server: {e}")


if __name__ == "__main__":
    start_exporter_server(port=8000)

    while True:
        time.sleep(1)
