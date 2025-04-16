from flask import Flask, render_template, request

app = Flask(__name__)

book_list = []
author_list = []

@app.route('/', methods=["GET", 'POST'])
def homepage():

    book = None
    author = None

    if request.method == 'POST':
        book = request.form['book']
        author = request.form['author']

        book_list.append(book)
        author_list.append(author)

        
    return render_template('index.html', book=book, author=author, book_list=book_list, author_list=author_list)

@app.route('/another_page')
def another_page():
    return "<h2>This is another page</h2>"

if __name__ == '__main__':
    app.run(debug=True)