import re

class SentenceReadingAgent:
    def __init__(self):
        self.names = {'Serena', 'Andrew', 'Bobbie', 'Cason', 'David', 'Farzana', 'Frank', 'Hannah', 'Ida', 'Irene', 'Jim', 'Jose', 'Keith', 'Laura', 'Lucy', 'Red', 'Meredith', 'Nick', 'Ada', 'Yeeling', 'Yan'}
        self.nouns = {'language', 'weight', 'bed', 'heat', 'shape', 'game', 'check', 'thousand', 'age', 'plane', 'gold', 'boat', 'record', 'test', 'foot', 'island', 'moon', 'surface', 'object', 'fact', 'street', 'inch', 'it', 'you', 'he', 'yes', 'no', 'wheel', 'machine', 'unit', 'note', 'noun', 'children', 'field', 'star', 'box', 'science', 'map', 'road', 'love', 'person', 'money', 'center', 'I', 'his', 'they', 'we', 'sleep', 'minute', 'front', 'cry', 'lead', 'sun', 'cover', 'food', 'plant', 'girl', 'dark', 'fly', 'fine', 'power', 'town', 'fall', 'voice', 'notice', 'cold', 'pull', 'rule', 'road', 'serve', 'pattern', 'war', 'vowel', 'several', 'morning', 'table', 'reach', 'interest', 'ground', 'hold', 'step', 'hour', 'size', 'king', 'whole', 'top', 'farm', 'force', 'stay', 'course', 'lot', 'produce', 'tail', 'behind', 'mind', 'quick', 'final', 'week', 'drive', 'beauty', 'pound', 'rest', 'figure', 'pass', 'order', 'fire', 'piece', 'problem', 'rock', 'half', 'area', 'ship', 'question', 'wind', 'class', 'numeral', 'family', 'dog', 'body', 'bird', 'product', 'state', 'song', 'pose', 'leave', 'talk', 'list', 'wood', 'face', 'color', 'watch', 'adults', 'cut', 'horse', 'base', 'mountain', 'fish', 'idea', 'friend', 'room', 'rain', 'group', 'second', 'care', 'feet', 'him', 'her', 'car', 'river', 'mile', 'letter', 'book', 'mark', 'music', 'paper', 'ease', 'example', 'children', 'stop', 'life', 'night', 'press', 'while', 'run', 'sea', 'saw', 'story', 'start', 'tree', 'city', 'door', 'last', 'eye', 'thought', 'answer', 'school', 'country', 'page', 'head', 'father', 'mother', 'earth', 'self', 'light', 'world', 'animal', 'short', 'point', 'us', 'try', 'picture', 'house', 'need', 'change', 'man', 'men', 'act', 'here', 'land', 'port', 'hand', 'home', 'end', 'play', 'well', 'she', 'he', 'they', 'air', 'set', 'sentence', 'boy', 'turn', 'line', 'help', 'our', 'me', 'show', 'name', 'year', 'form', 'back', 'place', 'take', 'work', 'part', 'this', 'can', 'word', 'each', 'she', 'them', 'time', 'snow', 'way', 'thing', 'look', 'day', 'sound', 'number', 'water', 'call', 'first', 'people', 'side', 'many', 'blue', 'red', 'green', 'white', 'black'}

        self.verbs = {'fill', 'sit', 'bring', 'brought', 'miss', 'heat', 'cool', 'ran', 'laugh', 'wonder', 'dry', 'age', 'record', 'test', 'decide', 'object', 'is', 'was', 'full', 'field', 'wait', 'plan', 'correct', 'map', 'love', 'center', 'warm', 'sleep', 'free', 'front', 'teach', 'contain', 'cry', 'lead', 'cover', 'plant', 'fly', 'fine', 'power', 'fall', 'voice', 'notice', 'pull', 'govern', 'rule', 'appear', 'serve', 'slow', 'lay', 'travel', 'listen', 'sing', 'reach', 'interest', 'ground', 'hold', 'step', 'remember', 'am', 'better', 'best', 'heard', 'force', 'stay', 'produce', 'clear', 'mind', 'develop', 'gave', 'stood', 'drive', 'pound', 'rest', 'figure', 'pass', 'knew', 'told', 'order', 'fire', 'rock', 'half', 'ship', 'complete', 'happen', 'question', 'wind', 'direct', 'state', 'measure', 'pose', 'leave', 'talk', 'feel', 'list', 'ready', 'face', 'color', 'watch', 'cut', 'hear', 'base', 'fish', 'began', 'eat', 'rain', 'took', 'carry', 'group', 'care', 'book', 'ease', 'mark', 'walk', 'got', 'begin', 'seem', 'open', 'stop', 'close', 'press', 'run', 'draw', 'saw', 'might', 'start', 'cross', 'last', 'keep', 'let', 'thought', 'learn', 'study', 'grow', 'answer', 'found', 'should', 'own', 'stand', 'build', 'point', 'try', 'picture', 'need', 'went', 'change', 'ask', 'act', 'follow', 'must', 'land', 'add', 'spell', 'read', 'put', 'end', 'play', 'want', 'set', 'tell', 'does', 'move', 'differ', 'cause', 'turn', 'help', 'say', 'think', 'show', 'form', 'give', 'came', 'live', 'made', 'place', 'get', 'take', 'work', 'part', 'are', 'be', 'have', 'had', 'can', 'were', 'use', 'said', 'do', 'time', 'would', 'write', 'like', 'see', 'has', 'look', 'more', 'could', 'go', 'come', 'did', 'know', 'call', 'may', 'been', 'find'}

        self.adjectives = {'cool', 'hundred', 'thousand', 'dry', 'possible', 'common', 'busy', 'deep', 'blue', 'inch', 'green', 'red', 'warm', 'minute', 'strong', 'free', 'front', 'lead', 'cover', 'white', 'plain', 'young', 'dark', 'fly', 'certain', 'fine', 'cold', 'slow', 'toward', 'simple', 'fast', 'ground', 'early', 'true', 'better', 'best', 'whole', 'top', 'a lot', 'clear', 'special', 'quick', 'final', 'done', 'able', 'half', 'complete', 'class', 'short', 'black', 'direct', 'soon', 'ever', 'above', 'ready', 'usual', 'main', 'wood', 'color', 'sure', 'cut', 'base', 'second', 'next', 'together', 'open', 'few', 'real', 'close', 'late', 'left', 'hard', 'cross', 'last', 'still', 'own', 'head', 'near', 'big', 'high', 'light', 'off', 'kind', 'such', 'land', 'even', 'large', 'small', 'well', 'old', 'right', 'mean', 'same', 'low', 'great', 'much', 'good', 'just', 'through', 'round', 'only', 'little', 'back', 'live', 'part', 'new', 'any', 'hot', 'some', 'many', 'like', 'so', 'long', 'make', 'more', 'my', 'sound', 'most', 'over', 'first', 'down', 'now'}

        self.adverbs = {'yes', 'no', 'full', 'that', 'strong', 'free', 'fine', 'cold', 'slow', 'several', 'less', 'fast', 'early', 'better', 'best', 'whole', 'top', 'nothing', 'clear', 'behind', 'quick', 'south', 'half', 'soon', 'though', 'ever', 'above', 'enough', 'once', 'always', 'often', 'next', 'together', 'late', 'left', 'hard', 'since', 'last', 'never', 'still', 'near', 'again', 'off', 'even', 'also', 'well', 'too', 'before', 'just', 'through', 'very', 'under', 'only', 'after', 'live', 'part', 'new', 'by', 'out', 'other', 'all', 'up', 'about', 'so', 'first', 'now'}

        self.locations = {'north', 'east', 'west', 'in', 'center', 'on', 'front', 'ground', 'top', 'behind', 'south', 'above', 'base', 'between', 'here', 'end', 'under', 'back', 'mountain', 'there', 'up', 'down', 'side', 'school', 'farm'}

        self.numbers = {'one', 'two', 'three', 'four', 'five', 'six', 'ten'}

        self.others = {'against', 'oh', 'for', 'until', 'yet', 'ago', 'perhaps', 'among', 'the', 'of', 'to', 'and', 'a', 'don\'t', 'why', 'these', 'her', 'him', 'who', 'than', 'what', 'your', 'when', 'how', 'an', 'which', 'their', 'if', 'then', 'at', 'every', 'from', 'or', 'but', 'with', 'as', 'where', 'between'}

    def solve(self, sentence, question):
        # Tokenize the sentence and question
        sentence_tokens = sentence.split()
        question_tokens = question.split()

        # Remove punctuation from the last token
        sentence_tokens[-1] = sentence_tokens[-1].rstrip('.')
        question_tokens[-1] = question_tokens[-1].rstrip('?')

        # Initialize answer
        answer = None
        ans_type = None

        # Handle different types of questions.
        if 'Who' in question_tokens:
            for token in sentence_tokens:
                # Answer is a name in the sentence
                if (token in self.names) and (token not in question_tokens):
                    answer = token
                    break
                elif (token not in self.names) and (token in self.nouns) and (token not in self.adjectives) and (token not in question_tokens):
                    answer = token
                    break

        # What color? What did they do? What kind?
        # --> Adj or verb or noun
        elif 'What' in question_tokens:
            word_after_q = question_tokens[1]

            if (word_after_q == 'kind') or (word_after_q == 'will'):
                ans_type = 'ADJ'
            elif 'name' in question:
                ans_type = 'NAME'
            else:
                ans_type = 'NOUN'

            for token in sentence_tokens:
                if (ans_type == 'NOUN'):
                    if (token in self.nouns) and not (token in self.verbs or token in self.adjectives) and (token not in question_tokens):
                        answer = token
                        break
                    elif (token in self.nouns):
                        answer = token
                elif (ans_type == 'NAME'):
                    if (token in self.names) and (token not in question_tokens):
                        answer = token
                        break
                else:
                    if (token in self.adjectives) and (token not in question_tokens):
                        answer = token
                        break
                    if (token in self.verbs) and (token not in question_tokens):
                        answer = token
                        break

        
        # Noun or location
        # Where is Suzy? At school.
        elif 'Where' in question_tokens:
            word_after_q = question_tokens[1]
            if (word_after_q == 'do') or (word_after_q == 'is'):
                ans_type = 'loc'

            for token in sentence_tokens:
                if (ans_type == 'loc'):
                    if (token in self.locations) and (token not in question_tokens):
                        answer = token
                        break
                else:
                    if (token in self.nouns) and (token not in self.verbs) and (token not in question_tokens):
                        answer = token
                        break
        
        elif 'When' in question_tokens:
            for token in sentence_tokens:
                if (token in self.nouns) and (token not in self.verbs) and (token not in question_tokens):
                    answer = token
                    break

        # Questions like: 'How many? How long? How far? How do they do that?'
        # Adverb, adj, noun, verb
        elif 'How' in question_tokens:
            word_after_q = question_tokens[1]

            if (word_after_q in self.nouns):
                ans_type = 'ADJ'
            elif (word_after_q in self.adjectives):
                ans_type = 'ADJ'
            elif (word_after_q in self.verbs):
                ans_type = 'VERB'
            elif (word_after_q in self.adverbs):
                ans_type = 'ADJ'
            elif (word_after_q == 'many'):
                ans_type = 'NUM'
            else: # Return noun or verb
                ans_type = 'NOUN'

            for token in sentence_tokens:
                if (ans_type == 'NOUN') and (token in self.nouns):
                    answer = token
                    break
                elif (ans_type == 'VERB') and (token in self.verbs):
                    answer = token
                    break
                elif (ans_type == 'ADJ') and (token in self.adjectives):
                    answer = token
                    break
                elif (ans_type == 'NUM') and (token in self.numbers):
                    answer = token
                    break
                else:
                    answer = token
        
        # Questions like: 'At what time?'
        elif 'At' in question_tokens:
            # Iterate over each sentence token
            for token in sentence_tokens:
                # Determine if token is a valid time
                if self.is_valid_clock_time(token):
                    answer = token
                    break

        # If an answer was found, return it; otherwise, return 'None.'
        return answer if answer else 'None'

    '''
    Method to determine whether a token is a valid clock time.
    '''
    def is_valid_clock_time(self, token):
        # Define a regular expression pattern for valid clock times
        clock_time_pattern = r'^[0-1]?[0-9]:[0-5][0-9](AM|PM)?$'
        
        # Use re.match to check if the token matches the pattern
        if re.match(clock_time_pattern, token):
            return True
        return False