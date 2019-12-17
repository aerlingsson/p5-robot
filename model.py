from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, Lambda, Input
import tensorflow as tf


def build_model(state_shape, action_size):
    '''
            encoder = load_model('enc.h5')
            encoder.trainable = False

            inp = Input(shape=self.state_shape)
            lamb1 = Lambda(lambda x: tf.image.rgb_to_grayscale(x))(inp)
            lamb2 = Lambda(lambda x: x / 255)(lamb1)
            enc = encoder(lamb2)
            flatten = Flatten()(enc)
            drp1 = Dropout(0.3)(flatten)
            dense1 = Dense(100, activation='relu')(drp1)
            drp2 = Dropout(0.3)(dense1)
            dense2 = Dense(50, activation='relu')(drp2)
            drp3 = Dropout(0.2)(dense2)
            dense3 = Dense(self.action_size, activation='linear')(drp3)

            model = Model(inputs=inp, outputs=dense3)

            '''

    model = Sequential([
        Input(shape=state_shape),
        Lambda(lambda x: tf.image.rgb_to_grayscale(x)),
        Lambda(lambda x: x / 255),
        Conv2D(24, (5, 5), strides=(2, 2), activation='relu'),
        Conv2D(36, (5, 5), strides=(2, 2), activation='relu'),
        Conv2D(48, (5, 5), strides=(2, 2), activation='relu'),
        Conv2D(64, (3, 3), strides=(1, 1), activation='relu'),
        Flatten(),
        Dropout(0.3),
        Dense(100, activation='relu'),
        Dropout(0.3),
        Dense(50, activation='relu'),
        Dropout(0.2),
        Dense(action_size, activation='linear')
    ])

    return model