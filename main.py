import werkzeug.exceptions
import waitress
import flask
import os

SERVER_PATH = os.path.dirname(os.path.realpath(__file__))
CLIENT_PATH = os.path.join(SERVER_PATH, "client/build")
ERROR_PATH = os.path.join(SERVER_PATH, "error.html")
HOST = "0.0.0.0"
PORT = 8080

app = flask.Flask(__name__)

@app.errorhandler(werkzeug.exceptions.HTTPException)
def page_not_found(error):
    with open(ERROR_PATH, "r") as file:
        data = file.read()

    return data.replace("{status}", str(error.code)).replace("{message}", "".join(error.description)), error.code

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def send_file(path):
    path = os.path.abspath(os.path.join(CLIENT_PATH, path.replace("../", "")))

    if os.path.isdir(path):
        index_path = os.path.join(path, "index.html")

        if os.path.isfile(index_path):
            path = index_path

    print(path)

    if not os.path.exists(path):
        flask.abort(404)
        
    return flask.send_file(path)

@app.after_request
def apply_headers(response):
    response.headers["Server"] = "drakeerv/1.0.0"
    return response

def get_app():
    return app

if __name__ == "__main__":
    print(f"Server running on http://localhost:{PORT}/")
    waitress.serve(app, host=HOST, port=PORT)
    