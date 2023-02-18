import sys 
import os
import nltk
# import ssl

# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context
    
nltk.download('book')
from nltk.book import *
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob
from random import randint

def read_file(filepath):
    with open(os.path.join(os.getcwd(), filepath), 'r') as f:
        text_in = f.read().split()
    return text_in


def preprocess(data):    
    # 2: calculate lexical diversity
    tokens = [t.lower() for t in data if t.isalpha()]
    unique_tokens = set(tokens)
    print("\nLexical diversity: %.2f" % (len(unique_tokens) / len(tokens))) # lexical diversity
    
    # 3a: tokenize to lowercase, only alpha, not in stopwords, and greater than 5 letters
    tokens = [t.lower() for t in tokens if t not in stopwords.words('english') and len(t) > 5]
    
    # 3b: get the lemmas and use set to make unique
    wnl = WordNetLemmatizer()
    lemmas = [wnl.lemmatize(t) for t in tokens]
    lemmas_unique = list(set(lemmas))
    print("\nThe number of unique lemmas in data: ", len(lemmas_unique))
    
    # 3c: do pos tagging and load a model
    s = ' '.join(lemmas_unique)
    
    blob = TextBlob(s)
    print("\nFirst 20 tagged: ", blob.tags[:20])
    blob_nouns = [word for word, tag in blob.tags if tag == "NN"]

    # 3d: print num of tokens and num of nouns
    print("\nThe number of tokens: ", len(tokens))
    print("The number of nouns: ", len(blob_nouns))   
    
    return tokens, blob_nouns


def create_dict(tokens, nouns_lemmas):
    # make a dictionary of counts
    counts = {}
    for item in tokens:
        if item not in nouns_lemmas:
            continue
        if item in counts:
            counts[item] += 1
        else:
            counts[item] = 1
    # print 50 most common words
    # dicts are unordered so we sort it and put it in a list of tuples
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    print("\n50 most common words:")
    for i in range(50):
        print(sorted_counts[i])
    nouns_list = [sorted_counts[i][0] for i in range(50)]
    return nouns_list


def get_word_output(nouns_list):
    index = randint(0, 49)
    word = nouns_list[index]
    output = '_' * len(word)
    return word, output


def get_new_output(word, letter, output):
    indices = [i for i, c in enumerate(word) if c == letter]
    new_output = ""
    
    for i, c in enumerate(output):
        if i in indices:
            new_output += letter
        else:
            new_output += c
    return new_output


def guessing_game(nouns_list):
    user_score = 5
    word, output = get_word_output(nouns_list)
    print(output)
    
    while True:
        # if user guesses all letters from word
        if output == word:
            print("\nGood Job! New word~")
            word, output = get_word_output(nouns_list)
            print(output)
        
        # user inputs same letter from board
        while True:
            letter = input("\nGuess a letter:")
            if letter not in output:
                break
        
        # user inputs "!"
        if letter == '!':
            print("\nFinal score: ", user_score)
            break
            
        # if guessed right, replaces output to include letter
        if letter in word:    
            output = get_new_output(word, letter, output)
            user_score += 1
            print("Right! Score is: ", user_score)
            print(output)
            
        else:
            user_score -= 1
            if user_score < 0:
                print("game over")
                print("Word was ", word)
                print("Final score: ", user_score)
                break
            else:
                print("Sorry, guess again. Score is:", user_score)
                
        
            
            
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please enter a filename as a system arg')
    else:
        fp = sys.argv[1]
        data = read_file(fp)
        tokens, nouns_lemmas = preprocess(data)
        nouns_list = create_dict(tokens, nouns_lemmas)
        print("\nLet's play a word guessing game!")
        guessing_game(nouns_list)
        