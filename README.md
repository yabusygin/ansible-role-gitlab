Ansible Role: gitlab
====================

![Test workflow status](https://github.com/yabusygin/ansible-role-gitlab/workflows/test/badge.svg)
![Release workflow status](https://github.com/yabusygin/ansible-role-docker/workflows/release/badge.svg)

An Ansible role for setting up [GitLab][GitLab].

[GitLab]: https://docs.gitlab.com/ce/README.html

Requirements
------------

The role uses [community.docker.docker_compose][ComposeModule] module. Therefore,
[community.docker][DockerCollection] collection is required on a control node.

[ComposeModule]: https://docs.ansible.com/ansible/latest/collections/community/docker/docker_compose_module.html
[DockerCollection]: https://docs.ansible.com/ansible/latest/collections/community/docker/index.html

The following requirements are needed on a managed node to execute this role:

* [Docker Engine](https://docs.docker.com/engine/install/)
* [Docker Compose](https://docs.docker.com/compose/install/)
* [community.docker.docker_compose][ComposeModule] module requirements

It's recommended to use [yabusygin.docker][DockerRole] role for installing all
the requirements on the managed node.

[DockerRole]: https://galaxy.ansible.com/yabusygin/docker

Role Variables
--------------

### Docker Configuration ###

Variable reference:

*   `gitlab_image` -- [Docker container image][GitLabImages] to use. Default
    value: `gitlab/gitlab-ce:latest`.

    [GitLabImages]: https://hub.docker.com/u/gitlab

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

### HTTPS ###

Variable reference:

*   `gitlab_https_enable` -- enable HTTPS. Default: `no`.
*   `gitlab_letsencrypt_enable` -- enable automated HTTPS with Let’s Encrypt.
    Default: `no`.
*   `gitlab_https_key` -- path to private key on the control host.
*   `gitlab_https_cert` -- path to certificate chainon the control host.

#### Manual HTTPS Configuration ####

```yaml
gitlab_https_enable: yes
gitlab_https_key: https/gitlab.key.pem
gitlab_https_cert: https/gitlab.crt.pem
```

The default configuration will be replaced with the following:

```ruby
external_url 'https://gitlab.test'
registry_external_url 'https://gitlab.test:5050'
letsencrypt['enable'] = false
```

Private key `https/gitlab.key.pem` will be mounted to
`/etc/gitlab/ssl/gitlab.test.key` in container. Certificate
`https/gitlab.crt.pem` will be mounted to `/etc/gitlab/ssl/gitlab.test.crt` in
container.

#### Let's Encrypt HTTPS Configuration ####

```yaml
gitlab_https_enable: yes
gitlab_letsencrypt_enable: yes
```

The default configuration will be replaced with the following:

```ruby
external_url 'https://gitlab.test'
registry_external_url 'https://gitlab.test:5050'
letsencrypt['enable'] = true
```

### Outgoing Emails ###

Variable reference:

*   `gitlab_email_enable` -- enable outgoing emails. Values: `yes`, `no`.
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
gitlab_email_enable: yes
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

#### SMTP Server Certificate Issued by Private CA ####

```yaml
gitlab_email_smtp_ca_cert: /path/to/private-ca.pem
```

The following configuration will be added:

```ruby
gitlab_rails['smtp_ca_file'] = '/etc/ssl/certs/smtp.crt.pem'
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

### Backup ###

See [Gitlab documentation][Backup] for details.

[Backup]: https://docs.gitlab.com/ee/raketasks/backup_restore.html

#### Automated Backups ####

Variable reference:

*   `gitlab_backup_cron_enable` -- enable cron job that performs periodic
    backups. Default value: `no`.

*   `gitlab_backup_cron_minute` -- a "minute" field of cron command line.
    Mandatory variable. See [`crontab(5)`][Crontab5].

*   `gitlab_backup_cron_hour` -- a "hour" field of cron command line. Mandatory
    variable. See [`crontab(5)`][Crontab5].

*   `gitlab_backup_cron_day_of_month` -- a "day of month" field of cron command
    line. Default value: `*`.

*   `gitlab_backup_cron_month` -- a "month" field of cron command line. Default
    value: `*`.

*   `gitlab_backup_cron_day_of_week` -- a "day of week" field of cron command
    line. Default value: `*`.

*   `gitlab_backup_cron_docker_cmd` -- command that backup cron job uses to
    invoke Docker Engine. Default: `docker`.

*   `gitlab_backup_cron_docker_compose_cmd` -- command that backup cron job uses
    to invoke Docker Compose. Default: `docker compose`.

[Crontab5]: https://man7.org/linux/man-pages/man5/crontab.5.html

#### Uploading Backups to Remote Storage ####

Only S3 compatible remote storage is currently supported.

Variable reference:

*   `gitlab_backup_upload_enable` -- enable uploading backups to remote storage.
    Default value: `no`.

*   `gitlab_backup_upload_type` -- remote storage type. Supported values: `s3`.
    Default value: `s3`.

*   `gitlab_backup_upload_s3_region` -- AWS [region][AWSRegion].

    [AWSRegion]: https://docs.aws.amazon.com/general/latest/gr/glos-chap.html#region

*   `gitlab_backup_upload_s3_bucket` -- S3 [bucket][AWSS3Bucket] to store backup
    objects. Mandatory variable.

    [AWSS3Bucket]: https://docs.aws.amazon.com/general/latest/gr/glos-chap.html#bucket

*   `gitlab_backup_upload_s3_access_key_id` -- [access key ID][AWSAccessKeyID].
    Mandatory variable.

    [AWSAccessKeyID]: https://docs.aws.amazon.com/general/latest/gr/glos-chap.html#accesskeyID

*   `gitlab_backup_upload_s3_secret_access_key` --
    [secret access key][AWSsecretAccessKey]. Mandatory variable.

    [AWSsecretAccessKey]: https://docs.aws.amazon.com/general/latest/gr/glos-chap.html#SecretAccessKey

*   `gitlab_backup_upload_s3_endpoint` -- S3 compatible storage HTTP API endpoint.

*   `gitlab_backup_upload_s3_path_style_enable` -- use path-style method for
    accessing a bucket (see
    [Methods for accessing a bucket][AWSS3AccessBucket]). Sets
    `gitlab_rails['backup_upload_connection']['path_style']` value.

    [AWSS3AccessBucket]: https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-bucket-intro.html

Example of uploading backups to Digital Ocean Spaces:

```yaml
gitlab_backup_upload_enable: yes
gitlab_backup_upload_type: s3
gitlab_backup_upload_s3_endpoint: https://ams3.digitaloceanspaces.com
gitlab_backup_upload_s3_region: ams3
gitlab_backup_upload_s3_bucket: my.s3.bucket
gitlab_backup_upload_s3_access_key_id: AKIAKIAKI
gitlab_backup_upload_s3_secret_access_key: secret123
```

The following configuration will be added:

```ruby
gitlab_rails['backup_upload_connection'] = {
  'provider' => 'AWS',
  'endpoint' => 'https://ams3.digitaloceanspaces.com',
  'region' => 'ams3',
  'aws_access_key_id' => 'AKIAKIAKI',
  'aws_secret_access_key' => 'secret123'
}
gitlab_rails['backup_upload_remote_directory'] = 'my.s3.bucket'
```

#### Limit Lifetime of Local Backup Files ####

Variable reference:

*   `gitlab_backup_keep_time` -- sets `gitlab_rails['backup_keep_time']` value.

Dependencies
------------

If [yabusygin.docker][DockerRole] role is used for installing Docker and other
requirements, then it is recommended to enable
[user namespace remapping feature][UsernsRemap]:

```yaml
docker_config:
  userns-remap: default
  log-driver: json-file
  log-opts:
    max-size: 10m
    max-file: "3"
gitlab_userns_remap_enable: yes
```

Example Playbook
----------------

Default setup (Docker and other requirements are already installed):

```yaml
- name: set up GitLab
  hosts: gitlab
  tasks:
    - name: set up GitLab
      ansible.builtin.import_role:
        name: yabusygin.gitlab
```

Default setup with [yabusygin.docker][DockerRole] role:

```yaml
- name: set up Docker and GitLab
  hosts: gitlab
  tasks:
    - name: set up Docker
      ansible.builtin.import_role:
        name: yabusygin.docker

    - name: set up GitLab
      ansible.builtin.import_role:
        name: yabusygin.gitlab
```

Customized setup:

```yaml
---
- name: set up customized Docker and GitLab
  hosts: gitlab
  tasks:
    - name: set up Docker
      ansible.builtin.import_role:
        name: yabusygin.docker
      vars:
        userns-remap: default
        log-driver: json-file
        log-opts:
          max-size: 10m
          max-file: "3"

    - name: set up GitLab
      ansible.builtin.import_role:
        name: yabusygin.gitlab
      vars:
        gitlab_userns_remap_enable: yes

        gitlab_image: gitlab/gitlab-ce:13.12.8-ce.0
        gitlab_restart_policy: always

        gitlab_hostname: gitlab.example.com
        gitlab_web_port: 3443
        gitlab_registry_port: 5001
        gitlab_ssh_port: 2222

        gitlab_https_enable: yes
        gitlab_https_key: https/gitlab.key.pem
        gitlab_https_cert: https/gitlab.crt.pem

        gitlab_workers: 2
        gitlab_min_threads: 4
        gitlab_max_threads: 4

        gitlab_monitoring_whitelist:
          - 192.168.10.39
          - 10.0.1.0/24

        gitlab_email_enable: yes
        gitlab_email_from_mailbox: gitlab@example.com
        gitlab_email_from_display_name: GitLab
        gitlab_email_reply_to_mailbox: noreply@example.com
        gitlab_email_smtp_server_host: smtp.example.com
        gitlab_email_smtp_server_port: 587
        gitlab_email_smtp_transport_security: starttls
        gitlab_email_smtp_user_auth_method: login
        gitlab_email_smtp_user_name: gitlab
        gitlab_email_smtp_user_password: Pa$$w0rD

        gitlab_backup_cron_enable: yes
        gitlab_backup_cron_minute: 0
        gitlab_backup_cron_hour: 2
        gitlab_backup_cron_docker_cmd: /usr/bin/docker
        gitlab_backup_cron_docker_compose_cmd: /usr/local/bin/docker-compose

        gitlab_backup_upload_enable: yes
        gitlab_backup_upload_type: s3
        gitlab_backup_upload_s3_endpoint: https://ams3.digitaloceanspaces.com
        gitlab_backup_upload_s3_region: ams3
        gitlab_backup_upload_s3_bucket: my.s3.bucket
        gitlab_backup_upload_s3_access_key_id: AKIAKIAKI
        gitlab_backup_upload_s3_secret_access_key: secret123

        gitlab_backup_keep_time: 604800
```

License
-------

MIT

Author Information
------------------

Alexey Busygin \<yaabusygin@gmail.com\>
