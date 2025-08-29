# jvincipy/tags.py
from .core import Tag

_TAG_NAMES = """
a abbr address area article aside audio b base bdi bdo blockquote body br button canvas caption cite code col colgroup data datalist dd del details dfn dialog div dl dt em embed fieldset figcaption figure footer form h1 h2 h3 h4 h5 h6 head header hr html i iframe img input ins kbd label legend li link main map mark menu menuitem meta meter nav noscript object ol optgroup option output p param picture pre progress q rp rt ruby s samp script section select small source span strong style sub summary sup table tbody td template textarea tfoot th thead time title tr track u ul var video wbr
svg circle rect path g line polyline polygon ellipse text defs clipPath linearGradient stop symbol use
""".split()

class TagFactory:
    def __init__(self, name):
        self._name = name

    def __call__(self, *children, **attrs):
        return Tag(self._name, *children, **attrs)

    def __repr__(self):
        return f"TagFactory({self._name!r})"

globals().update({name: TagFactory(name) for name in _TAG_NAMES})

__all__ = [name for name in _TAG_NAMES]
