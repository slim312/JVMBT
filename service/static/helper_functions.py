from requests_kerberos import HTTPKerberosAuth, DISABLED
from subprocess import Popen, PIPE
import os

WINDOWS_PRINCIPAL = "{username}@D800.MIL:{pwd}"
LINUX_PRINCIPAL = "{username}@D800.MIL"
KINIT_PRINCIPAL = "{username}@D800.MIL"
LINUX = "posix"
WINDOWS = "nt"


def run_kinit(username: str, password: str) -> int:
    process = Popen(["kinit", KINIT_PRINCIPAL.format(username=username)], stdin=PIPE)
    stdout, stderr = process.communicate(password)
    return process.returncode


def create_kerberos_token(username: str, pwd) -> HTTPKerberosAuth:
    # Make sure to run kinit on host machine before creating token
    run_kinit(username=username, password=pwd)
    if os.name == WINDOWS:
        principal = WINDOWS_PRINCIPAL.format(username=username, pwd=pwd)
    elif os.name == LINUX:
        principal = LINUX_PRINCIPAL.format(username=username)
    else:
        raise OSError(f"Unrecognized OS: {os.name}")
    return HTTPKerberosAuth(principal=principal, mutual_authentication=DISABLED)
