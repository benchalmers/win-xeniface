upstream = r"git://xenbits.xen.org/pvdrivers/win/xeniface.git"
internal_push = r"ssh://xenhg@hg.uk.xensource.com/closed/windows/xenbits/win-xeniface.git"
internal_pull = r"git://hg.uk.xensource.com/closed/windows/xenbits/win-xeniface.git"

ref = "master"
patches = [
        '0001-CP-15479-Debrand-lite-agent.patch',
        '0001-Add-write-to-data-updated-to-wake-XAPI.patch',
        '0002-Also-check-platform-timeoffset.patch',
        ]
