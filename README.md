Summon
======

[![CI](https://github.com/deekayen/ansible-role-summon/actions/workflows/ci.yml/badge.svg)](https://github.com/deekayen/ansible-role-summon/actions/workflows/ci.yml) [![Project Status: Concept – Minimal or no implementation has been done yet, or the repository is only intended to be a limited example, demo, or proof-of-concept.](https://www.repostatus.org/badges/latest/concept.svg)](https://www.repostatus.org/#concept)

Install [Summon](https://cyberark.github.io/summon/) from [CyberArk](https://github.com/cyberark).


Requirements
------------

[Homebrew](https://brew.sh)

If the cyberark tap fails, try:

```
sudo xcodebuild -license accept
```

The role installs Summon from Homebrew as your user, and uses `become` for
the steps under `/usr/local`, so run it with `--ask-become-pass` (or
passwordless sudo). The keyring library goes into its own virtualenv, since
Homebrew's Python does not allow pip installs, and `ring.py` in the provider
directory is a wrapper that runs the upstream script with that virtualenv's
Python.

CI runs the role twice on the current GitHub macOS runner and checks the
result with testinfra. It skips the two Homebrew tasks (tag `homebrew`),
because the cyberark/tools tap queries the GitHub API for every formula it
loads, which the shared runners' rate limits reject.

Role Variables
--------------

    summon_provider_dir: /usr/local/lib/summon
    summon_keyring_venv: /usr/local/share/summon-keyring
    summon_ring_url: https://raw.githubusercontent.com/conjurinc/summon-keyring/master/ring.py

Dependencies
------------

None.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: all:!platform_windows

      roles:
        - deekayen.summon

License
-------

BSD-3-Clause

Author Information
------------------

David Norman
