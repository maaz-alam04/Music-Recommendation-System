import os
import numpy as np
from tensorflow.keras.utils import to_categorical
from keras.layers import Input, Dense
from keras.models import Model

# Initialize variables
is_init = False
label = []
dictionary = {}
c = 0

# Iterate over all npy files in the directory
for i in os.listdir():
    if i.endswith(".npy") and not i.startswith("labels"):  # Check for npy files excluding labels.npy
        data = np.load(i)
        print(f"Loaded {i} with shape {data.shape}")

        # Skip files that do not match the expected 2D shape
        if data.ndim != 2:
            print(f"Skipping {i} due to dimension mismatch: {data.ndim} dimensions found")
            continue
        
        # Check if we are initializing or concatenating
        if not is_init:
            is_init = True
            X = data
            size = X.shape[0]
            y = np.array([i.split('.')[0]] * size).reshape(-1, 1)
        else:
            if data.shape[1] == X.shape[1]:  # Ensure data has the correct number of columns
                X = np.concatenate((X, data))
                y = np.concatenate((y, np.array([i.split('.')[0]] * data.shape[0]).reshape(-1, 1)))
            else:
                print(f"Skipping {i} due to shape mismatch: {data.shape[1]} columns found, expected {X.shape[1]}")

        label.append(i.split('.')[0])
        dictionary[i.split('.')[0]] = c
        c += 1

# Convert labels to numerical format using the dictionary
for i in range(y.shape[0]):
    y[i, 0] = dictionary[y[i, 0]]
y = np.array(y, dtype="int32")

# Convert labels to one-hot encoding
y = to_categorical(y)

# Shuffle the data
X_new = X.copy()
y_new = y.copy()
counter = 0

cnt = np.arange(X.shape[0])
np.random.shuffle(cnt)

for i in cnt:
    X_new[counter] = X[i]
    y_new[counter] = y[i]
    counter += 1

# Print the final shape of X and y for verification
print(f"Final shape of X: {X_new.shape}")
print(f"Final shape of y: {y_new.shape}")

# Define the model architecture
ip = Input(shape=(X_new.shape[1],))  # Ensure shape is a tuple
m = Dense(512, activation="relu")(ip)
m = Dense(256, activation="relu")(m)
op = Dense(y_new.shape[1], activation="softmax")(m)

model = Model(inputs=ip, outputs=op)

# Compile the model
model.compile(optimizer='rmsprop', loss="categorical_crossentropy", metrics=['acc'])

# Train the model
model.fit(X_new, y_new, epochs=50)

# Save the model and labels
model.save("model.h5")
np.save("labels.npy", np.array(label))

print("Model training completed and saved.")
