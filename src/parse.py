#!/usr/bin/env python
# encoding: utf-8
#
# Copyright  (c) 2017 tobias@scheck-media.de
#
# MIT Licence. See http://opensource.org/licenses/MIT
#
# Created on 2017-07-25
#

"""
Alfred parser for insect a high precision scientific calculator with full support for physical units.
https://insect.sh/
"""

import sys,os
import subprocess
import syslog
from workflow import Workflow, ICON_WARNING, ICON_INFO
from workflow.background import run_in_background, is_running

log = None
os.environ['PATH'] += ':/usr/local/bin'

BINARY = "/usr/local/bin/insect"
def cmd_exists(cmd):
    return subprocess.call("type " + cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0

def call_cmd(cmd):
    return subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)

def main(wf):
    if not len(wf.args):
        return 1

    query = wf.args[0]
    log.debug('query : %s', query)
    log.debug('PATH: %s' % os.environ['PATH'])

    # Notify of available update
    if wf.update_available:
        wf.add_item('A newer version is available',
                    'Action this item to download & install the new version',
                    autocomplete='workflow:update')

    if cmd_exists(BINARY):
        out = None
        error = None

        try:
            arg = (BINARY + ' "%s"' % (query))
            out = call_cmd(arg)
        except Exception as err:
            log.exception('%s : %s', err.__class__, err)
            error = err.message

        if error:  # Show error
            wf.add_item(error,
                        'For example: 30 cm -> mm OR deg(30) -> rad OR 30 km / 30 m',
                        valid=False, icon=ICON_WARNING)
        else:
            wf.add_item(out,
                        valid=True,
                        arg=out,
                        copytext=out,
                        largetext=out,
                        icon='icon.png')

        wf.send_feedback()
        log.debug('finished')
        return 0

    else:
        wf.add_item('Insect not found','Please install CLI. https://github.com/sharkdp/insect',
                        valid=False, icon=ICON_WARNING)
        wf.send_feedback()
        log.debug('insect not found')
        return 1

if __name__ == '__main__':
    wf = Workflow(
        help_url='https://github.com/scheckmedia/Alfred-Insect/issues',
        update_settings={'github_slug': 'scheckmedia/Alfred-Insect'})
    log = wf.logger
    sys.exit(wf.run(main))