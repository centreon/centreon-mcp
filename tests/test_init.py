from pathlib import Path

import pytest

from centreon_mcp import Settings


@pytest.mark.parametrize(
    "tls_secure,ca_bundle,verify",
    [
        (False, None, False),
        (False, "/does/not/exist", False),
        (True, None, True),
    ],
)
def test_settings_verify(tls_secure: bool, ca_bundle: str | None, verify: bool):

    settings = Settings(tls_secure=tls_secure, ca_bundle=ca_bundle)
    assert settings.verify == verify


def test_settings_verify_ca_bundle_exists(tmp_path: Path):

    ca_bundle = tmp_path / "ca-bundle.pem"
    ca_bundle.touch()

    settings = Settings(tls_secure=True, ca_bundle=str(ca_bundle))
    assert settings.verify == str(ca_bundle)


def test_settings_ca_bundle_not_exists():

    with pytest.raises(ValueError):
        _ = Settings(tls_secure=True, ca_bundle="/fake/path")
