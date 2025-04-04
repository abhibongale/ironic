# Copyright 2014 Rackspace, Inc.
# All Rights Reserved
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from ironic.dhcp import base


class NoneDHCPApi(base.BaseDHCP):
    """No-op DHCP API."""

    def update_port_dhcp_opts(self, port_id, dhcp_options, context=None):
        pass

    def update_dhcp_opts(self, task, options, vifs=None):
        pass

    def get_ip_addresses(self, task):
        return []
