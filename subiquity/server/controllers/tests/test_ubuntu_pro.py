# Copyright 2021 Canonical, Ltd.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import unittest

import jsonschema
from jsonschema.validators import validator_for

from subiquity.server.controllers.ubuntu_pro import UbuntuProController
from subiquity.server.dryrun import DRConfig
from subiquitycore.tests.mocks import make_app


class TestUbuntuProController(unittest.TestCase):
    def setUp(self):
        app = make_app()
        app.dr_cfg = DRConfig()
        self.controller = UbuntuProController(app)

    def test_serialize(self):
        self.controller.model.token = "1a2b3C"
        self.assertEqual(self.controller.serialize(), "1a2b3C")

    def test_deserialize(self):
        self.controller.deserialize("1A2B3C4D")
        self.assertEqual(self.controller.model.token, "1A2B3C4D")

    def test_valid_schema(self):
        """Test that the expected autoinstall JSON schema is valid"""

        JsonValidator: jsonschema.protocols.Validator = validator_for(
            UbuntuProController.autoinstall_schema
        )

        JsonValidator.check_schema(UbuntuProController.autoinstall_schema)
