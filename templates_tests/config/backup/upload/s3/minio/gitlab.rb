# URL
external_url 'http://gitlab.test'
registry_external_url 'http://gitlab.test:5050'

# HTTPS

# Application server

# Monitoring

# Outgoing emails
gitlab_rails['gitlab_email_enabled'] = false

# Backup
gitlab_rails['backup_upload_connection'] = {
  'provider' => 'AWS',
  'endpoint' => 'https://minio.test',
  'path_style' => true,
  'aws_access_key_id' => 'AKIAKIAKI',
  'aws_secret_access_key' => 'secret123'
}
gitlab_rails['backup_upload_remote_directory'] = 'my.s3.bucket'
