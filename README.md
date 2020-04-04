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

All variables are optional. The most of variables set values of corresponding
Omnibus GitLab settings:

*   Docker:

    | Role Variable  | Omnibus GitLab setting | Default Value      |
    | -------------- | ---------------------- | ------------------ |
    | `gitlab_image` | none                   | `gitlab/gitlab-ce` |

    `gitlab_image` variable specifies [GitLab Docker image][gitlab/gitlab-ce]
    to install.

    [gitlab/gitlab-ce]: https://hub.docker.com/r/gitlab/gitlab-ce

*   Basic settings:

    | Role Variable         | Omnibus GitLab setting | Default Value               |
    | --------------------- | ---------------------- | --------------------------- |
    | `gitlab_external_url` | `external_url`         | `http://gitlab.example.com` |

*   GitLab shell SSH port:

    | Role Variable                        | Omnibus GitLab setting                  |
    | ------------------------------------ | --------------------------------------- |
    | `gitlab_rails_gitlab_shell_ssh_port` | `gitlab_rails['gitlab_shell_ssh_port']` |

*   Monitoring white list:

    | Role Variable                       | Omnibus GitLab setting                 |
    | ----------------------------------- | -------------------------------------- |
    | `gitlab_rails_monitoring_whitelist` | `gitlab_rails['monitoring_whitelist']` |

*   SMTP:

    | Role Variable                            | Omnibus GitLab setting                      |
    | ---------------------------------------- | ------------------------------------------- |
    | `gitlab_rails_smtp_enable`               | `gitlab_rails['smtp_enable']`               |
    | `gitlab_rails_smtp_address`              | `gitlab_rails['smtp_address']`              |
    | `gitlab_rails_smtp_port`                 | `gitlab_rails['smtp_port']`                 |
    | `gitlab_rails_smtp_user_name`            | `gitlab_rails['smtp_user_name']`            |
    | `gitlab_rails_smtp_password`             | `gitlab_rails['smtp_password']`             |
    | `gitlab_rails_smtp_domain`               | `gitlab_rails['smtp_domain']`               |
    | `gitlab_rails_smtp_authentication`       | `gitlab_rails['smtp_authentication']`       |
    | `gitlab_rails_smtp_enable_starttls_auto` | `gitlab_rails['smtp_enable_starttls_auto']` |
    | `gitlab_rails_smtp_openssl_verify_mode`  | `gitlab_rails['smtp_openssl_verify_mode']`  |
    | `gitlab_rails_smtp_tls`                  | `gitlab_rails['smtp_tls']`                  |
    | `gitlab_rails_smtp_ssl`                  | `gitlab_rails['smtp_ssl']`                  |
    | `gitlab_rails_smtp_force_ssl`            | `gitlab_rails['smtp_force_ssl']`            |
    | `gitlab_rails_gitlab_email_enabled`      | `gitlab_rails['gitlab_email_enabled']`      |
    | `gitlab_rails_gitlab_email_from`         | `gitlab_rails['gitlab_email_from']`         |
    | `gitlab_rails_gitlab_email_display_name` | `gitlab_rails['gitlab_email_display_name']` |
    | `gitlab_rails_gitlab_email_reply_to`     | `gitlab_rails['gitlab_email_reply_to']`     |

*   NGINX:

    | Role Variable               | Omnibus GitLab setting  |
    | --------------------------- | ----------------------- |
    | `gitlab_nginix_listen_port` | `nginix['listen_port']` |

*   Unicorn

    | Role Variable                     | Omnibus GitLab setting        |
    | --------------------------------- | ----------------------------- |
    | `gitlab_unicorn_worker_processes` | `unicorn['worker_processes']` |

*   Container Registry:

    | Role Variable                  | Omnibus GitLab setting  |
    | ------------------------------ | ----------------------- |
    | `gitlab_registry_external_url` | `registry_external_url` |

    Port number is a required part of registry URL. Choose a port different than
    5000.

Dependencies
------------

The role depends on [yabusygin.docker][Docker Role] role.

It is recommended to enable [userns-remap feature][User Namespace]:

```yaml
docker_userns_remap_enable: yes
```

[Docker Role]: https://galaxy.ansible.com/yabusygin/docker
[User Namespace]: https://docs.docker.com/engine/security/userns-remap/

Example Playbook
----------------

```yaml
---
- hosts: production
  roles:
    - role: yabusygin.gitlab
  vars:
    docker_userns_remap_enable: yes
  
    gitlab_image: gitlab/gitlab-ce:12.7.6-ce.0
  
    gitlab_external_url: http://gitlab.test:8000
    gitlab_nginix_listen_port: 80
    gitlab_rails_gitlab_shell_ssh_port: 2222

    gitlab_rails_monitoring_whitelist:
      - 127.0.0.0/8
      - 10.0.1.0/24

    gitlab_rails_smtp_enable: "true"
    gitlab_rails_smtp_address: smtp.example.com
    gitlab_rails_smtp_port: 465
    gitlab_rails_smtp_user_name: gitlab
    gitlab_rails_smtp_password: 'Pa$$w0rD'
    gitlab_rails_smtp_domain: example.com
    gitlab_rails_smtp_authentication: login
    gitlab_rails_smtp_tls: "true"
    gitlab_rails_smtp_enable_starttls_auto: "true"
    gitlab_rails_smtp_openssl_verify_mode: peer

    gitlab_rails_gitlab_email_enabled: "true"
    gitlab_rails_gitlab_email_from: gitlab@example.com
    gitlab_rails_gitlab_email_display_name: GitLab
    gitlab_rails_gitlab_email_reply_to: noreply@example.com

    gitlab_unicorn_worker_processes: 3
```

License
-------

MIT

Author Information
------------------

Alexey Busygin \<busygin.contact@yandex.ru\>
