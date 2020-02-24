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
