import cv2 
import mediapipe as mp
import pyautogui

cap = cv2.VideoCapture(0)  # Cero representa la camara de la computadora predeterminada 

cap.set(3, 1280) # 3 es el ancho de la ventana 
cap.set(4, 720) # 4 es la altura de la ventana 

mp_hands = mp.solutions.hands # Se define la variable mp_hands como la solucion de manos de mediapipe 
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7) # Se define la variable hands como la solucion de manos de mediapipe con un maximo de 1 mano y una confianza minima de 0.7
mp_drawing = mp.solutions.drawing_utils # Se define la variable mp_drawing como la solucion de dibujo de mediapipe

green = (0, 250, 0)
white = (0, 0, 0)

down_pressed = False  # Variable para controlar el estado de la tecla

while True:
    success, image = cap.read() # Se lee el video de la camara 
    image = cv2.flip(image, 1) # Se voltea el video de la camara 
    imgRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # Se convierte el video de la camara a RGB
    results = hands.process(imgRGB) # Se procesa el video de la camara 

    cv2.line(image, (0,360), (1280,360), white, 10) # Se dibuja una linea blanca en el video de la camara    
    cv2.rectangle(image, (600,280), (680,440), green, cv2.FILLED) # Se dibuja un rectangulo verde en el video de la camara 

    if results.multi_hand_landmarks: # Si hay una mano en el video 
        handPoints = [] 
        for handLms in results.multi_hand_landmarks: # Se dibuja la mano en el video 
            mp_drawing.draw_landmarks(image, handLms, mp_hands.HAND_CONNECTIONS) # Se dibuja la mano en el video 

        for idx, lm in enumerate(handLms.landmark): # Se obtiene la posicion de los puntos de la mano
            h, w, c = image.shape                   # Se obtiene el ancho y alto de la imagen
            cx, cy = int(lm.x * w), int(lm.y * h)   # Se obtiene la posicion x y y del punto
            handPoints.append((cx, cy))             # Se agrega la posicion x y y del punto a la lista handPoints

        if handPoints[8][1] < 280:    # Si el punto 8 de la mano esta por encima de la linea blanca
            print("UP")
            if down_pressed:           # Si la tecla down esta presionada
                pyautogui.keyUp("down")
                down_pressed = False
            pyautogui.keyDown("space")   # Se presiona la tecla espacio
            pyautogui.keyUp("space")     # Se suelta la tecla espacio

        elif handPoints[8][1] > 440:  # Si el punto 8 de la mano esta por debajo de la linea blanca
             print("DOWN")
             if not down_pressed:     # Si la tecla down no esta presionada
                 pyautogui.keyDown("down")
                 down_pressed = True
        else:
            print('CENTER')            # Si el punto 8 de la mano esta en el centro de la linea blanca
            if down_pressed:           # Si la tecla down esta presionada
                pyautogui.keyUp("down")
                down_pressed = False


    cv2.imshow("Dino Game", image)
    cv2.waitKey(1) # Se espera 1 milisegundo para que se actualice el video
