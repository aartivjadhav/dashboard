import streamlit as st
import pandas as pd
# import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import datetime
import data.data_extraction as de
import numpy as np

def Overview():
    st.header('HR Data Analysis')
    cols = st.columns(6)
    metrices = de.metrices_calculation()
    # st.write(metrices)
    with cols[0]:
        st.metric(label="Total Employees", value=metrices['total_emp'])
    with cols[1]:
        st.metric(label="Active Employees", value=metrices['active_emp'])
    with cols[2]:
        st.metric(label="Inactive Employees", value=metrices['inactive_emp'])
    with cols[3]:
        st.metric(label="Attrition Rate", value=f"{round(metrices['attrition_rate'].iloc[0],2)}%")
    with cols[4]:
        st.metric(label="Females", value=metrices['female_emp'])
    with cols[5]:
        st.metric(label="Males", value=metrices['male_emp'])
    
    
    ############################################################# 
    # BAR CHART - deparment by employee count
    ###############################################################################
    
    col1,col2,col3 = st.columns([1,1,1])
    with col1:
        ###########################################################################################################
        # stacked bar chart for attrition by year
        ###########################################################################################################
        chart_data = de.attrition_by_year()
        # st.write(chart_data)
        fig = go.Figure()
        attrition = ['Active','Inactive']
        colors = {'Inactive':'#DAA520','Active':'#2E8B57'}
        for a in attrition:
            fig.add_trace(go.Bar(
                x=chart_data["HireYear"],
                y=chart_data[a],
                name=a,
                marker=dict(color=colors[a]),
                text=chart_data[a],
                textposition='inside',
                textangle=0,
                hovertemplate=(
                    "<b>Year:</b> %{x}<br>" +
                    "<b>Employees:</b> %{y}<extra></extra>"
                )
                ))
        fig.update_layout(barmode='stack',
                           xaxis=dict(
                            tickmode='linear',
                            tickangle=-40,
                            # showticks=True    
                        ),
                        title='Total Employees by year')
        st.plotly_chart(fig,use_container_width=True)
    
    with col2:
    ######################################################################################################## 
    # PIE CHART for gender
    ######################################################################################################## 

        # gender_data = data.groupby('Gender')['EmployeeID'].count().reset_index()
        gender_data = de.total_emps_by_gender(attrition_analysis=False)
        fig = px.pie(gender_data, names='Gender', values='EmployeeID', hole=0.7,
                title="Number of Employees by Gender")
        st.plotly_chart(fig,use_container_width=True)

    #######################################################################################
    # 100% stacked Column chart for Age-range and gender
    #########################################################################################
    with col3:
               
    # Create traces for each gender
        Percent_Emp_By_Age = de.emps_by_age(attrition_analysis=False)
        fig = go.Figure()
        genders = ['Female', 'Male', 'Non-Binary', 'Prefer Not To Say']

        for gender in genders:
            fig.add_trace(go.Bar(
                x=Percent_Emp_By_Age['Age-Range'],
                y=Percent_Emp_By_Age[gender],
                name=gender,
                hovertemplate=(
                f"<b>Gender:</b> {gender}<br>" +
                "<b>Percent:</b> %{y:.1f}%<extra></extra>"
                )
            ))

        # Update layout for 100% stacked bar
        fig.update_layout(
            title="Percentage of Employees by Age Range <br>and Gender",
            barmode='stack',
            yaxis=dict(title='Percentage'),
            xaxis=dict(title='Age Range'),
            legend_title="Gender",
            # height=450
        )
        st.plotly_chart(fig,use_container_width=True)

    #########################################################################################################
    # Icicle chart - active and inactive employees by department and job role
    #########################################################################################################
    col4 = st.columns(1)[0]
    with col4:
       
        # Icicle chart
        Tree_Data = de.attrition_by_department()
        fig = px.icicle(
            Tree_Data,
            path=[px.Constant('Departments'),'Department', 'JobRole', 'Attrition'],  # Hierarchical order
            values='Count',
            title='Employee Distribution by Department and Role',
            color='Attrition',
            color_discrete_sequence=['seaGreen', 'LightCoral']
        )
        fig.update_traces(hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percent: %{percentRoot:.2%}')
        
        fig.update_layout(margin=dict(t=50, l=25, r=25, b=25),
                            height=450,
                            width=800  
                        )

        st.plotly_chart(fig,use_container_width=True)

    col5,col6 = st.columns([1,1])
    ##########################################################################################################################
    # Grouped bar chart - total employees education level and departments
    ##########################################################################################################################
    with col5:
        chart_data = de.total_emps_by_education(attrition_analysis=False)
        fig = px.bar(chart_data, 
                    x="EducationLevel", 
                    y="Total Employees",
                    color='Department', 
                    barmode='group', 
                    height=450,
                    title='Employee Distribution by Education',
                    text="Total Employees")
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig,use_container_width=True)

    with col6:
        ########################################################################################################################
        # line and bar chart for ethinicity and salary
        ########################################################################################################################
      
        chart_data = de.emps_by_ethnicity_salary()
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=chart_data['Ethnicity'],
            y=chart_data['EmployeeID'],
            name='Total Employees',
            marker=dict(color='#DAA520')
        ))

        # Line chart: Average salary
        fig.add_trace(go.Scatter(
            x=chart_data['Ethnicity'],
            y=chart_data['Salary'],
            name='Average Salary',
            mode='lines+markers+text',
            text=chart_data['Salary'],
            textposition='top center',
            yaxis='y2',
            line=dict(color='#2E8B57', width=3),    
            marker=dict(color='#2E8B57', size=8)
        ))

        fig.update_layout(
            height=450,
            title='Employee Count and Average Salary by Ethnicity',
            xaxis_title='Ethnicity',
            yaxis=dict(title='Employee Count'),
            yaxis2=dict(
                title='Average Salary',
                overlaying='y',
                showticklabels=False,
                showgrid=False,
                side='right'
            ),
            legend=dict(x=0.5, xanchor='right'),
            margin=dict(t=50, b=50)
        )
        st.plotly_chart(fig,use_container_width=True)

    

