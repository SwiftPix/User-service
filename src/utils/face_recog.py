# import face_recognition
# import numpy as np
# import base64
# from io import BytesIO
# from PIL import Image
# import sys

def validade_faces(inp_img_b64, usr_img_b64):
    # file_contents = inp_img_b64.read()

    # inp_img_base64 = base64.b64encode(file_contents).decode('utf-8')
    # inp_img = Image.open(BytesIO(base64.b64decode(inp_img_base64)))
    # usr_img = Image.open(BytesIO(base64.b64decode(usr_img_b64.get("file").get("file_b64"))))

    # if usr_img is None or inp_img is None:
    #     return False
        
    # usr_img_np = np.array(usr_img)
    # inp_img_np = np.array(inp_img)

    # usr_encoding = face_recognition.face_encodings(usr_img_np)[0]
    # inp_encoding = face_recognition.face_encodings(inp_img_np)[0]
    
    # result = face_recognition.compare_faces([usr_encoding], inp_encoding)
    
    # if result[0]:
    #     return True
    
    # return False
    return True
