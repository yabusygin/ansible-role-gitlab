Ansible Role: gitlab
====================

![Test workflow status](https://github.com/yabusygin/ansible-role-gitlab/workflows/test/badge.svg)
![Release workflow status](https://github.com/yabusygin/ansible-role-docker/workflows/release/badge.svg)

An Ansible role installing [GitLab CE][GitLab].

[GitLab]: https://docs.gitlab.com/ce/README.html

Requirements
------------

None.

Role Variables
--------------

All variables are optional.

`gitlab_image` variable specifies [GitLab Docker image][gitlab/gitlab-ce]
to install. Default value: `gitlab/gitlab-ce`.

`gitlab_external_url` variable specifies a value of `external_url` Omnibus
GitLab configuration option. Default value: `http://gitlab.example.com`.

`gitlab_rails_gitlab_shell_ssh_port` variable specifies a value of
`gitlab_rails['gitlab_shell_ssh_port']` Omnibus GitLab configuration option.
Default value: `22022`.

`gitlab_rails_monitoring_whitelist` variable specifies a value of
`gitlab_rails['monitoring_whitelist']` Omnibus GitLab configuration option.
The value could be specified as a string (address, subnet) or an array
of strings.

`gitlab_nginix_listen_port` variable specifies a value of
`nginix['listen_port']` Omnibus GitLab configuration option.

[gitlab/gitlab-ce]: https://hub.docker.com/r/gitlab/gitlab-ce

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
    - role: yabusygin.gitlab
  vars:
    gitlab_image: gitlab/gitlab-ce:12.7.6-ce.0
    gitlab_external_url: http://gitlab.test:8000
    gitlab_nginix_listen_port: 80
    gitlab_rails_gitlab_shell_ssh_port: 2222
    gitlab_rails_monitoring_whitelist:
      - 127.0.0.0/8
      - 10.0.1.0/24
```

License
-------

MIT

Author Information
------------------

Alexey Busygin \<busygin.contact@yandex.ru\>
