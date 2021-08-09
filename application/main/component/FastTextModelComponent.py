# /*
# FAST TEXT MODEL COMPONENT
# IMPORTANT-LOAD THIS COMPONENT ONLY WHEN REQUIRED
# */

import fasttext
import os
from fasttext import train_supervised
from flask import current_app


class FastTextModelComponent():
    def __init__(self):
        ""
    # /*
    # TRAIN MODEL WITH TRAINING FILES
    # Training_file_dir-/resources/classifier_model
    # */

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
    # /*
    # IMPORTANT-LOAD MODEL ONLY WHEN REQUIRED
    # */

    def load_model(self):
        return fasttext.load_model(os.path.join(
            current_app.config['CLASSIFIER_MODEL'], 'fast_text_model.bin'))
