#!/bin/sh

set -o errexit

exit_handler() {
    if [ $? -ne 0 ]; then
        echo "Failure" >&2
    fi
}

trap exit_handler EXIT

testinfra_tests=$(find molecule/ -name 'test_*.py')

echo "Running ansible-lint..."
ansible-lint

echo "Running mypy..."
for file in ${testinfra_tests}; do
    mypy ${file}
done

echo "Running flake8..."
flake8 molecule/

echo "Success"
