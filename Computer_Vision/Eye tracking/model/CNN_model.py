from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPool2D, Flatten, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import pandas as pd

image_gen = ImageDataGenerator(rescale=1 / 255, rotation_range=0.2)  # Rescale the image by normalzing it.
image_shape = (40, 120, 3)
model = Sequential()


## FIRST SET OF LAYERS

# CONVOLUTIONAL LAYER
model.add(Conv2D(filters=16, kernel_size=(5, 5), input_shape=image_shape, activation='relu', ))
# POOLING LAYER
model.add(MaxPool2D(pool_size=(2, 2)))

## SECOND SET OF LAYERS

# CONVOLUTIONAL LAYER
model.add(Conv2D(filters=32, kernel_size=(3, 3), input_shape=image_shape, activation='relu', ))
# POOLING LAYER
model.add(MaxPool2D(pool_size=(2, 2)))

# CONVOLUTIONAL LAYER
model.add(Conv2D(filters=64, kernel_size=(3, 3), input_shape=image_shape, activation='relu', ))
# POOLING LAYER
model.add(MaxPool2D(pool_size=(2, 2)))

# FLATTEN IMAGES FROM 40 by 120 to 4800 BEFORE FINAL LAYER
model.add(Flatten())

# 256 NEURONS IN DENSE HIDDEN LAYER (YOU CAN CHANGE THIS NUMBER OF NEURONS)
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))

# 100 NEURONS IN DENSE HIDDEN LAYER (YOU CAN CHANGE THIS NUMBER OF NEURONS)
model.add(Dense(100, activation='relu'))
model.add(Dropout(0.5))

# LAST LAYER IS THE CLASSIFIER, THUS 5 POSSIBLE CLASSES 
model.add(Dense(5, activation='softmax'))

from tensorflow.keras.optimizers import Adam

opt = Adam(lr=0.001)

model.compile(loss='categorical_crossentropy',
              optimizer=opt,
              metrics=['accuracy'])

batch_size = 8

train_image_gen = image_gen.flow_from_directory('../dataset/train',
                                                target_size=image_shape[:2],
                                                batch_size=batch_size,
                                                class_mode='categorical')

test_image_gen = image_gen.flow_from_directory('../dataset/test',
                                               target_size=image_shape[:2],
                                               batch_size=batch_size,
                                               class_mode='categorical')

results = model.fit(train_image_gen, epochs=100,
                    steps_per_epoch=12,
                    validation_data=test_image_gen,
                    validation_steps=4)

pd.DataFrame(results.history).plot(figsize=(8, 5))
model.save('50epochs_5classes.h5')

