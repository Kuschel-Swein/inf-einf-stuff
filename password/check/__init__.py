import check50.c

# Format of cases: (password, fails_at_task, skip_before_task)
TEST_PASSWORDS = [
    ('hello', 1, None),  # Fails at Task 1 due to lack of uppercase, number, and symbol
    ('H3!lo', 3, None),  # Fails at Task 3 due to length requirement (Task 2 would pass)
    ('Pas123456!', None, None),  # Passes all tasks
    ('P@ssw0rd', 3, None),      # Fails at Task 3 due to length requirement
    ('1234abcd', 1, None),      # Fails at Task 1 due to lack of uppercase and symbol
    ('!@#ABC123def', None, None),  # Passes all tasks
    ('1111aAaa!!!!', 4, None),  # Fails at Task 4 due to consecutive same characters
    ('QwErTy123!@', None, None),  # Passes all tasks
    ('!!AAaa11bb', 4, None),    # Fails at Task 4 due to consecutive same characters
    ('AbC!123xyz@', None, None),  # Passes all tasks

    # Fails at Task 1 due to lack of uppercase, number, and symbol
    ('admin', 1, None),
    ('letMein123!', None, None),   # Passes all tasks
    ('pas5word!23A', None, None),  # Passes all tasks
    ('abcDE!ghi1234', None, None),  # Passes all tasks
    ('P@$W0rD12345', None, None),  # Passes all tasks
    ('ABCabc123', 1, None),     # Fails at Task 1 due to lack of symbol

    # Fails at Task 4 due to consecutive same characters
    ('Abc@1233Abc_', 4, None),

    ('12abc!XYZ', 3, None),     # Fails at Task 3 due to length requirement
    ('mySecret2021!', None, None),  # Passes all tasks
    ('qwerty!@123ABC', None, None),  # Passes all tasks
    ('dragon!@123ABC', None, None),  # Passes all tasks
    ('Hello123!!', 4, None),    # Fails at Task 4 due to consecutive same characters
    ('Zyx!9876lmNOP', None, None),  # Passes all tasks
    ('Test@123', 3, None),      # Fails at Task 3 due to length requirement
    ('R@nd0mPasw0rd', None, None),  # Passes all tasks
    ('$up3r$trongP@s5', None, None),  # Passes all tasks
    ('abc123def!', 1, None),     # Fails at Task 1 due to lack of uppercase

    # Ten most common passwords
    ('123456', 6, 5),
    ('password', 6, 5),
    ('12345678', 6, 5),
    ('qwerty', 6, 5),
    ('123456789', 6, 5),
    ('12345', 6, 5),
    ('1234', 6, 5),
    ('111111', 6, 5),
    ('1234567', 6, 5),
    ('dragon', 6, 5)
]


def _get_relevant_passwords(task, is_failing):
    relevant = []

    for password, fails_at_task, skip_before_task in TEST_PASSWORDS:

        # Check if we should include that case yet
        if skip_before_task is None or task >= skip_before_task:
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
