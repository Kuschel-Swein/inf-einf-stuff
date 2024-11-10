import check50
import check50.c

check = check50.import_checks('../')


@check50.check()
def exists():
    check50.exists('password.c')


@check50.check(exists)
def compiles():
    check50.c.compile('./password', lcs50=True)


@check50.check(compiles)
def accepts_passwords():
    check.passwords(task=1, should_be_valid=True)


@check50.check(compiles)
def rejects_passwords():
    check.passwords(task=1, should_be_valid=False)
