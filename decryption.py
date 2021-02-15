from cryptography.fernet import Fernet, InvalidToken
import os
from pathlib import Path
import shutil

def decrypt(key):
   
    input_file = 'test.encrypted'
    

    curr_dir = os.getcwd()
    folder_name =  'Decrypt_Data'

    path = os.path.join(curr_dir , folder_name) 
    result = os.path.join(path , 'result.csv') 
    os.mkdir(path)


    with open(input_file, 'rb') as f:
        data = f.read()  # Read the bytes of the encrypted file

    fernet = Fernet(key)
    try:
        decrypted = fernet.decrypt(data)

        with open(result, 'wb') as f:
            f.write(decrypted)  # Write the decrypted bytes to the output file

        # delete input older 
        shutil.rmtree('Clean_Data')

    except InvalidToken as e:
        print("Invalid Key - Unsuccessfully decrypted")