import gzip
from email.message import Message

from build.marketing_mirror.fetcher import decode, moved_to


def _headers(**values: str) -> Message:
    message = Message()
    for name, value in values.items():
        message[name.replace("_", "-")] = value
    return message


def test_decode_inflates_a_gzip_body():
    assert decode(gzip.compress(b"page"), _headers(Content_Encoding="gzip")) == b"page"


def test_decode_passes_an_uncompressed_body_through():
    assert decode(b"page", _headers()) == b"page"


def test_a_page_answering_itself_has_not_moved():
    assert moved_to("https://redis.io/blog/a/", "https://redis.io/blog/a/") is None


def test_a_trailing_slash_redirect_is_the_same_page():
    assert (
        moved_to(
            "https://redis.io/api/blog/feed?x=1", "https://redis.io/api/blog/feed/?x=1"
        )
        is None
    )


def test_a_redirect_to_another_page_is_a_move():
    assert (
        moved_to(
            "https://redis.io/tutorials/create/aws/chatapp/",
            "https://redis.io/partners/aws/",
        )
        == "/partners/aws/"
    )
