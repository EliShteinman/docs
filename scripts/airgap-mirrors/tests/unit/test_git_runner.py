import base64
import subprocess
from pathlib import Path

import pytest
from pydantic import SecretStr
from pytest_mock import MockerFixture

from airgap_mirrors.exceptions import GitCommandError
from airgap_mirrors.git import GitRunner
from airgap_mirrors.internal import gitlab_git_config
from airgap_mirrors.settings import InternalRepoSpec, InternalSettings


def completed(returncode: int = 0, stdout: str = "", stderr: str = "") -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(args=[], returncode=returncode, stdout=stdout, stderr=stderr)


def test_output_is_returned(mocker: MockerFixture) -> None:
    mocker.patch("subprocess.run", return_value=completed(stdout="abc\n"))
    assert GitRunner().run(["rev-parse", "HEAD"]) == "abc\n"


def test_failure_carries_git_stderr(mocker: MockerFixture) -> None:
    mocker.patch("subprocess.run", return_value=completed(returncode=128, stderr="fatal: bad"))
    with pytest.raises(GitCommandError, match="fatal: bad"):
        GitRunner().run(["fetch"])


def test_config_travels_in_the_environment_not_the_arguments(mocker: MockerFixture) -> None:
    run = mocker.patch("subprocess.run", return_value=completed())
    GitRunner(config={"http.extraHeader": "Authorization: Basic x"}).run(["push"])
    environment: dict[str, str] = run.call_args.kwargs["env"]
    assert (environment["GIT_CONFIG_KEY_0"], environment["GIT_CONFIG_VALUE_0"]) == (
        "http.extraHeader",
        "Authorization: Basic x",
    )


def test_secret_never_appears_in_the_arguments(mocker: MockerFixture) -> None:
    run = mocker.patch("subprocess.run", return_value=completed())
    GitRunner(config={"http.extraHeader": "secret"}).run(["push", "url"])
    assert "secret" not in " ".join(run.call_args.args[0])


def test_git_never_prompts_for_a_password(mocker: MockerFixture) -> None:
    run = mocker.patch("subprocess.run", return_value=completed())
    GitRunner().run(["fetch"])
    assert run.call_args.kwargs["env"]["GIT_TERMINAL_PROMPT"] == "0"


def test_succeeds_reports_the_exit_status(tmp_path: Path) -> None:
    assert GitRunner().succeeds(["rev-parse", "--git-dir"], cwd=tmp_path) is False


@pytest.fixture
def internal(tmp_path: Path) -> InternalSettings:
    return InternalSettings(
        mirrors_dir=tmp_path,
        transfer_dir=tmp_path,
        gitlab_url="https://gitlab.example",
        gitlab_group="g",
        release_package_name="p",
        http_timeout_seconds=5,
        GITLAB_TOKEN=SecretStr("glpat-x"),
        repos=[InternalRepoSpec(name="r", gitlab_path="g/r")],
    )


def test_gitlab_push_uses_the_token_as_basic_auth(internal: InternalSettings) -> None:
    header: str = gitlab_git_config(internal)["http.extraHeader"]
    assert base64.b64decode(header.removeprefix("Authorization: Basic ")).decode() == "oauth2:glpat-x"


def test_company_ca_is_passed_to_git(internal: InternalSettings, tmp_path: Path) -> None:
    with_ca: InternalSettings = internal.model_copy(update={"ca_file": tmp_path / "ca.pem"})
    assert gitlab_git_config(with_ca)["http.sslCAInfo"] == str(tmp_path / "ca.pem")
