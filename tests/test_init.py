import pytest

from centreon_mcp import Settings


@pytest.mark.parametrize(
    "tls_secure,ca_bundle,verify",
    [(False, None, False), (False, "/does/not/exist", False), (True, None, True)],
)
def test_settings_verify(tls_secure: bool, ca_bundle: str | None, verify: bool):

    settings = Settings(
        base_url="http://localhost:4000/centreon", tls_secure=tls_secure, ca_bundle=ca_bundle
    )
    assert settings.verify == verify
