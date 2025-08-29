# examples/flask_app.py
from flask import Flask, url_for, Response, send_from_directory
import json
from jvincipy import html, head, title, body, h1, p, div, link, style, script, Markup

app = Flask(__name__, static_folder='assets', static_url_path='/static')

@app.route('/')
def index():
    css_url = url_for('static', filename='style.css')
    js_url = url_for('static', filename='script.js')

    initial = {'user': 'guest', 'authenticated': False}
    page = html(
        head(
            title('jvincipy Flask demo'),
            link(rel='stylesheet', href=css_url),
            style('.container { max-width:900px; margin:0 auto; padding:1rem }')
        ),
        body(
            div(
                h1('Hello from Flask + jvincipy'),
                p('This page is rendered with the DSL and serves static assets from /static.'),
                class_='container'
            ),
            script(src=js_url, defer=True),
            script(Markup('window.__INIT__ = ' + json.dumps(initial) + ';'))
        )
    )
    html_text = page.render(pretty=True)
    resp = Response(html_text, mimetype='text/html')
    # Example CSP header - adjust for your deployment
    # resp.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'; style-src 'self';"
    return resp

if __name__ == '__main__':
    app.run(debug=True, port=5000)