# if st.sidebar.button("Employee Performance"):
def Employee_Performance():
    st.header("Performance Rating")
    col1,col2,col3 = st.columns(3,gap="small")

    with col1:
        name_to_id = {"None": None}
        for _, row in de.data.iterrows():
            full_name = f"{row['FirstName']} {row['LastName']}"
            name_to_id[full_name] = row['EmployeeID']
            
        selected_name = st.selectbox("Employee Name:", options=list(name_to_id.keys()))
        selected_emp_id = name_to_id[selected_name]
        
    def line_chart(chart_data):
        y_col = chart_data.columns[1]
        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=chart_data['ReviewYear'],
                y=chart_data[y_col],
                mode='lines+markers',
                name=y_col
            )
        )

        fig.update_layout(
            height = 400,
            title=f'Average {y_col} by Year',
            xaxis=dict(
                type='category',
                tickangle=-45,
            ),
            yaxis=dict(
                tickvals=np.arange(1, 6),  # ticks from 1 to 5
                range=[.8, 5.2],      #visible y-axis range
                dtick=1,
            ),
        )
        st.plotly_chart(fig)
    
    items = ['EnvironmentSatisfaction', 'JobSatisfaction', 'RelationshipSatisfaction', 'WorkLifeBalance', 'SelfRating', 'ManagerRating']
    rows = [items[i:i+3] for i in range(0, len(items), 3)]

    if selected_emp_id != None:
        with col2:
            fig = go.Figure(data=[go.Table(
                    header=dict(values=list(de.RatingLevel.columns),
                                fill_color='paleturquoise',
                                align='left'),
                    cells=dict(values=[de.RatingLevel.RatingID, de.RatingLevel.RatingLevel],
                            fill_color='lavender',
                            align='left'))
                ])
            fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=160)
            st.plotly_chart(fig,use_container_width=True)

        with col3:
            fig = go.Figure(data=[go.Table(
                    header=dict(values=list(de.SatisfiedLevel.columns),
                                fill_color='paleturquoise',
                                align='left'),
                    cells=dict(values=[de.SatisfiedLevel.SatisfactionID, de.SatisfiedLevel.SatisfactionLevel],
                            fill_color='lavender',
                            align='left'))
                ])
            fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=160)
            st.plotly_chart(fig,use_container_width=True)

        for row in rows:
            cols = st.columns(3)
            for col, item in zip(cols, row):
                with col:
                    # st.write(item) 
                    chart_data = de.prepare_data(item,selected_emp_id)
                    line_chart(chart_data)

####################################################################### Attrition Analysis
def Attrition_Analysis():
    st.header("Attrition Analysis")
########################################################################################################################
# statewise attrition
########################################################################################################################
    
    attrition_by_state = de.statewise_attrition()
