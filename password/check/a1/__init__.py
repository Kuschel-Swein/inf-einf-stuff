import check50
import check50.c
from .. import get_passing_passwords, get_failing_passwords, check_passwords


@check50.check()
def exists():
    check50.exists('password.c')


@check50.check(exists)
def compiles():
    check50.c.compile('./password', lcs50=True)


@check50.check(compiles)
def accepts_passwords():
    check_passwords(passwords=get_passing_passwords(1), should_be_valid=True)


@check50.check(compiles)
def rejects_passwords():
    check_passwords(passwords=get_failing_passwords(1), should_be_valid=False)
