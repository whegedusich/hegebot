# Author: Wm Hegedusich
# Created: 07/23/2020

import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Dense, GRU

base_dir = '/home/william/PycharmProjects/hegebot'
checkpoint_dir = f'{base_dir}/training_checkpoints'
checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt_{epoch}")

seq_length = 100
BATCH_SIZE = 64
'''
Buffer size to shuffle the dataset
(TF data is designed to work with possibly infinite sequences,
so it doesn't attempt to shuffle the entire sequence in memory. Instead,
it maintains a buffer in which it shuffles elements).
'''
BUFFER_SIZE = 10000
EPOCHS = 10


def get_vocab():
    with open(f'{base_dir}/text.txt', 'r') as f:
        corpus = f.read()

    # Vocab is set of unique characters in body of text
    v = sorted(set(corpus))

    # Create mapping of chars to nums, and vice versa
    c2i = {u: i for i, u in enumerate(v)}
    i2c = np.array(v)

    return corpus, v, c2i, i2c


def split_input_target(chunk):
    input_text = chunk[:-1]
    target_text = chunk[1:]

    return input_text, target_text


def build_model(vocab_size, embedding_dim, rnn_units, batch_size):
    m = Sequential([
        Embedding(vocab_size, embedding_dim, batch_input_shape=[batch_size, None]),
        GRU(rnn_units, return_sequences=True, stateful=True, recurrent_initializer='glorot_uniform'),
        Dense(vocab_size)]
    )

    return m


def loss(labels, logits):
    return tf.keras.losses.sparse_categorical_crossentropy(labels, logits, from_logits=True)


def generate_text(m, start_string):
    # Evaluation step (generating text using the learned model)

    # Number of characters to generate
    num_generate = 280

    # Converting our start string to numbers (vectorizing)
    input_eval = [char2idx[s] for s in start_string]
    input_eval = tf.expand_dims(input_eval, 0)

    # Empty string to store our results
    text_generated = []

    # Low temperatures results in more predictable text.
    # Higher temperatures results in more surprising text.
    # Experiment to find the best setting.
    temperature = 1.0

    # Here batch size == 1
    m.reset_states()
    for i in range(num_generate):
        predictions = m(input_eval)
        # remove the batch dimension
        predictions = tf.squeeze(predictions, 0)

        # using a categorical distribution to predict the character returned by the model
        predictions = predictions / temperature
        predicted_id = tf.random.categorical(predictions, num_samples=1)[-1, 0].numpy()

        # We pass the predicted character as the next input to the model
        # along with the previous hidden state
        input_eval = tf.expand_dims([predicted_id], 0)

        text_generated.append(idx2char[predicted_id])

    return start_string + ''.join(text_generated)


if __name__ == '__main__':
    text, vocab, char2idx, idx2char = get_vocab()
    # Map text to integer representation
    text_as_int = np.array([char2idx[c] for c in text])

    ex_per_epoch = len(text) // (seq_length + 1)
    # convert the text vector into a stream of character indices.
    char_dataset = tf.data.Dataset.from_tensor_slices(text_as_int)

    # convert these individual characters to sequences of the desired size.
    sequences = char_dataset.batch(seq_length + 1, drop_remainder=True)

    dataset = sequences.map(split_input_target)
    dataset = dataset.shuffle(BUFFER_SIZE).batch(BATCH_SIZE, drop_remainder=True)

    model = build_model(vocab_size=len(vocab),
                        embedding_dim=256,
                        rnn_units=1024,
                        batch_size=BATCH_SIZE)

    model.compile(optimizer='adam', loss=loss)

    checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_prefix, save_weights_only=True)

    history = model.fit(dataset, epochs=EPOCHS, callbacks=[checkpoint_callback])

    model = build_model(vocab_size=len(vocab), embedding_dim=256, rnn_units=1024, batch_size=1)
    model.load_weights(tf.train.latest_checkpoint(checkpoint_dir))
    model.build(tf.TensorShape([1, None]))

    print(generate_text(model, start_string='T'))
