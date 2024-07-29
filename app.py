from flask import Flask, render_template, request
import re

app = Flask(__name__)

def parse_chat(file_content):
    messages = []
    message_pattern = re.compile(r'(\d{2}/\d{2}/\d{4}, \d{1,2}:\d{2}\s?[ap]m) - (.*?): (.*)', re.IGNORECASE)
    system_message_pattern = re.compile(r'(\d{2}/\d{2}/\d{4}, \d{1,2}:\d{2}\s?[ap]m) - (.*)')
    for line in file_content.split('\n'):
        match = message_pattern.match(line)
        if match:
            timestamp, sender, message = match.groups()
            messages.append({'timestamp': timestamp, 'sender': sender, 'message': message})
            print(f'Parsed message: {timestamp} - {sender}: {message}')  # Debug output
        else:
            match = system_message_pattern.match(line)
            if match:
                timestamp, message = match.groups()
                messages.append({'timestamp': timestamp, 'sender': 'System', 'message': message})
                print(f'Parsed system message: {timestamp} - {message}')  # Debug output
            else:
                print(f'No match for line: {line}')  # Debug output
    return messages

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        content = file.read().decode('utf-8')
        print(content)  # Debug output
        messages = parse_chat(content)
        return render_template('chat.html', messages=messages)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
