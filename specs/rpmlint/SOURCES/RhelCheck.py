"""
Rpmlint plugin for checking if there fedora contitional without redhat conditional.

Author: Radek Novacek <rnovacek@redhat.com>
        Thomas Woerner <twoerner@redhat.com>

"""

from Filter import printError, printWarning, addDetails
import AbstractCheck

class RhelCheck(AbstractCheck.AbstractCheck):
    def __init__(self):
        AbstractCheck.AbstractCheck.__init__(self, "RhelCheck")

    def check(self, pkg):
        # Check will be performed only on the source package
        if not pkg.isSource():
            return

        # Find name of the specfile
        spec = None
        for fname, pkgfile in pkg.files().items():
            if not fname.endswith(".spec"):
                continue

            try:
                f = open(pkgfile.path, "r")
            except Exception, e:
                printWarning(pkg, 'read-error', fname, e)
                continue

            fedora = rhel = False
            line_no = 0
            for line in f:
                line_no += 1

                # Check only conditional expressions
                if not "%if" in line:
                    continue

                if "0%{?fedora}" in line:
                    fedora = True
                elif "%{?fedora}" in line:
                    printWarning(pkg, "malformed-fedora-conditional",
                                 "%s:%d" % (fname, line_no))
                if "0%{?rhel}" in line:
                    rhel = True
                elif "%{?rhel}" in line:
                    printWarning(pkg, "malformed-rhel-conditional",
                                 "%s:%d" % (fname, line_no))

            # If there is a fedora check there should also be a rhel check
            if fedora and not rhel:
                printWarning(pkg, "no-rhel-conditional", fname)

            f.close()

check = RhelCheck()

addDetails(
'no-rhel-conditional',
"""There is a check for fedora version but no check for version of RHEL.""",
)
