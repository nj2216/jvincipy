# examples/example_css_js.py
from jvincipy import (
    html, head, title, link, style, script,
    body, h1, p, div, a, img, Markup
)
import json

def load_css_file():
    page = html(
        head(
            title("jvincipy — CSS & JS demo"),

            # External stylesheet (e.g. /static/css/main.css)
            link(rel="stylesheet", href="/static/css/main.css"),

            # Inline critical CSS (useful for small critical styles)
            style("""
                /* critical inline CSS */
                body { font-family: system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial; margin: 0; }
                .hero { padding: 2rem; background: #f7f7f9; }
            """),
        ),

        body(
            div(
                h1("Hello from jvincipy"),
                p("This page demonstrates CSS and JS integration"),
                class_="hero"
            ),

            # External script (placed near the end, with defer)
            script(src="/static/js/main.js", defer=True),

            # Inline small script — use Markup to avoid HTML-escaping the JS
            # Use json.dumps to safely serialize data to JS
            script(
                Markup("window.__INITIAL_DATA__ = " + json.dumps({"user": "guest", "id": 123}) + ";")
            ),

            # If you want an inline event handler (not recommended for CSP)
            # a("Click me", href="#", onclick="alert('hi')")  # this is inline-HTML approach (not recommended)
        )
    )

    # render as pretty HTML (string)
    return page.render(pretty=True)
