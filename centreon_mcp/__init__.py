import os

CREDENTIALS = {
    name: (os.environ.get(name) or default)
    for name, default in [
        ("CENTREON_HOST", "localhost"),
        ("CENTREON_PORT", "4000"),
        ("CENTREON_API_TOKEN", ""),
    ]
}
