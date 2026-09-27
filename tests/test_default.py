"""Testinfra checks for the summon role, run against the local macOS host."""

import pytest

PROVIDER = "/usr/local/lib/summon/ring.py"
VENV = "/usr/local/share/summon-keyring"
VENV_PYTHON = VENV + "/bin/python"

testinfra_hosts = ["local://"]


def test_summon_installed(host):
    assert host.run("summon --version").rc == 0


def test_ring_provider(host):
    ring = host.file(PROVIDER)
    assert ring.is_file
    assert ring.mode & 0o111
    assert VENV_PYTHON in ring.content_string
    assert host.file(VENV + "/ring.py").is_file


def test_ring_provider_runs(host):
    # With no secret argument ring.py prints usage and exits non-zero,
    # which proves the wrapper, interpreter, and keyring import work.
    # ring.py reaches this message only after importing keyring.
    result = host.run(PROVIDER)
    assert result.rc == 1
    assert "No variable was provided." in result.stderr


def test_provider_directory_only_holds_providers(host):
    assert host.file("/usr/local/lib/summon").listdir() == ["ring.py"]


@pytest.mark.parametrize("module", ["keyring"])
def test_keyring_importable(host, module):
    assert host.run(f"{VENV_PYTHON} -c 'import {module}'").rc == 0
