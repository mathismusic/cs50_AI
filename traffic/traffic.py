import cv2
import numpy as np
import os
import sys
import tensorflow as tf

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    # 1. read in files as np ndarrays.
    # 2. resize files.

    images = []
    labels = []

    for subdir in os.scandir(data_dir):  # scandir returns DirEntry Objects
        if subdir.name == ".DS_Store":
            continue

        abs_subdir = os.path.join(data_dir, subdir)
        for image in os.scandir(abs_subdir):
            img = cv2.imread(os.path.join(abs_subdir, image.name))  # reads img in BGR
            img = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT), interpolation=cv2.INTER_CUBIC)
            images.append(img)  # images is list of imgs as np ndarrays
            labels.append(subdir.name)

    return images, labels

    # Note: DirEntry object attribute (NOT method) name returns filename. (Corres. to an element of return of listdir)


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    # create a SequentialNN(in sequence, layers one after the other. One input -> hidden layers in line->output layer).
    # Behaves like a list of layers
    model = tf.keras.models.Sequential([

        # Convolutional layer. Learn 24 filters using a 4x4 kernel matrix
        tf.keras.layers.Conv2D(
            24, (4, 4), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)  # WIDTH first as it's (x, y, z)
        ),

        # Avg-pooling layer, using 3x3 pool size
        tf.keras.layers.AveragePooling2D(pool_size=(3, 3)),

        # Flatten units
        tf.keras.layers.Flatten(),

        # Add a hidden layer with dropout of 25%
        tf.keras.layers.Dense(337, activation="relu"),
        tf.keras.layers.Dropout(0.25),

        # Add an output layer with output units for all NUM_CATEGORIES possible outputs
        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])

    # Train neural network
    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )
    return model


if __name__ == "__main__":
    main()
