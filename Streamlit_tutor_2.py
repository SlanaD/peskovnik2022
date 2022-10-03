## SLD 2022-10-02
#to run local:
# py -m streamlit run Dataframe_compare_streamlit.py
#
#Prepared for streamlit.io

import streamlit as st
import pandas as pd
import numpy as np

def highlight_diff(data, color='yellow'):
    attr = 'background-color: {}'.format(color)
    other = data.xs('self', axis='columns', level=-1)
    return pd.DataFrame(np.where(data.ne(other, level=0), attr, ''),
                        index=data.index, columns=data.columns)
    


st.title('Primerjaj dva mesečna izvoza')

#path_xlsx_A = r"C:\Users\slanad\OneDrive\Dokumenti\Palfinger\DATA\Tests\2022-07.xlsx"
#path_xlsx_B = r"C:\Users\slanad\OneDrive\Dokumenti\Palfinger\DATA\Tests\2022-09.xlsx"
sheet_name_A = "DATA2"
sheet_name_B = "DATA2"

path_xlsx_A = st.file_uploader("Izberi mesec A:")
if path_xlsx_A is not None:
     ##read xlsx
     dfA = pd.read_excel(path_xlsx_A, sheet_name=sheet_name_A, header=0,).iloc[:,0:7]
#     st.dataframe(df1)

path_xlsx_B = st.file_uploader("Izberi mesec B:")
if path_xlsx_B is not None:
     ##read xlsx
     dfB = pd.read_excel(path_xlsx_B, sheet_name=sheet_name_B, header=0,).iloc[:,0:7]
#     st.dataframe(df1)


if st.button('PREVERI'):
    with st.spinner("Training ongoing"):


        #Novi sodelavci
        dft=pd.merge(dfB,dfA,on=['MS'],how="outer",indicator=True)
        dft=dft[dft['_merge']=='left_only'].iloc[:,1:6]

        st.subheader(f"Novi sodelavci: {len(dft)}")
        st.dataframe(dft)   

        #Niso več v seznamu
        dft=pd.merge(dfA,dfB,on=['MS'],how="outer",indicator=True)
        dft=dft[dft['_merge']=='left_only'].iloc[:,1:6]

        st.subheader(f"Niso več na seznemu: {len(dft)}")
        st.dataframe(dft)  


        vse_MS = (sorted( set(dfA["MS"]).union( set(dfB["MS"]) ) )) #tukaj so vse maticne iz obeh datotek
        dfTemp = pd.DataFrame(list(vse_MS),columns=["MS_all"])
        dfAA = dfTemp.merge(dfA, how='outer', left_on="MS_all", right_on="MS")
        dfBB = dfTemp.merge(dfB, how='outer', left_on="MS_all", right_on="MS")

        #in A is old in B is new - this is an agreement (). B=self, A=other

        dfCC = dfBB.compare(dfAA, keep_equal=True, keep_shape=False)

        st.subheader(f"Ostale spremembe:")
        #st.text("pritisni check.box za prikaz")
        #checkbox
        #Spremembe pri tistih, ki so ostali
        dft = dfCC[dfCC.MS.self.notnull() & dfCC.MS.other.notnull()==True]
        #if st.checkbox('Spremembe pri ne-novih novih'):
        st.table(dft.style.apply(highlight_diff, axis=None))

        #Vse spremembe
        #if st.checkbox('Pokaži vse spremembe'):
        #st.dataframe(dfCC.style.apply(highlight_diff, axis=None))
            

