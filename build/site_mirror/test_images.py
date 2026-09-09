"""Tests for resolving image references and the format each one is stored in."""

import pytest

from build.site_mirror.images import (
    parse_reference,
    site_path,
    source_url,
    stored_name,
)

PNG = "image-d12eaa7d5f1f8289f7ae4c9f33dc3e2ea4fdd2b8-772x550-png"
SVG = "image-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa-100x100-svg"
GIF = "image-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb-400x300-gif"


def test_a_reference_splits_into_digest_dimensions_and_format():
    assert parse_reference(PNG) == ("d12eaa7d5f1f8289f7ae4c9f33dc3e2ea4fdd2b8", "772x550", "png")


def test_an_unparseable_reference_is_rejected_rather_than_guessed():
    assert parse_reference("not-an-image-ref") is None


def test_a_raster_image_is_stored_as_webp():
    """82 KB average becomes 34 KB, measured over a 20-image sample."""
    assert stored_name(PNG).endswith(".webp")


@pytest.mark.parametrize("reference,suffix", [(SVG, ".svg"), (GIF, ".gif")])
def test_vector_and_animated_formats_are_kept_as_they_are(reference, suffix):
    assert stored_name(reference).endswith(suffix)


def test_a_raster_url_asks_the_cdn_to_convert():
    url = source_url(PNG)
    assert "fm=webp" in url and "w=1600" in url


def test_a_pass_through_url_asks_for_no_conversion():
    assert "?" not in source_url(SVG)


def test_the_site_path_is_where_hugo_will_serve_it_from():
    assert site_path(PNG).startswith("/images/site-mirror/")


def test_an_unusable_reference_yields_no_path_rather_than_a_broken_one():
    assert site_path("rubbish") == ""


def test_a_cdn_url_is_turned_back_into_a_reference():
    """Markdown bodies embed images as URLs; the mirroring works from references."""
    from build.site_mirror.images import reference_from_url

    url = "https://cdn.sanity.io/images/sy1jschh/production/abc123-772x550.png"
    assert reference_from_url(url) == "image-abc123-772x550-png"


def test_a_url_from_somewhere_else_is_not_a_reference():
    from build.site_mirror.images import reference_from_url

    assert reference_from_url("https://example.com/a.png") == ""


def test_an_animated_format_is_marked_for_re_encoding():
    """Sanity flattens a GIF on every conversion; gif2webp keeps the animation."""
    from build.site_mirror.images import ANIMATED_FORMATS, PASS_THROUGH_FORMATS

    assert "gif" in ANIMATED_FORMATS
    assert "gif" in PASS_THROUGH_FORMATS  # fetched untouched, converted after
    assert "svg" not in ANIMATED_FORMATS
