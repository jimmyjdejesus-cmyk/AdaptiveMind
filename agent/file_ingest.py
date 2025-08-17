import os
from PIL import Image
import pytesseract
import textract

def ingest_file(file_path):
    ext = os.path.splitext(file_path)[-1].lower()
    if ext in ['.png', '.jpg', '.jpeg', '.bmp', '.gif']:
        # OCR for image
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)
        return {"type": "image", "content": text}
    elif ext in ['.pdf']:
        # PDF to text
        text = textract.process(file_path)
        return {"type": "pdf", "content": text.decode('utf-8')}
    elif ext in ['.mp3', '.wav', '.m4a']:
        # Audio to text
        import speech_recognition as sr
        r = sr.Recognizer()
        with sr.AudioFile(file_path) as source:
            audio = r.record(source)
            text = r.recognize_google(audio)
        return {"type": "audio", "content": text}
    elif ext in ['.txt', '.md', '.py', '.docx']:
        text = textract.process(file_path)
        return {"type": ext[1:], "content": text.decode('utf-8')}
    else:
        return {"type": "unknown", "content": None}