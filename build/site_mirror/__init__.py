"""Mirror redis.io content into the docs site as Hugo pages.

Much of what Redis publishes about its own architecture exists outside the
documentation -- on the blog, and in the /technology/ guides -- so an
air-gapped reader who follows one of those links loses the material entirely.
This package brings it inside.

The blog is not scraped. redis.io is a Sanity-backed site whose `production`
dataset is publicly readable, so the posts come across as structured content --
Portable Text, not HTML -- which is why a post lands here as 8 KB of markdown
instead of the 1.6 MB of Next.js payload its rendered page weighs.

Two shapes, one pipeline. A blog post is a single Portable Text field; a
/technology/ page is a list of layout sections with its prose spread across
them (see pages.py). Both land under the paths redis.io publishes them at.

Everything it writes is generated: `content/blog/`, `content/technology/` and
`static/images/site-mirror/` are outputs, not sources. Re-running reproduces
them.
"""
