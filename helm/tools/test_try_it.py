import pytest

from try_it import try_it_lines

CLIENTS_EXAMPLE = """
{{< clients-example set="s" step="a" >}}
> SET k v
OK
redis> GET k
"v"
{{< /clients-example >}}
"""

NOT_RUNNABLE = """
{{< clients-example set="s" step="b" runnable="false" >}}
> BLPOP k 0
{{< /clients-example >}}
"""

REDIS_CLI = """
{{% redis-cli %}}
redis> ROLE
1) "master"
{{% /redis-cli %}}
"""

PLAIN_FENCE = """
```
> ACL LIST
```
"""

SELF_CLOSING_THEN_BLOCK = """
{{< clients-example set="s" step="c" />}}
> FLUSHALL
{{< clients-example set="s" step="d" >}}
> PING
{{< /clients-example >}}
"""


@pytest.mark.parametrize(
    "markdown,expected",
    [
        (CLIENTS_EXAMPLE, ["SET k v", "GET k"]),
        (NOT_RUNNABLE, []),
        (REDIS_CLI, ["ROLE"]),
        (PLAIN_FENCE, []),
        (SELF_CLOSING_THEN_BLOCK, ["PING"]),
    ],
    ids=["clients-example", "runnable-false", "redis-cli", "plain-fence", "self-closing"],
)
def test_try_it_lines(markdown, expected):
    assert try_it_lines(markdown) == expected
