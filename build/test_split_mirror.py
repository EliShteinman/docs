"""Tests for dividing a built site into the documentation and the mirror."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from split_mirror import belongs_to_mirror, path_of, split, split_feed, split_sitemap


def _site(tmp_path: Path) -> tuple[Path, Path]:
    site = tmp_path / "public"
    for section in ("blog/a-post", "tutorials/one", "develop/clients", "glossary/cache"):
        (site / section).mkdir(parents=True)
        (site / section / "index.html").write_text("<html></html>", encoding="utf-8")
    (site / "images/site-mirror").mkdir(parents=True)
    (site / "images/site-mirror" / "a.webp").write_bytes(b"\x00")
    (site / "images" / "logo.svg").write_text("<svg/>", encoding="utf-8")
    return site, tmp_path / "public-mirror"


def test_a_mirrored_section_moves_out(tmp_path):
    site, mirror = _site(tmp_path)
    split(site, mirror)
    assert not (site / "blog").exists()
    assert (mirror / "blog" / "a-post" / "index.html").is_file()


def test_the_documentation_stays_where_it_is(tmp_path):
    site, mirror = _site(tmp_path)
    split(site, mirror)
    assert (site / "develop" / "clients" / "index.html").is_file()


def test_the_glossary_stays_with_the_documentation(tmp_path):
    """Its terms publish inside the documentation's own section; no path splits them."""
    site, mirror = _site(tmp_path)
    split(site, mirror)
    assert (site / "glossary" / "cache").is_dir()
    assert not (mirror / "glossary").exists()


def test_the_pictures_leave_the_site_in_a_tree_of_their_own(tmp_path):
    """Their own tree so the image can hold them in their own layer: they are
    243 MB that change only when content is mirrored, while the pages beside
    them are rewritten by any change to a layout."""
    site, mirror = _site(tmp_path)
    assets = tmp_path / "public-mirror-assets"
    split(site, mirror, assets)
    assert (assets / "images" / "site-mirror" / "a.webp").is_file()
    assert not (mirror / "images").exists()
    assert (site / "images" / "logo.svg").is_file(), "the site keeps its own pictures"


def test_the_assets_tree_is_named_after_the_mirror_when_it_is_not_given(tmp_path):
    site, mirror = _site(tmp_path)
    split(site, mirror)
    assert (tmp_path / "public-mirror-assets" / "images" / "site-mirror" / "a.webp").is_file()


def test_splitting_twice_does_not_fail(tmp_path):
    """A rerun of a build step has to be allowed to find the work already done."""
    site, mirror = _site(tmp_path)
    split(site, mirror)
    assert split(site, mirror)["sections"] == 0


def _feed(site: Path, *urls: str) -> None:
    site.mkdir(parents=True, exist_ok=True)
    (site / "docs.ndjson").write_text(
        "\n".join(json.dumps({"url": url, "title": "x"}) for url in urls) + "\n",
        encoding="utf-8",
    )


def test_a_mirrored_page_leaves_the_documentation_feed(tmp_path):
    """Otherwise search answers with a post the site no longer serves."""
    site = tmp_path / "public"
    _feed(site, "/develop/clients/", "/blog/a-post/")
    kept, moved = split_feed(site, tmp_path / "public-mirror")
    assert (kept, moved) == (1, 1)
    assert "/blog/a-post/" not in (site / "docs.ndjson").read_text()
    assert "/blog/a-post/" in (tmp_path / "public-mirror" / "mirror.ndjson").read_text()


def test_an_absolute_url_in_the_feed_is_read_by_its_path(tmp_path):
    """A build with a canonical URL set writes them fully qualified."""
    site = tmp_path / "public"
    _feed(site, "https://docs.example.com/blog/a-post/")
    _, moved = split_feed(site, tmp_path / "public-mirror")
    assert moved == 1


def test_a_line_that_cannot_be_read_stays_with_the_documentation(tmp_path):
    site = tmp_path / "public"
    site.mkdir(parents=True)
    (site / "docs.ndjson").write_text('{"url": "/develop/"}\nnot json\n', encoding="utf-8")
    kept, _ = split_feed(site, tmp_path / "public-mirror")
    assert kept == 2


def test_the_documentation_stops_advertising_what_it_no_longer_serves(tmp_path):
    site = tmp_path / "public"
    site.mkdir(parents=True)
    (site / "sitemap.xml").write_text(
        "<urlset>"
        "<url><loc>https://x/develop/</loc></url>"
        "<url><loc>https://x/blog/a-post/</loc></url>"
        "</urlset>",
        encoding="utf-8",
    )
    assert split_sitemap(site, tmp_path / "public-mirror") == 1
    text = (site / "sitemap.xml").read_text()
    assert "/develop/" in text and "/blog/a-post/" not in text


def test_a_path_is_read_out_of_either_url_form():
    assert path_of("https://redis.io/blog/a/") == "/blog/a/"
    assert path_of("/blog/a/?x=1#y") == "/blog/a/"


def test_a_section_name_that_merely_starts_the_same_is_not_mirrored():
    """`/technology-of-ours/` is not `/technology/`."""
    assert belongs_to_mirror("/technology/redis-enterprise/")
    assert not belongs_to_mirror("/technology-of-ours/")


def test_the_section_index_itself_belongs_to_the_mirror():
    assert belongs_to_mirror("/blog")
    assert belongs_to_mirror("/blog/")


def test_the_diagrams_move_by_the_path_they_publish_at(tmp_path):
    """content/architecture-diagrams publishes at /resources/architecture-diagrams/."""
    site = tmp_path / "public"
    (site / "resources" / "architecture-diagrams" / "active-active").mkdir(parents=True)
    (site / "resources" / "architecture-diagrams" / "active-active" / "index.html").write_text(
        "<html></html>", encoding="utf-8"
    )
    split(site, tmp_path / "public-mirror")
    assert (tmp_path / "public-mirror" / "resources" / "architecture-diagrams").is_dir()
    assert belongs_to_mirror("/resources/architecture-diagrams/active-active/")


def test_a_category_page_travels_inside_its_section(tmp_path):
    """The category trees publish under /blog/ and /tutorials/, not beside them."""
    assert belongs_to_mirror("/blog/category/benchmarks/")
    assert belongs_to_mirror("/tutorials/category/developers/")
