#!/usr/local/bin/python3

#
# Cool, you are interested in python?
# After the entire module, you should be able to write most of this file's content on your own!
#

from flask import Flask, request
from threading import Timer
import webbrowser
import subprocess
import html

# Create flask app
app = Flask(__name__)

STDOUT_PREFIX = 'Enter your password: '

# CSS to use
CSS = '''
html, body {
    font-family: system-ui, -apple-system, sans-serif;
}

.empty {
    color: gray;
}

.error {
    color: orange;
}

.invalid {
    color: red;
}

.valid {
    color: green;
} 

fieldset {
    margin-bottom: 1rem;
}

footer {
    font-style: italic;
    margin-top: 2rem;
}

code {
    user-select: all;
}
'''.lstrip()

# The html template with placeholders of the page
PAGE_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Password Security</title>
    <style>{css}</style>
</head>
<body>
    <h1>Password Security</h2>
    <p>Enter your password below to check if its secure!</p>
    <form action="?type={type}" method="post">
        <fieldset>
            <legend>Ergebnis</legend>
            <p>{message}</p>
        </fieldset>

        <input type="{type}" name="password" />
        <button type="submit">Check security</button>
    </form>
    <hr>
    <p>
        Click the following links to change the appearance of the text field:
        <ul>
            <li>
                <a href="?type=password">Use actual password field</a>
            </li>
            <li>
                <a href="?type=text">Use text field</a>
            </li>
        </ul>
    </p>
    <footer>
        <small>Inf-Einf-B Tutorial on 14<sup>th</sup> of November, 12 - 14 o'clock</small>
    </footer>
</body>
</html>
'''.lstrip()


# Handles the index route (one and only route) of the app
@app.route('/', methods=['GET', 'POST'])
def index():
    message = '<span class="empty">Noch nichts gesendet...</span>'
    input_type = request.args.get('type', 'text')

    # Enforce correct values here
    if input_type != 'password' and input_type != 'text':
        input_type = 'text'

    # If there is form data, process it
    if request.method == 'POST':
        try:
            password = request.form.get('password', '').strip()

            # Pluck the given value in the process
            process = subprocess.run(
                ['./password'],
                input=password + '\n',
                capture_output=True, text=True, check=True
            )

            # Prevent accidental XSS
            output = html.escape(process.stdout.removeprefix(STDOUT_PREFIX))

            if 'valid' in output:
                message = f'<span class="valid">{output}</span>'
            else:
                message = f'<span class="invalid">{output}</span>'

        except subprocess.CalledProcessError as e:
            message = f'<span class="error">Could not run the process for password {
                html.escape(password)}: {html.escape(str(e))}</span>'
        except FileNotFoundError:
            message = '<span class="error">Could not find the <code>password</code> binary, did you forget to run <code>make password</code>?</span>'
        except ValueError:
            message = '<span class="error">Invalid request</span>'

    return PAGE_TEMPLATE.format(message=message, type=input_type, css=CSS)


def open_browser():
    webbrowser.open_new_tab('http://127.0.0.1:8080')


if __name__ == '__main__':
    # Wait a bit before opening the browser so flask can start
    Timer(1, open_browser).start()

    # Run flask using the built-in server
    app.run(host='127.0.0.1', port=8080)
