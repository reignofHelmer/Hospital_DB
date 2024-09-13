import face_recognition
import cv2
import numpy as np
from cryptography.fernet import Fernet

def resize_image(image, width=800):
    if image is None:
        raise ValueError("Cannot resize a NoneType image")
    height = int((width / image.shape[1]) * image.shape[0])
    return cv2.resize(image, (width, height))

def save_compressed_image(image, path, quality=90):
    if not isinstance(image, np.ndarray):
        raise ValueError("The provided image is not a valid numpy array.")
    cv2.imwrite(path, image, [int(cv2.IMWRITE_JPEG_QUALITY), quality])

def capture_and_encode_face():
    # Capture image from the webcam
    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        raise ValueError("Could not open video device")

    ret, frame = video_capture.read()
    video_capture.release()
    cv2.destroyAllWindows()

    if not ret or frame is None:
        raise ValueError("Failed to capture image from camera")

    # Resize the captured image to a smaller size
    resized_frame = resize_image(frame, width=800)

    # Optionally, save the resized image with compression
    save_compressed_image(resized_frame, 'compressed_frame.jpg', quality=80)

    # Encode the resized frame to extract face encodings
    face_encodings = face_recognition.face_encodings(resized_frame)

    if not face_encodings:
        print("No face detected.")
        return None

    return face_encodings[0]  # Return the first detected face encoding

# Generate a key for encryption/decryption
key = Fernet.generate_key()
cipher_suite = Fernet(key)

def encrypt_encoding(encoding):
    encoding_bytes = encoding.tobytes()
    encrypted_encoding = cipher_suite.encrypt(encoding_bytes)
    return encrypted_encoding

def decrypt_encoding(encrypted_encoding):
    decrypted_encoding = cipher_suite.decrypt(encrypted_encoding)
    encoding = np.frombuffer(decrypted_encoding, dtype=np.float64)
    return encoding

# Example usage
if __name__ == "__main__":
    encoding = capture_and_encode_face()
    if encoding is not None:
        encrypted = encrypt_encoding(encoding)
        print("Encrypted Encoding:", encrypted)
        decrypted = decrypt_encoding(encrypted)
        print("Decrypted Encoding:", decrypted)
