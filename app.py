from enum import auto
from turtle import title

from numpy import histogram
import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go

st.markdown("<h1 style='text-align: center;'>Voting Machine</h1>",
            unsafe_allow_html=True)
df = pd.read_csv('Voter_data.csv')
df.index = df.index + 1
df2 = pd.read_csv('voted.csv')
if"button_clicked" not in st.session_state:
    st.session_state.button_clicked = False

def callback():
    st.session_state.button_clicked = True
    
selected = option_menu(
    menu_title=None,
    options=["Vote", "Result", "Refresh"],
    orientation="horizontal"
)

if selected == "Vote":
    voting_form = st.form("Form")
    voter_id = voting_form.text_input("Enter Voter Id")
    vote = voting_form.radio("Party", ["BJP", "Congress", "AAP", "NOTA"])
    submit = voting_form.form_submit_button("Vote")
    if submit:
        if (df.iat[int(voter_id)-1, df.columns.get_loc('Voted')] != 1):
            df.iat[int(voter_id)-1, df.columns.get_loc('Voted')] = 1
            df.to_csv("Voter_data.csv", index=False)
            df2 = df2.append({'Voted': vote}, ignore_index=True)
            df2.to_csv("voted.csv", index=False)
            st.success("Voted Successfully")
        else:
            st.error("You have already voted") 
if selected == "Result":
    bjp = df2['Voted'].value_counts()['BJP']
    aap = df2['Voted'].value_counts()['AAP']
    congress = df2['Voted'].value_counts()['Congress']
    nota = df2['Voted'].value_counts()['NOTA']
    total_votes = [bjp, aap, congress, nota]
    val_count  = df['Voted'].value_counts()
    maxi = max(total_votes)
    if(bjp == maxi):
        winner = "BJP"
    elif(aap == maxi):
        winner = "AAP"
    elif(congress == maxi):
        winner = "Congress"
    elif(nota == maxi):
        winner = "NOTA"
    st.header("Winner is " + winner + " with " + str(maxi) + " votes")
    list1 = ['AAP', 'Congress', 'BJP', 'NOTA']
    list2 = [aap, congress, bjp, nota]
    fig = go.Figure(
        go.Pie(
        labels = list1,
        values = list2,
        hoverinfo = "label+percent",
        textinfo = "value"
    ))
    st.header("Votes Distribution")
    st.plotly_chart(fig)
    x = df[df["Voted"] == 1.0]
    st.header("Agewise Distribution of Voters")
    fig = go.Figure(data=[go.Histogram(x=x['Age'])])
    st.plotly_chart(fig)
    st.subheader("Total Votes: " + str(sum(total_votes)))
    st.subheader("BJP Votes: " + str(bjp))
    st.subheader("AAP Votes: " + str(aap))
    st.subheader("Congress Votes: " + str(congress))
    st.subheader("NOTA Votes: " + str(nota))
    total_percentage = sum(total_votes)/20 * 100
    st.subheader("Total percentage of voting is "+ str(total_percentage) + "%")
    

   
if selected == "Refresh":
    st.balloons()
    st.success("Go to Vote for voting")
