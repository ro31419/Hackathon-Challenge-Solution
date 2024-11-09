from flask import Flask, render_template, request, jsonify
from google.cloud import speech, texttospeech
from google.cloud.speech_v1 import SpeechClient
import openai
import os
import tempfile
import wave
import numpy as np
from datetime import datetime

app = Flask(__name__)

# Initialize clients (you'll need to set up credentials)
speech_client = speech.SpeechClient()
tts_client = texttospeech.TextToSpeechClient()

# Configure OpenAI (you'll need to set your API key)
openai.api_key = 'your-openai-api-key'

class FrenchEvaluator:
    def evaluate_pronunciation(self, transcript, confidence_score):
        # Basic scoring based on confidence and common French pronunciation rules
        base_score = confidence_score * 100
        
        # Check for common French pronunciation patterns
        patterns = {
            'eu': 1.1,
            'ou': 1.1,
            'ai': 1.1,
            'é': 1.2,
            'è': 1.2
        }
        
        for pattern, multiplier in patterns.items():
            if pattern in transcript.lower():
                base_score *= multiplier
        
        return min(100, base_score)

    def evaluate_grammar(self, transcript):
        # Use OpenAI to evaluate grammar
        prompt = f"""
        Evaluate the following French sentence for grammatical correctness. 
        Provide a score from 0-100 and brief explanation in English:
        "{transcript}"
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Extract score from response (assuming GPT provides a numerical score)
        return float(response.choices[0].message.content.split()[0])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_audio', methods=['POST'])
def process_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    audio_file = request.files['audio']
    
    # Save audio file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio:
        audio_file.save(temp_audio.name)
        
        # Process with Google Speech-to-Text
        with open(temp_audio.name, 'rb') as audio_file:
            content = audio_file.read()
            
        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(
            language_code='fr-FR',
            enable_word_confidence=True
        )
        
        response = speech_client.recognize(config=config, audio=audio)
        
        # Get transcript and confidence
        transcript = response.results[0].alternatives[0].transcript
        confidence = response.results[0].alternatives[0].confidence
        
        # Evaluate pronunciation and grammar
        evaluator = FrenchEvaluator()
        pronunciation_score = evaluator.evaluate_pronunciation(transcript, confidence)
        grammar_score = evaluator.evaluate_grammar(transcript)
        
        # Generate AI response using OpenAI
        ai_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a friendly French language tutor. Respond in French, keeping responses natural and encouraging."},
                {"role": "user", "content": transcript}
            ]
        )
        
        ai_text_response = ai_response.choices[0].message.content
        
        # Convert AI response to speech
        synthesis_input = texttospeech.SynthesisInput(text=ai_text_response)
        voice = texttospeech.VoiceSelectionParams(
            language_code='fr-FR',
            name='fr-FR-Standard-A'
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        
        response = tts_client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )
        
        # Save AI response audio
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        response_audio_path = f'static/responses/response_{timestamp}.mp3'
        os.makedirs('static/responses', exist_ok=True)
        
        with open(response_audio_path, 'wb') as out:
            out.write(response.audio_content)
        
        return jsonify({
            'transcript': transcript,
            'pronunciation_score': pronunciation_score,
            'grammar_score': grammar_score,
            'ai_text_response': ai_text_response,
            'ai_audio_response': response_audio_path
        })

if __name__ == '__main__':
    app.run(debug=True)
