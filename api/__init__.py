"""App entry point"""
import os
import tempfile
import openai

from flask import Flask, jsonify, request
from api.conversations import get_conversation, get_conversations, new_message
from api.llms.openai_functions import run_conversation

application = Flask(__name__)


@application.route('/')
def index():
    """Placeholder route"""
    return 'Hello, World!'


# Create a route to test an OpenAI function call
@application.route('/test-function')
def test_function():
    """Create test call to OpenAI function"""
    return run_conversation()


@application.route('/message', methods=['POST'])
def message():
    """Handle sending a new message to a conversation."""
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        return new_message()
    else:
        return jsonify({"success": False, "error": "Invalid content type"}), 400


@application.route('/user/<npub>/conversations', methods=['GET'])
def go_get_conversations(npub):
    """Fetch conversations for a user npub"""
    return get_conversations(npub)


@application.route('/conversation/<conversationId>', methods=['GET'])
def go_get_conversation(conversationId):
    return get_conversation(conversationId)


@application.route('/recording', methods=['POST'])
def upload_recording():
    print("here so lets try")
    print(request.files)

    if 'audio' not in request.files:
        print("No audio thing")
        return jsonify({'error': 'No audio file provided'}), 400

    audio = request.files['audio']

    if audio.filename == '':
        print("no filename maybe")
        return jsonify({'error': 'No audio file provided'}), 400

    if audio:
        # Save audio file to uploads folder
        # filename = os.path.join('uploads', audio.filename)
        tmp_folder = tempfile.gettempdir()
        filename = os.path.join(tmp_folder, audio.filename)
        audio.save(filename)

        print("Saved to:", filename)

      # Open saved temp file
        with open(filename, 'rb') as audio_file:
            print("Opened audio file. Transcripting...")
            # Transcribe audio
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
            print(transcript)

        # audio_file = open(filename, 'rb')

        # Transcribe audio with Whisper
        # transcript = openai.Audio.transcribe("whisper-1", audio_file)

        # Return transcript text
        return jsonify({'transcript': transcript, 'success': True}), 201
