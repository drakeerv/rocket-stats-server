import waitress
import flask

CLIENT_PATH = "client/build"
HOST = "0.0.0.0"
PORT = 8080

app = flask.Flask(__name__, static_url_path="", static_folder=CLIENT_PATH)

def get_app():
    return app

if __name__ == "__main__":
    print(f"Server running on http://localhost:{PORT}/index.html")
    waitress.serve(app, host=HOST, port=PORT)
    