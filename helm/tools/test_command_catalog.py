import pytest

from command_catalog import CommandCatalog

PAGES = [
    "---\ntitle: HOTKEYS\nacl_categories:\n- '@slow'\n---\nbody",
    "---\ntitle: HOTKEYS START\nacl_categories:\n- '@admin'\n- '@dangerous'\n---\nbody",
    "---\ntitle: GET\nacl_categories:\n- '@read'\n---\nbody",
    "---\ntitle: Commands\n---\nan index page with no categories",
    "no frontmatter at all",
]


@pytest.fixture(scope="module")
def catalog() -> CommandCatalog:
    return CommandCatalog.from_pages(PAGES)


@pytest.mark.parametrize(
    "line,expected",
    [
        ("HOTKEYS START METRICS 2 CPU NET COUNT 10", "HOTKEYS START"),
        ("hotkeys start", "HOTKEYS START"),
        ("HOTKEYS", "HOTKEYS"),
        ("GET product:1", "GET"),
        ("[!NOTE] not a command", None),
        ("COMMANDS", None),
    ],
)
def test_resolve(catalog, line, expected):
    assert catalog.resolve(line) == expected


def test_categories(catalog):
    assert catalog.categories("HOTKEYS START") == frozenset({"@admin", "@dangerous"})
