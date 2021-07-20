import fasttext
import os
from fasttext import train_supervised
from flask import current_app


class FastTextModelComponent():
    def __init__(self):
        ""

    def create_model(self, training_file_name):
        # input=os.path.join(os.path.dirname(
        # os.path.abspath(__file__)), training_file_name),
        model = train_supervised(
            input=os.path.join(
                current_app.config['CLASSIFIER_MODEL'], training_file_name),
            epoch=5, lr=1.0,
            wordNgrams=2,
            verbose=2,
            minCount=1,
            loss="softmax"
        )
        model.save_model(os.path.join(
            current_app.config['CLASSIFIER_MODEL'], 'fast_text_model.bin'))

    def load_model(self):
        return fasttext.load_model(os.path.join(
            current_app.config['CLASSIFIER_MODEL'], 'fast_text_model.bin'))

# from flask import current_app
# print(os.path.dirname(os.path.abspath(__file__)))
# model = fasttext.train_supervised('.train.txt')
# model = train_supervised(
#     input=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'train.txt'), epoch=25, lr=1.0, wordNgrams=2, verbose=2, minCount=1,
#     loss="hs"
# )

# model.quantize(input='data.train.txt', retrain=True)
# model.save('./model.bin')
# model=fasttext.load_model(current_app.config['CLASSIFIER_MODEL'])
#
