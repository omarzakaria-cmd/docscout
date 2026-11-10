import re

from markupsafe import Markup, escape


def highlight_matches(text, query):
    if not query.strip():
        return escape(text)

    parts = []
    position = 0

    for match in re.finditer(re.escape(query.strip()), text, re.IGNORECASE):
        parts.append(escape(text[position:match.start()]))
        parts.append(
            Markup("<mark>") + escape(match.group()) + Markup("</mark>")
        )
        position = match.end()

    parts.append(escape(text[position:]))
    return Markup("").join(parts)
