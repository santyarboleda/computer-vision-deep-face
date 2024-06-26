import streamlit as st
import json
import cv2
from PIL import Image
from deepface import DeepFace
import numpy as np

st.title("Face Emotion Detection")

# File uploader with the unique key from session state
uploaded_image = st.file_uploader("Choose a photo", type=["png", "jpg", "jpeg"])

# Verifica si se ha cargado una imagen
if uploaded_image:
    st.image(uploaded_image, width=300)
    pil_image = Image.open(uploaded_image).convert('RGB')
    if st.button('Detect emotions'):
        with st.spinner('Detecting emotions ...'):
            # Analiza la imagen para detectar emociones
            # Convierte la imagen de PIL a un array de numpy
            img_array = np.array(pil_image)
            analysis = DeepFace.analyze(img_array)
            st.success('Emotion detection completed!')
                    
            # Obtener las coordenadas y dimensiones de la región facial desde el diccionario
            x = analysis[0]['region']['x']
            y = analysis[0]['region']['y']
            w = analysis[0]['region']['w']
            h = analysis[0]['region']['h']
            
            # Dibujar un rectángulo alrededor de la región facial en la imagen original
            img = cv2.rectangle(img_array, (x, y), (x + w, y + h), (0, 255, 0), 2) 
            st.image(img, width=300)
            
            # Muestra el resultado del análisis como una cadena JSON
            st.write(analysis[0])
            
            st.header('Emotion Analysis:')
            # Muestra las emociones detectadas y sus respectivas probabilidades
            emotions = analysis[0]['emotion']
            for emotion, score in emotions.items():
                st.write(f"{emotion}: {score:.2f}%")
            
            st.write(f"Dominant emotion: {analysis[0]['dominant_emotion']}")
            
            st.header('Age Analysis:')
            st.write(f"Age: {analysis[0]['age']}")

            st.header('Race:')
            races = analysis[0]['race']
            for race, score in races.items():
                st.write(f"{race}: {score:.2f}%")

            st.header('Gender:')
            genders = analysis[0]['gender']
            for gender, score in genders.items():
                st.write(f"{gender}: {score:.2f}%")