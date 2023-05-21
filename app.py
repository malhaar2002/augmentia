from flask import Flask, render_template, request
from blender import make_glb

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/model', methods=['POST'])
def model():
    file = request.files['file']
    file.save('static/netlist_file/circuit.net')
    make_glb()
    return render_template('model_display.html')

if __name__ == '__main__':
    app.run(debug=True)
