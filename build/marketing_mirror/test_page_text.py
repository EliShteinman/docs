from build.marketing_mirror import page_text

MAIN_PAGE = (
    "<html><head><title>Apna &amp; Redis | Redis</title></head><body>"
    "<header><nav>Platform Deploy</nav></header>"
    "<main><h1>Apna</h1><p>50,000 queries per second</p>"
    "<script>track()</script><button>Try free</button></main>"
    "<footer>Use cases</footer></body></html>"
)
STREAMED_PAGE = (
    "<html><body><header>Menu</header><main></main><footer>Footer</footer>"
    '<div hidden id="S:0"><h2>How they stack up</h2><p>Any cloud.</p></div>'
    "<script>swap()</script></body></html>"
)


def test_content_reads_the_main_element():
    assert "50,000 queries per second" in page_text.content(MAIN_PAGE)


def test_content_leaves_out_the_header_menus():
    assert "Platform" not in page_text.content(MAIN_PAGE)


def test_content_leaves_out_the_footer():
    assert "Use cases" not in page_text.content(MAIN_PAGE)


def test_content_leaves_out_scripts_and_buttons():
    text = page_text.content(MAIN_PAGE)
    assert "track()" not in text and "Try free" not in text


def test_content_reads_a_streamed_block():
    assert "Any cloud." in page_text.content(STREAMED_PAGE)


def test_content_marks_a_heading_for_the_section_split():
    assert "## How they stack up" in page_text.content(STREAMED_PAGE)


def test_content_is_empty_for_a_page_with_no_text():
    assert page_text.content("<html><body><main></main></body></html>") == ""


def test_title_drops_the_site_suffix_and_unescapes():
    assert page_text.title(MAIN_PAGE) == "Apna & Redis"


def test_title_falls_back_to_og_title():
    page = '<head><meta property="og:title" content="Apna &#x27;s story"/></head>'
    assert page_text.title(page) == "Apna 's story"


def test_title_falls_back_to_the_first_heading():
    page = '<main><h1 class="x"><span>Groww</span> scales</h1></main>'
    assert page_text.title(page) == "Groww scales"
