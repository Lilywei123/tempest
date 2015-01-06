# Copyright 2013 OpenStack Foundation
# All Rights Reserved.
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

import re

from tempest_lib import exceptions

from tempest import cli
from tempest import config
from tempest.openstack.common import log as logging
import random
from cherrypy.test.benchmark import NullResponse
from scss.types import Null

CONF = config.CONF

LOG = logging.getLogger(__name__)


class CRUDKeystoneClientTest(cli.ClientTestBase):
    """Basic, read-only tests for Keystone CLI client.

    Checks return values and output of read-only commands.
    These tests do not presume any content, nor do they create
    their own. They only verify the structure of output if present.
    """

    def keystone(self, *args, **kwargs):
        return self.clients.keystone(*args, **kwargs)

    def test_admin_role_list(self):
        LOG.debug("==========================start==========================")
        roles = self.parser.listing(self.keystone('role-list'))
        self.assertTableStruct(roles, ['id', 'name'])

        
    def test_admin_role_create_delete(self):
        role_name = 'rolename_' + str(random.random())
        cmd = 'role-create --name ' + role_name
        roles = self.parser.listing(self.keystone(cmd))
        self.assertTableStruct(roles, ['Property', 'Value'])
        #LOG.debug(roles[0]['Value'])
        #LOG.debug(roles[1]['Value'])
        role_id=roles[0]['Value']
        cmd = 'role-delete ' + role_id
        role_delete = self.parser.listing(self.keystone(cmd))
        self.assertEquals([], role_delete, "role was deleted.")

    def test_admin_role_get(self):
        role_name = 'rolename_' + str(random.random())
        cmd = 'role-create --name ' + role_name
        roles = self.parser.listing(self.keystone(cmd))
        self.assertTableStruct(roles, ['Property', 'Value'])
        #LOG.debug(roles[0]['Value'])
        #LOG.debug(roles[1]['Value'])
        role_id=roles[0]['Value']
        cmd = 'role-get ' + role_id
        role_created = self.parser.listing(self.keystone(cmd))
        role_id_created=role_created[0]['Value']
        self.assertEqual(role_id, role_id_created, "role ids was the same")
        cmd = 'role-delete ' + role_id
        role_delete = self.parser.listing(self.keystone(cmd))
        self.assertEquals([], role_delete, "role was deleted.")
