import cv2, base64, qrcode, json, os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from pyzbar.pyzbar import decode
from getpass import getpass

def generate_qr(receiver, present, order):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.ERROR_CORRECT_M,
        box_size=12,
        border=4
    )
    data = {
        'Person' : receiver,
        'Gift' : str(present),
        'Priority' : order
    }
    qr.add_data(json.dumps(data, indent=2))
    qr.make(fit=True)
    img = qr.make_image()
    img.show()
    
def generate_key(password):
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000
    )
    return base64.urlsafe_b64encode(kdf.derive(password))
    
def encrypt_data(key, data):
    f = Fernet(key=key)
    return f.encrypt(b"" + data)


if __name__ == "__main__":
    mode = input("Enter Mode (Generate : G or Decode : D): ")
    password = getpass()
    password = bytes(password, 'utf-8')

    if( mode == "G" ):
        #Do stuff
        receiver = input("Receiver: ")
        gift = input("Gift: ")
        gift = bytes(gift, 'utf-8')
        priority = input("Priority: ")
        key = generate_key(password=password)
        encrypted_data = encrypt_data(key=key, data=gift)
        generate_qr(receiver=receiver, present=encrypted_data, order=priority)
    if( mode == "D"):
        # Do other stuff
        vid = cv2.VideoCapture(0)
        while( True ):
            rect, frame = vid.read()
            h, w = frame.shape[:2]
            cv2.imshow('Gift Identifier', frame)
            message = decode((frame[:, :, 0].astype('uint8').tobytes(), w, h))
            if( len(message) > 0 and message[0] is not None and message[0] != ""):
                print("Decoded message is " + str(message[0]))
                break
            if( cv2.waitKey(1) & 0xFF == ord('q') ):
                break
        vid.release()
        cv2.destroyAllWindows()
    else:
        print("Incorrect input!")