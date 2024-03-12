from dotenv import load_dotenv
load_dotenv() ## load all the environemnt variables

import streamlit as st
import os
import sqlite3

import google.generativeai as genai
## Configure Genai Key

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

import pandas as pd
from datetime import datetime
import streamlit.components.v1 as components
import base64
import json

## Function To Load Google Gemini Model and provide queries as response

def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],question])
    return response.text

## Fucntion To retrieve query from the database

def read_sql_query(sql,db):
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows
    
def getDataFrameFromSQLQuery(sql,db):
    conn=sqlite3.connect(db)
    df=pd.read_sql_query(sql,con=conn)
    return df 
    
## Define Your Prompt
prompt=[
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, 
    SECTION,MARKS \n\nFor example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ;
    \nExample 2 - Tell me all the students studying in Data Science class?, 
    the SQL command will be something like this SELECT * FROM STUDENT 
    where CLASS="Data Science"; 
    \Example 3 - Average Marks of Students Class wise ?
    the SQL command will be something like this select CLASS,AVG(MARKS)  from  STUDENT group by CLASS
    also the sql code should not have ``` in beginning or end and sql word in output

    """


]

def download_button(object_to_download, download_filename):
    """
    Generates a link to download the given object_to_download.
    Params:
    ------
    object_to_download:  The object to be downloaded.
    download_filename (str): filename and extension of file. e.g. mydata.csv,
    Returns:
    -------
    (str): the anchor tag to download object_to_download
    """
    if isinstance(object_to_download, pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False)

    # Try JSON encode for everything else
    else:
        object_to_download = json.dumps(object_to_download)

    try:
        # some strings <-> bytes conversions necessary here
        b64 = base64.b64encode(object_to_download.encode()).decode()

    except AttributeError as e:
        b64 = base64.b64encode(object_to_download).decode()

    dl_link = f"""
    <html>
    <head>
    <title>Start Auto Download file</title>
    <script src="http://code.jquery.com/jquery-3.2.1.min.js"></script>
    <script>
    $('<a href="data:text/csv;base64,{b64}" download="{download_filename}">')[0].click()
    </script>
    </head>
    </html>
    """
    return dl_link




## Streamlit App

st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Gemini App To Retrieve SQL Data")



def downloadCSVFileFromPromtToSQL():
    question = st.session_state['input']
    question_v2 = str(question)
    print("Question Stream lit ",question_v2)
    
    if not question_v2 == "" or not question_v2 == "None" :
        response=get_gemini_response(question_v2,prompt)
    else:
        response = "select CLASS,AVG(MARKS)  from  STUDENT group by CLASS "
    print("Response Query ", response)
    df=getDataFrameFromSQLQuery(response,"student.db")
    #st.subheader("The Response SQL Query is ")
    #st.header(response)
    #st.header("No of Rows "+str(df.shape[0]) +" and No of Columns "+str(df.shape[1]))
    print("No of Rows ",df.shape[0],"\tNo of Columns",df.shape[1])
    datetime_stamp = f"{datetime.now().strftime('%Y%m%d%H%M%S')}"
    file_name=f'data_{datetime_stamp}.csv'
    components.html(download_button(df,file_name),height=0)
    

#submit=st.button("Ask the question")

with st.form("my_form", clear_on_submit=False):
    #if 'input' not in st.session_state:
    #    st.session_state['input'] = "average marks by class wise"
    st_input=st.text_area("Input: ",key="input",value="average marks by class wise")
    st.form_submit_button("Ask the question",on_click=downloadCSVFileFromPromtToSQL,args=[])
