external_url 'http://gitlab.test'
registry_external_url 'http://gitlab.test:5050'

unicorn['worker_processes'] = 3

gitlab_rails['gitlab_email_enabled'] = false