import fasttext
import os
from fasttext import train_supervised
import sys


def create_model():
    training_file_name = sys.argv[1]
    # input=os.path.join(os.path.dirname(
    # os.path.abspath(__file__)), training_file_name),
    model = train_supervised(
        input=os.path.join(
            './resources/classifier_model', training_file_name),
        epoch=5, lr=1.0,
        wordNgrams=2,
        verbose=2,
        minCount=1,
        loss="softmax"
    )
    model.save_model(os.path.join(
        './resources/classifier_model', 'fast_text_model.bin'))


if __name__ == '__main__':
    create_model()
