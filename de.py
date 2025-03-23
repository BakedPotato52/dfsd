import cv2
video_path = "isl_animation.mp4"
cap = cv2.VideoCapture(video_path)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    cv2.imshow("ISL Animation", frame)
    if cv2.waitKey(25) & 0xFF == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()
