from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import io
from parse import parse
from ref_value import ref_value

app = Flask(__name__)

@app.route('/parse_circuit', methods=['POST'])
def parse_circuit():
    file = request.files['file']
    filename = secure_filename(file.filename)
    content = io.StringIO(file.read().decode('utf-8')).getvalue()

    result = parse(content)

    return jsonify(result)

@app.route('/ref_value', methods=['POST'])
def ref_value_circuit():
    file = request.files['file']
    filename = secure_filename(file.filename)
    content = io.StringIO(file.read().decode('utf-8')).getvalue()
    result = ref_value(content)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
