import json
import pickle
import random

import numpy as np
import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Dense, Dropout, Input
from tensorflow.keras.models import Sequential

from myapp.chatbot_service import CLASSES_PATH, INTENTS_PATH, MODEL_PATHS, WORDS_PATH, tokenize

SEED = 42
random.seed(SEED)
np.random.seed(SEED)
tf.random.set_seed(SEED)


def build_training_data():
    intents = json.loads(INTENTS_PATH.read_text(encoding="utf-8"))

    words = []
    classes = []
    documents = []

    for intent in intents["intents"]:
        tag = intent["tag"]

        for pattern in intent.get("patterns", []):
            tokens = tokenize(pattern)
            if not tokens:
                continue
            if tag not in classes:
                classes.append(tag)
            words.extend(tokens)
            documents.append((tokens, tag))

    words = sorted(set(words))
    classes = sorted(set(classes))

    training_x = []
    training_y = []

    for tokens, tag in documents:
        token_set = set(tokens)
        training_x.append([1 if word in token_set else 0 for word in words])

        output_row = [0] * len(classes)
        output_row[classes.index(tag)] = 1
        training_y.append(output_row)

    return (
        intents,
        words,
        classes,
        np.array(training_x, dtype=np.float32),
        np.array(training_y, dtype=np.float32),
    )


def create_model(input_size: int, output_size: int) -> Sequential:
    model = Sequential(
        [
            Input(shape=(input_size,)),
            Dense(128, activation="relu"),
            Dropout(0.35),
            Dense(64, activation="relu"),
            Dropout(0.25),
            Dense(output_size, activation="softmax"),
        ]
    )
    model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
    return model


def main():
    _, words, classes, train_x, train_y = build_training_data()

    if train_x.size == 0 or train_y.size == 0:
        raise ValueError("No training data could be created from intents.json.")

    with WORDS_PATH.open("wb") as words_handle:
        pickle.dump(words, words_handle)

    with CLASSES_PATH.open("wb") as classes_handle:
        pickle.dump(classes, classes_handle)

    model = create_model(train_x.shape[1], train_y.shape[1])
    callbacks = [
        EarlyStopping(
            monitor="loss",
            patience=20,
            restore_best_weights=True,
        )
    ]

    model.fit(
        train_x,
        train_y,
        epochs=300,
        batch_size=min(8, len(train_x)),
        verbose=0,
        callbacks=callbacks,
    )

    loss, accuracy = model.evaluate(train_x, train_y, verbose=0)
    model.save(MODEL_PATHS[-1])

    print(f"Saved vocabulary to {WORDS_PATH.name}")
    print(f"Saved classes to {CLASSES_PATH.name}")
    print(f"Saved model to {MODEL_PATHS[-1].name}")
    print(f"Training accuracy: {accuracy:.3f}")
    print(f"Training loss: {loss:.3f}")


if __name__ == "__main__":
    main()
