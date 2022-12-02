import cv2, base64, qrcode
from cryptography.fernet import Fernet
from pyzbar.pyzbar import decode
from getpass import getpass

def generate_qr(password):
    gift_id = input("Enter gift: ")
    Fernet.generate_key()
    f = Fernet(password)
    f.encrypt(b"" + gift_id)
    print("Encrypted Gift: " + gift_id)

if __name__ == "__main__":
    mode = input("Enter Mode (Generate : G or Decode : D): ")
    password_input = getpass()
    password = base64.urlsafe_b64decode(password_input)

    if( mode == "G" ):
        #Do stuff
        generate_qr(password=password)

    if( mode == "D"):
        # Do other stuff
        vid = cv2.VideoCapture(0)
        while( True ):
            rect, frame = vid.read()
            h, w = frame.shape[:2]
            cv2.imshow('Gift Identifier', frame)
            message = decode((frame[:, :, 0].astype('uint8').tobytes(), w, h))
            if( len(message) > 0 and message[0] is not None and message[0] is not ""):
                print("Decoded message is " + str(message[0]))
                break
            if( cv2.waitKey(1) & 0xFF == ord('q') ):
                break
        vid.release()
        cv2.destroyAllWindows()
    else:
        print("Incorrect input!")