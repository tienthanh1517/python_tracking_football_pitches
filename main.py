# Importing all modules
import cv2
import numpy as np
import serial

# Specifying upper and lower ranges of color to detect in hsv format
lower_co_xanh = np.array([45, 50, 20])  # co xanh
upper_co_xanh = np.array([75, 255, 255])  # co xanh

lower_co_xam = np.array([15, 10, 20])  # co xam
upper_co_xam = np.array([45, 175, 255])  # co xam

# Capturing webcam footage
webcam_phone = cv2.VideoCapture('http://192.168.1.3:8080/video')

while True:
    success, video = webcam_phone.read()  # Reading webcam footage
    video = cv2.resize(video, (1080, 720))

    img = cv2.cvtColor(video, cv2.COLOR_BGR2HSV)  # Converting BGR image to HSV format

    mask_co_xanh = cv2.inRange(img, lower_co_xanh, upper_co_xanh)  # Masking the image to find our color
    mask_co_xam = cv2.inRange(img, lower_co_xam, upper_co_xam)

    mask_contours, hierarchy = cv2.findContours(mask_co_xanh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # Finding contours in mask image
    mask_contours2, hierarchy2 = cv2.findContours(mask_co_xam, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Finding position of all contours
    count = 0
    count2 = 0
    if len(mask_contours) != 0:
        for mask_contour in mask_contours:
            if cv2.contourArea(mask_contour) > 500:
                x, y, w, h = cv2.boundingRect(mask_contour)
                cv2.rectangle(video, (x, y), (x + w, y + h), (0, 0, 255), 3)  # drawing rectangle
                count = count + 1

    if len(mask_contours2) != 0:
        for mask_contour2 in mask_contours2:
            if cv2.contourArea(mask_contour2) > 500:
                x, y, w, h = cv2.boundingRect(mask_contour2)
                cv2.rectangle(video, (x, y), (x + w, y + h), (0, 0, 0), 3)  # drawing rectangle
                count2 = count2 + 1

    print("số màu cỏ xanh là", count)
    print("số màu cỏ xám là: ", count2)



    cv2.imshow("mask image", mask_co_xanh)  # Displaying mask image
    cv2.imshow("mask image", mask_co_xam)
    cv2.imshow("window", video)  # Displaying webcam image

    key = cv2.waitKey(1)
    if key == ord("q"):
        break

webcam_phone.release()
cv2.destroyAllWindows()
