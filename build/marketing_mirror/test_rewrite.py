import pytest

from build.marketing_mirror import rewrite, settings

PAGE = (
    '<html><head><meta charset="utf-8"/>'
    '<script src="https://www.googletagmanager.com/gtm.js?id=X"></script>'
    '<link rel="preload" href="https://consent.trustarc.com/notice?x=1" as="script"/>'
    '<link rel="stylesheet" href="/_next/static/immutable/chunks/a1.css"/>'
    "</head><body>"
    '<img src="https://cdn.sanity.io/images/sy1jschh/production/abc-10x10.png?w=64"/>'
    '<script>self.__next_f.push([1,"{\\"_ref\\":\\"image-'
    + "f"
    * 40
    + '-32x32-svg\\"}"])</script>'
    "</body></html>"
)


def test_next_assets_finds_a_stylesheet():
    assert "/_next/static/immutable/chunks/a1.css" in rewrite.next_assets(PAGE)


def test_next_assets_finds_a_lazily_loaded_chunk():
    chunk = 'e.l("x"),Promise.all(["static/immutable/chunks/0k2c.js"].map(t=>e.l(t)))'
    assert rewrite.next_assets(chunk) == {"/_next/static/immutable/chunks/0k2c.js"}


def test_next_assets_finds_a_font_in_a_stylesheet():
    css = "@font-face{src:url(/_next/static/immutable/media/f.woff2) format('woff2')}"
    assert rewrite.next_assets(css) == {"/_next/static/immutable/media/f.woff2"}


@pytest.mark.parametrize(
    "text", ['"/_next/static/immutable"', '"/_next/static/${e}.js"']
)
def test_next_assets_skips_what_is_not_a_file(text):
    assert rewrite.next_assets(text) == set()


def test_sanity_assets_finds_an_image_by_url_without_its_query():
    assert "/images/sy1jschh/production/abc-10x10.png" in rewrite.sanity_assets(PAGE)


def test_sanity_assets_finds_an_image_named_only_by_asset_id():
    expected = f"{settings.SANITY_PROJECT_PATH}/{'f' * 40}-32x32.svg"
    assert expected in rewrite.sanity_assets(PAGE)


def test_rewrite_page_points_images_at_this_site():
    assert "https://cdn.sanity.io" not in rewrite.rewrite_page(PAGE)


def test_rewrite_page_removes_the_tag_manager():
    assert "googletagmanager" not in rewrite.rewrite_page(PAGE)


def test_rewrite_page_removes_the_consent_banner():
    assert "trustarc" not in rewrite.rewrite_page(PAGE)


def test_rewrite_page_keeps_the_stylesheet():
    assert "/_next/static/immutable/chunks/a1.css" in rewrite.rewrite_page(PAGE)


def test_rewrite_page_loads_the_runtime_config_first():
    assert rewrite.rewrite_page(PAGE).startswith(
        '<html><head><script src="/runtime-config.js"></script>'
    )


def test_rewrite_page_rejects_a_page_without_a_head():
    with pytest.raises(ValueError):
        rewrite.rewrite_page("<html><body></body></html>")


@pytest.mark.parametrize("description, pattern, replacement", settings.JS_PATCHES)
def test_patch_chunk_applies_each_patch(description, pattern, replacement):
    patched, applied = rewrite.patch_chunk(b"x" + pattern + b"y")
    assert (patched, applied) == (b"x" + replacement + b"y", {description})


def test_patch_chunk_reports_nothing_for_an_unrelated_chunk():
    assert rewrite.patch_chunk(b"console.log(1)") == (b"console.log(1)", set())
