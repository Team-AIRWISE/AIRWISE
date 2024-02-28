from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('/AIRWISE/airwise.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
