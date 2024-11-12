#!/usr/local/bin/python3

#
# Cool, you are interested in python?
# After the entire module, you should be able to write most of this file's content on your own!
#
# Currenty you do not have to understand ANYTHING thats written inside this file.
# However, if you have any questions on it's content, I'm happy to answer them.
#

from flask import Flask, request
from threading import Timer
import webbrowser
import subprocess
import html
import logging

# Create flask app
app = Flask(__name__)

# ANSI color codes for use on the terminal
TERMINAL_YELLOW = '\033[93m'
TERMINAL_RESET = '\033[0m'

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
<html lang="de-DE">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Passwort Sicherheit</title>
    <style>{css}</style>
</head>
<body>
    <h1>Passwort Sicherheit</h2>
    <p>Gib dein Passwort unten ein, um zu prüfen, ob es sicher ist!</p>
    <form action="?type={type}" method="post">
        <fieldset>
            <legend>Ergebnis</legend>
            <p>{message}</p>
        </fieldset>

        <input type="{type}" name="password" />
        <button type="submit">Sicherheit prüfen</button>
    </form>
    <hr>
    <p>
        Klicke auf die folgenden Links, um das Aussehen des Textfelds zu ändern:
        <ul>
            <li>
                <a href="?type=password">Passwordfeld verwenden</a>
            </li>
            <li>
                <a href="?type=text">Textfeld verwenden</a>
            </li>
        </ul>
    </p>
    <footer>
        <small>Vergiss nicht dieses Skript mit <kbd>Strg</kbd> + <kbd>C</kbd> in deinem Terminal zu beenden!</small>
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
            message = '<span class="error">Die <code>password</code>-Binary konnte nicht gefunden werden. Hast du vergessen, <code>make password</code> auszuführen?</span>'
        except ValueError:
            message = '<span class="error">Ungültige Anfrage</span>'

    return PAGE_TEMPLATE.format(message=message, type=input_type, css=CSS)


def flask_started():
    # Open the browser once the app is started
    webbrowser.open_new_tab('http://127.0.0.1:8080')

    # Remind how to exit the script
    print(
        f'\n{TERMINAL_YELLOW}🚪 Press STRG + C to exit this script!{TERMINAL_RESET}\n')


if __name__ == '__main__':
    # Wait a bit before calling so flask can start
    Timer(1, flask_started).start()

    # disable flask's logger so students don't get confused
    logging.getLogger('werkzeug').disabled = True

    # Run flask using the built-in server
    app.run(host='127.0.0.1', port=8080)
