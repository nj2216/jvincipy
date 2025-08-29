# jvincipy/css.py
from typing import Dict, List, Union, Optional

# helpers
def _prop_name(name: str) -> str:
    # allow snake_case or dash-case; convert trailing underscore e.g., 'class_' not used here
    return name.replace("_", "-")

def _render_value(v):
    if v is True:
        return "true"
    if v is False or v is None:
        return ""
    return str(v)


class Rule:
    """Represents a single CSS rule with optional nested rules."""
    def __init__(self, selector: str, declarations: Optional[Dict] = None):
        self.selector = selector
        # declarations: mapping property->value or nested selector->dict
        self.declarations = declarations.copy() if declarations else {}
        self.nested: List[Rule] = []

    def set(self, **props):
        """Set properties for this rule using keyword args (snake_case -> kebab-case)."""
        for k, v in props.items():
            self.declarations[_prop_name(k)] = v
        return self

    def add(self, declarations: Dict):
        """Merge a dict (can contain nested selectors)."""
        for k, v in declarations.items():
            self.declarations[k] = v
        return self

    def add_nested(self, selector: str, declarations: Optional[Dict] = None):
        r = Rule(selector, declarations)
        self.nested.append(r)
        return r

    def _render_decls(self, decls: Dict, indent: str) -> List[str]:
        lines = []
        for k, v in decls.items():
            if isinstance(v, dict):
                # nested selector shorthand handled elsewhere
                continue
            name = _prop_name(k)
            val = _render_value(v)
            if val == "":
                continue
            lines.append(f"{indent}{name}: {val};")
        return lines

    def _collect_nested(self) -> List['Rule']:
        # nested rules supplied via nested list and also nested dicts in declarations
        nested_rules = list(self.nested)
        # find keys in declarations that are dict -> treat as nested selectors
        keys_to_remove = []
        for k, v in list(self.declarations.items()):
            if isinstance(v, dict):
                # nested selector: k could contain '&' to mean parent selector
                child_selector_raw = k
                child_selector = child_selector_raw.replace("&", self.selector) if "&" in child_selector_raw else f"{self.selector} {child_selector_raw}"
                nested_rules.append(Rule(child_selector, v))
                keys_to_remove.append(k)
        # optionally remove the nested-dict keys from declarations (so they won't be rendered as props)
        for k in keys_to_remove:
            del self.declarations[k]
        # include nested rules' nested descendants
        all_nested = []
        for nr in nested_rules:
            all_nested.append(nr)
            all_nested.extend(nr._collect_nested())
        return all_nested

    def render(self, indent_level: int = 0, indent_str: str = "  ") -> str:
        indent = indent_str * indent_level
        inner_indent = indent_str * (indent_level + 1)
        lines = [f"{indent}{self.selector} {{"]

        # render simple declarations (skip dict-values handled as nested)
        decl_lines = self._render_decls(self.declarations, inner_indent)
        lines.extend(decl_lines)
        lines.append(f"{indent}}}")
        # now nested rules collected from explicit nested list and dict-values
        nested_rules = self._collect_nested()
        for nr in nested_rules:
            lines.append(nr.render(indent_level=indent_level, indent_str=indent_str))
        return "\n".join(lines)


class AtRule:
    """Represents an at-rule like @media or @keyframes which wraps other rules."""
    def __init__(self, header: str):
        self.header = header  # e.g., "@media (max-width:600px)"
        self.rules: List[Rule] = []

    def add_rule(self, rule: Rule):
        self.rules.append(rule)
        return rule

    def render(self, indent_level: int = 0, indent_str: str = "  ") -> str:
        indent = indent_str * indent_level
        lines = [f"{indent}{self.header} {{"]
        for r in self.rules:
            # render rules inside at-rule with one extra indent
            lines.append(r.render(indent_level=indent_level + 1, indent_str=indent_str))
        lines.append(f"{indent}}}")
        return "\n".join(lines)


class Stylesheet:
    def __init__(self):
        self.rules: List[Rule] = []
        self.at_rules: List[AtRule] = []
        self.raw_lines: List[str] = []

    def rule(self, selector: str, declarations: Optional[Dict] = None, **props) -> Rule:
        """Create and append a rule. props are declarations (snake_case OK)."""
        decls = declarations.copy() if declarations else {}
        # merge kwargs into decls
        for k, v in props.items():
            decls[_prop_name(k)] = v
        r = Rule(selector, decls)
        self.rules.append(r)
        return r

    def at(self, header: str) -> AtRule:
        ar = AtRule(header)
        self.at_rules.append(ar)
        return ar

    def raw(self, text: str):
        """Append raw css text (kept verbatim)."""
        self.raw_lines.append(text)
        return self

    def render(self, pretty: bool = True) -> str:
        parts: List[str] = []
        if self.raw_lines:
            parts.extend(self.raw_lines)
        for r in self.rules:
            parts.append(r.render(indent_level=0))
        for ar in self.at_rules:
            parts.append(ar.render(indent_level=0))
        if pretty:
            return "\n\n".join(parts) + "\n"
        else:
            return "".join(p.replace("\n", "") for p in parts)

    def write(self, path: str, pretty: bool = True, encoding: str = "utf8"):
        txt = self.render(pretty=pretty)
        with open(path, "w", encoding=encoding) as f:
            f.write(txt)
        return path
