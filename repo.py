upstream = r"git://xenbits.xen.org/pvdrivers/win/xeniface.git"
internal_push = r"ssh://xenhg@hg.uk.xensource.com/closed/windows/xenbits/win-xeniface.git"
internal_pull = r"git://hg.uk.xensource.com/closed/windows/xenbits/win-xeniface.git"

ref = "staging-8.2"
patches = [
        '0001-Add-write-to-data-updated-to-wake-XAPI.patch',
        '0002-Also-check-platform-timeoffset.patch',
        '0001-Work-around-XAPI-using-halt-rather-then-poweroff.patch',
        '0001-CA-224610.patch'
        ]
