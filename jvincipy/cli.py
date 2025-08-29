# jvincipy/cli.py
import argparse
import runpy
import sys
from pathlib import Path
from .core import Markup
from .core import Tag

def find_renderable(ns):
    # 1) page variable
    if 'page' in ns:
        return ns['page']
    # 2) render() callable
    if 'render' in ns and callable(ns['render']):
        return ns['render']()
    # 3) get_page()
    if 'get_page' in ns and callable(ns['get_page']):
        return ns['get_page']()
    return None

def main(argv=None):
    p = argparse.ArgumentParser(prog='jvincipy', description='Render a python file that creates a jvincipy page')
    p.add_argument('input', help='Python file to execute (should expose `page` or `render()`/`get_page()` )')
    p.add_argument('-o', '--output', help='Write output HTML file')
    p.add_argument('--pretty', action='store_true', help='Pretty-print HTML')
    args = p.parse_args(argv)

    path = Path(args.input)
    if not path.exists():
        print('Input file not found:', path, file=sys.stderr)
        sys.exit(2)

    ns = runpy.run_path(str(path))
    page = find_renderable(ns)
    if page is None:
        print('No `page` variable or `render()` / `get_page()` found in the file.', file=sys.stderr)
        sys.exit(3)

    if isinstance(page, (str, Markup)):
        out = str(page)
    elif hasattr(page, 'render'):
        out = page.render(pretty=args.pretty)
    else:
        out = str(page)

    if args.output:
        Path(args.output).write_text(out, encoding='utf8')
    else:
        print(out)

if __name__ == '__main__':
    main()
