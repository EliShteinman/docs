import gzip
from email.message import Message

from build.marketing_mirror.fetcher import decode


def _headers(**values: str) -> Message:
    message = Message()
    for name, value in values.items():
        message[name.replace("_", "-")] = value
    return message


def test_decode_inflates_a_gzip_body():
    assert decode(gzip.compress(b"page"), _headers(Content_Encoding="gzip")) == b"page"


def test_decode_passes_an_uncompressed_body_through():
    assert decode(b"page", _headers()) == b"page"
