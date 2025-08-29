import pytest
from jvincipy.css import css, selector

def test_css_render():
    styles = css(
        selector("h1", {"color": "blue"}),
        selector("p", {"font-size": "14px"})
    )
    output = styles.render()
    assert "h1" in output
    assert "color: blue;" in output
