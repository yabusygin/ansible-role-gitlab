FROM gitlab/gitlab-ce:latest
COPY https.key https.crt /opt/gitlab/tls/
RUN chmod 'u=rw,g=,o=' /opt/gitlab/tls/https.key
