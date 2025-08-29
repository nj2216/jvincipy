# jvincipy/core.py
from html import escape as html_escape
from typing import Any

# HTML void elements (no closing tag, no content)
VOID_ELEMENTS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr"
}

class Markup:
    """Wrap raw HTML to avoid escaping when rendering."""
    __slots__ = ("text",)

    def __init__(self, text: str):
        self.text = str(text)

    def __repr__(self):
        return f"Markup({self.text!r})"

def _escape_child(child: Any) -> str:
    if isinstance(child, Markup):
        return child.text
    if isinstance(child, Tag):
        return child.render(pretty=False)
    return html_escape(str(child), quote=True)

class Tag:
    """Represents a single HTML tag instance (name + attributes + children)."""
    __slots__ = ("name", "attrs", "children")


    def __init__(self, name: str, *children, **attrs):
        self.name = name
        # normalize attributes (class_ -> class, data__x -> data:x)
        norm = {}
        for k, v in attrs.items():
            if k.endswith("_") and not k.startswith("__"):
                key = k[:-1]
            else:
                key = k
            norm[key.replace("__", ":")] = v
        self.attrs = norm
        # flatten children
        self.children = []
        for c in children:
            if c is None:
                continue
            if isinstance(c, (list, tuple)):
                for x in c:
                    if x is None:
                        continue
                    self.children.append(x)
            else:
                self.children.append(c)

    def __call__(self, *children, **attrs):
        """Return a new Tag instance of the same tag name with added children/attrs."""
        merged_attrs = {**self.attrs, **attrs}
        merged_children = [*self.children, *children]
        return Tag(self.name, *merged_children, **merged_attrs)

    def _render_attrs(self) -> str:
        parts = []
        for k, v in self.attrs.items():
            if v is True:
                parts.append(k)
            elif v is False or v is None:
                continue
            else:
                parts.append(f'{k}="{html_escape(str(v), quote=True)}"')
        return (" " + " ".join(parts)) if parts else ""

    def render(self, pretty: bool = True, indent: int = 0, _indent_str: str = "  ") -> str:
        attrs = self._render_attrs()
        name = self.name

        # Void element
        if name in VOID_ELEMENTS:
            if pretty:
                return f"{_indent_str * indent}<{name}{attrs}>\n"
            return f"<{name}{attrs}>"

        # No children -> short form
        if not self.children:
            if pretty:
                return f"{_indent_str * indent}<{name}{attrs}></{name}>\n"
            return f"<{name}{attrs}></{name}>"

        # Otherwise render children
        if pretty:
            lines = [f"{_indent_str * indent}<{name}{attrs}>"]
            for child in self.children:
                if isinstance(child, Tag):
                    lines.append(child.render(pretty=True, indent=indent + 1, _indent_str=_indent_str).rstrip('\n'))
                else:
                    lines.append(f"{_indent_str * (indent + 1)}{_escape_child(child)}")
            lines.append(f"{_indent_str * indent}</{name}>")
            return "\n".join(lines) + "\n"
        else:
            inner = "".join(_escape_child(c) if not isinstance(c, Tag) else c.render(pretty=False) for c in self.children)
            return f"<{name}{attrs}>{inner}</{name}>"

    def __str__(self):
        return self.render(pretty=False)

    def __repr__(self):
        return f"Tag({self.name!r}, children={len(self.children)}, attrs={self.attrs})"

def tag(name: str, *children, **attrs) -> Tag:
    return Tag(name, *children, **attrs)
