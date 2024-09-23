import streamlit as st

st.set_page_config(layout="wide", page_title="ATV Cimitar Account Register", page_icon="logo/C_logo.png")
                   
register_acc = st.Page(
    page="userRegister_streamlit.py",
    title="Cimitar Account Register",
    icon=":material/account_circle:",
    default=True
)

update_password = st.Page(
    page = "updatePass.py",
    title="Update Password",
    icon=":material/security:"
)

pg = st.navigation(
    {
        "Register": [register_acc],
        "Update Password" : [update_password]
    }
)

st.logo("logo/cimitar_acc.png")
st.sidebar.text("♨️ ATV Test IT")

pg.run()