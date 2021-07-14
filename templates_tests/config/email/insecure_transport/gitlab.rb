external_url 'http://gitlab.test'
registry_external_url 'http://gitlab.test:5050'

gitlab_rails['gitlab_email_enabled'] = true
gitlab_rails['gitlab_email_from'] = 'gitlab@test'
gitlab_rails['gitlab_email_display_name'] = 'GitLab'
gitlab_rails['gitlab_email_reply_to'] = 'noreply@test'
gitlab_rails['smtp_enable'] = true
gitlab_rails['smtp_address'] = 'smtp.test'
gitlab_rails['smtp_port'] = 587
gitlab_rails['smtp_tls'] = false
gitlab_rails['smtp_enable_starttls_auto'] = false
gitlab_rails['smtp_authentication'] = 'login'
gitlab_rails['smtp_user_name'] = 'gitlab'
gitlab_rails['smtp_password'] = 'Pa$$w0rD'
