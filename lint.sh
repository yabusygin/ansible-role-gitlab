#!/bin/sh

set -o errexit

exit_status_hook() {
    if [ $? -ne 0 ]; then
        echo "Failure"
    fi
}

trap exit_status_hook EXIT

echo "Running yamllint..."
yamllint .

echo "Running ansible-lint..."
ansible-lint

echo "Running flake8..."
flake8 molecule/

echo "Success"
