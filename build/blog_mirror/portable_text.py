"""Rendering Sanity's Portable Text as the markdown Hugo builds.

The block vocabulary is small and closed -- checked across all 1,108 posts,
there are fourteen block types, eight paragraph styles and seven marks -- so
this covers the corpus rather than the format in general.

Two kinds of block are deliberately dropped rather than rendered: the CTA
interrupters and button rows that sell Redis Cloud mid-article. They are
marketing furniture pointing at pages an air-gapped reader cannot reach, and
carrying them across would put dead "Try Redis Cloud" buttons inside mirrored
documentation.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable

from build.blog_mirror.links import localize

# Rendered for their content.
HEADING_STYLES = {"h1", "h2", "h3", "h4", "h5", "h6"}

# Dropped: outbound marketing, not article content.
PROMOTIONAL_BLOCKS = {
    "blockContentCtaInterrupter",
    "blockContentBlogCta",
    "blockContentBlogButtons",
}

ImageResolver = Callable[[str, str], str]


def _escape_cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ").strip()


def _link_target(definition: dict) -> str:
    """Return the URL a link markDef points at, or "" when it points nowhere.

    Two shapes occur in the corpus: a plain {href}, and Sanity's link element
    {linkType, externalLink, anchor}. A third carries only an unresolved
    internal reference; those become plain text rather than a link to nothing.
    """
    return localize(definition.get("href") or definition.get("externalLink") or "")


def _without_emphasis(span: dict) -> dict:
    kept = [m for m in span.get("marks", []) if m not in ("strong", "em")]
    return {**span, "marks": kept}


def _render_span(span: dict, definitions: list[dict]) -> str:
    text = span.get("text", "")
    if not text:
        return ""
    marks = span.get("marks", [])
    # Innermost first: code before emphasis before strong, so the delimiters
    # nest the way markdown parses them.
    if "inlineCode" in marks:
        text = f"`{text}`"
    if "em" in marks:
        text = f"*{text}*"
    if "strong" in marks:
        text = f"**{text}**"
    for mark in marks:
        definition = next((d for d in definitions if d.get("_key") == mark), None)
        if definition and definition.get("_type") == "link":
            target = _link_target(definition)
            if target:
                text = f"[{text}]({target})"
    return text


def _render_text_block(block: dict) -> str:
    definitions = block.get("markDefs") or []
    style = block.get("style") or "normal"
    # Most of the corpus bolds its own headings, which markdown renders as bold
    # text inside a heading that is already bold. The heading level carries the
    # emphasis, so the marks are dropped rather than doubled.
    heading = style in HEADING_STYLES
    text = "".join(
        _render_span(_without_emphasis(span) if heading else span, definitions)
        for span in block.get("children") or []
    )
    if block.get("listItem"):
        indent = "  " * max((block.get("level") or 1) - 1, 0)
        marker = "1." if block["listItem"] == "number" else "-"
        return f"{indent}{marker} {text}"
    if style in HEADING_STYLES:
        return "#" * int(style[1]) + " " + text
    if style == "blockquote":
        return "> " + text
    return text


def _render_code(block: dict) -> str:
    snippet = block.get("codeSnippet") or {}
    code = snippet.get("code") or ""
    if not code.strip():
        return ""
    # "plain" is Sanity's no-highlighting choice, and jscript is its spelling of
    # JavaScript; neither is a language Hugo's highlighter knows.
    language = (snippet.get("language") or "").strip()
    if language in ("plain", "jscript"):
        language = "javascript" if language == "jscript" else ""
    return f"```{language}\n{code}\n```"


def _render_table(block: dict) -> str:
    rows = ((block.get("table") or {}).get("rows")) or []
    cells = [[_escape_cell(str(cell)) for cell in (row.get("cells") or [])] for row in rows]
    cells = [row for row in cells if row]
    if not cells:
        return ""
    width = max(len(row) for row in cells)
    padded = [row + [""] * (width - len(row)) for row in cells]
    header, *body = padded
    lines = ["| " + " | ".join(header) + " |", "|" + "---|" * width]
    lines += ["| " + " | ".join(row) + " |" for row in body]
    return "\n".join(lines)


def _asset_ref(container: dict) -> str:
    return ((container.get("image") or container).get("asset") or {}).get("_ref") or ""


def _render_image(block: dict, resolve_image: ImageResolver) -> str:
    reference = _asset_ref(block)
    if not reference:
        return ""
    alt = ((block.get("image") or {}).get("altText") or "").replace("]", ")")
    path = resolve_image(reference, alt)
    return f"![{alt}]({path})" if path else ""


def _render_video(block: dict) -> str:
    """A video becomes a link, not an embed.

    The player is hosted off-site, so an embedded frame is a blank rectangle in
    an air-gapped browser. A labelled link at least tells the reader what they
    are missing and where it lives.
    """
    url = localize(block.get("videoUrl") or "")
    label = block.get("buttonLabel") or "Watch the video"
    return f"[{label}]({url})" if url else ""


def _render_quote(block: dict, resolve_image: ImageResolver) -> str:
    inner = render(block.get("quote") or [], resolve_image)
    return "\n".join("> " + line if line else ">" for line in inner.splitlines())


def _render_embed(block: dict) -> str:
    """Third-party iframes are named, not carried.

    The markup points at S3 buckets and chart hosts that do not resolve in an
    air-gapped network, and pasting a dead iframe into the page would look like
    a rendering fault rather than a missing external resource.
    """
    return "" if not (block.get("embed") or "").strip() else "*(interactive chart, not available offline)*"


def _render_anchor(block: dict) -> str:
    identifier = (block.get("identifier") or {}).get("current") or ""
    title = block.get("title") or identifier
    # Hugo's explicit-anchor heading syntax, so in-page links to it still land.
    return f"### {title} {{#{identifier}}}" if identifier else ""


def render(blocks: Iterable[dict], resolve_image: ImageResolver) -> str:
    """Return the markdown for `blocks`."""
    rendered: list[str] = []
    for block in blocks or []:
        block_type = block.get("_type")
        if block_type in PROMOTIONAL_BLOCKS:
            continue
        if block_type == "block":
            piece = _render_text_block(block)
        elif block_type == "blockContentBlogCode":
            piece = _render_code(block)
        elif block_type == "blockContentBlogTable":
            piece = _render_table(block)
        elif block_type in ("blockContentBlogImage", "blockContentBlogComparisonTable"):
            piece = _render_image(block, resolve_image)
        elif block_type == "blockContentBlogVideo":
            piece = _render_video(block)
        elif block_type == "blockContentBlogQuote":
            piece = _render_quote(block, resolve_image)
        elif block_type == "blockContentBlogEmbed":
            piece = _render_embed(block)
        elif block_type == "blockContentAnchorPoint":
            piece = _render_anchor(block)
        elif block_type == "divider":
            piece = "---"
        else:
            piece = ""
        if piece.strip():
            rendered.append(piece)
    return _join(rendered)


def _join(pieces: list[str]) -> str:
    """Join blocks with a blank line, except between consecutive list items."""
    output: list[str] = []
    for piece in pieces:
        if output and _is_list_item(piece) and _is_list_item(output[-1]):
            output.append(piece)
        else:
            if output:
                output.append("")
            output.append(piece)
    return "\n".join(output)


def _is_list_item(piece: str) -> bool:
    stripped = piece.lstrip()
    return stripped.startswith("- ") or stripped.startswith("1. ")
