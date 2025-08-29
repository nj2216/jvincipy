from jvincipy import html, head, style, body, h1, div, Markup
from jvincipy.css import Stylesheet, Rule

s = Stylesheet()
s.rule("body", margin="0", font_family="system-ui, Arial, sans-serif")
s.rule(".hero", padding="2rem", background="#f7f7f9")
s.at("@media (max-width: 600px)").add_rule(
    Rule(".hero", {"padding": "1rem"})
)
css_text = s.render(pretty=True)

page = html(
    head(
        style(Markup(css_text)),  # use Markup so DSL doesn't escape CSS
    ),
    body(
        div(h1("Hello"), class_="hero")
    )
)
print(page.render(pretty=True))
