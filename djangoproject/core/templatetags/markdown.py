import misaka
from misaka import HtmlRenderer, SmartyPants, BaseRenderer
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from django import template


#Tell django that this is a template filter module
register = template.Library()


class HighlighterRenderer(HtmlRenderer, SmartyPants):
    def block_code(self, text, lang):
        s = ''
        if not lang:
            lang = 'text'
        try:
            lexer = get_lexer_by_name(lang, stripall=True)
        except:
            s += '<div class="highlight"><span class="err">Error: language "%s" is not supported</span></div>' % lang
            lexer = get_lexer_by_name('text', stripall=True)
        formatter = HtmlFormatter()
        s += highlight(text, lexer, formatter)
        return s

    def table(self, header, body):
        return '<table class="table">\n'+header+'\n'+body+'\n</table>'


class TextRenderer(BaseRenderer):
    def block_code(self, code, language):
        return code

    def block_quote(self, quote):
        return quote

    def block_html(self, raw_html):
        return raw_html

    def header(self, text, level):
        return text

    def hrule(self):
        return ''

    def list(self, contents, is_ordered):
        return contents

    def list_item(self, text, is_ordered):
        return text

    def paragraph(self, text):
        return text

    def table(self, header, body):
        return ''

    def table_row(self, content):
        return ''

    def table_cell(self, content, flags):
        return content

# And use the renderer
renderer = HighlighterRenderer(flags=misaka.HTML_ESCAPE | misaka.HTML_HARD_WRAP | misaka.HTML_SAFELINK)
md = misaka.Markdown(renderer,
                     extensions=misaka.EXT_FENCED_CODE |
                                misaka.EXT_NO_INTRA_EMPHASIS |
                                misaka.EXT_TABLES |
                                misaka.EXT_AUTOLINK |
                                misaka.EXT_SPACE_HEADERS |
                                misaka.EXT_STRIKETHROUGH |
                                misaka.EXT_SUPERSCRIPT)


text_renderer = TextRenderer()
mdt = misaka.Markdown(text_renderer)


def markdown(text):
    if not text:
        text = ""
    return md.render(text)


def strip_markdown(text):
    return mdt.render(text)


register.filter('markdown', markdown)
register.filter('strip_markdown', strip_markdown)
