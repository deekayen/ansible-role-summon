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

Role Variables
--------------

None.

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

BSD

Author Information
------------------

David Norman
