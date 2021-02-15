from cryptography.fernet import Fernet
def encrypt(input_file):
    key = Fernet.generate_key()# Use one of the methods to get a key (it must be the same when decrypting)
    
    output_file = 'test.encrypted'
    key_file = 'key.txt'

    with open("key.key", "wb") as f:
        f.write(key)  # Write the encrypted key to the file

    with open(input_file, 'rb') as f:
        data = f.read()  # Read the bytes of the input file

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(output_file, 'wb') as f:
        f.write(encrypted)  # Write the encrypted bytes to the output file

    # Note: You can delete input_file here if you want
    return 'File successfuly encrypted'