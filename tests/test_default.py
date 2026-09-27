"""Testinfra checks for the summon role, run against the local macOS host."""

import pytest

PROVIDER = "/usr/local/lib/summon/ring.py"
VENV_PYTHON = "/usr/local/share/summon-keyring/bin/python"

testinfra_hosts = ["local://"]


def test_summon_installed(host):
    assert host.run("summon --version").rc == 0


def test_ring_provider(host):
    ring = host.file(PROVIDER)
    assert ring.is_file
    assert ring.mode & 0o111
    assert ring.content_string.splitlines()[0] == "#!" + VENV_PYTHON


def test_provider_directory_only_holds_providers(host):
    assert host.file("/usr/local/lib/summon").listdir() == ["ring.py"]


@pytest.mark.parametrize("module", ["keyring"])
def test_keyring_importable(host, module):
    assert host.run(f"{VENV_PYTHON} -c 'import {module}'").rc == 0
