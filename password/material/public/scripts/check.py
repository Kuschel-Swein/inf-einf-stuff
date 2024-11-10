#!/usr/local/bin/python3

#
# Cool, you are interested in python?
# After the entire module, you should be able to write part of this file's content on your own!
#

import subprocess
import argparse

# Format of cases: (password, fails_at_task, skip_before_task)
TEST_CASES = [
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
    ('123456', 5, 5),
    ('password', 5, 5),
    ('12345678', 5, 5),
    ('qwerty', 5, 5),
    ('123456789', 5, 5),
    ('12345', 5, 5),
    ('1234', 5, 5),
    ('111111', 5, 5),
    ('1234567', 5, 5),
    ('dragon', 5, 5)
]


def run_test(password, task):
    try:
        outputs = []

        # Run with standard input for all tasks
        process = subprocess.run(
            ['./password'],
            input=password + '\n',
            capture_output=True, text=True, check=True
        )

        outputs.append(process.stdout)

        # For all tasks besides one also run with command line argument
        if task > 1:
            process = subprocess.run(
                ['./password', password],
                stdin=subprocess.DEVNULL,  # fail if stdin is requested even if password is given
                capture_output=True, text=True, check=True
            )
            outputs.append(process.stdout)

        # Check if 'valid' is present in all outputs
        return all('valid' in output.lower() for output in outputs)

    except FileNotFoundError:
        print(
            f'[⚡] Could not find the "password" binary, did you forget to run "make password"?')

    except subprocess.CalledProcessError as e:
        print(f'[⚡] Error running "{password}": {e}')
        return None


def main():
    parser = argparse.ArgumentParser(
        description='Validates the C password program lab')
    parser.add_argument('-t', '--task', type=int, default=5,
                        help='Up to which task to validate (1-5)')
    args = parser.parse_args()

    if not (1 <= args.task <= 5):
        print('Error: --task flag must be between 1 and 5.')
        return

    print(f'Running tests for Task {args.task}...')

    # Iterate over each test case and check if the output matches expected results
    passed = 0
    total = 0
    for password, fails_at_task, skip_before_task in TEST_CASES:
        # Check if we should run that task yet
        if skip_before_task is None or args.task >= skip_before_task:
            total += 1

            # Determine expected result: True if the task is before or equal to fails_at_task, False otherwise
            expected = fails_at_task is None or args.task < fails_at_task
            actual = run_test(password, args.task)

            if actual == expected:
                print(f'[✅] Password: "{password}"')
                passed += 1
            else:
                print(f'[❌] Password: "{password}"')
                print(f'  Expected: {expected}, Got: {actual}')

    print(f'\nTotal passed: {passed}/{total}')


if __name__ == '__main__':
    main()
