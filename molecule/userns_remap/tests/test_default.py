import json
import os
from pathlib import Path
import time
from typing import Optional

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('instance')


def test_config_permissions(host) -> None:
    entry = _get_entry(host=host, path=Path("/etc/subuid"), name="dockremap")
    assert entry is not None
    subuid = entry[1]

    entry = _get_entry(host=host, path=Path("/etc/subgid"), name="dockremap")
    assert entry is not None
    subgid = entry[1]

    assert host.file("/etc/docker-gitlab/gitlab.rb").uid == subuid
    assert host.file("/etc/docker-gitlab/gitlab.rb").gid == subgid


def test_health(host) -> None:
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


def test_registry_health(host) -> None:
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


def _get_entry(host, path: Path, name: str) -> Optional[tuple[str, int, int]]:
    content = host.file(str(path)).content_string
    entries = [tuple(line.split(":")) for line in content.splitlines()]
    matches = [entry for entry in entries if entry[0] == name]
    if matches:
        login, first_id, count = matches[0]
        return login, int(first_id), int(count)
    return None
