from jvincipy import html, head, title, link, style, body, div, h1, p, script, Markup
import json
from flask import Flask, Response, url_for
import example_css_js

app = Flask(__name__, static_folder='assets', static_url_path="/static")

@app.route('/')
def index():
    css_url = url_for('static', filename='style.css')
    js_url = url_for('static', filename='script.js')
    initial = {'user': 'guest', 'authenticated': False}


    page = html(
        head(
            title('made by jvincipy'),
            link(rel='stylesheet', href=css_url),
            style('.container {max-width:900px; margin:0 auto; padding:1rem}')
        ),
        body(
            div(
                h1('Helo from try'),
                p('Ok working good I think'),
                class_='container'
            ),
            div(
                h1("wow"),
                class_='hero'
            ),
            script(src=js_url, defer=True),
            script(Markup('window.__INIT__ = ' + json.dumps(initial) + ';'))
        )
    )
    return Response(page.render(pretty=True), mimetype='text/html')

@app.route('/a')
def rrr():
    example_css_js.load_css_file()
    return Response(example_css_js.load_css_file(), mimetype='text/html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)