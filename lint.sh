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
ANSIBLE_ROLES_PATH="${MOLECULE_EPHEMERAL_DIRECTORY}/roles" \
ANSIBLE_COLLECTIONS_PATH="${MOLECULE_EPHEMERAL_DIRECTORY}/collections" \
ansible-lint \
    "${MOLECULE_PROJECT_DIRECTORY}" \
    "${MOLECULE_SCENARIO_DIRECTORY}"

python_src="$(find "${MOLECULE_SCENARIO_DIRECTORY}" -name '*.py')"
if [ ! -z "${python_src}" ]; then
    echo "Running mypy..."
    mypy ${python_src}

    echo "Running pylint..."
    pylint ${python_src}

    echo "Running black..."
    black --check ${python_src}
fi

echo "Success"
