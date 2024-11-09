import random

class FrenchLearningBot:
    def __init__(self):
        self.conversation_starters = {
            "greetings": [
                "Bonjour! Comment allez-vous?",
                "Salut! Comment ça va?",
                "Bienvenue! Comment allez-vous aujourd'hui?"
            ],
            "topics": [
                "la nourriture (food)",
                "les hobbies (hobbies)",
                "la famille (family)",
                "la météo (weather)"
            ]
        }
        
        self.common_phrases = {
            "je ne comprends pas": "I don't understand",
            "pouvez-vous répéter": "Can you repeat",
            "qu'est-ce que ça veut dire": "What does that mean",
            "en anglais, s'il vous plaît": "In English, please"
        }
        
        self.vocabulary = {
            "food": {
                "le pain": "bread",
                "le fromage": "cheese",
                "les fruits": "fruits",
                "l'eau": "water"
            },
            "weather": {
                "il fait beau": "It's nice weather",
                "il pleut": "It's raining",
                "il fait chaud": "It's hot",
                "il fait froid": "It's cold"
            }
        }

    def respond_to_user(self, user_input):
        user_input = user_input.lower().strip()
        
        if user_input == 'quit':
            return "Au revoir! (Goodbye!)", False
        elif user_input == 'help':
            return """
Available commands:
- 'vocabulary': Show common words
- 'phrases': Show useful phrases
- 'help': Show this help message
- 'en anglais': Get English translation
- 'quit': End conversation
            """, True
        elif user_input == 'vocabulary':
            vocab_text = "Common vocabulary:\n"
            for category, words in self.vocabulary.items():
                vocab_text += f"\n{category.title()}:\n"
                for french, english in words.items():
                    vocab_text += f"- {french}: {english}\n"
            return vocab_text, True
        elif user_input == 'phrases':
            phrases_text = "Useful phrases:\n"
            for french, english in self.common_phrases.items():
                phrases_text += f"- {french}: {english}\n"
            return phrases_text, True
        elif user_input in ['en anglais', 'english', 'en anglais s\'il vous plait']:
            return "Please type the French phrase you want translated:", True
        elif user_input in self.common_phrases:
            return f"'{user_input}' means '{self.common_phrases[user_input]}' in English", True
        elif any(user_input in words for words in self.vocabulary.values()):
            for category, words in self.vocabulary.items():
                if user_input in words:
                    return f"'{user_input}' means '{words[user_input]}' in English (Category: {category})", True
        else:
            responses = [
                f"Très bien! (Very good!) Let's practice more. {random.choice(self.conversation_starters['greetings'])}",
                f"Excellent! Parlons de {random.choice(self.conversation_starters['topics'])}",
                "Je comprends! (I understand!) Would you like to learn more vocabulary?",
                "Désolé, je ne comprends pas. Pouvez-vous répéter? (Sorry, I don't understand. Can you repeat?)"
            ]
            return random.choice(responses), True
