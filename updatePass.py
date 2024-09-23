import pyodbc, os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

connectionStr = "DRIVER={ODBC Driver 17 for SQL Server}" 
connectionStr += ";SERVER=" + os.environ["Server"] + "," + os.environ["Port"] 
connectionStr +=  ";DATABASE=" + os.environ["Database"] 
connectionStr += ";UID=" + os.environ["User"] 
connectionStr += ";PWD=" + os.environ["Password"]
conn = pyodbc.connect(connectionStr)
cursor = conn.cursor()

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

def process_badgeno(badgeno: str, uid: int,  execute_sql=False):
    if badgeno == "":
        st.write("Please enter badgeno")

    else:
        total_comand = 0
        for ind in badgeno.split('\n'):
            ind = ind.strip()
            enscrypt = EncryptionPass.base_encryption(str(ind))
            sqlInsertQuery = f"""UPDATE CIMitar_AppConfig.dbo.UserSetting 
            Set userpw = '{enscrypt}'
            WHERE uid = {uid}  """
            uid += 1
            total_comand += 1

            if execute_sql:
                cursor.execute(sqlInsertQuery)
                cursor.commit()
                if cursor.rowcount > 0:
                    st.write("Insert successful")
                else:
                    st.write("Insert failed")
                st.write(f"Excute : {sqlInsertQuery}")
            else:
                st.write(sqlInsertQuery)
        st.write(f"Total command performed = {total_comand}")

st.header("Update Password for Cimitar Account")
badgeno = st.text_area(
    "Enter badgeno",
    height=400
)
uid = st.number_input("uid start from")

bt_checkPW = st.button("Check Before Update")
bt_update = st.button("Update Password")

if bt_checkPW:
    process_badgeno(badgeno, uid)

if bt_update:
    process_badgeno(badgeno, uid, execute_sql=True)

cursor.close()
conn.close()




