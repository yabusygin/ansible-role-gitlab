# URL
external_url 'http://gitlab.test'
registry_external_url 'http://gitlab.test:5050'

# HTTPS

# Application server

# Monitoring

# Outgoing emails
gitlab_rails['gitlab_email_enabled'] = false

# Backup
gitlab_rails['backup_keep_time'] = 604800