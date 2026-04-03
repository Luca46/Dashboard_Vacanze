
#%pip install gspread
#%pip install streamlit
import gspread
import pandas as pd
import streamlit as st
import json
import os

st.set_page_config(layout="wide")

st.set_page_config(layout="wide")

# Tentativo di recupero credenziali
creds_dict = None

# 1. Prova a vedere se siamo su Streamlit Cloud
try:
    if "gcp_service_account" in st.secrets:
        # Se siamo su Streamlit, usiamo i Secrets
        creds_dict = json.loads(st.secrets["gcp_service_account"]["json_string"])
except Exception:
    # Se NON siamo su Streamlit (es. Notebook), st.secrets darà errore. 
    # Python entrerà qui e noi gli diciamo di ignorare l'errore.
    pass

# 2. Se non abbiamo trovato nulla nei Secrets, cerchiamo il file locale
if creds_dict is None:
    path_locale = r'C:\Users\puglisil\OneDrive - UPMC\Documents\File\Personale\Tutto_Python_fatto_da_me\Esercizi_Progetti_Programmazione_Pacchetti\Progetto_Vacanza\chiave.json'
    if os.path.exists(path_locale):
        service_account = gspread.service_account(filename=path_locale)
    else:
        print("Errore: Chiave non trovata né nei Secrets né in locale!")
else:
    # Se abbiamo le credenziali dai Secrets, usiamo quelle
    service_account = gspread.service_account_from_dict(creds_dict)

nome_foglio = service_account.open_by_key('1Ti60AlQgYqOUlFQOjKOSGzp4OVmgdiMTpnM8F3FQML4').sheet1

dizionario=nome_foglio.get_all_records()

df=pd.DataFrame(dizionario)

df=df[['Cognome Nome Adulto 1','Cognome Nome Adulto 2','Cognome Nome Adulto 3','Cognome Nome Adulto 4','Cognome Nome Adulto 5','Cognome Nome Ragazzo Bambino 1','Cognome Nome Ragazzo Bambino 2','Cognome Nome Ragazzo Bambino 3','Cognome Nome Ragazzo Bambino 4','Cognome Nome Ragazzo Bambino 5','Tipologia Stanza']]

df['Adulto_1']=df['Cognome Nome Adulto 1']
df['Adulto_2']=df['Cognome Nome Adulto 2']
df['Adulto_3']=df['Cognome Nome Adulto 3']
df['Adulto_4']=df['Cognome Nome Adulto 4']
df['Adulto_5']=df['Cognome Nome Adulto 5']

df['Ragazzo_Bambino_1']=df['Cognome Nome Ragazzo Bambino 1']
df['Ragazzo_Bambino_2']=df['Cognome Nome Ragazzo Bambino 2']
df['Ragazzo_Bambino_3']=df['Cognome Nome Ragazzo Bambino 3']
df['Ragazzo_Bambino_4']=df['Cognome Nome Ragazzo Bambino 4']
df['Ragazzo_Bambino_5']=df['Cognome Nome Ragazzo Bambino 5']

df=df.drop(['Cognome Nome Adulto 1','Cognome Nome Adulto 2','Cognome Nome Adulto 3','Cognome Nome Adulto 4','Cognome Nome Adulto 5','Cognome Nome Ragazzo Bambino 1','Cognome Nome Ragazzo Bambino 2','Cognome Nome Ragazzo Bambino 3','Cognome Nome Ragazzo Bambino 4','Cognome Nome Ragazzo Bambino 5'],axis=1)


groupby_stanze=df.groupby('Tipologia Stanza').agg(Tipologia_Stanza= ('Tipologia Stanza','count'))
count_stanze=df['Tipologia Stanza'].value_counts()


iscritti_adulti1=len(df['Adulto_1'])
iscritti_adulti2=len(df[df['Adulto_2']!='']['Adulto_2'])
iscritti_adulti3=len(df[df['Adulto_3']!='']['Adulto_3'])
iscritti_adulti4=len(df[df['Adulto_4']!='']['Adulto_4'])
iscritti_adulti5=len(df[df['Adulto_5']!='']['Adulto_5'])

iscritti_adulti= iscritti_adulti1+iscritti_adulti2+iscritti_adulti3+iscritti_adulti4+iscritti_adulti5

iscritti_bambini_1=len(df[df['Ragazzo_Bambino_1']!='']['Ragazzo_Bambino_1'])
iscritti_bambini_2=len(df[df['Ragazzo_Bambino_2']!='']['Ragazzo_Bambino_2'])
iscritti_bambini_3=len(df[df['Ragazzo_Bambino_3']!='']['Ragazzo_Bambino_3'])
iscritti_bambini_4=len(df[df['Ragazzo_Bambino_4']!='']['Ragazzo_Bambino_4'])
iscritti_bambini_5=len(df[df['Ragazzo_Bambino_5']!='']['Ragazzo_Bambino_5'])

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