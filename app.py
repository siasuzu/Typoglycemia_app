from flask import Flask, render_template, request
import re
import random
from janome.tokenizer import Tokenizer
import pykakasi

app = Flask(__name__)

t = Tokenizer()

# Kanji and Katakana to Hiragana conversion
def kanji_katakana_to_hiragana(text):
    kks = pykakasi.kakasi()
    result = []
    for word in text.split():
        converted_word = kks.convert(word)
        hiragana_word = "".join([item['hira'] for item in converted_word])
        result.append(hiragana_word)
    return " ".join(result)

# # Text splitting by particles and auxiliaries
def split_by_particle_and_auxiliary(text):
    result = []
    tokens = t.tokenize(text)
    prev_token = None

    for token in tokens:
        surface = token.surface
        part_of_speech = token.part_of_speech.split(',')[0]
        if prev_token and prev_token.part_of_speech.split(',')[0] == '動詞' and part_of_speech == '名詞':
            result.append(" ")
        if prev_token and prev_token.part_of_speech.split(',')[0] == '形容詞' and part_of_speech in ('名詞', '動詞', '副詞'):
            result[-1] += surface
        elif part_of_speech == '助詞':
            result.append(" ")
            result.append(surface)
            result.append(" ")
        elif part_of_speech == '記号':
            result.append(" ")
            result.append(surface)
            result.append(" ")
        elif part_of_speech == '助動詞':
            result.append(" ")
            result.append(surface)
            result.append(" ")
        elif part_of_speech == '副詞':
            result.append(" ")
            result.append(surface)
            result.append(" ")
        elif part_of_speech == '連体詞':
            result.append(" ")
            result.append(surface)
            result.append(" ")
        elif part_of_speech == '形容詞':
            result.append(" ")
            result.append(surface)
            result.append(" ")
        elif part_of_speech == '助動詞' and prev_token and prev_token.part_of_speech.split(',')[0] == '助動詞':
            result[-1] += surface
        else:
            result.append(surface)
        prev_token = token

    return "".join(result)



# Shuffling long words
def shuffle_long_words(text):
    words = text.split()
    shuffled_words = []
    for word in words:
        if len(word) >= 4:
            first_char = word[0]
            last_char = word[-1]
            middle_chars = list(word[1:-1])
            while True:
                random.shuffle(middle_chars)
                shuffled_word = first_char + "".join(middle_chars) + last_char
                if shuffled_word != word:
                    break
            shuffled_words.append(shuffled_word)
        else:
            shuffled_words.append(word)
    return " ".join(shuffled_words)

# Removing consecutive spaces
def remove_consecutive_spaces(text):
    return re.sub(' +', ' ', text)

# Main Typoglycemia function
def Typoglycemia(text):
    split_text = split_by_particle_and_auxiliary(text)
    split_text_hiragana = kanji_katakana_to_hiragana(split_text)
    shuffled_text = shuffle_long_words(split_text_hiragana)
    Typoglycemia_text = remove_consecutive_spaces(shuffled_text)
    return Typoglycemia_text

# Route definitions
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        input_text = request.form["text"]
        output_text = Typoglycemia(input_text)
        return render_template("result.html",input_text=input_text ,output_text=output_text)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

