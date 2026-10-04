import pytest

from build.marketing_mirror import manifest

DATE = "2026-09-24T22:31:58Z"


@pytest.fixture
def previous() -> manifest.Manifest:
    return manifest.Manifest(pages={"/blog/a/": DATE})


def test_a_page_with_the_same_date_is_current(previous):
    assert previous.is_current("/blog/a/", DATE)


def test_a_page_with_a_newer_date_is_not_current(previous):
    assert not previous.is_current("/blog/a/", "2026-09-30T00:00:00Z")


def test_a_page_the_last_run_did_not_have_is_not_current(previous):
    assert not previous.is_current("/blog/b/", DATE)


def test_an_undated_page_is_never_current():
    assert not manifest.Manifest(pages={"/x/": ""}).is_current("/x/", "")


def test_a_manifest_reads_back_as_written(tmp_path, previous):
    manifest.save(tmp_path, previous)
    assert manifest.load(tmp_path) == previous


def test_a_missing_manifest_reads_as_empty(tmp_path):
    assert manifest.load(tmp_path) == manifest.Manifest()
