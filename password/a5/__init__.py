import check50
import check50.c

TASK = 5
TOP_TEN_COMMON_PASSWORDS = [
    '123456',
    'password',
    '12345678',
    'qwerty',
    '123456789',
    '12345',
    '1234',
    '111111',
    '1234567',
    'dragon'
]

check = check50.import_checks('../')


@check50.check()
def exists():
    check.exists()


@check50.check(exists)
def compiles():
    check.compiles()


@check50.check(compiles)
def supports_arguments():
    check.supports_arguments()


@check50.check(supports_arguments)
def accepts_passwords():
    check.passwords(task=TASK, should_be_valid=True, include_arguments=True)


@check50.check(supports_arguments)
def rejects_passwords():
    check.passwords(task=TASK, should_be_valid=False, include_arguments=True)


@check50.check(supports_arguments)
def rejects_common_passwords():
    for password in TOP_TEN_COMMON_PASSWORDS:
        try:
            check50.run('./password').stdin(password).stdout('common').exit()
            check50.run('./password ' + password).stdout('common').exit()

        except check50.Failure as f:
            rationale = f'Expected password "{
                password}" to be flagged as common password.'

            raise check50.Failure(rationale, f.payload['help'])
