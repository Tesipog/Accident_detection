from cv2 import cv2
from Predictor import AccidentDetectionModel
from twilio.rest import Client
import numpy as np

model = AccidentDetectionModel("model.json",
                               r"C:\Users\krish\PycharmProjects\python\AccidentDetector\model_weights .h5")
font = cv2.FONT_HERSHEY_DUPLEX


def startapplication():
    Non_accident_probability, Accident_probability, text = 0, 0, ""
    video = cv2.VideoCapture('Tesipog85E.mp4')
    while video.isOpened():
        Success, frame = video.read()
        if not Success:
            break
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        roi = cv2.resize(gray_frame, (250, 250))
        pred, prob = model.predict_accident(roi[np.newaxis, :, :])
        pred_l = np.argmax(pred)
        q, w = prob[0][0], prob[0][1]
        Non_accident_probability = Non_accident_probability + q
        Accident_probability = Accident_probability + w
        text = "No Accident" if Accident_probability > Non_accident_probability else "Accident"
        if pred_l == 0:
            prob = (round(prob[0][0] * 100, 2))
            cv2.rectangle(frame, (0, 0), (280, 40), (0, 0, 0), -1)
            cv2.putText(frame, text, (20, 30), font, 1, (255, 255, 0), 2)
        if cv2.waitKey(33) & 0xFF == ord('q'):
            return
        cv2.imshow('Video', frame)
    if text == "Accident":
        client = Client('Your Twilio Account SID', 'Your auth Token')
        client.messages.create(from_='+19713182679',
                               to='+919014868551',
                               body='Accident occurred At Ameerpet Metro,Hyderabad')


if __name__ == '__main__':
    startapplication()
