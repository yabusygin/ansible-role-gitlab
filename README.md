Ansible Role: gitlab
====================

An Ansible role installing [GitLab CE][GitLab].

[GitLab]: https://docs.gitlab.com/ce/README.html

Requirements
------------

None.

Role Variables
--------------

Optional variables:

*   `gitlab_image` (default: `gitlab/gitlab-ce`)
*   `gitlab_url` (default: `http://gitlab.example.com`)
*   `gitlab_ssh_port` (default: `22022`)
*   `gitlab_monitoring_whitelist` (default: `127.0.0.0/8`)

An example of variables usage provided in *Example Playbook* section.

Dependencies
------------

The role depends on [yabusygin.docker][Docker Role] role.

[Docker Role]: https://galaxy.ansible.com/yabusygin/docker

Example Playbook
----------------

```yaml
---
- hosts: production
  roles:
    - role: yabusygin.docker
  vars:
    gitlab_image: gitlab/gitlab-ce:12.7.6-ce.0
    gitlab_url: http://gitlab.test
    gitlab_ssh_port: 2222
    gitlab_monitoring_whitelist:
      - 127.0.0.0/8
      - 10.0.1.0/24
```

License
-------

MIT

Author Information
------------------

Alexey Busygin \<busygin.contact@yandex.ru\>
