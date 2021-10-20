import tensorflow as tf

def IUNET_model():
    inputs = tf.keras.Input(shape=[256, 256, 1])

    # step 1
    conv1 = tf.keras.layers.Conv2D(filters=16, kernel_size=3, padding="same", activation="relu")(inputs)

    context1 = tf.keras.layers.Conv2D(filters=16, kernel_size=3, padding="same", activation="relu")(conv1)
    drop1 = tf.keras.layers.Dropout(0.3)(context1)
    context1 = tf.keras.layers.Conv2D(filters=16, kernel_size=3, padding="same", activation="relu")(drop1)

    sum1 = tf.math.add(conv1, context1)

    # step 2

    stride2 = tf.keras.layers.Conv2D(filters=32, kernel_size=3, padding="same", strides=2, activation="relu")(sum1)

    context2 = tf.keras.layers.Conv2D(filters=32, kernel_size=3, padding="same", activation="relu")(stride2)
    drop2 = tf.keras.layers.Dropout(0.3)(context2)
    context2 = tf.keras.layers.Conv2D(filters=32, kernel_size=3, padding="same", activation="relu")(drop2)

    sum2 = tf.math.add(stride2, context2)

    # step 3

    stride3 = tf.keras.layers.Conv2D(filters=64, kernel_size=3, padding="same", strides=2, activation="relu")(sum2)

    context3 = tf.keras.layers.Conv2D(filters=64, kernel_size=3, padding="same", activation="relu")(stride3)
    drop3 = tf.keras.layers.Dropout(0.3)(context3)
    context3 = tf.keras.layers.Conv2D(filters=64, kernel_size=3, padding="same", activation="relu")(drop3)

    sum3 = tf.math.add(stride3, context3)

    # step 4

    stride4 = tf.keras.layers.Conv2D(filters=128, kernel_size=3, padding="same", strides=2, activation="relu")(sum3)

    context4 = tf.keras.layers.Conv2D(filters=128, kernel_size=3, padding="same", activation="relu")(stride4)
    drop4 = tf.keras.layers.Dropout(0.3)(context4)
    context4 = tf.keras.layers.Conv2D(filters=128, kernel_size=3, padding="same", activation="relu")(drop4)

    sum4 = tf.math.add(stride4, context4)

    # step 5 lowest one
    stride5 = tf.keras.layers.Conv2D(filters=256, kernel_size=3, padding="same", strides=2, activation="relu")(sum4)

    context5 = tf.keras.layers.Conv2D(filters=256, kernel_size=3, padding="same", activation="relu")(stride5)
    drop5 = tf.keras.layers.Dropout(0.3)(context5)
    context5 = tf.keras.layers.Conv2D(filters=256, kernel_size=3, padding="same", activation="relu")(drop5)

    sum5 = tf.math.add(stride5, context5)

    up5 = tf.keras.layers.UpSampling2D(size=(2, 2))(sum5)

    # step 6 up 1
    conc6 = tf.keras.layers.concatenate([up5, sum4])
    loc6 = tf.keras.layers.Conv2D(filters=128, kernel_size=3, padding="same", activation="relu") (conc6)
    loc6 = tf.keras.layers.Conv2D(filters=128, kernel_size=1, padding="same", activation="relu") (loc6)
    up6 = tf.keras.layers.UpSampling2D(size=(2, 2))(loc6)

    # step 7 up 2
    conc7 = tf.keras.layers.concatenate([up6, sum3])
    loc7 = tf.keras.layers.Conv2D(filters=64, kernel_size=3, padding="same", activation="relu")(conc7)
    loc7 = tf.keras.layers.Conv2D(filters=64, kernel_size=1, padding="same", activation="relu")(loc7)
    up7 = tf.keras.layers.UpSampling2D(size=(2, 2))(loc7)

    uploc7 = tf.keras.layers.Conv2DTranspose(filters=32, kernel_size=3, padding='same')(up7)  # tf.keras.layers.UpSampling2D(size=(2, 2))(loc7)

    # step 8 up 3
    conc8 = tf.keras.layers.concatenate([up7, sum2])
    loc8 = tf.keras.layers.Conv2D(filters=32, kernel_size=3, padding="same", activation="relu")(conc8)
    loc8 = tf.keras.layers.Conv2D(filters=32, kernel_size=1, padding="same", activation="relu")(loc8)
    up8 = tf.keras.layers.UpSampling2D(size=(2, 2))(loc8)

    seg8 = tf.math.add(uploc7, loc8)

    # step 9 up 4
    conc9 = tf.keras.layers.concatenate([up8, sum1])
    conv9 = tf.keras.layers.Conv2D(filters=32, kernel_size=3, padding="same", activation="relu")(conc9)

    upseg8 = tf.keras.layers.Conv2DTranspose(filters=32, kernel_size=3, strides=2, padding="same")(seg8)
    seg9 = tf.math.add(upseg8, conv9)

    sig = tf.keras.layers.Conv2D(filters=1, kernel_size=1, activation='sigmoid')(seg9)

    finalModel = tf.keras.Model(inputs, sig)

    return finalModel


