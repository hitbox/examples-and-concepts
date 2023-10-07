import textwrap

from flask import Flask, Response, jsonify, render_template, request, url_for

app = Flask('server_sent_events')

messages = []

@app.context_processor
def inject():
    return dict(MESSAGE=url_for('message'), EVENTS=url_for('events'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/message', methods=['POST'])
def message():
    messages.append(request.form['message'])
    return jsonify({})

def eventsource(payload):
    return textwrap.indent(payload, 'data: ') + '\n\n'

@app.route('/events')
def events():
    def stream():
        n = 0
        while True:
            if n != len(messages):
                for message in messages[-(len(messages)-n):]:
                    result = eventsource(message)
                    yield result
                n = len(messages)
    return Response(stream(), mimetype="text/event-stream")
