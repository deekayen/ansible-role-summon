Summon
=========

[![Build Status](https://travis-ci.org/deekayen/ansible-role-summon.svg?branch=master)](https://travis-ci.org/deekayen/ansible-role-summon)

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
