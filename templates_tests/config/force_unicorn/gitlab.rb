external_url 'http://gitlab.test'
registry_external_url 'http://gitlab.test:5050'

puma['enable'] = false
unicorn['enable'] = true
unicorn['worker_processes'] = 3

gitlab_rails['gitlab_email_enabled'] = false
