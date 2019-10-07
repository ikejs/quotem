from flask import Flask, render_template
from dotenv import load_dotenv

title = " Quotem - Quotes for days 🤡"

app = Flask(__name__, static_url_path='')

@app.route('/')
def index():
    return render_template(
        'index.html',
        testText='testing123',
        title='Home' + title
        )

if __name__ == '__main__':
    app.run(debug=True)
