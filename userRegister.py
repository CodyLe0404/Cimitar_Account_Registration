import pyodbc, os
import pandas as pd
from unidecode import unidecode
from dotenv import load_dotenv

load_dotenv()

# connectionStr = "DRIVER={ODBC Driver 17 for SQL Server}" 
# connectionStr += ";SERVER=" + os.environ["Server"] + "," + os.environ["Port"] 
# connectionStr +=  ";DATABASE=" + os.environ["Database"] 
# connectionStr += ";UID=" + os.environ["User"] 
# connectionStr += ";PWD=" + os.environ["Password"]

# conn = pyodbc.connect(connectionStr)

# cursor = conn.cursor()

class EncryptionPass:
    @staticmethod
    def base_encryption(base_str):
        base_char = 0xFF
        result = ""
        try:
            for char in base_str:
                code = ord(char)
                encrypted_code = base_char ^ code 
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
    
def convertName(fullName):
    newName = []
    newName2 = []
    oldName = unidecode(fullName)
    oldName = oldName.strip().split(" ")
    newName.append(oldName[-1])
    newName.append(oldName[0])
    newName2.extend([name.lower() for name in oldName[1:-1]])
    newName = newName + newName2
    newName = " ".join(newName)
    newName = newName.split(" ")
    if len(newName) > 1:
        newName = newName[0] + " " + newName[1] + "".join(newName[2:])
    return newName

df = pd.read_excel(r'CIMITAR Access Request TEST_MFG - 21.09.2024 (update).xlsx')
df = df.fillna('')
badgeno = ""
userid = ""
username = ""
usergroup = ""
mailaddress = ""
decode = ""

for index, line in df.iterrows():
    # print(f"------Row--{index}----------------")
    badgeno = line.iloc[1]
    userid = line.iloc[2]
    username = convertName(line.iloc[3])

    if "@" in str(line.iloc[4]):
        mailaddress = line.iloc[4]
    else:
        mailaddress = ""
    usergroup = line.iloc[6]
    
    sqlInsertQuery = f"""INSERT INTO CIMitar_AppConfig.dbo.UserSetting
    (badgeno, userid, userpw, username, usergroup, mailaddress, onfactory, auth, firstlogin, lastlogin, lastupdate, checktime, varsion, islive, userstring1, userstring2, userstring3, userstring4, userstring5, userstring6, userstring7, userstring8, userstring9, userstring10, Trycount, Lock)
    VALUES('{badgeno}', '{userid}', '{EncryptionPass.base_encryption(str(badgeno))}','{username}', '{usergroup}', '{mailaddress}', '000000000000001', '000000000000001', getdate(), getdate(), getdate(), getdate(), '', 1, '', '', '', '', '', '', '', '', '', '', 0, 0);"""
    # print(sqlInsertQuery)
    # decode = EncryptionPass.base_encryption(str(badgeno))
    print(username)

    # try:
    #     # cursor.execute(sqlInsertQuery)
    #     # cursor.commit()
    #     # print(username)
    # except:
    #     cursor.close()
    #     conn.close()

# print(EncryptionPass.base_encryption(str(230183)))

# cursor.close()
# conn.close()
