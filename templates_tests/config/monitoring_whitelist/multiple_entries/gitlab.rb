external_url 'http://gitlab.test'
registry_external_url 'http://gitlab.test:5050'

gitlab_rails['monitoring_whitelist'] = ['127.0.0.0/8', '192.168.0.10']

gitlab_rails['gitlab_email_enabled'] = false
