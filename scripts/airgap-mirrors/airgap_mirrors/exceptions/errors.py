class AirgapMirrorError(Exception):
    pass


class ConfigurationError(AirgapMirrorError):
    pass


class GitCommandError(AirgapMirrorError):
    def __init__(self, arguments: list[str], returncode: int, stderr: str) -> None:
        self.arguments: list[str] = arguments
        self.returncode: int = returncode
        self.stderr: str = stderr
        super().__init__(f"git {' '.join(arguments)} failed ({returncode}): {stderr.strip()}")


class TransferError(AirgapMirrorError):
    pass


class MissingObjectsError(TransferError):
    def __init__(self, repository: str, missing_count: int) -> None:
        self.repository: str = repository
        self.missing_count: int = missing_count
        super().__init__(
            f"{repository}: {missing_count} commits this transfer builds on are not here yet. "
            "An earlier transfer was skipped: bring it over first, or run export with --full."
        )


class ApiError(AirgapMirrorError):
    def __init__(self, status: int, url: str, body: str) -> None:
        self.status: int = status
        self.url: str = url
        self.body: str = body
        super().__init__(f"HTTP {status} from {url}: {body[:300]}")


class GitHubApiError(ApiError):
    pass


class GitLabApiError(ApiError):
    pass


class ExtraFileDownloadError(ApiError):
    pass
