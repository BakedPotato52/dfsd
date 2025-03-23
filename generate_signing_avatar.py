from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap, QImage
import sys
import os  # Missing import for file path checks
from app import audio_to_text, parse_to_isl
import cv2

# Placeholder function to map ISL grammar to sign animations
def generate_signing_avatar(isl_structure):
    """
    Map ISL grammar output to corresponding sign animations and render them on a signing avatar.
    """
    if not isl_structure.strip():
        print("Error: No ISL grammar available for animation.")
        return

    print("Generating ISL signs on avatar...")
    signs = isl_structure.split()
    for sign in signs:
        # Placeholder: Replace with actual rendering logic
        print(f"Performing sign: {sign}")
        # Add delay or animation rendering for each sign (in a GUI or 3D tool)

class AvatarWindow(QMainWindow):
    def __init__(self, words):
        """
        Initialize the window and display ISL animations for given words using preloaded videos.
        :param words: List of words to render as ISL signs.
        """
        super().__init__()
        self.setWindowTitle("ISL Signing Avatar")
        self.setGeometry(100, 100, 800, 600)
        self.words = words
        self.current_word_index = 0
        self.cap = None

        # Set up the central widget and layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # QLabel for displaying video frames
        self.video_label = QLabel(self)
        self.video_label.setStyleSheet("background-color: black;")
        self.layout.addWidget(self.video_label)

        # QTimer for frame updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

        # Start playing the first video
        self.play_next_video()

    def play_next_video(self):
        """
        Play the next video in the list.
        """
        if self.cap:
            self.cap.release()  # Release the previous video capture

        if self.current_word_index >= len(self.words):
            print("All videos played.")
            self.timer.stop()
            return

        word = self.words[self.current_word_index]
        video_path = f"assets/{word}.mp4"
        if os.path.exists(video_path):
            print(f"Playing ISL animation for: {word}")
            self.cap = cv2.VideoCapture(video_path)
            self.current_word_index += 1
            self.timer.start(30)  # Update frames every 30ms (~33fps)
        else:
            print(f"No animation found for word: {word}")
            self.current_word_index += 1
            self.play_next_video()  # Skip to the next video

    def update_frame(self):
        """
        Update the QLabel with the next frame of the video.
        """
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                # Convert the frame to RGB format and create a QImage
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = frame.shape
                bytes_per_line = ch * w
                qimg = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(qimg)
                self.video_label.setPixmap(pixmap)
            else:
                self.timer.stop()
                self.play_next_video()  # Move to the next video
        else:
            self.play_next_video()  # If capture is not opened, skip

    def closeEvent(self, event):
        """
        Clean up resources on window close.
        """
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        super().closeEvent(event)

def main():
    """Main program to orchestrate the process."""
    print("Audio-to-Sign Language Translator\n")

    # Step 1: Audio to Text
    text = audio_to_text()
    if not text:
        print("Failed to capture audio input.")
        return

    print(f"Captured Text: {text}")

    # Step 2: Text to ISL Grammar
    isl_output = parse_to_isl(text)
    if not isl_output:
        print("Failed to parse text to ISL grammar.")
        return

    print(f"ISL Grammar Output: {isl_output}")

    # Step 3: Generate Signing Avatar
    generate_signing_avatar(isl_output)

    # Optional: Launch a GUI for avatar rendering
    app = QApplication(sys.argv)
    words = isl_output.split()  # Split ISL grammar into individual words
    window = AvatarWindow(words)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
