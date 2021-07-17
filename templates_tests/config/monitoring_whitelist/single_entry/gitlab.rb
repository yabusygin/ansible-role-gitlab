# URL
external_url 'http://gitlab.test'
registry_external_url 'http://gitlab.test:5050'

# Application server

# Monitoring
gitlab_rails['monitoring_whitelist'] = ['127.0.0.0/8']

# Outgoing emails
gitlab_rails['gitlab_email_enabled'] = false
