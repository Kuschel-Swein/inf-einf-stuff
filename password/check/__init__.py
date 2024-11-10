import check50.c

# Format of cases: (password, fails_at_task)
TEST_PASSWORDS = [
    ('hello', 1),  # Fails at Task 1 due to lack of uppercase, number, and symbol
    ('H3!lo', 3),  # Fails at Task 3 due to length requirement (Task 2 would pass)
    ('Pas123456!'),  # Passes all tasks
    ('P@ssw0rd', 3),      # Fails at Task 3 due to length requirement
    ('1234abcd', 1),      # Fails at Task 1 due to lack of uppercase and symbol
    ('!@#ABC123def'),  # Passes all tasks
    ('1111aAaa!!!!', 4),  # Fails at Task 4 due to consecutive same characters
    ('QwErTy123!@'),  # Passes all tasks
    ('!!AAaa11bb', 4),    # Fails at Task 4 due to consecutive same characters
    ('AbC!123xyz@'),  # Passes all tasks
    ('admin', 1),  # Fails at Task 1 due to lack of uppercase, number, and symbol
    ('letMein123!'),   # Passes all tasks
    ('pas5word!23A'),  # Passes all tasks
    ('abcDE!ghi1234'),  # Passes all tasks
    ('P@$W0rD12345'),  # Passes all tasks
    ('ABCabc123', 1),     # Fails at Task 1 due to lack of symbol
    ('Abc@1233Abc_', 4),  # Fails at Task 4 due to consecutive same characters
    ('12abc!XYZ', 3),     # Fails at Task 3 due to length requirement
    ('mySecret2021!'),  # Passes all tasks
    ('qwerty!@123ABC'),  # Passes all tasks
    ('dragon!@123ABC'),  # Passes all tasks
    ('Hello123!!', 4),    # Fails at Task 4 due to consecutive same characters
    ('Zyx!9876lmNOP'),  # Passes all tasks
    ('Test@123', 3),      # Fails at Task 3 due to length requirement
    ('R@nd0mPasw0rd'),  # Passes all tasks
    ('$up3r$trongP@s5'),  # Passes all tasks
    ('abc123def!', 1)   # Fails at Task 1 due to lack of uppercase
]


def _get_relevant_passwords(task, is_failing):
    relevant = []

    for password, fails_at_task in TEST_PASSWORDS:

        should_include = fails_at_task is None or task < fails_at_task

        if is_failing:
            should_include = not should_include

        if should_include:
            relevant.append(password)

    return relevant


def exists():
    check50.exists('password.c')


def compiles():
    check50.run('make password').exit(0)


def accepts_arguments():
    try:
        check50.run('./password a').exit()

    except check50.Failure as f:
        raise check50.Failure(
            'Expected the program to accept command line arguments.', help=f.payload['help'])


def passwords(task, should_be_valid, include_arguments=False):
    passwords = _get_relevant_passwords(task, is_failing=not should_be_valid)
    text = 'valid' if should_be_valid else 'uppercase letter, lowercase letter, number and symbol'

    for password in passwords:
        try:
            check50.run('./password').stdin(password).stdout(text).exit()

            # '$' cannot be reliably used in arguments, thus it will be skipped here
            if include_arguments and not '$' in password:
                check50.run('./password ' + password).stdout(text).exit()

        except check50.Failure as f:
            rationale = f'Expected password "{
                password}" to be accepted.' if should_be_valid else f'Expected password "{password}" to be rejected.'

            raise check50.Failure(rationale, f.payload['help'])
