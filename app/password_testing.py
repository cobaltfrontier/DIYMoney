from cryptography.fernet import Fernet

def create_encrypt_password():
    password = 'pepsi'
    byte_password = bytes(password, 'utf-8')
    key = b'gmfF8SYTuBl1fXC7Fzu342l-XsfVph3WgUCVjM5oFME='
    crypter = Fernet(key)
    encrypted_password_byte = crypter.encrypt(byte_password)
    print(encrypted_password_byte)
    encrypted_password_string = str(encrypted_password_byte, 'utf-8')
    print(encrypted_password_string)
    return encrypted_password_byte, crypter

def encrypt_password(form_password):
    key = b'gmfF8SYTuBl1fXC7Fzu342l-XsfVph3WgUCVjM5oFME='
    byte_password = bytes(form_password, 'utf-8')
    crypter = Fernet(key)
    encrypted_password_byte = crypter.encrypt(byte_password)
    encrypted_password_string = str(encrypted_password_byte, 'utf-8')
    return encrypted_password_string

def decrypt_password(encrypted_password_byte):
    key = b'gmfF8SYTuBl1fXC7Fzu342l-XsfVph3WgUCVjM5oFME='
    crypter = Fernet(key)
    decrypted_password = crypter.decrypt(encrypted_password_byte)
    decrypted_password_string = str(decrypted_password, 'utf-8')
    print(decrypted_password_string)
    return decrypted_password_string

decrypt_password(b'gAAAAABicTK_p0e8Yrys1Tk41QTR2szR3c3ZZ4p1s7GFKpfCqooSYentrDTzcBxXyLd8h6hd2fI-ZRCZ9YbdLOgz-KC1L6IKfw==')

create_encrypt_password()