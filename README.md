# deekayen.summon

[![CI](https://github.com/deekayen/ansible-role-summon/actions/workflows/ci.yml/badge.svg)](https://github.com/deekayen/ansible-role-summon/actions/workflows/ci.yml) [![Ansible Galaxy](https://img.shields.io/badge/galaxy-deekayen.summon-blue.svg)](https://galaxy.ansible.com/ui/standalone/roles/deekayen/summon/) [![Project Status: Concept – Minimal or no implementation has been done yet, or the repository is only intended to be a limited example, demo, or proof-of-concept.](https://www.repostatus.org/badges/latest/concept.svg)](https://www.repostatus.org/#concept) ![BSD 3-Clause license](https://img.shields.io/badge/license-BSD%203--Clause-blue)

An Ansible role that installs CyberArk [Summon](https://cyberark.github.io/summon/) on macOS from Homebrew and sets up the [summon-keyring](https://github.com/conjurinc/summon-keyring) `ring.py` provider, so Summon can read secrets from the macOS keychain through the Python `keyring` library.

The role taps `cyberark/tools` and installs `cyberark/tools/summon` as the connecting user. It then creates a virtualenv at `summon_keyring_venv` with `/usr/bin/python3 -m venv`, installs `keyring` into it with that virtualenv's `pip`, and downloads the upstream `ring.py` into the virtualenv unmodified. The provider Summon loads, `{{ summon_provider_dir }}/ring.py`, is a small shell wrapper that runs the downloaded script with the virtualenv's Python. Upstream `ring.py` asks for `python`, which current macOS does not provide, and Homebrew's Python refuses `pip` installs (PEP 668), hence the separate virtualenv.

## Requirements

- ansible-core 2.15 or newer on the controller.
- The `community.general` collection for the Homebrew modules: `ansible-galaxy collection install community.general`.
- A macOS target with [Homebrew](https://brew.sh) installed for the connecting user, and `/usr/bin/python3` present.
- Outbound HTTPS from the target to GitHub, for the Homebrew tap and `summon_ring_url`, and to PyPI for `keyring`.
- Privilege escalation for the steps under `/usr/local`. Those tasks set `become: true` themselves; the Homebrew tasks must run as the unprivileged user because Homebrew refuses to run as root. Do not set `become: true` for the whole play. Pass `--ask-become-pass` or configure passwordless sudo instead.

## Supported platforms

| Platform | Versions |
| --- | --- |
| macOS | all |

CI applies the role twice to the `macos-latest` GitHub runner and verifies the result with testinfra. It skips the two Homebrew tasks, so CI exercises the provider directory, virtualenv, and `ring.py` setup but not the Summon install itself.

## Installation

From Ansible Galaxy:

```bash
ansible-galaxy role install deekayen.summon
ansible-galaxy collection install community.general
```

Or pin it in `requirements.yml`:

```yaml
---
roles:
  - name: deekayen.summon
    src: https://github.com/deekayen/ansible-role-summon.git
    scm: git
    version: main

collections:
  - name: community.general
```

```bash
ansible-galaxy install -r requirements.yml
```

## Role variables

| Variable | Default | Description |
| --- | --- | --- |
| `summon_provider_dir` | `/usr/local/lib/summon` | Directory Summon loads providers from. The role writes the `ring.py` wrapper here. Must be an absolute path. If you change it, set `SUMMON_PROVIDER_PATH` to match, since Summon looks in the default location otherwise. |
| `summon_keyring_venv` | `/usr/local/share/summon-keyring` | Virtualenv for the `keyring` library and the downloaded upstream `ring.py`. Must be an absolute path, and `tasks/assert.yml` fails the play if it sits inside `summon_provider_dir`, since Summon treats every file in that directory as a provider. |
| `summon_ring_url` | `https://raw.githubusercontent.com/conjurinc/summon-keyring/master/ring.py` | URL of the upstream `ring.py` script. The default tracks the `master` branch. |

## Behavior

- `ring.py` is requested from `summon_ring_url` on every run. Raw GitHub downloads ignore the conditional request, so the role replaces the copy in the virtualenv, and reports a change, whenever the upstream file changes.
- The virtualenv is created only if `{{ summon_keyring_venv }}/bin/python` is missing, and `keyring` is installed only if importing it fails. Neither is upgraded on later runs.
- The `homebrew` tasks use `state: present`, so an existing Summon install is not upgraded.

## Dependencies

None.

## Example playbook

```yaml
---
- name: Install Summon with the keychain provider.
  hosts: mac_workstations

  roles:
    - deekayen.summon
```

```bash
ansible-playbook -i inventory summon.yml --ask-become-pass
```

## Tags

| Tag | Tasks |
| --- | --- |
| `homebrew` | Tap `cyberark/tools` and install Summon. Skip it with `--skip-tags homebrew` when Summon is already installed or the tap is unreachable. |
| `always` | Input validation in `tasks/assert.yml`. |

## Development

CI runs on every push to `main` and every pull request (see `.github/workflows/ci.yml`):

1. Lint, on `ubuntu-latest`: `ansible-lint --profile production` and `flake8 tests/`.
2. macOS, on `macos-latest` with `ANSIBLE_SKIP_TAGS=homebrew`: runs `tests/test.yml` against localhost, runs it again and fails unless the recap shows `changed=0`, then runs testinfra with `-k 'not summon_installed'`. The workflow comment gives the reason for skipping Homebrew: the `cyberark/tools` tap queries the GitHub API for every formula it loads, and shared runners hit the rate limit.

The local commands below apply the role to the Mac you run them on, including the `sudo` steps under `/usr/local`:

```bash
pip3 install ansible-core ansible-lint flake8 pytest-testinfra
ansible-galaxy collection install community.general
ansible-lint --profile production
flake8 tests/
mkdir -p .ansible/roles && ln -sfn "$PWD" .ansible/roles/deekayen.summon
ANSIBLE_ROLES_PATH=.ansible/roles ANSIBLE_SKIP_TAGS=homebrew ansible-playbook -i tests/inventory tests/test.yml
py.test -v -k 'not summon_installed' tests/test_default.py
```

`tests/test_default.py` checks that the `ring.py` wrapper is executable and references the virtualenv's Python, that the upstream `ring.py` is in the virtualenv, that running the wrapper with no arguments exits 1 with `No variable was provided.` (printed only after `keyring` imports), that `ring.py` is the only file in the provider directory, and that `keyring` imports. `test_summon_installed` checks `summon --version` and is the test CI deselects. The tests hardcode the default paths.

The repository also has a `.pre-commit-config.yaml`; run `pre-commit run --all-files` before pushing.

### Repository layout

| Path | Purpose |
| --- | --- |
| `tasks/main.yml` | Homebrew tap and install, virtualenv, `keyring`, `ring.py` download, and the provider wrapper. |
| `tasks/assert.yml` | Path checks, tagged `always`. |
| `defaults/main.yml` | Every user-facing variable. |
| `meta/argument_specs.yml` | Argument types and descriptions. |
| `tests/` | Test playbook, inventory, and testinfra checks used by CI. |
| `.github/workflows/` | `ci.yml` for lint and the macOS run, `release.yml` for Galaxy import. |

## Releases

Pushing a git tag runs `.github/workflows/release.yml`, which imports the tagged commit into Ansible Galaxy as `deekayen.summon`. The import needs a `GALAXY_API_KEY` repository or organization secret.

## License

BSD 3-Clause. See [LICENSE](LICENSE).

## Author

[David Norman](https://github.com/deekayen). Sponsorship links are in [.github/FUNDING.yml](.github/FUNDING.yml).
