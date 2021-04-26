import os.path
import json

from flask import Flask, Response, request


app = Flask(__name__)
app.config.from_object(__name__)
app.config['DEBUG'] = True


def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.dirname(__file__))


def get_file(filename):  # pragma: no cover
    try:
        src = os.path.join(root_dir(), filename)
        # Figure out how flask returns static files
        # Tried:
        # - render_template
        # - send_file
        # This should not be so non-obvious
        return open(src).read()
    except IOError as exc:
        return str(exc)


@app.route('/', methods=['GET'])
def metrics():  # pragma: no cover
    content = get_file('index.html')
    return Response(content, mimetype="text/html")


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def get_resource(path):  # pragma: no cover
    mimetypes = {
        ".css": "text/css",
        ".html": "text/html",
        ".js": "application/javascript",
    }
    complete_path = os.path.join(root_dir(), path)
    ext = os.path.splitext(path)[1]
    mimetype = mimetypes.get(ext, "text/html")
    content = get_file(complete_path)
    return Response(content, mimetype=mimetype)


@app.route("/write_map", methods=['POST'])
def write_map():
    if "manual_maps" in os.listdir():
        os.chdir("manual_maps")
    cnt = 1
    file_name = f"map{cnt}.json"
    while file_name in os.listdir():
        cnt += 1
        file_name = f"map{cnt}.json"
    print(file_name)
    with open(file_name, "w") as f:
        f.write(json.dumps(json.loads(request.get_data())))
    return Response("ok")


if __name__ == '__main__':  # pragma: no cover
    app.run(port=8000)
