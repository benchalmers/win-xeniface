import sys
import os
import subprocess
import shutil

import clean
import git
import repo

def shell(cmd, dir):
    print(' '.join(cmd))
    sys.stdout.flush()

    sub = subprocess.Popen(' '.join(cmd), cwd=dir,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)

    for line in sub.stdout:
        print(line.decode(sys.getdefaultencoding()).rstrip())

    sub.wait()

    return sub.returncode

def main(argv):
    path = 'local'
    artefact = 'xeniface.tar'

    clean.main([])

    git.clone(repo.internal_pull, path)
    git.checkout(path, repo.ref)

    for patch in repo.patches:
        git.am(path, patch)

    os.environ['VENDOR_NAME'] = 'Citrix'
    os.environ['VENDOR_PREFIX'] = 'XS'
    os.environ['PRODUCT_NAME'] = 'XenServer'

    cmd = ['python', '-u', 'build.py'] + argv[1:]

    res = shell(cmd, path)
    if res != 0:
        raise Exception("%s returned :" % ' '.join(cmd), res)

    shutil.copy(os.path.join(path, artefact), '.')

if __name__ == '__main__':
    main(sys.argv)
