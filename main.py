import json
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder

# load intent file for the first time
with open('data/intents.json') as file:
    data = json.load(file)

training_sentences = []
training_labels = []
labels = []
responses = []

for intent in data['intents']:
    for pattern in intent['patterns']:
        training_sentences.append(pattern)
        training_labels.append(intent['tag'])
    responses.append(intent['responses'])

    if intent['tag'] not in labels:
        labels.append(intent['tag'])

enc = LabelEncoder()
enc.fit(training_labels)
training_labels = enc.transform(training_labels)

vocab_size = 10000
embedding_dim = 16
max_len = 20
trunc_type = 'post'
oov_token = "<OOV>"

tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_token)  # adding out of vocabulary token
tokenizer.fit_on_texts(training_sentences)
word_index = tokenizer.word_index
sequences = tokenizer.texts_to_sequences(training_sentences)
padded = pad_sequences(sequences, truncating=trunc_type, maxlen=max_len)
classes = len(labels)

model = tf.keras.models.Sequential()
model.add(keras.layers.Embedding(vocab_size, embedding_dim, input_length=max_len))
model.add(keras.layers.GlobalAveragePooling1D())
model.add(keras.layers.Dense(16, activation='relu'))
model.add(keras.layers.Dense(16, activation='relu'))
model.add(keras.layers.Dense(classes, activation='softmax'))

training_labels_final = np.array(training_labels)
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

try:
    model = keras.models.load_model("data/final_model.h5")
except:
    model.fit(padded, training_labels_final, epochs=300)
    model.save("data/final_model.h5")

def bot_response(input):
    inp = input
    if inp == 'quit':
        exit()
    result = model.predict(pad_sequences(tokenizer.texts_to_sequences([inp]),
                                         truncating=trunc_type, maxlen=max_len))[0]
    category = enc.inverse_transform([np.argmax(result)])

    if result[np.argmax(result)] > 0.5:
        for i in data['intents']:
            if i['tag'] == category:
                return np.random.choice(i['responses'])
    else:
        return "Please try a different sentence!"