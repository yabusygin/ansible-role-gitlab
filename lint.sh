#!/bin/sh

set -o errexit

exit_handler() {
    if [ $? -ne 0 ]; then
        echo "Failure" >&2
    fi
}

trap exit_handler EXIT

echo "Running yamllint..."
yamllint .

echo "Running ansible-lint..."
ansible-lint

echo "Running flake8..."
flake8 molecule/

echo "Success"
