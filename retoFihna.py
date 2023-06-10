import robomaster
import time
import cv2
from robomaster import robot
import numpy as np
from statistics import mode

color = None



def detectColors(l_camera):
    #   Inicia a capturar imagen
    l_camera.start_video_stream(display=False)
    moda = []
    for i in range(0, 50):
        #   Obtiene el frame actual de la imagen
        frame = l_camera.read_cv2_image()
        #   Convierte el frame a formato HSV
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        #   Obtenemos el tamaño del frame
        hegith, width, _ = frame.shape

        #   Calculamos las componentes centrales de la resolución de la imagen
        cx = int(width / 2)
        cy = int(hegith / 2)

        #   Calculamos el centro de la imagen
        pixel_center = hsv_frame[cx, cy]
        #   Obtenemos el valor del Hue del pixel central
        hue_val = pixel_center[0]

        color = "TBA"
        #   Sí el valor es menor a 5, entonces es Rojo, de lo contrario es otro de los colores
        
        if(hue_val > 80 and hue_val < 150 and (pixel_center[1] > 4) and (pixel_center[1] < 34)):
            color = "GRAY"
        elif(hue_val > 150 and hue_val < 165 and (pixel_center[1] > 40) or (pixel_center[1] < 47)):
            color = "PINK"
        elif(hue_val > 160 and hue_val < 173 and  (pixel_center[1] > 150) or (pixel_center[1] < 240)):
            color = "RED"
        #elif(hue_val > 99 or hue_val < 106 and (pixel_center[1] > 172) or (pixel_center[1] < 252)):
        #    color = "BLUE"
        else:
            color = "TBA"
        #   Imprime el centro del píxel
        print(pixel_center)

        cv2.putText(frame, color, (10, 50), 0, 1, (0, 255, 0), 2)
        #   Dibuja un círculo en la imagen
        cv2.circle(frame, (cx, cy), 5, (255, 0, 0), 3)

        cv2.imshow("Frame", frame)
        moda.append(color)
        key = cv2.waitKey(1)
        if key == 27:
            break
    #   Cierra ventanas
    color = mode(moda)
    cv2.destroyAllWindows()
    l_camera.stop_video_stream()

    return color



def initialSequence(tl_flight):
    """
        This trayectory moves the Tello Drone in front of an image to detect the next action
        Params:
        @tl_flight  |   Drone robot object
    """
    #   Goes up a little bit
    tl_flight.forward(distance=50).wait_for_completed()
    print("Forward 30cm")
    #   Stops moving for a bit.
    time.sleep(4)


def graySequence(tl_flight):
    """
        This trayectory moves the Tello Drone in front of an image by avoiding an obstacle.
        Params:
        @tl_flight  |   Drone robot object
    """
    print("Starting Gray trayectory")
    tl_flight.up(distance=50).wait_for_completed()
    time.sleep(2)
    tl_flight.forward(distance=90).wait_for_completed()
    time.sleep(2)
    #   Rotates drone in y axis
    tl_flight.rotate(angle=180).wait_for_completed()
    time.sleep(2)
    #   Goes down to final position
    tl_flight.down(distance=49).wait_for_completed()
    time.sleep(2)
    print("Finished Gray trayectory")

def blueSequence(tl_flight):
    """
        This trayectory draws a Triangle and then lands the Tello Drone.
        Params:
        @tl_flight  |   Drone robot object
    """
    print("Starting Blue trayectory")
    tl_flight.up(distance=20).wait_for_completed()
    time.sleep(2)
    #   Generates trayectory for a triangle
    for i in range(3):
        # Moves forward and rotates for next position
        tl_flight.rotate(angle=135).wait_for_completed()
        tl_flight.forward(distance=50).wait_for_completed() 
        time.sleep(2)
    #   Returns to initial color detection
    tl_flight.forward(distance=40).wait_for_completed()
    time.sleep(2)
    tl_flight.down(distance=40).wait_for_completed()
    print("Finished Blue trayectory")

def redSequence(tl_flight):
    """
        This trayectory draws a Circle and then lands the Tello Drone.
        Params:
        @tl_flight  |   Drone robot object
    """
    print("Starting Red trayectory")
    tl_flight.up(distance=20).wait_for_completed()
    tl_flight.rc(a=7, b=20, c=1, d=40)
    tl_flight.rc(a=7, b=20, c=1, d=40)

    time.sleep(10)
    #   Prepares drone to land
    tl_flight.down(distance=50).wait_for_completed()
    print("Finished Magenta trayectory")


def pinkSequence(tl_flight):
    """
        This trayectory the Tello Drone back to its starting position
        Params:
        @tl_flight  |   Drone robot object
    """
    print("Starting Pink trayectory")
    tl_flight.up(distance=52).wait_for_completed()
    tl_flight.forward(distance=100).wait_for_completed()
    time.sleep(2)
    #   Goes down to final position
    tl_flight.down(distance=52).wait_for_completed()
    tl_flight.forward(distance=30).wait_for_completed()
    time.sleep(2)

    #   Prepares drone to land
    tl_flight.down(distance=30).wait_for_completed()
    print("Finished Pink trayectory")


  

def chooseSequence(color, tl_flight):
    """
        Defines the sequence that must be executed by the robot
        Params:
        @color      |   Color detected by the camera to execute a sequence
        @tl_flight  |   Drone robot object
    """
    #   Magenta executes redSequence
    if(color is "GRAY"):
        graySequence(tl_flight)
    elif(color is "RED"):
        blueSequence(tl_flight)
    elif(color is "PINK"):
        pinkSequence(tl_flight)
    
    else:
        # mata el dron
        pass



if __name__ == '__main__':
    #   Initialization of robot Drone
    l_drone = robot.Drone()
    l_drone.initialize()
    #   Camera init
    l_camera = l_drone.camera
    #   Flight init
    tl_flight = l_drone.flight
    # Get battery status
    tl_battery = l_drone.battery
    battery_info = tl_battery.get_battery()
    print("Drone battery soc: {0}".format(battery_info))

    # Set the QUAV to takeoff
    tl_flight.takeoff().wait_for_completed()
    print("Take off")
    time.sleep(2)
    #   Does initial sequence
    initialSequence(tl_flight)
    #   Obtains the color of the image in frames
    color = detectColors(l_camera)
    time.sleep(2)
    try:
        if(color != "TBA"):
            print(color)
            chooseSequence(color, tl_flight)
            color = detectColors(l_camera)
            print(color)
            chooseSequence(color, tl_flight)
    except:
        print("Sorry, killing drone")  
        print(color)
        print("Landing drone")
         # Set the QUAV to land
        tl_flight.land().wait_for_completed()

        # Close resources
        l_drone.close()

    print("Landing drone")
    # Set the QUAV to land
    tl_flight.land().wait_for_completed()

    # Close resources
    l_drone.close()