from gevent.pywsgi import WSGIServer
from service import app

if __name__ == '__main__':
    server = WSGIServer(('0.0.0.0', 8080), application=app)
    app.logger.info("Starting server...")
    server.serve_forever()
