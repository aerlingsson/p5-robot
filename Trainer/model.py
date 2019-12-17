from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, Lambda, Input
import tensorflow as tf


def build_model(state_shape, action_size):
    model = Sequential([
        Input(shape=state_shape),
        Lambda(lambda x: tf.image.rgb_to_grayscale(x)),
        Lambda(lambda x: x / 255),
        Conv2D(24, (5, 5), strides=(2, 2), activation='relu'),
        Conv2D(36, (5, 5), strides=(2, 2), activation='relu'),
        Conv2D(48, (5, 5), strides=(2, 2), activation='relu'),
        Conv2D(64, (3, 3), strides=(1, 1), activation='relu'),
        Flatten(),
        Dense(256, activation='relu'),
        Dense(action_size, activation='linear')
    ])

    return model
