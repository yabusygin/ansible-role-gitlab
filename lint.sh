#!/bin/sh

set -o errexit
set -o nounset

exit_handler() {
    if [ $? -ne 0 ]; then
        echo "Failure" >&2
    fi
}

trap exit_handler EXIT

testinfra_tests=$(find "${MOLECULE_SCENARIO_DIRECTORY}" -name 'test_*.py')

echo "Running ansible-lint..."
ANSIBLE_COLLECTIONS_PATH="${MOLECULE_EPHEMERAL_DIRECTORY}/collections" ansible-lint \
    "${MOLECULE_PROJECT_DIRECTORY}" \
    "${MOLECULE_SCENARIO_DIRECTORY}"

if [ ! -z "${testinfra_tests}" ]; then
    echo "Running mypy..."
    for file in ${testinfra_tests}; do
        mypy ${file}
    done

    echo "Running pylint..."
    pylint ${testinfra_tests}

    echo "Running black..."
    black --check ${testinfra_tests}
fi

echo "Success"
