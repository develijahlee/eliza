import nltk
import random
import string
from nltk.corpus import wordnet as wn
from nltk import pos_tag
import re

start_chat = ["Hello. How are you feeling today?",
              "Hi there, welcome to my office. I'm here to chat about anything. What's on your mind?",
              "How do you do. Please tell me your problem.", "Please tell me what's been bothering you.",
              "Is something troubling you?", "Hello. How are you doing today?"]


def chat(user_input):
    lemmatizer = nltk.stem.WordNetLemmatizer()

    responses = {
        "him": {
            "weight": 0,
            "grammar": "VB",
            "responses": ["This is a test *"]
        },
        "NOTFOUND": {
            "weight": 0,
            "responses": [
                "What does that suggest to you?",
                "I see.",
                "I'm not sure I understand you fully.",
                "Can you elaborate?",
                "That is quite interesting.",
                "Please tell me more.",
                "Let's change focus a bit... Tell me about your family.",
                "Can you elaborate on that?",
                "Why do you say that?"
            ]
        },
        "sorry": {
            "weight": 1,
            "responses": ["Please don't apologize.", "Apologies are not necessary.", "Apologies are not required."]
        },
        "always": {
            "weight": 2,
            "responses": ["Can you think of a specific example?"]
        },
        "because": {
            "weight": 3,
            "responses": ["Is that the real reason?"]
        },
        "maybe": {
            "weight": 4,
            "responses": ["You don't seem very certain."]
        },
        "think": {
            "weight": 5,
            "responses": ["Do you really think so?"]
        },
        "you": {
            "weight": 6,
            "responses": ["Why do you care whether I *?"],
            "grammar": "VB"
        },
        "yes": {
            "weight": 7,
            "responses": ["Why do you think so?", "You seem quite positive."]
        },
        "no": {
            "weight": 8,
            "responses": ["Why not?", "Are you sure?"]
        },
        "am": {
            "weight": 9,
            "responses": ["I am sorry to hear you are *.", "How long have you been *?",
                          "Do you believe it is normal to be *?", "Do you enjoy being *?",
                          "Did you come to me because you are *?"],
            "grammar": "JJ"
        },
        "feel": {
            "weight": 10,
            "responses": ["Tell me more about such feelings."]
        },
        "family": {
            "weight": 11,
            "responses": ["Tell me more about your family.", "How do you get along with your family?",
                          "Is your family important to you?"]
        },
        "mother": {
            "weight": 12,
            "responses": ["Tell me more about your mother."]
        },
        "father": {
            "weight": 13,
            "responses": ["Tell me more about your father."]
        },
        "mom": {
            "weight": 14,
            "responses": ["Tell me more about your mom."]
        },
        "sister": {
            "weight": 15,
            "responses": ["Tell me more about your sister."]
        },
        "brother": {
            "weight": 16,
            "responses": ["Tell me more about your brother."]
        },
        "husband": {
            "weight": 17,
            "responses": ["Tell me more about your family.", "How do you get along with your family?",
                          "Is your family important to you?"]
        },
        "wife": {
            "weight": 18,
            "responses": ["Tell me more about your wife."]
        },
        "child": {
            "weight": 19,
            "responses": ["Did you have close friends as a child?", "What is your favorite childhood memory?",
                          "Do you remember any dreams or nightmares from childhood?",
                          "Did the other children sometimes tease you?",
                          "How do you think your childhood experiences relate to your feelings today?"]
        },
        "dream": {
            "weight": 20,
            "responses": ["What does that dream suggest to you?", "Do you dream often?",
                          "What people appear in your dreams?", "Are you disturbed by your dreams?",
                          "Have you ever fantasized * while you were awake?"]
        },
        "nightmare": {
            "weight": 21,
            "responses": ["What does that nightmare suggest to you?"]
        },
        "hello": {
            "weight": 22,
            "responses": ["Hello, how is it going?", "How are you today? Any problems?"]
        },
        "afternoon": {
            "weight": 23,
            "responses": ["Afternoon!"]
        },
        "morning": {
            "weight": 24,
            "responses": ["And a good morning to you too!"]
        },
        "hi": {
            "weight": 25,
            "responses": ["Hi, how is it going?"]
        },
        "goodbye": {
            "weight": 26,
            "responses": ["Goodbye. Thank you for talking to me."]
        },
        "need": {
            "weight": 27,
            "responses": ["Why do you need *?", "Would it really help you to get *?", "Are you sure you need *?"],
            "grammar": "NN"
        },
        "don't": {
            "weight": 28,
            "responses": ["Do you really think I don't *?", "Perhaps eventually I will *.",
                          "Do you really want me to *?"],
            "grammar": "VB"
        },
        "can't": {
            "weight": 29,
            "responses": ["Do you think you should be able to *?", "If you could *, what would you do?",
                          "I don't know -- why can't you *?", "Have you really tried?"],
            "grammar": "VB"
        },
        "remember": {
            "weight": 32,
            "responses": ["Do you often think of *?", "Does thinking of * bring anything else to mind",
                          "What else do you recollect?", "Why do you recollect * just now?",
                          "What in the present situation reminds you of *?",
                          "What is the connection between me and *?"],
            "grammar": "NN"
        },
        "name": {
            "weight": 35,
            "responses": ["I am not interested in names.",
                          "I\'ve told you before, I do not care about names -- please continue."]
        },
        "computer": {
            "weight": 37,
            "responses": ["Do computers worry you?", "Why do you mention computers?",
                          "Could you expand on how computers and * are related?",
                          "What do you think machines have to do with your problem?",
                          "Don't you think computers can help people?", "What about machines worries you?",
                          "What do you think about machines?"],
            "grammar": "NN"
        },
        "are": {
            "weight": 39,
            "responses": ["Did you think they might not be *?", "Would you like it if they were not *?",
                          "What if they were not *?", "Possibly they are *."],
            "grammar": "JJ"
        },
        "your": {
            "weight": 40,
            "responses": ["Why are you concerned over my *?", "What about your own *?",
                          "Are you worried about someone else's *?", "Really, my *?"],
            "grammar": "NN"
        },
        "was": {
            "weight": 41,
            "responses": ["What does * suggest to you?"],
            "grammar": "JJ"
        },
        "sad": {
            "weight": 45,
            "responses": ["Sorry to hear you are sad. Tell me about it."]
        },
        "happy": {
            "weight": 46,
            "responses": ["What is making you happy?"]
        },
        "bored": {
            "weight": 47,
            "responses": ["What makes you bored?"]
        }
    }

    end_chat = ["Goodbye :)", "I have to leave ):"]

    # user_input = input("ELIZA: " + random.choice(start_chat) + ' ')
    continue_chat = True

    # check if a synonym is in responses
    def synonyms(token):
        synsets = wn.synsets(token)
        for syn in synsets:
            syn_list = syn.lemma_names()
            for word in syn_list:
                if word in responses:
                    return word

    # replace * in responses with unused words
    def pos(all_words):
        pos_list = []
        for pos in pos_tag(all_words):
            pos_list.append(pos)
        print('pos_list', pos_list)
        grammar_exists = False
        # If known_words is not empty and the last known_word has a grammar
        if len(known_words) > 0 and "grammar" in sorted(known_words, key=lambda item: item['weight'])[-1]:
            grammar = sorted(known_words, key=lambda item: item['weight'])[-1]["grammar"]
            print('grammar in known_words:', grammar)
            grammar_exists = True
        else:
            grammar = ''
        chunking(pos_list)
        if len(pos_list) > 0:
            for word in pos_list:
                # ex: pos_list [('you', 'PRP'), ('think', 'VBP')] and "you" in responses has a grammar key of "VB"
                if grammar in word[1] and grammar != '' and word[0] != 'i':
                    print('word[1]', word[1])
                    print('grammar:', grammar)
                    # if there is no grammar key in any word[1], the first word is returned. Why?
                    return word[0]
                else:
                    # keep looking for matching response grammar key
                    continue
            # if matching response grammar key does exist, return 'NOT_FOUND'. Ex) "you"
            if grammar_exists:
                return 'NOT_FOUND'
            # if matching response grammar key does not exist, return 'X'. Ex) "mother"
            else:
                return 'X'
        else:
            return 'NOT_FOUND'

    # organize user input into noun phrases
    def chunking(sentence):
        grammar = """NP: {<DT>?<JJ>*<NN>}
        VBD: {<VBD>}
        IN: {<IN>}"""
        NPchunker = nltk.RegexpParser(grammar)
        result = NPchunker.parse(sentence)
        print("chunking", list(traverse_tree(result, 2)))
        return list(traverse_tree(result, 2))

    def traverse_tree(tree, depth=float('inf')):
        """
        Traversing the Tree depth-first,
        yield leaves up to `depth` level.
        """
        for subtree in tree:
            if type(subtree) == nltk.tree.Tree:
                if subtree.height() <= depth:
                    yield subtree.leaves()
                    traverse_tree(subtree)

    while continue_chat:
        all_words = []
        unknown_words = []
        known_words = []
        # Check if there is a prepared response for each unique word user enters
        for word in user_input.split():
            # make every user input word lowercase and delete all punctuation
            clean_word = word.lower().strip(string.punctuation)
            all_words.append(clean_word)
            # lemmatizer requires the correct POS tag, the default tag is noun
            # token = lemmatizer.lemmatize(clean_word)
            token = clean_word
            # For words like "you" that have no synonyms but are in responses
            if token in responses:
                # For words in responses that have a grammar key
                if "grammar" in responses[token]:
                    known_words.append(
                        {"word": token, "weight": responses[token]["weight"], "grammar": responses[token]["grammar"]})
                # For words in responses that don't have a grammar key
                else:
                    known_words.append({"word": token, "weight": responses[token]["weight"]})
            # For words like "mommmy" that have a synonym of "mom" in responses
            elif synonyms(token) is not None:
                found_word = synonyms(token)
                known_words.append({"word": found_word, "weight": responses[found_word]["weight"]})
            # For words like "walmart" that have no synonyms and are not in responses
            else:
                unknown_words.append(clean_word)
        # Debugging
        print('all_words:', all_words)
        print('known_words:', sorted(known_words, key=lambda item: item['weight']))
        print('unknown_words:', unknown_words)
        # Store replacement word
        replace_word = pos(all_words)
        print('replace_word:', replace_word)
        # Respond with the highest weight response. If there is no prepared response, end chat.
        if len(known_words) > 0:
            highest_weight = sorted(known_words, key=lambda item: item['weight'])[-1]["word"]
            response = random.choice(list(responses[highest_weight]["responses"]))
            # If replace_word is not found
            if replace_word == "NOT_FOUND":
                response = random.choice(list(responses["NOTFOUND"]["responses"]))
                print('random response', response)
                return 'ELIZA: ' + response
            # Replace * with replacement word if * is in response
            elif re.search(r'\*', response):
                print(re.sub(r'\*', replace_word, response))
                return 'ELIZA: ' + re.sub(r'\*', replace_word, response)
            else:
                print(response)
                return 'ELIZA: ' + response
            # user_input = input('ELIZA: Talk to me again: ')
        else:
            continue_chat = False
    print("ELIZA: " + random.choice(end_chat) + ' ')
    return "ELIZA: " + random.choice(end_chat) + ' '

# TODO
# debug "I can't be sure"
# lemmatizer does not work
# hypernyms hyponyms?
# do I even need chunking?
