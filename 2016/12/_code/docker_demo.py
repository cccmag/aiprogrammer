#!/usr/bin/env python3
"""Docker Demo: Containerize a Python Application"""

from flask import Flask, jsonify, request
import os
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

COUNTER = 0


@app.route('/')
def hello():
    return jsonify({
        'message': 'Hello from Docker!',
        'version': '1.0',
    })


@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})


@app.route('/counter', methods=['GET', 'POST'])
def counter():
    global COUNTER

    if request.method == 'POST':
        COUNTER += 1
        logger.info(f"Counter incremented to {COUNTER}")
        return jsonify({'counter': COUNTER, 'action': 'incremented'})
    else:
        return jsonify({'counter': COUNTER})


@app.route('/reset', methods=['POST'])
def reset():
    global COUNTER
    COUNTER = 0
    logger.info("Counter reset")
    return jsonify({'counter': COUNTER, 'action': 'reset'})


def demo():
    print("=== Docker Demo Application ===")
    print("A simple Flask app with health check and counter endpoints")
    print("Endpoints:")
    print("  GET  /         - Hello message")
    print("  GET  /health   - Health check")
    print("  GET  /counter  - Get counter")
    print("  POST /counter  - Increment counter")
    print("  POST /reset    - Reset counter")
    print("\nTo run this with Docker:")
    print("  docker build -t myapp .")
    print("  docker run -p 8080:80 myapp")


if __name__ == "__main__":
    demo()
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)