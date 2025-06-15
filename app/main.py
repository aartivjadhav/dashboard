
import streamlit as st
st.set_page_config(page_title="",layout='wide')
import Visuals.charts as ch

if 'page' not in st.session_state:
    st.session_state.page = 'Overview'

# Sidebar buttons
if st.sidebar.button("Overview"):
    st.session_state.page = "Overview"

if st.sidebar.button("Performance Rating"):
    st.session_state.page = "Employee Performance"

if st.sidebar.button("Attrition Analysis"):
    st.session_state.page = "Attrition Analysis"

# Show content based on current page stored in session state
if st.session_state.page == "Overview":
    ch.Overview()

elif st.session_state.page == "Employee Performance":
    ch.Employee_Performance()

elif st.session_state.page == "Attrition Analysis":
    ch.Attrition_Analysis()

########################################################################################
# age and distancefromhome binning
# convert date to datetime?
# HR Overview page
# department wise - number of employees, aittrated employees, avg age, avg salary, avg years at company, 
# gender pie chart or donut chart
# statewise total employees
# ethinicity and total employees
# year and Total Employees

# Aitration page
# atrition by age, salary, experience, satisfaction, rating

# forecast
# forecasting atrition rate
