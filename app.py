from flask import Flask, render_template, request
import os
from waitress import serve

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/model', methods=['POST'])
def model():
    file = request.files['file']
    file.save('static/netlist_file/circuit.net')
    os.system("blender --background --python blender.py")
    return render_template('model_display.html')

if __name__ == '__main__':
    # app.run(debug=True)
    # For production server:
    serve(app, host="0.0.0.0", port=8080)
