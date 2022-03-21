from flask import Flask, send_from_directory, render_template, request

app = Flask(__name__,)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/player-stats/<name>')
def stats(name):
    # request.
    return render_template('details.html', name=name)

if __name__ == '__main__':    
    app.run("0.0.0.0", port=8088, debug=True)