from flask import Flask

app = Flask(__name__)

@app.route('/')
def homepage():
    return "<h2>Welcome to Book Recommendation System</h2>"

@app.route('/another_page')
def another_page():
    return "<h2>This is another page</h2>"

if __name__ == '__main__':
    app.run(debug=True)