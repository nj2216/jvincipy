# jvincipy — Python DSL for HTML

Extended project: full HTML5 tag coverage + CLI + Flask example

This document contains the full project layout, implementation, CLI and a minimal Flask app that demonstrates serving rendered pages.

---

## Project structure

```
jvincipy_dsl/
├── README.md
├── pyproject.toml
├── jvincipy/
│   ├── __init__.py
│   ├── core.py
│   ├── tags.py
│   └── cli.py
├── examples/
│   ├── example.py
│   └── flask_app.py
└── tests/
    └── test_basic.py
```

---

> **Note:** The code below is intended to be copied into the corresponding files inside `jvincipy/`, `examples/` and so on. The library is dependency-free except for the Flask example (which requires Flask).

---
## Implementation (files)

### `jvincipy/core.py`

(keeps the same core implementation as before: `Tag`, `Markup`, `VOID_ELEMENTS`, `tag()` helper and rendering logic.)

> See the canvas file `jvincipy/core.py` for the full source.

### `jvincipy/tags.py` — now includes all HTML5 elements and common SVG elements

This file programmatically creates `TagFactory` objects for a comprehensive list of element names. The list includes:

    
    

> See the canvas file `jvincipy/tags.py` for the exact expanded list and generated factories.

### `jvincipy/css.py` — Pythonic CSS DSL

This file provides a small, dependency-free API for building CSS rules and stylesheets in Python. It includes:

- `Rule`: Represents a CSS rule with a selector and declarations. Supports nested rules and dict-based selectors.
- `AtRule`: For at-rules like `@media` and `@keyframes`, which wrap other rules.
- `Stylesheet`: Collects rules and at-rules, and renders the full CSS.

**Usage Example:**

```python
from jvincipy.css import Rule, Stylesheet

# Create a rule
main_rule = Rule('body', {'margin': 0, 'font-family': 'sans-serif'})
main_rule.set(color='black')

# Add a nested rule
main_rule.add_nested('a', {'color': 'blue', 'text-decoration': 'none'})

# At-rule example
media = AtRule('@media (max-width:600px)')
media.add_rule(Rule('body', {'font-size': '14px'}))

# Build stylesheet
sheet = Stylesheet()
sheet.rules.append(main_rule)
sheet.at_rules.append(media)
print(sheet.rules[0].render(pretty=True))
print(sheet.at_rules[0].render())
```

**Features:**
- Python dicts for declarations, snake_case auto-converted to kebab-case.
- Nested selectors via dicts or explicit nesting.
- At-rules for media queries, keyframes, etc.
- Renders readable CSS with indentation.

See `jvincipy/css.py` for full API and helpers.
### `jvincipy/cli.py` — a small CLI to render `.py` files to HTML

**Behavior**

- Accepts a path to a Python file that _creates a `page` variable_ (a `Tag` instance) or defines a function `render()` which returns a `Tag` or string.
    
- Loads and executes the file safely with `runpy.run_path()` and then finds `page` or `render` in the executed module's globals.
    
- Writes an output HTML file or prints to stdout.
    

**Usage**

```bash
# render and pretty-print to stdout
python -m jvincipy.cli input.py --pretty

# render and write to output file
python -m jvincipy.cli input.py -o out.html
```

> Exact code is available in `jvincipy/cli.py` in the canvas (includes `argparse`, error messages, and examples).

### `examples/flask_app.py` — minimal Flask integration

This example shows how to use the library inside a Flask route. It expects you to have Flask installed.

Run:

```bash
pip install flask
python examples/flask_app.py
# then open http://127.0.0.1:5000/
```

> See the file `examples/flask_app.py` in the canvas for the full code. It demonstrates two routes: `/` (renders a `page` created with jvincipy) and `/raw` (renders raw HTML string or Markup).

### `pyproject.toml` — console script

The project includes an entry point so you can run the CLI as `jvincipy` after installing:

```toml
[project.scripts]
jvincipy = "jvincipy.cli:main"
```

(If you prefer not to install, run via `python -m jvincipy.cli`.)

## How the CLI decides what to render

When you point the CLI at a Python file, it will run it and look for the following (in order):

1. a global variable named `page` that is a `Tag` instance (or a string), or
    
2. a callable `render()` function that returns a `Tag` or string, or
    
3. a `get_page()` function which returns a `Tag` or string.
    

If none are found, the CLI exits with an error message describing what it expects.

## Flask example behavior

The Flask example demonstrates:

- importing the library (`from jvincipy import html, head, body, h1, p, Markup, ...`)
    
- building a tag tree and returning a fully-formed HTML response using `page.render(pretty=True)`
    
- using `Markup` to inject pre-rendered HTML safely when needed
    

The example also shows how to pass query parameters to choose pretty/compact rendering.

## Tests

The `tests/test_basic.py` remains the same — a minimal test ensuring a simple `div(p('hello'))` renders correctly.

## Next steps I implemented in the canvas

1. **Expanded `tags.py`** to include a comprehensive HTML5 + SVG tag list and exported names.
    
2. **Added `jvincipy/cli.py`** that provides a usable CLI with `argparse`, helpful errors, and `--pretty` / `--minify` options.
    
3. **Added `examples/flask_app.py`** showing how to wire the DSL into Flask routes.
    
4. Updated `pyproject.toml` snippet with an installable console script entry.
    

---

## How you can run and test locally (commands)

1. Create a virtual environment and install dev/test dependencies (optional):
    

```bash
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install pytest
```

2. Run the examples using the module CLI:
    

```bash
# render example.py to stdout
python -m jvincipy.cli examples/example.py --pretty

# render and save
python -m jvincipy.cli examples/example.py -o dist/example.html
```

3. Try the Flask example:
    

```bash
pip install flask
python examples/flask_app.py
# open http://127.0.0.1:5000/
```

4. Run tests:
    

```bash
pytest
```

---

## Usage patterns & examples

**1) Build pages programmatically**

Create a Python file that constructs a `page` object using tag factories and run it with the CLI or import the module from an app.

**2) Build CSS programmatically**

Use the CSS DSL to generate stylesheets in Python:

```python
from jvincipy.css import Stylesheet, Rule

sheet = Stylesheet()
sheet.rules.append(Rule('body', {'margin': 0, 'color': 'black'}))
print(sheet.rules[0].render())
```

You can combine this with HTML generation for full Python-powered web pages.
**2) CLI rendering**

The CLI expects the executed file to expose either:
- a global `page` (Tag or string), or
- a callable `render()` / `get_page()` that returns a Tag/string.

**3) Flask integration**

Use the Flask example to serve static files from an `assets/` directory and return `page.render(pretty=True)` in a route.

**4) CSS integration**

You can use the CSS API to generate stylesheets and serve them in Flask or write to files for static sites.
---

## How to extend


- Extend the CSS DSL with more helpers, custom at-rules, or minification.

---

## Contributing

Please read `CONTRIBUTING.md` for the suggested workflow. In short:

- Fork the repo
- Create a small branch with focused commits
- Add tests for new behavior
- Open a PR with a clear description and any migration notes

---

## License

This project is released under the MIT License — see the `LICENSE` file.

---

## CODE_OF_CONDUCT

A `CODE_OF_CONDUCT.md` has been added to help foster a welcoming community. The project follows the Contributor Covenant v2.1 with a zero-tolerance policy for harassment.
