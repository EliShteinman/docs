import pytest

from build.marketing_mirror import settings
from build.marketing_mirror.__main__ import CaptureFailed, _verify, replace
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
