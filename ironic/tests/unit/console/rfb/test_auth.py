# Copyright (c) 2016 Red Hat, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from unittest import mock

from oslo_config import cfg

from ironic.common import exception
from ironic.console.rfb import auth
from ironic.console.rfb import authnone
from ironic.console.rfb import auths
from ironic.tests import base

CONF = cfg.CONF


class RFBAuthSchemeListTestCase(base.TestCase):

    def setUp(self):
        super(RFBAuthSchemeListTestCase, self).setUp()

    def test_load_ok(self):
        schemelist = auths.RFBAuthSchemeList()

        security_types = sorted(schemelist.schemes.keys())
        self.assertEqual([auth.AuthType.NONE],
                         security_types)

    def test_load_unknown(self):
        """Ensure invalid auth schemes are not supported.

        We're really testing oslo_policy functionality, but this case is
        esoteric enough to warrant this.
        """
        self.assertRaises(
            ValueError, CONF.set_override, 'novnc_auth_schemes',
            ['none', 'wibble'], group='vnc')

    def test_find_scheme_ok(self):
        schemelist = auths.RFBAuthSchemeList()

        scheme = schemelist.find_scheme(
            [auth.AuthType.TIGHT,
             auth.AuthType.NONE])

        self.assertIsInstance(scheme, authnone.RFBAuthSchemeNone)

    def test_find_scheme_fail(self):
        schemelist = auths.RFBAuthSchemeList()

        self.assertRaises(exception.RFBAuthNoAvailableScheme,
                          schemelist.find_scheme,
                          [auth.AuthType.TIGHT])

    def test_find_scheme_priority(self):
        schemelist = auths.RFBAuthSchemeList()

        tight = mock.MagicMock(spec=auth.RFBAuthScheme)
        schemelist.schemes[auth.AuthType.TIGHT] = tight

        scheme = schemelist.find_scheme(
            [auth.AuthType.TIGHT,
             auth.AuthType.NONE])

        self.assertEqual(tight, scheme)
