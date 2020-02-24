import unittest
import pathlib
try:
    import importlib.resources as resources
except ImportError:
    import importlib_resources as resources

from ..utils import (
    resolve_path,
    render_role_template,
    yaml_parse,
)


_ROLE_PATH = resolve_path(
    base_path=pathlib.Path(__file__),
    relative_path=pathlib.Path("..", ".."),
)
_TEMPLATE_VARIABLES_FILENAME = "vars.yml"

_TEMPLATE_FILENAME = "gitlab.rb.j2"
_EXPECTED_RESULT_FILENAME = "gitlab.rb"


class RenderFromTemplate(unittest.TestCase):

    def test(self):
        expect = resources.read_text(
            package=__package__,
            resource=_EXPECTED_RESULT_FILENAME,
        )
        variables = None
        if resources.is_resource(
                package=__package__,
                name=_TEMPLATE_VARIABLES_FILENAME):
            variables = yaml_parse(
                data=resources.read_text(
                    package=__package__,
                    resource=_TEMPLATE_VARIABLES_FILENAME,
                ),
            )
        actual = render_role_template(
            role_path=_ROLE_PATH,
            template_filename=_TEMPLATE_FILENAME,
            variables=variables,
        )
        self.assertEqual(expect, actual)
