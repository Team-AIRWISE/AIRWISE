from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('airwise.html', template_folder='templates')

if __name__ == '__main__':
    app.run(debug=True, host='AIRWISE.local', port=5000)
