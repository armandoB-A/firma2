# -*- coding: utf-8 -*-
# coding=utf-8

import base64
import numpy as np
import cv2
from skimage.metrics import structural_similarity as ssim
from http.server import HTTPServer, BaseHTTPRequestHandler


# Mach Threshold
THRESHOLD = 85


def similitud(image11, image22):
    # Decodificar las imágenes en formato bytes a imágenes de OpenCV
    image1 = cv2.imdecode(np.frombuffer(image11, np.uint8), cv2.IMREAD_UNCHANGED)
    image2 = cv2.imdecode(np.frombuffer(image22, np.uint8), cv2.IMREAD_UNCHANGED)
    
    #image1 = cv2.imread(r"C:\Users\N-135\OneDrive\Documentos\vicioso\firma\dataset\armando\1.png")
    # image2 = cv2.imread(r"C:\Users\N-135\OneDrive\Documentos\vicioso\firma\dataset\armando\4.png")
    print(image1)
    print(image11)
    
    # Convertir las imágenes a escala de grises y cambiar su tamaño
    img1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    img1 = cv2.resize(img1, (300, 300))
    img2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    img2 = cv2.resize(img2, (300, 300))

    # Calcular el valor de similitud
    similarity_value = "{:.2f}".format(ssim(img1, img2)*100)
    print("answer is ", float(similarity_value),
           "type=", type(similarity_value))
    return similarity_value
                            

#Clase para definir el servidor http. Solo recibe solicitudes POST.
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        print("Peticion recibida")
        # Leer la imagen de la solicitud
        content_length = int(self.headers['Content-Length'])
        image = self.rfile.read(content_length)
        image = image.decode().replace("data:image/png;base64,", '')
        #print(image)
        decoded_image = base64.b64decode(image)
        # Realizar la predicción con el modelo entrenado
        # prediction = model.predict(image)
        resp = similitud(decoded_image, decoded_image)

        # Enviar la respuesta a la solicitud
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(resp.encode())
        
print("Iniciando el servidor...")
# Crear el servidor HTTP
httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)

# Iniciar el servidor
httpd.serve_forever()
