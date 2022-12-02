import cv2, cryptography
from pyzbar.pyzbar import decode
from getpass import getpass

mode = input("Enter Mode (Generate : G or Decode : D): ")

psswrd = getpass()

if( mode == "G" ):
    #Do stuff
    print("Not available yet")

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