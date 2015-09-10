#!python -u

import patchqueue
import os
import sys
import posixpath
import shutil
import subprocess

def shell(command, dir):
    print(dir)
    print(command)
    sys.stdout.flush()

    sub = subprocess.Popen(' '.join(command), cwd=dir,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)

    for line in sub.stdout:
        print(line.decode(sys.getdefaultencoding()).rstrip())

    sub.wait()

    return sub.returncode

def rebase():
    pregitdir = os.getcwd()

    cmd = ['git', 'clone', '--bare', patchqueue.remoterepo, 'rebase.git']
    shell(cmd, None)

    os.chdir('rebase.git')

    cmd = ['git', 'push', '--mirror', patchqueue.baserepopush]
    shell(cmd, None)

    os.chdir(pregitdir)

if __name__ == '__main__':
    rebase()
    if os.path.exists(patchqueue.package):
        print("Package")
        count = 0
        rebasename=""
        while True:
            rebasename = patchqueue.package+".rebase."+str(count)
            if (not os.path.exists(rebasename)):
                break;
            count+=1
        os.rename(patchqueue.package,rebasename)

