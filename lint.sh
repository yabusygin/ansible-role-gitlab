#!/bin/sh

set -o errexit
set -o nounset

exit_handler() {
    if [ $? -ne 0 ]; then
        echo "Failure" >&2
    fi
}

trap exit_handler EXIT

testinfra_tests=$(find molecule/ -name 'test_*.py')

echo "Running ansible-lint..."
ansible-lint "${MOLECULE_PROJECT_DIRECTORY}" "${MOLECULE_SCENARIO_DIRECTORY}"

echo "Running mypy..."
for file in ${testinfra_tests}; do
    mypy ${file}
done

echo "Running pylint..."
pylint ${testinfra_tests}

echo "Running black..."
black --check ${testinfra_tests}

echo "Success"
