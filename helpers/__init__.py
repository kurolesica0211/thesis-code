import re


def strip_uri(uri: str) -> str:
    """Extract local name from URI."""
    return uri.rsplit("#", 1)[-1].rsplit("/", 1)[-1]

_NS_PREFIX_RE = re.compile(r'^[A-Za-z][A-Za-z0-9]*:(?!//)')
def strip_ns(s: str) -> str:
    """Strip a namespace prefix from an RDF prefixed name (e.g. 'rel:location' → 'location')."""
    return _NS_PREFIX_RE.sub("", s)