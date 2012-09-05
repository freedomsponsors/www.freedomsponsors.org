import misaka
from misaka import HtmlRenderer, SmartyPants
from pygments import highlight, lexers, formatters
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

class HighlighterRenderer(HtmlRenderer, SmartyPants):
    def block_code(self, text, lang):
        if not lang:
            return '\n<pre><code>%s</code></pre>\n' % text.strip()
        try:
            lexer = get_lexer_by_name(lang, stripall=True)
        except:
            return '<div class="highlight"><span class="err">Error: language "%s" is not supported</span></div>' % lang + \
                '\n<pre><code>%s</code></pre>\n' % text.strip()
        formatter = HtmlFormatter()
        return highlight(text, lexer, formatter)

    def table(self, header, body):
        return '<table class="table">\n'+header+'\n'+body+'\n</table>'

# And use the renderer
renderer = HighlighterRenderer(flags=misaka.HTML_ESCAPE | misaka.HTML_HARD_WRAP | misaka.HTML_SAFELINK)
md = misaka.Markdown(renderer,
    extensions=misaka.EXT_FENCED_CODE | misaka.EXT_NO_INTRA_EMPHASIS | misaka.EXT_TABLES | misaka.EXT_AUTOLINK | misaka.EXT_SPACE_HEADERS | misaka.EXT_STRIKETHROUGH | misaka.EXT_SUPERSCRIPT)

def markdownFormat(text):
    return md.render(text)