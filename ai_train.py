import tensorflow as tf
import numpy as np
from PIL import Image
import os

dataset_dir = 'C:\\Users\\chh36\\Desktop\\target_trace\\'

train_dir = os.listdir(dataset_dir)
print(train_dir)

test_ratio = 0.1

image_size = 100

train_image, train_label, test_image, test_label = [], [], [], []

for a, category in enumerate(train_dir):
    count = 0
    images_names = os.listdir(dataset_dir+category)
    split_point = int(round(len(images_names)*(1-test_ratio)))
    for b, image_name in enumerate(images_names):
        image = Image.open(dataset_dir+category+'\\'+image_name).convert('RGB')
        image = image.resize((image_size, image_size))
        image = np.array(image)
        label = np.zeros(len(train_dir))
        label[a] = 1

        if count < split_point:
            train_image.append(image)
            train_label.append(label)
        else:
            test_image.append(image)
            test_label.append(label)

        count += 1

train_image = np.asarray(train_image)
train_image = np.reshape(train_image, [train_image.shape[0], image_size, image_size, 3])
train_label = np.asarray(train_label)
test_image = np.asarray(test_image)
test_image = np.reshape(test_image, [test_image.shape[0], image_size, image_size, 3])
test_label = np.asarray(test_label)

model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(128, (3, 3), input_shape=(image_size, image_size, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(100, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(100, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(len(train_dir), activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(x=train_image, y=train_label, validation_data=(test_image, test_label), epochs=30)

model.save('C:\\Users\\chh36\\Desktop\\stupid_robot_model')