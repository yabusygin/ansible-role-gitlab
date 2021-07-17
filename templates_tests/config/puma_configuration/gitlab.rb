# URL
external_url 'http://gitlab.test'
registry_external_url 'http://gitlab.test:5050'

# Application server
puma['worker_processes'] = 3
puma['min_threads'] = 1
puma['max_threads'] = 4

# Monitoring

# Outgoing emails
gitlab_rails['gitlab_email_enabled'] = false
