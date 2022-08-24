#!/bin/sh

set -o errexit
set -o nounset

exit_handler() {
    if [ $? -ne 0 ]; then
        echo "Failure" >&2
    fi
}

trap exit_handler EXIT

echo "Running ansible-lint..."
ANSIBLE_COLLECTIONS_PATH="${MOLECULE_EPHEMERAL_DIRECTORY}/collections" ansible-lint \
    "${MOLECULE_PROJECT_DIRECTORY}" \
    "${MOLECULE_SCENARIO_DIRECTORY}"

testinfra_tests_directory="${MOLECULE_SCENARIO_DIRECTORY}/tests"
if [ -d "${testinfra_tests_directory}" ]; then
    testinfra_tests=$(find "${testinfra_tests_directory}" -name 'test_*.py')

    echo "Running mypy..."
    mypy ${testinfra_tests}

    echo "Running pylint..."
    pylint ${testinfra_tests}

    echo "Running black..."
    black --check ${testinfra_tests}
fi

echo "Success"
