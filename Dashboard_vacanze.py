
#%pip install gspread
#%pip install streamlit
import gspread
import pandas as pd
import streamlit as st
import json

st.set_page_config(layout="wide")

# Logica di autenticazione
if "gcp_service_account" in st.secrets:
    # 1. Leggiamo la stringa di testo dai Secrets
    stringa_json = st.secrets["gcp_service_account"]["json_string"]
    # 2. La trasformiamo in un vero dizionario Python
    dati_credenziali = json.loads(stringa_json)
    # 3. Passiamo il dizionario a gspread
    service_account = gspread.service_account_from_dict(dati_credenziali)
else:
    # Codice per il tuo PC (OneDrive)
    path = r'C:\Users\puglisil\...\chiave.json'
    service_account = gspread.service_account(filename=path)

nome_foglio = service_account.open_by_key('1Ti60AlQgYqOUlFQOjKOSGzp4OVmgdiMTpnM8F3FQML4').sheet1

dizionario=nome_foglio.get_all_records()
df=pd.DataFrame(dizionario)
groupby_stanze=df.groupby('Tipologia Stanza').agg(Tipologia_Stanza= ('Tipologia Stanza','count'))
count_stanze=df['Tipologia Stanza'].value_counts()


iscritti_adulti1=len(df['Cognome Nome Adulto 1'])
iscritti_adulti2=len(df[df['Cognome Nome Adulto 2']!='']['Cognome Nome Adulto 2'])
iscritti_adulti3=len(df[df['Cognome Nome Adulto 3']!='']['Cognome Nome Adulto 3'])
iscritti_adulti4=len(df[df['Cognome Nome Adulto 4']!='']['Cognome Nome Adulto 4'])
iscritti_adulti5=len(df[df['Cognome Nome Adulto 5']!='']['Cognome Nome Adulto 5'])

iscritti_bambini_1=len(df[df['Cognome Nome Ragazzo Bambino 1']!='']['Cognome Nome Ragazzo Bambino 1'])
iscritti_bambini_2=len(df[df['Cognome Nome Ragazzo Bambino 2']!='']['Cognome Nome Ragazzo Bambino 2'])
iscritti_bambini_3=len(df[df['Cognome Nome Ragazzo Bambino 3']!='']['Cognome Nome Ragazzo Bambino 3'])
iscritti_bambini_4=len(df[df['Cognome Nome Ragazzo Bambino 4']!='']['Cognome Nome Ragazzo Bambino 4'])
iscritti_bambini_5=len(df[df['Cognome Nome Ragazzo Bambino 5']!='']['Cognome Nome Ragazzo Bambino 5'])
iscritti_adulti= iscritti_adulti1+iscritti_adulti2+iscritti_adulti3+iscritti_adulti4+iscritti_adulti5
iscritti_ragazzi_bambini=iscritti_bambini_1+iscritti_bambini_2+iscritti_bambini_3+iscritti_bambini_4+iscritti_bambini_5
iscritti_totali=iscritti_adulti+iscritti_ragazzi_bambini

st.title('Dashboard vacanze Zafferana Etnea')

iscritti_totale_col, iscritti_adulti_col, iscritti_bambini_col = st.columns(3)

with iscritti_totale_col:
    st.metric('Totale iscritti', iscritti_totali) # Usa "st", non il nome della colonna!

with iscritti_adulti_col:
    st.metric('Adulti iscritti', iscritti_adulti)

with iscritti_bambini_col:
    st.metric('Ragazzi bambini iscritti', iscritti_ragazzi_bambini)


st.bar_chart(count_stanze)

st.dataframe(df)

st.balloons()
