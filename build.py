#!python -u

import os, sys
import xspatchq.buildtool as xsbuildtool
import xspatchq.symstore as xssymstore
import xspatchq.msvc as xsmsvc
import xspatchq.gittool as xsgittool
import patchqueue
import checkout

if __name__ == '__main__':
    debug = { 'checked': True, 'free': False }
    sdv = { 'nosdv': False, None: True }

    vs = xsmsvc.get_version()

    xsbuildtool.default_environment('VENDOR_NAME','Citrix')
    xsbuildtool.default_environment('VENDOR_PREFIX','XS')
    xsbuildtool.default_environment('PRODUCT_NAME','XenServer')
    xsbuildtool.default_environment('OBJECT_PREFIX','XenServer')

    os.environ['MAJOR_VERSION'] = '8'
    os.environ['MINOR_VERSION'] = '1'
    os.environ['MICRO_VERSION'] = '0'

    xsbuildtool.default_environment('BUILD_NUMBER',
            xsbuildtool.next_build_number())

    print("BUILD_NUMBER=%s" % os.environ['BUILD_NUMBER'])

    if 'GIT_REVISION' in os.environ.keys():
        revision = open('revision', 'w')
        print(os.environ['GIT_REVISION'], file=revision)
        revision.close()

    xssymstore.delete(patchqueue.package, 30)

    if vs=='vs2012':
        release = 'Windows Vista'
    else:
        release = 'Windows 7'
   
    buildwd = os.getcwd()

    if not os.path.exists(patchqueue.package):
        checkout.clone_apply_patchqueue()

    os.chdir(patchqueue.package)
    os.makedirs(patchqueue.package, exist_ok=True)
    
    xsbuildtool.archive(
            patchqueue.package + '\\source.tgz', 
            xsbuildtool.getfiles(os.getcwd()), 
            tgz = True)

    cmd=['python', '-u', 'build.py', sys.argv[1], sys.argv[2]]
    xsbuildtool.shell(cmd, None)

    xssymstore.add(patchqueue.package, release, 'x86', debug[sys.argv[1]], vs)
    xssymstore.add(patchqueue.package, release, 'x64', debug[sys.argv[1]], vs)

    if len(sys.argv) <= 2 or sdv[sys.argv[2]]:
        for component in patchqueue.sdv_components:
            xsmsvc.run_sdv(component, patchqueue.package, vs)

    xsbuildtool.archive(buildwd+'\\'+patchqueue.package + '.tar', [patchqueue.package,'revision'])

    os.chdir(buildwd)


