import tensorflow as tf
from model import build_model

STATE_SHAPE = (80,80,3)
ACTION_SIZE = 9

MODEL_PATH = 'model.h5'
EXPORT_PATH = 'model.tflite'


if __name__ == '__main__':
    model = build_model(STATE_SHAPE, ACTION_SIZE)
    model.load_weights(MODEL_PATH)

    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()

    open(EXPORT_PATH, "wb").write(tflite_model)