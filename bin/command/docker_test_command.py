#!/usr/bin/env/python
# -*- coding: utf-8 -*-
#
# (c) 2016 WebDevOps.io
#
# This file is part of Dockerfile Repository.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and
# to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions
# of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
# OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import pytest
import sys
from cleo import Output
from jinja2 import Environment, FileSystemLoader
from webdevops import Dockerfile, DockerfileUtility
from webdevops.command import DoitCommand
from webdevops.testinfra import TestinfraDockerPlugin
from webdevops.taskloader import DockerTestTaskLoader

class DockerTestCommand(DoitCommand):
    """
    Tests images

    docker:test
        {--dry-run               : show only which images will be build}
        {--t|threads=0           : threads}
        {--whitelist=?*          : image/tag whitelist }
        {--blacklist=?*          : image/tag blacklist }
    """

    def run_task(self, configuration):
        if configuration['threads'] > 1:
            return self.run_doit(
                task_loader=DockerTestTaskLoader(configuration),
                configuration=configuration
            )
        else:
            # Run directly
            if configuration['dryRun']:
                print 'pytest directory: %s' % (self.configuration['testPath'])
                print ''
            else :
                test_opts = []

                test_opts.extend(['-x', self.configuration['testPath']])

                if self.output.is_verbose():
                    test_opts.extend(['-v'])

                return pytest.main(test_opts, plugins = [TestinfraDockerPlugin(configuration)])

