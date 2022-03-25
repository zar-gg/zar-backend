from flask import Flask, send_from_directory, render_template, request

app = Flask(__name__,)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/player-stats/<name>')
def stats(name):
    return render_template('details.html', name=name)

@app.route('/not-found')
def not_found():
    return render_template('not_found.html')

if __name__ == '__main__':    
    app.run("0.0.0.0", port=8088, debug=True)