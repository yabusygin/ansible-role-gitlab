import pathlib

import jinja2
import ansible.plugins.filter.core
import ansible.template
import yaml


def resolve_path(base_path, relative_path):
    if not base_path.is_dir():
        base_path = base_path.parent
    return base_path.joinpath(relative_path).resolve()


def render_role_template(role_path, template_filename, variables=None):
    template_variables = {}
    default_variables_path = pathlib.Path(role_path, "defaults", "main.yml")
    if default_variables_path.exists():
        template_variables.update(
            yaml_parse(data=default_variables_path.read_text()),
        )
    if variables:
        template_variables.update(variables)
    env = _make_template_env(
        search_path=pathlib.Path(role_path, "templates"),
    )
    template = env.get_template(name=template_filename)
    return template.render(**template_variables)


def _make_template_env(search_path):
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(
            searchpath=str(search_path),
        ),
        undefined=ansible.template.AnsibleUndefined,
        keep_trailing_newline=True,
        lstrip_blocks=True,
        trim_blocks=True,
    )
    env.filters.update(ansible.plugins.filter.core.FilterModule().filters())
    return env


def yaml_parse(data):
    return yaml.load(
        stream=data,
        Loader=yaml.Loader
    )
