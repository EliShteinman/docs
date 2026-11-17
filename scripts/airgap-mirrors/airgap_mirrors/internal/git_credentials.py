import base64

from airgap_mirrors.settings import InternalSettings


def gitlab_git_config(settings: InternalSettings) -> dict[str, str]:
    """Git settings for pushing to GitLab over HTTPS with the token, passed through the environment."""
    credentials: bytes = f"oauth2:{settings.gitlab_token.get_secret_value()}".encode()
    config: dict[str, str] = {"http.extraHeader": f"Authorization: Basic {base64.b64encode(credentials).decode()}"}
    if settings.ca_file is not None:
        config["http.sslCAInfo"] = str(settings.ca_file)
    return config
