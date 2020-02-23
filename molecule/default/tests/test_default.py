import json
import os

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
    cmd = host.run_expect(
        expected=[0],
        command=" ".join(args),
    )
    response = json.loads(s=cmd.stdout)
    assert response["status"] == "ok"
    assert response["cache_check"][0]["status"] == "ok"
    assert response["db_check"][0]["status"] == "ok"
    assert response["gitaly_check"][0]["status"] == "ok"
    assert response["master_check"][0]["status"] == "ok"
    assert response["queues_check"][0]["status"] == "ok"
    assert response["redis_check"][0]["status"] == "ok"
    assert response["shared_state_check"][0]["status"] == "ok"
