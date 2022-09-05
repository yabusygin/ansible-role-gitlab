Ansible Role: gitlab
====================

![Test workflow status](https://github.com/yabusygin/ansible-role-gitlab/workflows/test/badge.svg)
![Release workflow status](https://github.com/yabusygin/ansible-role-docker/workflows/release/badge.svg)

An Ansible role for setting up [GitLab][GitLab] version 13.0 or newer.

Requirements
------------

The role uses [community.docker.docker_compose][ComposeModule] module. Therefore,
[community.docker][DockerCollection] collection is required on a control node.

The following requirements are needed on a managed node to execute this role:

* [Docker Engine](https://docs.docker.com/engine/install/)
* [Docker Compose](https://docs.docker.com/compose/install/)
* [community.docker.docker_compose][ComposeModule] module requirements

It's recommended to use [yabusygin.docker][DockerRole] role for installing all
the requirements on the managed node.

Role Variables
--------------

### Docker Configuration ###

* `gitlab_image` -- [Docker container image][GitLabImages] to use. Default
  value: `gitlab/gitlab-ce:latest`.
* `gitlab_restart_policy` -- Docker container [restart policy][RestartPolicy].
  Values: `always`, `on-failure`, `unless-stopped`. Docker doesn’t restart a
  container under any circumstance by default.

### URL ###

* `gitlab_hostname` -- domain name of GitLab host. Default value: `gitlab.test`.
* `gitlab_web_port` -- web UI port number. Default value: `80`.
* `gitlab_registry_port` -- container registry port number. Default value:
  `5050`.
* `gitlab_ssh_port` -- Git shell SSH port number. Default value: `22`.

### HTTPS ###

* `gitlab_https_enable` -- enable HTTPS. Default: `no`.
* `gitlab_letsencrypt_enable` -- enable automated HTTPS with Let’s Encrypt.
  Default: `no`.
* `gitlab_https_key` -- path to private key on the control host.
* `gitlab_https_cert` -- path to certificate chainon the control host.

### Outgoing Emails ###

* `gitlab_email_enable` -- enable outgoing emails. Values: `yes`, `no`. Default
  value: `no`.
* `gitlab_email_from_mailbox` -- mailbox value of "From" header in an outgoing
  email.
* `gitlab_email_from_display_name` -- display name value of "From" header in an
  outgoing email.
* `gitlab_email_reply_to_mailbox` -- mailbox value of "Reply-To" header in an
  outgoing email.
* `gitlab_email_smtp_server_host` -- SMTP server name.
* `gitlab_email_smtp_server_port` -- SMTP server port.
* `gitlab_email_smtp_transport_security` -- transport layer security mechanism.
  Values: `tls` (SMTPS), `starttls`.
* `gitlab_email_smtp_verify_server_cert` -- verify SMTP server certificate, when
  `tls` or `starttls` transport layer security mechanism is selected. Default
  value: `yes`.
* `gitlab_email_smtp_ca_cert` -- local path to CA certificate used to verify
  SMTP server certificate.
* `gitlab_email_smtp_user_auth_method` -- SMTP user authentication method.
  Values: `plain`, `login`, `cram_md5`.
* `gitlab_email_smtp_user_name` -- SMTP user name.
* `gitlab_email_smtp_user_password` -- SMTP user passphrase.

### Application server (Puma) ###

Variable reference:

* `gitlab_workers` -- number of [Puma][Puma] workers.
* `gitlab_min_threads` -- minimum number of Puma threads.
* `gitlab_max_threads` -- maximum number of Puma threads.

### Monitoring ###

Variable reference:

*   `gitlab_monitoring_whitelist` -- a list of addresses/subnets of monitoring
    endpoints that are allowed to perform healthchecks.

### Backup ###

See [Gitlab documentation][Backup] for details.

#### Automated Backups ####

* `gitlab_backup_cron_enable` -- enable cron job that performs periodic backups.
  Default value: `no`.
* `gitlab_backup_cron_minute` -- a "minute" field of cron command line.
  Mandatory variable. See [`crontab(5)`][Crontab5].
* `gitlab_backup_cron_hour` -- a "hour" field of cron command line. Mandatory
  variable. See [`crontab(5)`][Crontab5].
* `gitlab_backup_cron_day_of_month` -- a "day of month" field of cron command
  line. Default value: `*`.
* `gitlab_backup_cron_month` -- a "month" field of cron command line. Default
  value: `*`.
* `gitlab_backup_cron_day_of_week` -- a "day of week" field of cron command
  line. Default value: `*`.
* `gitlab_backup_cron_docker_cmd` -- command that backup cron job uses to invoke
  Docker Engine. Default: `docker`.
* `gitlab_backup_cron_docker_compose_cmd` -- command that backup cron job uses
  to invoke Docker Compose. Default: `docker compose`.

#### Upload Backups to S3 Compatible Storage ####

* `gitlab_backup_upload_enable` -- enable uploading backups to remote storage.
  Default value: `no`.
* `gitlab_backup_upload_type` -- remote storage type. Supported values: `s3`.
  Default value: `s3`.
* `gitlab_backup_upload_s3_region` -- AWS [region][AWSRegion].
* `gitlab_backup_upload_s3_bucket` -- S3 [bucket][AWSS3Bucket] to store backup
  objects. Mandatory variable.
* `gitlab_backup_upload_s3_access_key_id` -- [access key ID][AWSAccessKeyID].
  Mandatory variable.
* `gitlab_backup_upload_s3_secret_access_key` --
  [secret access key][AWSsecretAccessKey]. Mandatory variable.
* `gitlab_backup_upload_s3_endpoint` -- S3 compatible storage HTTP API endpoint.
* `gitlab_backup_upload_s3_path_style_enable` -- use path-style method for
  accessing a bucket (see [Methods for accessing a bucket][AWSS3AccessBucket]).

### Limit Lifetime of Local Backup Files ###

* `gitlab_backup_keep_time` -- sets `gitlab_rails['backup_keep_time']` value.

Dependencies
------------

If [yabusygin.docker][DockerRole] role is used for installing Docker and other
requirements, then it is recommended to enable
[user namespace remapping][UsernsRemap] (see the example below).

[UsernsRemap]: https://docs.docker.com/engine/security/userns-remap/

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

Customized with [yabusygin.docker][DockerRole] role:

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
        gitlab_image: gitlab/gitlab-ee:latest
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

[GitLab]: https://docs.gitlab.com/ee/index.html
[ComposeModule]: https://docs.ansible.com/ansible/latest/collections/community/docker/docker_compose_module.html
[DockerCollection]: https://docs.ansible.com/ansible/latest/collections/community/docker/index.html
[DockerRole]: https://galaxy.ansible.com/yabusygin/docker
[GitLabImages]: https://hub.docker.com/u/gitlab
[RestartPolicy]: https://docs.docker.com/compose/compose-file/#restart
[Puma]: https://docs.gitlab.com/ee/administration/operations/puma.html
[Backup]: https://docs.gitlab.com/ee/raketasks/backup_restore.html
[Crontab5]: https://man7.org/linux/man-pages/man5/crontab.5.html
[AWSRegion]: https://docs.aws.amazon.com/general/latest/gr/glos-chap.html#region
[AWSAccessKeyID]: https://docs.aws.amazon.com/general/latest/gr/glos-chap.html#accesskeyID
[AWSS3Bucket]: https://docs.aws.amazon.com/general/latest/gr/glos-chap.html#bucket
[AWSsecretAccessKey]: https://docs.aws.amazon.com/general/latest/gr/glos-chap.html#SecretAccessKey
[AWSS3AccessBucket]: https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-bucket-intro.html
