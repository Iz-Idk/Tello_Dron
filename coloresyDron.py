import cv2
import robomaster
from robomaster import robot


if __name__ == '__main__':
    l_drone = robot.Drone()
    l_drone.initialize()
    l_camera = l_drone.camera

    # Get battery status
    tl_battery = l_drone.battery
    battery_info = tl_battery.get_battery()
    print("Drone battery soc: {0}".format(battery_info))
    #   Muestra display
    l_camera.start_video_stream(display=False)
    for i in range(0, 300):
        #   Saca el frame
        frame = l_camera.read_cv2_image()

        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hegith, width, _ = frame.shape

        cx = int(width / 2)
        cy = int(hegith/2)


        #   Gets the center of the camera
        pixel_center = hsv_frame[cx, cy]
        #   Gets Hue value from pixel center frame
        hue_val = pixel_center[0]

        color = "TBA"
        if(hue_val > 80 and hue_val < 150 and (pixel_center[1] > 4) and (pixel_center[1] < 34)):
            color = "GRAY"
        elif(hue_val > 150 and hue_val < 165 and (pixel_center[1] > 40) or (pixel_center[1] < 47)):
            color = "PINK"
        elif(hue_val > 160 and hue_val < 173 and  (pixel_center[1] > 150) or (pixel_center[1] < 240)):
            color = "RED"
        #elif(hue_val < 131):
        #    color = "BLUE"
        else:
            color = "RED"
        
        # if(hue_val < 5):
        #    color = "RED"
        #elif(hue_val < 22):
        #    color = "ORANGE"
        #elif(hue_val < 33):
        #    color = "YELLOW"
        #elif(hue_val < 131):
        #    color = "BLUE"
        #else:
        #    color = "RED"

        print(pixel_center)
        cv2.putText(frame, color, (10, 50), 0, 1, (0, 255, 0), 2)
        #   Draws a circle at camera center
        cv2.circle(frame, (cx, cy), 5, (255, 0, 0), 3)

        cv2.imshow("Frame", frame)

        key = cv2.waitKey(1)
        if key == 27:
            break
    #   Cierra ventanas
    cv2.destroyAllWindows()
    l_camera.stop_video_stream()
    l_drone.close()
