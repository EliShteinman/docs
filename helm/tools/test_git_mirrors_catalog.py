"""The repositories the chart can rewrite links for are the ones the transfer tool copies."""

import os
import tomllib

import pytest
import yaml

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CATALOG = os.path.join(REPO, "helm", "redis-docs", "files", "external-links.yaml")
TRANSFER_CONFIG_DIR = os.path.join(REPO, "scripts", "airgap-mirrors", "config")


def catalog_names() -> set[str]:
    with open(CATALOG, encoding="utf-8") as catalog:
        return set(yaml.safe_load(catalog)["git-mirrors"])


def transfer_config_names(file_name: str) -> set[str]:
    with open(os.path.join(TRANSFER_CONFIG_DIR, file_name), "rb") as config:
        return {repo["name"] for repo in tomllib.load(config)["repos"]}


@pytest.mark.parametrize("file_name", ["external.toml.example", "internal.toml.example"])
def test_transfer_tool_carries_the_catalog_repositories(file_name: str) -> None:
    assert transfer_config_names(file_name) == catalog_names()


def test_transfer_tool_fetches_each_catalog_repo_from_its_github_name() -> None:
    with open(CATALOG, encoding="utf-8") as catalog:
        catalog_repos = {name: entry["repo"] for name, entry in yaml.safe_load(catalog)["git-mirrors"].items()}
    with open(os.path.join(TRANSFER_CONFIG_DIR, "external.toml.example"), "rb") as config:
        tool_repos = {repo["name"]: repo["github"] for repo in tomllib.load(config)["repos"]}
    assert tool_repos == catalog_repos
