Ansible Role: gitlab
====================

![Test workflow status](https://github.com/yabusygin/ansible-role-gitlab/workflows/test/badge.svg)
![Release workflow status](https://github.com/yabusygin/ansible-role-docker/workflows/release/badge.svg)

An Ansible role installing [GitLab CE][GitLab].

[GitLab]: https://docs.gitlab.com/ce/README.html

Requirements
------------

The following requirements are needed on a managed host to execute this role:

* [Docker Engine](https://docs.docker.com/engine/install/)
* [Docker Compose](https://docs.docker.com/compose/install/)
* [docker_compose module requirements](https://docs.ansible.com/ansible/2.9/modules/docker_compose_module.html#requirements)

Its recommended to use [yabusygin.docker][DockerRole] role for installing all
the requiremets.

[DockerRole]: https://galaxy.ansible.com/yabusygin/docker

Role Variables
--------------

### Docker Configuration ###

Variable reference:

*   `gitlab_image` -- [Docker container image][gitlab/gitlab-ce] to use. Default
    value: `gitlab/gitlab-ce:12.10.14-ce.0`.

    [gitlab/gitlab-ce]: https://hub.docker.com/r/gitlab/gitlab-ce

*   `gitlab_restart_policy` -- Docker container
    [restart policy][Restart Policy]. Values: `always`, `on-failure`,
    `unless-stopped`. Docker doesn’t restart a container under any
    circumstance by default.

    [Restart Policy]: https://docs.docker.com/compose/compose-file/compose-file-v2/#restart

### URL ###

Variable reference:

*   `gitlab_hostname` -- domain name of GitLab host. Default value:
    `gitlab.test`.

*   `gitlab_web_port` -- web UI port number. Default value: `80`.

*   `gitlab_registry_port` -- container registry port number. Default value: `5050`.

*   `gitlab_ssh_port` -- Git shell SSH port number. Default value: `22`.

A default Omnibus GitLab onfiguration:

```ruby
external_url 'http://gitlab.test'
registry_external_url 'http://gitlab.test:5050'
```

#### Specify Hostname ####

```yaml
gitlab_hostname: gitlab.example.com
```

The default configuration will be replaced with the following:

```ruby
external_url 'http://gitlab.example.com'
registry_external_url 'http://gitlab.example.com:5050'
```

#### Non Default Ports ####

```yaml
gitlab_web_port: 8000
gitlab_registry_port: 5001
gitlab_ssh_port: 2222
```

The default configuration will be replaced with the following:

```ruby
external_url 'http://gitlab.test:8000'
registry_external_url 'http://gitlab.test:5001'
gitlab_rails['gitlab_shell_ssh_port'] = 2222
```

### Outgoing Emails ###

Variable reference:

*   `gitlab_email_enabled` -- enable outgoing emails. Values: `yes`, `no`.
    Default value: `no`.

*   `gitlab_email_from_mailbox` -- mailbox value of "From" header in an outgoing
    email.

*   `gitlab_email_from_display_name` -- display name value of "From" header in
    an outgoing email.

*   `gitlab_email_reply_to_mailbox` -- mailbox value of "Reply-To" header in an
    outgoing email.

*   `gitlab_email_smtp_server_host` -- SMTP server name.

*   `gitlab_email_smtp_server_port` -- SMTP server port.

*   `gitlab_email_smtp_transport_security` -- transport layer security
    mechanism. Values: `tls` (SMTPS), `starttls`.

*   `gitlab_email_smtp_verify_server_cert` -- verify SMTP server certificate,
    when `tls` or `starttls` transport layer security mechanism is selected.
    Default value: `yes`.

*   `gitlab_email_smtp_ca_cert` -- local path to CA certificate used to verify SMTP
    server certificate.

*   `gitlab_email_smtp_user_auth_method` -- SMTP user authentication method.
    Values: `plain`, `login`, `cram_md5`.

*   `gitlab_email_smtp_user_name` -- SMTP user name.

*   `gitlab_email_smtp_user_password` -- SMTP user passphrase.

A default Omnibus GitLab onfiguration:

```ruby
gitlab_rails['gitlab_email_enabled'] = false
```

### Enable Outgoing Emails ###

To enable outgoing emails:

```yaml
gitlab_email_enabled: yes
```

The default configuration will be replaced with the following:

```ruby
gitlab_rails['gitlab_email_enabled'] = true
gitlab_rails['smtp_enable'] = true
```

#### Email Sender ####

To configure an outgoing email "From" and "Reply-To" headers:

```yaml
gitlab_email_from_mailbox: gitlab@example.com
gitlab_email_from_display_name: GitLab
gitlab_email_reply_to_mailbox: noreply@example.com
```

The following configuration will be added:

```ruby
gitlab_rails['gitlab_email_from'] = 'gitlab@example.com'
gitlab_rails['gitlab_email_display_name'] = 'GitLab'
gitlab_rails['gitlab_email_reply_to'] = 'noreply@example.com'
```

#### SMTP Server ####

```yaml
gitlab_email_smtp_server_host: smtp.example.com
gitlab_email_smtp_server_port: 587
```

The following configuration will be added:

```ruby
gitlab_rails['smtp_address'] = 'smtp.example.com'
gitlab_rails['smtp_port'] = 587
```

#### STARTTLS ####

```yaml
gitlab_email_smtp_transport_security: starttls
```

The following configuration will be added:

```ruby
gitlab_rails['smtp_tls'] = false
gitlab_rails['smtp_enable_starttls_auto'] = true
gitlab_rails['smtp_openssl_verify_mode'] = 'peer'
```

#### SMTPS ####

```yaml
gitlab_email_smtp_transport_security: tls
```

The following configuration will be added:

```ruby
gitlab_rails['smtp_tls'] = true
gitlab_rails['smtp_enable_starttls_auto'] = false
gitlab_rails['smtp_openssl_verify_mode'] = 'peer'
```

#### SMTP Server Certificate Signed by Private CA ####

```yaml
gitlab_email_smtp_ca_cert: /path/to/private-ca.pem
```

The following configuration will be added:

```ruby
gitlab_rails['smtp_ca_file'] = '/etc/gitlab/ssl/smtp-ca.crt'
```

#### Disable SMTP Server Certificate Verification ####

```yaml
gitlab_email_smtp_verify_server_cert: no
```

The following configuration will be added:

```ruby
gitlab_rails['smtp_openssl_verify_mode'] = 'none'
```

#### SMTP without TLS ####

```yaml
gitlab_email_smtp_transport_security: none
```

The following configuration will be added:

```ruby
gitlab_rails['smtp_tls'] = false
gitlab_rails['smtp_enable_starttls_auto'] = false
```

#### SMTP user/client authentication ####

```yaml
gitlab_email_smtp_user_auth_method: plain
gitlab_email_smtp_user_name: gitlab
gitlab_email_smtp_user_password: Pa$$w0rD
```

The following configuration will be added:

```ruby
gitlab_rails['smtp_authentication'] = 'plain'
gitlab_rails['smtp_user_name'] = 'gitlab'
gitlab_rails['smtp_password'] = 'Pa$$w0rD'
```

### Application Server Settings ###

Variable reference:

*   `gitlab_workers` -- number of [Puma][Puma] workers or [Unicorn][Unicorn]
    workers if `gitlab_unicorn_force` is set to `yes`.
*   `gitlab_min_threads` -- minimum number of Puma threads.
*   `gitlab_max_threads` -- maximum number of Puma threads.
*   `gitlab_unicorn_force` -- use Unicorn instead of Puma. Default: `no`.
*   `gitlab_unicorn_workers` -- number of Unicorn worker processes (for GitLab
    versions before 13.0). For Gitlab 13.0 user `gitlab_unicorn_force` and
    `gitlab_workers` instead.

[Puma]: https://docs.gitlab.com/ce/administration/operations/puma.html
[Unicorn]: https://docs.gitlab.com/12.10/omnibus/settings/unicorn.html

#### Puma ####

```yaml
gitlab_workers: 2
gitlab_min_threads: 4
gitlab_max_threads: 4
```

The following configuration will be added:

```ruby
puma['worker_processes'] = 2
puma['min_threads'] = 4
puma['max_threads'] = 4
```

#### Unicorn ####

For GitLab 13.0 and newer:

```yaml
gitlab_unicorn_force: yes
gitlab_workers: 3
```

The following configuration will be added:

```ruby
puma['enable'] = false
unicorn['enable'] = true
unicorn['worker_processes'] = 3
```

For GitLab versions before 13.0:

```yaml
gitlab_unicorn_workers: 3
```

The following configuration will be added:

```ruby
unicorn['worker_processes'] = 3
```

### Monitoring Settings ###

Variable reference:

*   `gitlab_monitoring_whitelist` -- a list of addresses/subnets of monitoring
    endpoints that are allowed to perform healthchecks.

### Docker User Namespace Remapping ###

Variable reference:

*   `gitlab_userns_remap_enable` -- signals that Docker
    [user namespace remapping feature][UsernsRemap] is enabled. Default value:
    `no`.

*   `gitlab_userns_remap_user` -- user used by Docker for running containers
    with enabled user namespace remapping. Default value `dockremap`.

[UsernsRemap]: https://docs.docker.com/engine/security/userns-remap/

Dependencies
------------

If [yabusygin.docker][DockerRole] role is used for installing Docker and other
requirements, then it is recommended to enable
[user namespace remapping feature][UsernsRemap]:

```yaml
docker_userns_remap_enable: yes
gitlab_userns_remap_enable: yes
```

Example Playbook
----------------

```yaml
---
- hosts: production
  tasks:
    - import_role:
        name: yabusygin.gitlab
      vars:
        gitlab_userns_remap_enable: yes
        gitlab_userns_remap_user: nsremap

        gitlab_image: gitlab/gitlab-ce:13.12.8-ce.0
        gitlab_restart_policy: always

        gitlab_hostname: gitlab.example.com
        gitlab_web_port: 8000
        gitlab_registry_port: 5001
        gitlab_ssh_port: 2222

        gitlab_workers: 2
        gitlab_min_threads: 4
        gitlab_max_threads: 4

        gitlab_monitoring_whitelist:
          - 192.168.10.39
          - 10.0.1.0/24

        gitlab_email_enabled: yes
        gitlab_email_from_mailbox: gitlab@example.com
        gitlab_email_from_display_name: GitLab
        gitlab_email_reply_to_mailbox: noreply@example.com
        gitlab_email_smtp_server_host: smtp.example.com
        gitlab_email_smtp_server_port: 587
        gitlab_email_smtp_transport_security: starttls
        gitlab_email_smtp_user_auth_method: login
        gitlab_email_smtp_user_name: gitlab
        gitlab_email_smtp_user_password: Pa$$w0rD
```

With [yabusygin.docker][DockerRole] role:

```yaml
- hosts: production
  tasks:
    - import_role:
        name: yabusygin.docker
      vars:
        docker_userns_remap_enable: yes

    - import_role:
        name: yabusygin.gitlab
      vars:
        gitlab_userns_remap_enable: yes
        gitlab_hostname: gitlab.example.com
```

License
-------

MIT

Author Information
------------------

Alexey Busygin \<yaabusygin@gmail.com\>
