# app.py
from flask import Flask, render_template, request, redirect, url_for
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.vgg16 import preprocess_input
import numpy as np
import os

app = Flask(__name__, static_folder="C:/Users/ASUS/OneDrive/Documents/static")

# Load the trained model
model = load_model("vgg16.h5")

# Class labels
class_labels = ['Biodegradable', 'Recyclable', 'Trash']

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        f = request.files['pc_image']
        upload_folder = os.path.join(app.static_folder, 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        img_path = os.path.join(upload_folder, f.filename)
        f.save(img_path)

        img = load_img(img_path, target_size=(224, 224))
        x = img_to_array(img)
        x = preprocess_input(x)
        x = np.expand_dims(x, axis=0)

        preds = model.predict(x)
        prediction = class_labels[np.argmax(preds)]

        return render_template("portfolio-details.html", prediction=prediction, image_url=url_for('static', filename='uploads/' + f.filename))

@app.route('/contact')
def contact():
    return render_template("contact.html")

if __name__ == '__main__':
    app.run(debug=True, port=2222)
