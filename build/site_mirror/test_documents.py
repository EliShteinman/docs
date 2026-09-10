"""Tests for the single-body document types: glossary, tutorials, diagrams."""

from pathlib import Path

from build.site_mirror.documents import (
    TREES,
    DocumentTree,
    localize_markdown_images,
    render_document,
    title_of,
)

CDN = "https://cdn.sanity.io/images/sy1jschh/production"


def _tree(**kwargs) -> DocumentTree:
    base = dict(name="t", doc_type="x", prefix="/x/*", directory=Path("content/x"), index=None)
    return DocumentTree(**{**base, **kwargs})


def _block(text):
    return {
        "_type": "block",
        "style": "normal",
        "children": [{"_type": "span", "text": text, "marks": []}],
        "markDefs": [],
    }


def _resolve(reference, _alt=""):
    return f"/images/site-mirror/{reference}.webp"


def test_a_portable_text_body_is_rendered():
    tree = _tree()
    assert render_document(tree, {"body": [_block("Text.")]}, _resolve, lambda u: "") == "Text."


def test_a_markdown_body_is_carried_through_as_it_was_written():
    tree = _tree(body_field="markdownBody", body_is_markdown=True)
    body = "## Step one\n\n```python\nr.set('k','v')\n```"
    assert render_document(tree, {"markdownBody": body}, _resolve, lambda u: "") == body


def test_images_embedded_in_markdown_are_pointed_at_the_mirror():
    """Tutorials embed images as plain CDN URLs, not as asset references."""
    body = f"![a diagram]({CDN}/abc-100x50.png)"
    out = localize_markdown_images(body, lambda u: "/images/site-mirror/abc-100x50.webp")
    assert out == "![a diagram](/images/site-mirror/abc-100x50.webp)"


def test_an_image_that_could_not_be_mirrored_keeps_its_original_url():
    body = f"![x]({CDN}/abc-1x1.png)"
    assert localize_markdown_images(body, lambda u: "") == body


def test_a_link_is_not_mistaken_for_an_image():
    body = "[not an image](https://example.com/a.png)"
    assert localize_markdown_images(body, lambda u: "/local") == body


def test_a_lead_image_is_placed_above_the_body():
    """An architecture diagram is a caption plus a diagram; the caption alone is not it."""
    tree = _tree(body_field="content", lead_image_field="image")
    document = {"content": [_block("What it shows.")], "image": {"asset": {"_ref": "image-a-1x1-png"}}}
    out = render_document(tree, document, _resolve, lambda u: "")
    assert out.startswith("![") and out.endswith("What it shows.")


def test_a_tree_without_a_lead_image_field_renders_only_its_body():
    document = {"body": [_block("Text.")], "image": {"asset": {"_ref": "image-a-1x1-png"}}}
    assert render_document(_tree(), document, _resolve, lambda u: "") == "Text."


def test_the_projection_asks_for_the_field_this_type_calls_its_title():
    """A glossary entry has a `term` where a tutorial has a `title`."""
    assert "term" in _tree(title_field="term").projection


def test_the_projection_asks_for_a_lead_image_only_when_one_is_configured():
    assert "image" not in _tree().projection
    assert "image" in _tree(lead_image_field="image").projection


def test_the_title_is_read_from_the_field_the_type_uses():
    assert title_of(_tree(title_field="term"), {"term": "ACID"}) == "ACID"


def test_the_title_falls_back_when_the_named_field_is_missing():
    assert title_of(_tree(title_field="term"), {"title": "Fallback"}) == "Fallback"


def test_every_registered_tree_has_a_distinct_directory():
    directories = [t.directory for t in TREES]
    assert len(set(directories)) == len(directories)


def test_the_glossary_stays_out_of_the_documentations_own_section():
    """content/glossary holds the docs' own glossary; the mirror adds, never edits."""
    glossary = next(t for t in TREES if t.name == "glossary")
    assert glossary.directory != Path("content/glossary")


def test_a_path_outside_the_tree_is_not_claimed_by_it():
    """GROQ's `match` is token-based: a query for /solutions/* also returns
    /tutorials/howtos/solutions/... , which belongs to the tutorials."""
    from build.site_mirror.__main__ import _under

    assert _under("/solutions/*", "/tutorials/howtos/solutions/microservices/caching/") == ""


def test_a_path_inside_the_tree_yields_its_sub_path():
    from build.site_mirror.__main__ import _under

    assert _under("/tutorials/*", "/tutorials/develop/java/getting-started/") == "develop/java/getting-started"


def test_the_tree_root_is_not_one_of_its_own_documents():
    from build.site_mirror.__main__ import _under

    assert _under("/compare/*", "/compare/") == ""


def test_every_generated_index_is_valid_frontmatter():
    """A blurb that mentions redis.io carries a colon, which unquoted fails the build."""
    import yaml

    for tree in TREES:
        if tree.index is None:
            continue
        yaml.safe_load(tree.index.split("---")[1])


def test_only_frontmatter_declares_a_published_path(tmp_path):
    """A `url:` in the body is prose, not a declaration."""
    from build.site_mirror.__main__ import _known_urls

    (tmp_path / "a.md").write_text('---\nurl: "/blog/a/"\n---\n\nurl: not this one\n')
    assert _known_urls(tmp_path) == {"/blog/a/"}


