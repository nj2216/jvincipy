# tests/test_basic.py
from jvincipy import div, p

def test_simple_render():
    out = div(p('hello'), id='root').render(pretty=False)
    assert '<div' in out and '<p>hello</p>' in out
