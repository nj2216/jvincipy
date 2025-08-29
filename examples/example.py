# examples/example.py
from jvincipy import html, head, title, body, h1, p, div, a, img, Markup, link, style, script
import json

page = html(
    head(
        title('jvincipy — demo'),
        link(rel='stylesheet', href='/static/style.css'),
        style('.hero { padding: 1rem; background: #fafafa }')
    ),
    body(
        div(
            h1('Welcome to jvincipy!'),
            p('A simple example with CSS and JS.'),
            class_='hero'
        ),
        script(src='/static/script.js', defer=True),
        # inline initial data
        script(Markup('window.__DATA__ = ' + json.dumps({'user':'guest'}) + ';'))
    )
)

if __name__ == '__main__':
    print(page.render(pretty=True))
