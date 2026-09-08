"""Tests for mapping a page to the modal's product dropdown."""

import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from search.product import KNOWN_PRODUCTS, product_of


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
    assert len(KNOWN_PRODUCTS) == 7
