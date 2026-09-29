"""Tests for writing the site's llms.txt from redis.io's."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from build.llms_txt import DOCS_FEED, MIRROR_FEED, LinkResolver, rewrite

PUBLISHED = {
    "/",
    "/commands/get/",
    "/develop/",
    "/develop/data-types/streams/",
    "/develop/reference/eviction/",
    "/develop/interact/pubsub/",
    "/develop/pubsub/",
    "/develop/reference/modules/api/",
}

ALIASES = {"/develop/interact/pubsub/": "/develop/pubsub/"}

SOURCE = """# Redis Documentation

> Redis: in-memory data platform.

## Core Docs

- [Docs homepage](https://redis.io/docs/latest/): Entry point.
- [Develop](https://redis.io/docs/latest/develop/index.html.md): Hub.

## Products

- [Pricing](https://redis.io/pricing/): Plans.

## Tutorials

### For AI

- [Flowise agent](https://redis.io/tutorials/flowise-agent.md): Hands-on.

### Missing

- [Gone tutorial](https://redis.io/tutorials/gone.md): Not on disk.
"""


@pytest.fixture
def mirror_dir(tmp_path: Path) -> Path:
    site = tmp_path / "site"
    (site / "tutorials").mkdir(parents=True)
    (site / "tutorials" / "flowise-agent.md").write_text("# Flowise\n")
    return site


@pytest.fixture
def followed() -> list[str]:
    return []


@pytest.fixture
def resolver(mirror_dir: Path, followed: list[str]) -> LinkResolver:
    moves = {
        "https://redis.io/docs/latest/develop/interact/streams/": (
            "https://redis.io/docs/latest/develop/data-types/streams/"
        ),
    }

    def follow(url: str) -> str:
        followed.append(url)
        return moves.get(url, url)

    return LinkResolver(PUBLISHED, ALIASES, mirror_dir, follow)


@pytest.fixture
def with_mirror(resolver: LinkResolver) -> str:
    return rewrite(SOURCE, resolver, with_mirror=True)


@pytest.fixture
def docs_only(resolver: LinkResolver) -> str:
    return rewrite(SOURCE, resolver, with_mirror=False)


def test_a_documentation_link_points_at_the_runtime_base_url(with_mirror: str) -> None:
    assert "(__DOCS_BASE_URL__/develop/index.html.md)" in with_mirror


def test_the_documentation_home_keeps_its_trailing_slash(with_mirror: str) -> None:
    assert "(__DOCS_BASE_URL__/)" in with_mirror


def test_no_link_to_redis_io_is_left(with_mirror: str) -> None:
    assert "https://redis.io" not in with_mirror


def test_a_product_page_the_image_lacks_is_dropped(with_mirror: str) -> None:
    assert "Pricing" not in with_mirror


def test_a_heading_left_without_links_is_dropped(with_mirror: str) -> None:
    assert "## Products" not in with_mirror


def test_a_mirrored_tutorial_is_kept_with_the_mirror(with_mirror: str) -> None:
    assert "(__DOCS_BASE_URL__/tutorials/flowise-agent.md)" in with_mirror


def test_a_tutorial_not_on_disk_is_dropped(with_mirror: str) -> None:
    assert "Gone tutorial" not in with_mirror


def test_a_subheading_left_empty_is_dropped_while_its_sibling_stays(
    with_mirror: str,
) -> None:
    assert "### Missing" not in with_mirror and "### For AI" in with_mirror


def test_the_docs_only_file_leaves_the_mirrored_tutorials_out(docs_only: str) -> None:
    assert "tutorials" not in docs_only


def test_the_docs_only_file_drops_the_section_the_mirror_filled(docs_only: str) -> None:
    assert "## Tutorials" not in docs_only


def test_both_files_list_the_documentation_feed(
    with_mirror: str, docs_only: str
) -> None:
    assert DOCS_FEED in with_mirror and DOCS_FEED in docs_only


def test_only_the_mirror_file_lists_the_mirror_feed(
    with_mirror: str, docs_only: str
) -> None:
    assert MIRROR_FEED in with_mirror and MIRROR_FEED not in docs_only


def test_the_title_and_summary_survive(docs_only: str) -> None:
    assert docs_only.startswith(
        "# Redis Documentation\n\n> Redis: in-memory data platform."
    )


def test_a_moved_documentation_page_links_to_where_redis_io_sends_it(
    resolver: LinkResolver,
) -> None:
    target = resolver.resolve(
        "https://redis.io/docs/latest/develop/interact/streams/index.html.md"
    )
    assert target is not None
    assert target.url == "__DOCS_BASE_URL__/develop/data-types/streams/index.html.md"


def test_a_documentation_page_that_lands_nowhere_local_is_dropped(
    resolver: LinkResolver,
) -> None:
    assert resolver.resolve("https://redis.io/docs/latest/never/was/") is None


def test_a_published_page_is_not_followed(
    resolver: LinkResolver, followed: list[str]
) -> None:
    resolver.resolve("https://redis.io/docs/latest/develop/")
    assert followed == []


def test_each_link_is_followed_once_for_both_files(
    resolver: LinkResolver, followed: list[str]
) -> None:
    source = "- [Old](https://redis.io/docs/latest/develop/interact/streams/): Moved."
    rewrite(source, resolver, with_mirror=True)
    rewrite(source, resolver, with_mirror=False)
    assert len(followed) == 1


def test_a_top_level_section_without_its_own_page_counts_as_published(
    resolver: LinkResolver,
) -> None:
    target = resolver.resolve("https://redis.io/docs/latest/commands/")
    assert target is not None and target.url == "__DOCS_BASE_URL__/commands/"


def test_a_leaf_bundle_counts_as_published(resolver: LinkResolver) -> None:
    target = resolver.resolve(
        "https://redis.io/docs/latest/develop/reference/eviction/"
    )
    assert target is not None


def test_a_nested_directory_without_its_own_page_does_not(
    resolver: LinkResolver,
) -> None:
    assert (
        resolver.resolve("https://redis.io/docs/latest/develop/reference/modules/")
        is None
    )
