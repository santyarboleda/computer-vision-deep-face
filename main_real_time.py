import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import av
import cv2
from deepface import DeepFace

class EmotionAnalyzer(VideoTransformerBase):
    def __init__(self):
        self.emotions = ["angry", "disgust", "fear", "happy", "sad", "surprise", "neutral"]

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")

        try:
            # Analizar la expresión facial
            result = DeepFace.analyze(img, actions=['emotion'], enforce_detection=False)

            st.write("DeepFace result:", result)  # Mostrar el resultado en Streamlit para depuración

            # Obtener la emoción dominante y las coordenadas de la región facial
            if isinstance(result, list):
                emotions = result[0]['emotion']
                dominant_emotion = result[0]['dominant_emotion']
                region = result[0]['region']
            else:
                emotions = result['emotion']
                dominant_emotion = result['dominant_emotion']
                region = result['region']

            st.write("Emotions detected:", emotions)  # Mostrar las emociones detectadas
            st.write("Region detected:", region)  # Mostrar la región detectada

            # Mostrar las emociones en la imagen
            for i, (emotion, score) in enumerate(emotions.items()):
                cv2.putText(img, f'{emotion}: {round(score, 2)}', (10, 30 + i * 20), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

            # Dibujar un rectángulo alrededor de la región facial
            cv2.rectangle(img, (region['x'], region['y']), (region['x'] + region['w'], region['y'] + region['h']), (0, 165, 255), 2)
        except Exception as e:
            cv2.putText(img, f"Error: {str(e)}", (10, 30), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
            st.write("Error:", e)  # Mostrar el error en Streamlit

        return av.VideoFrame.from_ndarray(img, format="bgr24")

# Configuración de la página de Streamlit
st.title("Análisis de Expresiones Faciales en Tiempo Real")
st.subheader("Usando DeepFace y Streamlit")

# Inicializar el streamer de WebRTC
webrtc_streamer(key="emotion-analyzer", video_transformer_factory=EmotionAnalyzer)
