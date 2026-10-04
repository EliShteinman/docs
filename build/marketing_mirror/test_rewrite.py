import pytest

from build.marketing_mirror import rewrite, settings

PAGE = (
    '<html><head><meta charset="utf-8"/>'
    '<script src="https://www.googletagmanager.com/gtm.js?id=X"></script>'
    '<link rel="preload" href="https://consent.trustarc.com/notice?x=1" as="script"/>'
    '<link rel="stylesheet" href="/_next/static/immutable/chunks/a1.css"/>'
    '<script type="module" src="https://static.cloudflareinsights.com/beacon.min.js/v1"'
    ' integrity="sha512-x" data-cf-beacon=\'{"version":"2024.11.0","spa":2}\''
    ' crossorigin="anonymous"></script>'
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


def test_rewrite_page_removes_the_cloudflare_beacon():
    assert "cloudflareinsights" not in rewrite.rewrite_page(PAGE)


def test_rewrite_page_keeps_the_stylesheet():
    assert "/_next/static/immutable/chunks/a1.css" in rewrite.rewrite_page(PAGE)


def test_rewrite_page_loads_the_runtime_config_first():
    assert rewrite.rewrite_page(PAGE).startswith(
        '<html><head><script src="/js/runtime-config.js"></script>'
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


def test_sanity_assets_finds_an_image_in_a_page_already_rewritten():
    page = '<img src="/sanity/images/sy1jschh/production/abc-10x10.png?w=64"/>'
    assert rewrite.sanity_assets(page) == {"/images/sy1jschh/production/abc-10x10.png"}


@pytest.mark.parametrize("description, pattern, replacement", settings.JS_PATCHES)
def test_patch_chunk_counts_a_chunk_already_patched(description, pattern, replacement):
    assert description in rewrite.patch_chunk(replacement)[1]


def test_patch_chunk_leaves_a_chunk_already_patched_unchanged():
    patched = b"".join(replacement for _, _, replacement in settings.JS_PATCHES)
    assert rewrite.patch_chunk(patched)[0] == patched


CHART = "https://vecsim-benchmarks-charts.s3.us-east-2.amazonaws.com/blog/chart.html"
LOCAL_CHART = "/_mirror/embeds/vecsim-benchmarks-charts/blog/chart.html"
PODCAST = "https://anchor.fm/show/embed/episodes/one"
VIDEO = "https://www.youtube.com/embed/abc"
LINK = "https://launchpad.redis.com/?id=project%3Ademo"

FRAMED_PAGE = (
    f'<iframe loading="lazy" src="{CHART}"></iframe>'
    f'<iframe src="{PODCAST}"></iframe>'
    f'<iframe src="https://launchpad.redis.com/"></iframe>'
    f'<a href="{LINK}">demo</a>'
    '<script>self.__next_f.push([1,"'
    f'\\"embed\\":\\"\\u003ciframe src=\\\\\\"{PODCAST}\\\\\\"\\u003e\\",'
    f'\\"videoUrl\\":\\"{VIDEO}?a=1\\u0026t=2\\"'
    '"])</script>'
)
FRAMED_REWRITTEN = rewrite.offline_players(rewrite.local_embeds(FRAMED_PAGE))


def test_local_embeds_points_a_chart_at_this_site():
    assert f'src="{LOCAL_CHART}"' in rewrite.local_embeds(FRAMED_PAGE)


def test_framed_urls_finds_an_iframe_in_the_next_payload():
    payload_only = FRAMED_PAGE[FRAMED_PAGE.index("<script>") :]
    assert PODCAST in rewrite.framed_urls(payload_only)


def test_framed_urls_finds_a_video_modal_player():
    assert f"{VIDEO}?a=1" in rewrite.framed_urls(FRAMED_PAGE)


def test_offline_players_leaves_no_frame_pointing_away():
    remote = [url for url in rewrite.framed_urls(FRAMED_REWRITTEN) if "//" in url]
    assert remote == []


def test_offline_players_removes_the_podcast_everywhere():
    assert "anchor.fm" not in FRAMED_REWRITTEN


def test_offline_players_drops_the_rest_of_a_url_cut_at_an_escaped_ampersand():
    assert "t=2" not in FRAMED_REWRITTEN


def test_offline_players_keeps_a_link_that_only_starts_like_a_frame():
    assert f'href="{LINK}"' in FRAMED_REWRITTEN


def test_offline_players_keeps_the_local_chart():
    assert f'src="{LOCAL_CHART}"' in FRAMED_REWRITTEN


def test_local_embed_pages_finds_the_local_chart():
    assert rewrite.local_embed_pages(FRAMED_REWRITTEN) == {LOCAL_CHART}


def test_rewrite_page_shows_the_unavailable_page_for_a_player():
    page = f'<html><head></head><body><iframe src="{VIDEO}"></iframe></body></html>'
    assert f'src="{settings.EMBED_UNAVAILABLE}"' in rewrite.rewrite_page(page)


INJECTED = "".join(
    f'<script src="{src}"></script>' for src in settings.INJECTED_SCRIPTS
)
OLD_RUN_PAGE = (
    '<html><head><script src="/js/runtime-config.js"></script>'
    '<script src="/_mirror/marketing-links.js"></script>'
    '<script type="module" src="https://static.cloudflareinsights.com/beacon.min.js/v1">'
    "</script></head><body>"
    f'<iframe src="{VIDEO}"></iframe></body></html>'
)


def test_rewrite_again_loads_each_script_once():
    again = rewrite.rewrite_again(OLD_RUN_PAGE)
    assert again.count("/_mirror/marketing-links.js") == 1


def test_rewrite_again_loads_today_s_scripts_first():
    assert rewrite.rewrite_again(OLD_RUN_PAGE).startswith(f"<html><head>{INJECTED}")


def test_rewrite_again_applies_a_rule_the_earlier_run_did_not_have():
    assert "cloudflareinsights" not in rewrite.rewrite_again(OLD_RUN_PAGE)


def test_rewrite_again_leaves_a_page_rewritten_today_as_it_is():
    today = rewrite.rewrite_again(OLD_RUN_PAGE)
    assert rewrite.rewrite_again(today) == today
