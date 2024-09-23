import streamlit as st
import pandas as pd
from unidecode import unidecode
from dotenv import load_dotenv
import pyodbc, os

load_dotenv()

connectionStr = "DRIVER={ODBC Driver 17 for SQL Server}" 
connectionStr += ";SERVER=" + os.environ["Server"] + "," + os.environ["Port"] 
connectionStr +=  ";DATABASE=" + os.environ["Database"] 
connectionStr += ";UID=" + os.environ["User"] 
connectionStr += ";PWD=" + os.environ["Password"]

conn = pyodbc.connect(connectionStr)

cursor = conn.cursor()

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
    
st.header("Create Account CIMitar")

badgeno = ""
userid = ""
username = ""
usergroup = ""
mailaddress = ""
uploaded_file = st.file_uploader("Upload List Account", type=['xlsx'])
bt = st.button("Create Account")
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    df = df.fillna('')
    st.write(df)
    row_no = 0
    for index, line in df.iterrows():
        row_no += 1
        badgeno = line.iloc[1]
        userid = line.iloc[2]
        username = convertName(line.iloc[3])
        if line.iloc[4] != "":
            mailaddress = line.iloc[4]
        usergroup = line.iloc[6]       
        if bt:
            sql_badgeno = f"""SELECT badgeno FROM CIMitar_AppConfig.dbo.UserSetting WHERE badgeno = {badgeno}"""
            cursor.execute(sql_badgeno)
            check_badgeno = cursor.fetchone()
            if check_badgeno is not None:
                st.write(f"Row {row_no} :")
                st.write(f"Badge no existed : {int(check_badgeno[0])}")
            else:
                sqlInsertQuery = f"""INSERT INTO CIMitar_AppConfig.dbo.UserSetting
                (badgeno, userid, userpw, username, usergroup, mailaddress, onfactory, auth, firstlogin, lastlogin, lastupdate, checktime, varsion, islive, userstring1, userstring2, userstring3, userstring4, userstring5, userstring6, userstring7, userstring8, userstring9, userstring10, Trycount, Lock)
                VALUES({badgeno}, {userid}, '{EncryptionPass.base_encryption(str(badgeno))}','{username}', '{usergroup}', '{mailaddress}', '000000000000001', '000000000000001', getdate(), getdate(), getdate(), getdate(), '', 1, '', '', '', '', '', '', '', '', '', '', 0, 0);"""       
                cursor.execute(sqlInsertQuery)
                cursor.commit()
                st.write(f"Row {row_no} :")
                if cursor.rowcount > 0:
                    st.write("Insert successful")
                else:
                    st.write("Insert failed")
                
                st.write(sqlInsertQuery)
        
cursor.close()
conn.close()
