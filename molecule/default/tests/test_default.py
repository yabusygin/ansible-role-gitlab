from json import loads
from os import environ
from time import sleep

from testinfra.utils.ansible_runner import AnsibleRunner

testinfra_hosts = AnsibleRunner(
    environ['MOLECULE_INVENTORY_FILE'],
).get_hosts('instance')


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
        sleep(1)
    assert retries > 0

    response = loads(s=cmd.stdout)
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
        sleep(1)
    assert retries > 0

    response = loads(s=cmd.stdout)
    assert "errors" in response
    assert len(response["errors"]) == 1
    assert response["errors"][0]["code"] == "UNAUTHORIZED"
