#!/usr/local/autopkg/python
#
# Copyright 2013 Jeremy Leggat, 2010 Per Olofsson
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

from __future__ import absolute_import

import os.path
import re
import subprocess

from autopkglib import Processor, ProcessorError

__all__ = ["MonitVersioner"]


class MonitVersioner(Processor):
    description = "Extracts version of Monit to be installed."
    input_variables = {
        "root_path": {
            "required": True,
            "description": "Path to root of unzipped Monit files.",
        },
    }
    output_variables = {
        "version": {
            "description": "Version of Monit.",
        },
    }

    description = __doc__

    def get_version(self, root_dir, bin_file, rc_file):

        bin_path = os.path.join(root_dir, bin_file)
        rc_path = os.path.join(root_dir, rc_file)
        p = subprocess.Popen([bin_path, '-c', rc_path, '-V'], stdout=subprocess.PIPE)
        (output, err) = p.communicate()

        m = re.search(r'This is Monit version ([0-9\.]+)', output)
        if not m:
            raise ProcessorError(
            "Couldn't find version, %s returned %s"
            % (file_path, output))

        return m.group(1)

    def main(self):
        root_path = self.env['root_path']
        bin_file = 'bin/monit'
        rc_file = 'conf/monitrc'
        self.env['version'] = self.get_version(root_path, bin_file, rc_file)
        self.output("Found version %s in file %s" % (self.env['version'], root_path))


if __name__ == '__main__':
    processor = MonitVersioner()
    processor.execute_shell()
