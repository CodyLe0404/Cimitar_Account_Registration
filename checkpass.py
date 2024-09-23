import os
import pandas as pd
 

class EncryptionPass:
    @staticmethod
    def base_encryption(base_str):
        base_char = 0xFF
        result = ""
        try:
            for char in base_str:
                code = ord(char)
                encrypted_code = base_char ^ code  # Using bitwise XOR
                result += f"{encrypted_code:X}"
        except Exception as ex:
            # Handle exceptions here
            pass
        return result

    @staticmethod
    def base_decoding(base_str):
        base_char = 0xFF
        result = ""
        try:
            if len(base_str) > 0 and len(base_str) % 2 == 0:
                for i in range(0, len(base_str), 2):
                    sub = base_str[i:i + 2]
                    code = int(sub, 16)  # Convert hexadecimal string to integer
                    decrypted_code = base_char ^ code  # Using bitwise XOR
                    char_code = chr(decrypted_code)
                    result += char_code
        except Exception as ex:
            # Handle exceptions here
            pass
        return result

badgeno = [240370, 240135, 240141, 240142, 240220, 240221, 240222, 240292, 240293, 240295, 240296, 240297, 240298, 240299, 240300, 240301, 240303, 240304, 240306, 240369, 240360, 240361, 240362, 240363]
password = 'C8CFCFC8C6C8'

for ind in badgeno:
    enscrypt = EncryptionPass.base_encryption(str(ind))
    print(enscrypt)

# decode = EncryptionPass.base_decoding(password)
# enscrypt = EncryptionPass.base_encryption(str(badgeno))

# print(decode)
# print(enscrypt)