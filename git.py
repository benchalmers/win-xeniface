import sys
import os
import shutil
import stat
import subprocess

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

def remove_readonly(func, path, execinfo):
    os.chmod(path, stat.S_IWRITE)
    os.unlink(path)

def clone(url, path, bare=False):
    if os.path.exists(path):
        print ("Removing %s" % path)
        shutil.rmtree(path, onerror=remove_readonly)

    cmd = ['git', 'clone']
    if bare:
        cmd.append('--bare')

    cmd.append(url)
    cmd.append(path)

    res = shell(cmd, None)
    if res != 0:
        raise Exception("%s returned :" % ' '.join(cmd), res)

def checkout(path, ref):
    cmd = ['git', 'checkout', ref]

    res = shell(cmd, path)
    if res != 0:
        raise Exception("%s returned :" % ' '.join(cmd), res)

def am(path, patch):
    cwd = os.getcwd()
    cmd = ['git', 'am', os.path.join(cwd, patch)]

    res = shell(cmd, path)
    if res != 0:
        raise Exception("%s returned :" % ' '.join(cmd), res)

def mirror(src_url, dst_url):
    path = 'local.git'

    clone(src_url, path, bare=True)

    cmd = ['git', 'push', '--mirror']
    cmd.append(dst_url)

    res = shell(cmd, path)
    if res != 0:
        raise Exception("%s returned :" % ' '.join(cmd), res)

    print ("Removing %s" % path)
    shutil.rmtree(path, onerror=remove_readonly)
