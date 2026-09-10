"""Tests for mapping a page to the modal's product dropdown."""

import os
import pathlib
import re
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from search.product import ALL_PRODUCTS, KNOWN_PRODUCTS, product_of


@pytest.mark.parametrize(
    "url,expected",
    [
        ("/operate/rs/clusters", "rs"),
        ("/operate/rc/databases", "rc"),
        ("/operate/oss_and_stack/install", "oss_and_stack"),
        ("/operate/kubernetes/deployment", "kubernetes"),
        ("/integrate/redis-data-integration/quickstart", "redis-data-integration"),
        ("/develop/clients/jedis/connect", "clients"),
    ],
)
def test_product_comes_from_the_second_path_segment(url, expected):
    assert product_of(url) == expected


def test_the_same_product_is_found_under_a_different_first_segment():
    """Measured against the live service: p=redisinsight returns both trees."""
    assert product_of("/operate/redisinsight/install") == "redisinsight"
    assert product_of("/integrate/redisinsight/tutorial") == "redisinsight"


def test_a_page_outside_the_seven_products_carries_no_tag():
    assert product_of("/develop/data-types/strings") == ""


def test_a_top_level_page_carries_no_tag():
    assert product_of("/commands") == ""


def test_every_dropdown_value_is_known():
    """Read from the modal itself, not counted.

    KNOWN_PRODUCTS exists to mirror the <select> in search-modal.html, an
    upstream partial this fork does not own. Asserting its length only proved
    there were still seven of something: a renamed value would have kept the
    count and quietly filtered nothing. Upstream drift going unnoticed is this
    fork's recurring failure, so the comparison is against the real markup.
    """
    modal = (
        pathlib.Path(__file__).resolve().parents[3]
        / "layouts" / "partials" / "search-modal.html"
    )
    if not modal.is_file():
        pytest.skip("search-modal.html is not in this checkout")
    offered = set(re.findall(r'<option value="([^"]*)"', modal.read_text(encoding="utf-8")))
    assert offered - {ALL_PRODUCTS} == set(KNOWN_PRODUCTS), (
        "the modal offers products the search service does not tag for, or the "
        "other way round"
    )
