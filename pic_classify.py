import keras
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.utils import np_utils
import numpy as np

# カテゴリー指定
categories = ["apple", "grape", "orange", "peach", "others"]
num_classes = len(categories)

batch_size = 172
epochs = 5

# データロード
x_train, x_test, y_train, y_test = np.load("./fruits.npy")
# データを正規化する
x_train = x_train.astype("float") / 256
x_test = x_test.astype("float") / 256
print('X_train shape:', x_train.shape)

y_train = np_utils.to_categorical(y_train, num_classes)
y_test = np_utils.to_categorical(y_test, num_classes)

# モデル構築
model = Sequential()
model.add(Conv2D(32, (3, 3), padding='same', input_shape=x_train.shape[1:]))
model.add(Activation('relu'))
model.add(Conv2D(32, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(512))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(num_classes))
model.add(Activation('softmax'))

model.summary()

model.compile(loss='binary_crossentropy',
              optimizer='rmsprop', metrics=['accuracy'])

tb_cb = keras.callbacks.TensorBoard(
    log_dir="logs/tflog_0403/", histogram_freq=1)
cbks = [tb_cb]

# モデルを訓練
history = model.fit(x_train, y_train,
                    batch_size=batch_size,
                    epochs=epochs,
                    verbose=2,
                    validation_data=(x_test, y_test),
                    callbacks=cbks)

score = model.evaluate(x_test, y_test, verbose=1)

# モデルの評価
print('loss=', score[0])
print('accuracy=', score[1])
