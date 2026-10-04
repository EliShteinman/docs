import pytest

from build.marketing_mirror import settings
from build.marketing_mirror import manifest
from build.marketing_mirror.__main__ import (
    CaptureFailed,
    _verify,
    replace,
    rewrite_on_disk,
)
from build.marketing_mirror.pages import html_file
from build.marketing_mirror.assets import AssetStore


class NoFetcher:
    def get(self, url: str) -> bytes:
        raise AssertionError("no network in this test")


@pytest.fixture
def assets(tmp_path) -> AssetStore:
    store = AssetStore(NoFetcher(), tmp_path)
    store.patches_applied = {description for description, _, _ in settings.JS_PATCHES}
    return store


def test_verify_accepts_a_run_with_no_failures(assets):
    _verify(["/a/"] * 100, [], assets)


def test_verify_rejects_a_run_that_lost_too_many_pages(assets):
    with pytest.raises(CaptureFailed):
        _verify(["/a/"] * 100, ["/a/"] * 3, assets)


def test_verify_rejects_a_run_where_a_js_patch_matched_nothing(assets):
    assets.patches_applied.pop()
    with pytest.raises(CaptureFailed):
        _verify(["/a/"], [], assets)


def test_replace_puts_the_new_run_in_place(tmp_path):
    site, staging = tmp_path / "site", tmp_path / "site.staging"
    site.mkdir()
    (site / "old.html").write_text("old")
    staging.mkdir()
    (staging / "new.html").write_text("new")
    replace(site, staging)
    assert sorted(path.name for path in site.iterdir()) == ["new.html"]


def test_replace_leaves_no_staging_directory_behind(tmp_path):
    site, staging = tmp_path / "site", tmp_path / "site.staging"
    staging.mkdir()
    replace(site, staging)
    assert not staging.exists()


def test_replace_keeps_the_submodule_gitlink(tmp_path):
    site, staging = tmp_path / "site", tmp_path / "site.staging"
    site.mkdir()
    (site / ".git").write_text("gitdir: ../../.git/modules/mirror/site")
    staging.mkdir()
    replace(site, staging)
    assert (site / ".git").read_text() == "gitdir: ../../.git/modules/mirror/site"


def test_replace_keeps_the_repository_attributes(tmp_path):
    site, staging = tmp_path / "site", tmp_path / "site.staging"
    site.mkdir()
    (site / ".gitattributes").write_text("* -diff")
    staging.mkdir()
    replace(site, staging)
    assert (site / ".gitattributes").read_text() == "* -diff"


@pytest.fixture
def site_on_disk(tmp_path):
    site = tmp_path / "site"
    html_file(site, "/blog/a/").parent.mkdir(parents=True)
    html_file(site, "/blog/a/").write_text(
        '<html><head><script src="/js/runtime-config.js"></script></head>'
        '<body><iframe src="https://www.youtube.com/embed/x"></iframe></body></html>'
    )
    manifest.save(site, manifest.Manifest(pages={"/blog/a/": "2026-10-01"}))
    return site


def test_rewrite_on_disk_rewrites_a_page_in_place(site_on_disk):
    rewrite_on_disk(site_on_disk)
    page = html_file(site_on_disk, "/blog/a/").read_text()
    assert settings.EMBED_UNAVAILABLE in page


def test_rewrite_on_disk_writes_the_unavailable_page(site_on_disk):
    rewrite_on_disk(site_on_disk)
    assert (site_on_disk / settings.EMBED_UNAVAILABLE.lstrip("/")).is_file()


def test_rewrite_on_disk_patches_a_chunk_on_disk(site_on_disk):
    chunk = site_on_disk / "_next/static/immutable/chunks/a.js"
    chunk.parent.mkdir(parents=True)
    _, pattern, replacement = settings.JS_PATCHES[0]
    chunk.write_bytes(pattern)
    rewrite_on_disk(site_on_disk)
    assert chunk.read_bytes() == replacement
