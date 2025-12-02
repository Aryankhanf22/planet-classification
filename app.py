from flask import Flask, render_template, request
from keras.models import load_model
import numpy as np
from tensorflow.keras.preprocessing import image
import os

app = Flask(__name__)
model = load_model('planets_and_moons_model.h5')
categories = ['earth', 'jupiter', 'mars', 'mercury', 'moon', 'neptune', 'pluto', 'saturn', 'uranus', 'venus']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"

    # Save the uploaded image
    filepath = os.path.join('static', 'uploads', file.filename)
    file.save(filepath)

    # Preprocess the image
    img = image.load_img(filepath, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0

    # Predict the class
    prediction = model.predict(img_array)
    predicted_class = categories[np.argmax(prediction)]

    # Return prediction and image
    return render_template('index.html', prediction=predicted_class, image_path=filepath)

if __name__ == "__main__":
    app.run(debug=True)

# if __name__ == "__main__":
#     app.run(debug=True, host='0.0.0.0', port=5000)
