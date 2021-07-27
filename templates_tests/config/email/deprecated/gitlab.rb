# URL
external_url 'http://gitlab.test'
registry_external_url 'http://gitlab.test:5050'

# HTTPS

# Application server

# Monitoring

# Outgoing emails
gitlab_rails['gitlab_email_enabled'] = true
gitlab_rails['gitlab_email_from'] = 'gitlab@test'
gitlab_rails['gitlab_email_display_name'] = 'GitLab'
gitlab_rails['gitlab_email_reply_to'] = 'noreply@test'
gitlab_rails['smtp_enable'] = true
gitlab_rails['smtp_address'] = 'smtp.test'
gitlab_rails['smtp_port'] = 465
gitlab_rails['smtp_tls'] = true
gitlab_rails['smtp_enable_starttls_auto'] = false
gitlab_rails['smtp_openssl_verify_mode'] = 'peer'
gitlab_rails['smtp_authentication'] = 'plain'
gitlab_rails['smtp_user_name'] = 'gitlab'
gitlab_rails['smtp_password'] = 'Pa$$w0rD'