# Create the choropleth map
    fig = px.choropleth(
        attrition_by_state,
        locations='State',         # Column with state abbreviations
        locationmode='USA-states', # use US state abbreviations
        color='EmployeeID',             # Values to color by
        scope='usa',               # Limit map to USA
        color_continuous_scale='Oranges',  # change color scale
        labels={'EmployeeID': 'Attrition Rate (%)'}
    )

    fig.update_layout(title_text='State-wise Attrition')
    st.plotly_chart(fig)
########################################################################################################################
# attrition line charts
########################################################################################################################
    def attrition_linechart(df, title='Line Chart', x_title=None, y_title=None):
        x_col = df.iloc[:,0]
        y_col = df.iloc[:,1]
        # st.write(df.columns[0],y_col)
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=x_col,
                y=y_col,
                mode='lines+markers'
            )
        )
        fig.update_layout(
            height = 400,
            title=title,
            xaxis_title = x_title,
            yaxis_title = y_title
        )
        st.plotly_chart(fig)

    col1,col2 = st.columns(2,gap='small')
    with col1:
        df = de.emps_by_age(attrition_analysis=True)
        attrition_linechart(df, title='Attrition rate by Age-Range', x_title='Age-Range', y_title='Attrition Rate(%)')

        df = de.total_emps_by_education(attrition_analysis=True)
        attrition_linechart(df, title='Attrition rate by Education Level', x_title=None, y_title='Attrition Rate(%)')

        df = de.total_emps_by_gender(attrition_analysis=True)
        attrition_linechart(df, title='Attrition rate by Gender', x_title=None, y_title='Attrition Rate(%)')

    with col2:       

        df = de.attrition_by_salary_range()
        attrition_linechart(df, title='Attrition rate by Salary-Range', x_title=None, y_title='Attrition Rate(%)')

        df = de.attrition_by_job_satisfaction()
        attrition_linechart(df, title='Attrition rate by Job Satisfaction Level', x_title=None, y_title='Attrition Rate(%)')
    
    ########################################################################################################################
    # attrition grouped stacked chart
    ########################################################################################################################
        
        df =de.grouped_stacked_chart()
        fig = go.Figure(
            layout=go.Layout(
                height=350,
                # width=1500,
                barmode="relative",
                yaxis_showticklabels=False,
                yaxis_showgrid=False,
                font=dict(size=15),
                legend_x=0,
                legend_y=1,
                legend_orientation="h",
                hovermode="closest",
                margin=dict(b=0,t=10,l=0,r=10),
                xaxis=dict(
                    tickmode="array",
                    tickvals=list(df.index),  # all ticks show
                    tickangle=0
                )
            )
        )

        colors1 = {
            "HR": {
                "Active": "#F28F1D",
                "Inactive": "#F6C619"
            },
            "Sales": {
                "Active": "#2B6045",
                "Inactive": "#5EB88A"
            },
            "Technology": {
                "Active": "#332B60",
                "Inactive": "#5EAFB8",
            }
        }

        for i, t in enumerate(colors1):
            base_values = [0] * len(df)
            
            for j, col in enumerate(df[t].columns):
                y_vals = df[t][col].values.tolist()
                fig.add_bar(
                    x=df.index,
                    y=df[t][col],
                    base=base_values,
                    # Offset the bar trace, offset needs to match the width
                    # For categorical traces, each category is spaced by 1
                    offsetgroup=str(i),
                    offset=(i - 1) * 0.25,
                    width=0.25,
                    legendgroup=t,
                    legendgrouptitle_text=t,
                    name=col,
                    marker_color=colors1[t][col],
                    marker_line=dict(width=2, color="#333"),
                    hovertemplate=f"Department: {t}<br>Year: %{{x}}<br>{col}: %{{y}}<extra></extra>"
                )            
            base_values = [a + b for a, b in zip(base_values, df[t][col])]
        st.plotly_chart(fig,use_container_width=True)   

    ########################################################################################################################
    # details table
    ########################################################################################################################
    final_df = de.details_table()
    # st.write(final_df)
    fig = go.Figure(data=[go.Table(
            columnwidth=[2,2,2,1,2,2,2,2,2],
            header=dict(values=[f"<b>{col}</b>" for col in final_df.columns],
                fill_color="#F58506",
                align='left',
                font=dict(color='black', size=12, family='Serif')
            ),
                        
            cells=dict(values=[final_df[col] for col in final_df.columns],
                fill_color="#F6F5F3",
                align='left')
            )])
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=150)
    st.plotly_chart(fig,use_container_width=True)
