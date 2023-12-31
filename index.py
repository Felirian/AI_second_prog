import numpy as np
from tensorflow.keras.datasets import cifar10

from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

from keras.utils import to_categorical
from kerastuner.tuners import RandomSearch

(X_train, y_train), (X_test, y_test) = cifar10.load_data()

X_train = X_train / 255.0
X_test = X_test / 255.0

y_train = to_categorical(y_train, 10)
y_test = to_categorical(y_test, 10)

def build_model(hp):
    model = Sequential()

    # 1 слой свертки
    model.add(Conv2D(filters=hp.Int('conv1_filters', min_value=32, max_value=64, step=16),
                     kernel_size=(3, 3),
                     activation='relu',
                     input_shape=(32, 32, 3)))    
    model.add(MaxPooling2D(pool_size=(2, 2)))
    
    # 2 слой свертки
    model.add(Conv2D(filters=hp.Int('conv2_filters', min_value=32, max_value=64, step=16),
                     kernel_size=(3, 3),
                     activation='relu',
                     input_shape=(32, 32, 3)))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    
    # model.add(Conv2D(filters=hp.Int('conv3_filters', min_value=32, max_value=64, step=16),
    #                  kernel_size=(3, 3),
    #                  activation='relu',
    #                  input_shape=(32, 32, 3)))
    # model.add(MaxPooling2D(pool_size=(2, 2)))
    
    model.add(Flatten())

    
    model.add(Dense(units=hp.Int('dense_units', min_value=32, max_value=64, step=16), activation='relu'))
    
    model.add(Dropout(rate=hp.Choice('dropout_rate', values=[0.2, 0.3, 0.4])))
    
    model.add(Dense(10, activation='softmax'))

    
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    return model

tuner = RandomSearch(
    build_model,
    objective='val_accuracy',
    max_trials=5,  
    directory='tuner_dir',
)

tuner.search(X_train, y_train, epochs=10, validation_split=0.2)

best_model = tuner.get_best_models(num_models=1)[0]