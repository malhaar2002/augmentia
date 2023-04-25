from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import io
from parse import parse

app = Flask(__name__)

@app.route('/parse_circuit', methods=['POST'])
def parse_circuit():
    file = request.files['file']
    filename = secure_filename(file.filename)
    content = io.StringIO(file.read().decode('utf-8')).getvalue()

    result = parse(content)

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