def test_a_file_without_frontmatter_declares_nothing(tmp_path):
    from build.site_mirror.__main__ import _known_urls

    (tmp_path / "a.md").write_text("Just text.\n")
    assert _known_urls(tmp_path) == set()


def test_a_link_to_a_published_path_is_not_stale(tmp_path):
    from build.site_mirror.__main__ import _stale_targets

    (tmp_path / "a.md").write_text("[x](/blog/a/) and [y](/blog/missing/)\n")
    assert _stale_targets(tmp_path, {"/blog/a/"}) == ["/blog/missing/"]


def test_an_absolute_source_link_is_normalised_before_comparison(tmp_path):
    from build.site_mirror.__main__ import _stale_targets

    (tmp_path / "a.md").write_text("[x](https://redis.io/blog/a/)\n")
    assert _stale_targets(tmp_path, {"/blog/a/"}) == []


def test_no_tree_writes_into_a_section_the_documentation_owns():
    """The mirror is an addition to this site, never an edit to it.

    content/glossary is the documentation's own glossary -- 188 definitions
    written by hand in the body of its _index.md -- and an earlier version of
    this filed 56 mirrored terms into it and overwrote its layout. The sections
    below belong to the documentation; nothing may be written into them.
    """
    from build.site_mirror import categories, hugo

    OWNED = {
        Path("content/glossary"), Path("content/develop"), Path("content/operate"),
        Path("content/commands"), Path("content/integrate"), Path("content/apis"),
        Path("content/embeds"), Path("content/get-started"),
    }
    targets = (
        {t.directory for t in TREES}
        | {categories.BLOG.directory, categories.TUTORIALS.directory}
        | {hugo.SECTION_DIR, hugo.TECHNOLOGY_DIR, hugo.COMPARE_DIR, hugo.SOLUTIONS_DIR}
    )
    trespassing = targets & OWNED
    assert not trespassing, f"the mirror would write into {trespassing}"


def test_every_mirrored_directory_is_only_mirrored_files():
    """Whatever the mirror writes into, it must be the only thing in there.

    A directory holding one file the mirror did not write is a directory where
    pruning could destroy something, and where a sync overwrites someone's work.
    """
    from build.site_mirror import categories, hugo
    from build.site_mirror.hugo import is_generated

    root = Path(__file__).resolve().parents[2]
    targets = (
        {t.directory for t in TREES}
        | {categories.BLOG.directory, categories.TUTORIALS.directory}
        | {hugo.SECTION_DIR, hugo.TECHNOLOGY_DIR, hugo.COMPARE_DIR, hugo.SOLUTIONS_DIR}
    )
    for directory in sorted(targets):
        full = root / directory
        if not full.is_dir():
            continue
        strangers = [f.name for f in full.glob("*.md")
                     if f.name != "_index.md" and not is_generated(f)]
        assert not strangers, f"{directory} holds files the mirror did not write: {strangers[:3]}"


def test_version_builds_remove_exactly_the_mirrored_sections():
    """Both pipelines must strip the mirror from a version build, and nothing else.

    A version build keeps only public/<product>/<version>/, so the mirrored
    sections are rendered and thrown away -- 28 times over. Both pipelines drop
    them first. The list is written by hand in shell, where no import can keep
    it honest, and it was wrong: it named content/glossary, the documentation's
    own glossary, and left content/redis-glossary in place. That deleted 188
    hand-written definitions out of every version build and left 28 versioned
    pages relref-ing a section that was no longer there.
    """
    from build.site_mirror import categories, hugo

    root = Path(__file__).resolve().parents[2]
    expected = sorted(
        str(d) for d in (
            {t.directory for t in TREES}
            | {categories.BLOG.directory, categories.TUTORIALS.directory}
            | {hugo.SECTION_DIR, hugo.TECHNOLOGY_DIR, hugo.COMPARE_DIR, hugo.SOLUTIONS_DIR}
        )
    )
    for pipeline in ("airgap-multibuild.sh", ".github/workflows/airgap-build.yml"):
        lines = [
            line.strip() for line in (root / pipeline).read_text().splitlines()
            if line.strip().startswith("rm -rf content/blog ")
        ]
        assert len(lines) == 1, f"{pipeline} has {len(lines)} version-build rm lines"
        removed = sorted(lines[0].removeprefix("rm -rf").split())
        assert removed == expected, (
            f"{pipeline} removes {sorted(set(removed) - set(expected))} which the mirror "
            f"does not own, and keeps {sorted(set(expected) - set(removed))} which it does"
        )


def test_a_grouped_section_files_an_ungrouped_document_somewhere():
    """GroupByParam drops a page with no group; it must never have none.

    A grouped section's index is the only list that leads to its pages. A page
    the source left ungrouped would still be written and still be findable by
    search, and would be missing from that list -- silently, with no warning
    and no empty heading to notice.
    """
    from build.site_mirror.__main__ import UNGROUPED

    assert UNGROUPED, "a group value has to be truthy for GroupByParam to keep the page"
    grouped = [tree.name for tree in TREES if tree.group_field]
    assert grouped, "the guard is pointless if no tree groups its documents"
