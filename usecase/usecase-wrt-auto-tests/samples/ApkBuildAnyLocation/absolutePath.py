#!/usr/bin/env python
#
# Copyright (c) 2015 Intel Corporation.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of works must retain the original copyright notice, this
#   list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the original copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
# * Neither the name of Intel Corporation nor the names of its contributors
#   may be used to endorse or promote products derived from this work without
#   specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY INTEL CORPORATION "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL INTEL CORPORATION BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Authors:
#         Hongjuan, Wang<hongjuanx.wang@intel.com>

import unittest
import os
import sys
import commands
import shutil
import comm


class TestPackertoolsFunctions(unittest.TestCase):

    def test_absolutePath_hostApp(self):
        comm.setUp()
        cmd = "python %smake_apk.py --package=org.xwalk.example --name=example --arch=%s --mode=%s --app-url=https://crosswalk-project.org/" % \
              (comm.Pck_Tools, comm.ARCH, comm.MODE)
        print os.getcwd()
        comm.gen_pkg(cmd, self)

    def test_absolutePath_manifest(self):
        comm.setUp()
        manifestPath = comm.ConstPath + "/res/manifest.json"
        cmd = "python %smake_apk.py --package=org.xwalk.example --arch=%s --mode=%s --manifest=%s" % \
              (comm.Pck_Tools, comm.ARCH, comm.MODE, manifestPath)
        os.chdir(comm.ConstPath + '/../../tools')
        print os.getcwd()
        comm.gen_pkg(cmd, self)

    def test_absolutePath_package(self):
        comm.setUp()
        appRoot = comm.ConstPath + "/res/"
        cmd = "python %smake_apk.py --package=org.xwalk.example --name=example --arch=%s --mode=%s --app-root=%s --app-local-path=index.html" % \
              (comm.Pck_Tools, comm.ARCH, comm.MODE, appRoot)
        os.chdir(comm.ConstPath + '/../../tools/crosswalk')
        print os.getcwd()
        comm.gen_pkg(cmd, self)


if __name__ == '__main__':
    unittest.main()
