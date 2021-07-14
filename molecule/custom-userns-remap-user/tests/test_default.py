import json
import os
import time

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('instance')


def test_health(host):
    args = (
        "http",
        "--ignore-stdin",
        "--check-status",
        "--body",
        "localhost/-/readiness?all=1",
    )
    retries = 120
    while retries > 0:
        cmd = host.run(
            command=" ".join(args),
        )
        if cmd.rc == 0:
            break
        retries -= 1
        time.sleep(1)
    assert retries > 0

    response = json.loads(s=cmd.stdout)
    assert response["status"] == "ok"
    assert response["cache_check"][0]["status"] == "ok"
    assert response["db_check"][0]["status"] == "ok"
    assert response["gitaly_check"][0]["status"] == "ok"
    assert response["master_check"][0]["status"] == "ok"
    assert response["queues_check"][0]["status"] == "ok"
    assert response["redis_check"][0]["status"] == "ok"
    assert response["shared_state_check"][0]["status"] == "ok"


def test_config_permissions(host):
    subuid = int(
        _get_subuid_entry(host=host, path="/etc/subuid", name="testuser")[1]
    )
    subgid = int(
        _get_subuid_entry(host=host, path="/etc/subgid", name="testuser")[1]
    )
    assert host.file("/etc/docker-gitlab/gitlab.rb").uid == subuid
    assert host.file("/etc/docker-gitlab/gitlab.rb").gid == subgid


def test_cert_permissions(host):
    subuid = int(
        _get_subuid_entry(host=host, path="/etc/subuid", name="testuser")[1]
    )
    subgid = int(
        _get_subuid_entry(host=host, path="/etc/subgid", name="testuser")[1]
    )
    assert host.file("/etc/docker-gitlab/smtp-ca.crt").uid == subuid
    assert host.file("/etc/docker-gitlab/smtp-ca.crt").gid == subgid


def _get_subuid_entry(host, path, name):
    content = host.file(path).content_string
    entries = [
        tuple(line.split(":"))
        for line in content.splitlines()
    ]
    matches = [
        entry
        for entry in entries
        if entry[0] == name
    ]
    if matches:
        return matches[0]
    return None


def test_registry_health(host):
    args = (
        "http",
        "--ignore-stdin",
        "--check-status",
        "--body",
        "localhost:5050/v2/",
    )
    retries = 120
    while retries > 0:
        cmd = host.run(
            command=" ".join(args),
        )
        if cmd.rc == 0 or cmd.rc == 4:
            break
        retries -= 1
        time.sleep(1)
    assert retries > 0

    response = json.loads(s=cmd.stdout)
    assert "errors" in response
    assert len(response["errors"]) == 1
    assert response["errors"][0]["code"] == "UNAUTHORIZED"
