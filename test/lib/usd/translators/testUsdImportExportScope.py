#!/pxrpythonsubst
#
# Copyright 2018 Pixar
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from pxr import Usd

from maya import cmds
from maya import standalone

import fixturesUtils

import os
import unittest


class testUsdImportExportScope(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        inputPath = fixturesUtils.setUpClass(__file__)

        cls._usdFile = os.path.join(inputPath, "UsdImportExportScopeTest",
            "Scopes.usda")

    @classmethod
    def tearDownClass(cls):
        standalone.uninitialize()

    def setUp(self):
        cmds.file(new=True, force=True)

    def testImportScope(self):
        cmds.usdImport(file=self._usdFile, primPath='/')
        dagObjects = cmds.ls(long=True, dag=True)

        self.assertIn('|A', dagObjects)
        self.assertEqual(cmds.nodeType('|A'), 'transform')
        self.assertFalse(cmds.getAttr('|A.tx', lock=True))

        self.assertIn('|A|A_1', dagObjects)
        self.assertEqual(cmds.nodeType('|A|A_1'), 'transform')
        self.assertEqual(cmds.getAttr('|A|A_1.USD_typeName'), 'Scope')
        self.assertTrue(cmds.getAttr('|A|A_1.tx', lock=True))

        self.assertIn('|A|A_1|A_1_I', dagObjects)
        self.assertEqual(cmds.nodeType('|A|A_1|A_1_I'), 'transform')
        self.assertFalse(cmds.getAttr('|A|A_1|A_1_I.tx', lock=True))

        self.assertIn('|A|A_1|A_1_II', dagObjects)
        self.assertEqual(cmds.nodeType('|A|A_1|A_1_II'), 'transform')
        self.assertFalse(cmds.getAttr('|A|A_1|A_1_II.tx', lock=True))

        self.assertIn('|A|A_1|A_1_III', dagObjects)
        self.assertEqual(cmds.nodeType('|A|A_1|A_1_III'), 'transform')
        self.assertEqual(cmds.getAttr('|A|A_1|A_1_III.USD_typeName'), 'Scope')
        self.assertTrue(cmds.getAttr('|A|A_1|A_1_III.tx', lock=True))

        self.assertIn('|A|A_2', dagObjects)
        self.assertEqual(cmds.nodeType('|A|A_2'), 'transform')
        self.assertEqual(cmds.getAttr('|A|A_2.USD_typeName'), 'Scope')
        self.assertTrue(cmds.getAttr('|A|A_2.tx', lock=True))

        self.assertIn('|B', dagObjects)
        self.assertEqual(cmds.nodeType('|B'), 'transform')
        self.assertEqual(cmds.getAttr('|B.USD_typeName'), 'Scope')
        self.assertTrue(cmds.getAttr('|B.tx', lock=True))

        self.assertIn('|B|B_1', dagObjects)
        self.assertEqual(cmds.nodeType('|B|B_1'), 'transform')
        self.assertFalse(cmds.getAttr('|B|B_1.tx', lock=True))

    def testReexportScope(self):
        cmds.usdImport(file=self._usdFile, primPath='/')

        exportedUsdFile = os.path.abspath('Scopes.reexported.usda')
        cmds.usdExport(file=exportedUsdFile)

        stage = Usd.Stage.Open(exportedUsdFile)
        self.assertTrue(stage)

        self.assertTrue(stage.GetPrimAtPath('/A'))
        self.assertEqual(stage.GetPrimAtPath('/A').GetTypeName(), 'Xform')
        self.assertTrue(stage.GetPrimAtPath('/A/A_1'))
        self.assertEqual(stage.GetPrimAtPath('/A/A_1').GetTypeName(), 'Scope')
        self.assertTrue(stage.GetPrimAtPath('/A/A_1/A_1_I'))
        self.assertEqual(stage.GetPrimAtPath('/A/A_1/A_1_I').GetTypeName(),
                'Mesh')
        self.assertTrue(stage.GetPrimAtPath('/A/A_1/A_1_II'))
        self.assertEqual(stage.GetPrimAtPath('/A/A_1/A_1_II').GetTypeName(),
                'Camera')
        self.assertTrue(stage.GetPrimAtPath('/A/A_1/A_1_III'))
        self.assertEqual(stage.GetPrimAtPath('/A/A_1/A_1_III').GetTypeName(),
                'Scope')
        self.assertTrue(stage.GetPrimAtPath('/A/A_2'))
        self.assertEqual(stage.GetPrimAtPath('/A/A_2').GetTypeName(), 'Scope')
        self.assertTrue(stage.GetPrimAtPath('/B'))
        self.assertEqual(stage.GetPrimAtPath('/B').GetTypeName(), 'Scope')
        self.assertTrue(stage.GetPrimAtPath('/B/B_1'))
        self.assertEqual(stage.GetPrimAtPath('/B/B_1').GetTypeName(), 'Xform')


if __name__ == '__main__':
    unittest.main(verbosity=2)
