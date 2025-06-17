import streamlit as st
import pandas as pd
import datetime

Education_level = pd.read_csv('app/data/EducationLevel.csv') 

Employee = pd.read_csv('app/data/Employee.csv')

PerformanceRating = pd.read_csv('app/data/PerformanceRating.csv')

RatingLevel = pd.read_csv('app/data/RatingLevel.csv')

SatisfiedLevel = pd.read_csv('app/data/SatisfiedLevel.csv')

merge_data_emp = pd.merge(PerformanceRating,Employee,how='left',on='EmployeeID')    
data = pd.merge(merge_data_emp,Education_level,how='left',left_on='Education',right_on='EducationLevelID')
data['ReviewDate'] = pd.to_datetime(data['ReviewDate'],errors='coerce').dt.date
data['HireDate'] = pd.to_datetime(data['HireDate'],errors='coerce').dt.date

def metrices_calculation():
    metrices = pd.DataFrame([{
        'total_emp':Employee['EmployeeID'].nunique(),
        'active_emp':Employee[Employee['Attrition']=='No']['EmployeeID'].nunique(),
        'inactive_emp':Employee[Employee['Attrition']=='Yes']['EmployeeID'].nunique(),
        'attrition_rate':(Employee[Employee['Attrition'] == 'Yes']['EmployeeID'].nunique() / Employee['EmployeeID'].nunique()) * 100,
        'female_emp':Employee[Employee['Gender']=='Female']['EmployeeID'].count(),
        'male_emp':Employee[Employee['Gender'] == 'Male']['EmployeeID'].count()}])
    return metrices
#######################################################################################################################################
# Attrition rate is calculated as 
# attrition rate = (total inactive employees in year(x) / average employees in year(x)) * 100

# average employees = (total employees at the start of the year + total employees at end of the year) / 2

# but I dont have the date information so i am calculating the attrition rate as
# attrition rate = (inactive employees / total Employees) * 100
########################################################################################################################################
        
        ###########################################################################################################
        # stacked bar chart for attrition by year
        ###########################################################################################################
def attrition_by_year():
    df = Employee[['HireDate','Attrition','EmployeeID']]
    df['HireYear'] = pd.to_datetime(df['HireDate']).dt.year
    chart_data= df.groupby(['HireYear','Attrition'])['EmployeeID'].size().unstack(fill_value=0).reset_index()
    chart_data.rename(columns={'Yes':'Inactive','No':'Active'},inplace=True)
    return chart_data
    ######################################################################################################## 
    # PIE CHART for gender
    ########################################################################################################    
def total_emps_by_gender(attrition_analysis:bool):
    gender_data = Employee.groupby('Gender')['EmployeeID'].count()
    if attrition_analysis==True:
        inactive_emp = Employee[Employee['Attrition']=='Yes']
        inactive_by_gender = inactive_emp.groupby(['Gender'])['EmployeeID'].count()
        attrition_by_gender = round(inactive_by_gender/gender_data*100,2).reset_index()
        attrition_by_gender = attrition_by_gender.sort_values(by='EmployeeID', ascending=False)
        return attrition_by_gender
    else:
        gender_data = gender_data.reset_index()
        return gender_data
    #######################################################################################
    # 100% stacked Column chart for Age-range and gender
    #########################################################################################
    # with col3:
def emps_by_age(attrition_analysis:bool):
    bins = [0,18,30,40,50]
    labels = ["<=18","19-30","31-40","41-50"]
    Employee['Age-Range'] = pd.cut(Employee['Age'],bins=bins,labels=labels)

    if attrition_analysis==True:
        emp_by_age_range = Employee.groupby(['Age-Range'])['EmployeeID'].count()
        df = Employee[Employee['Attrition']=='Yes']
        inactive_by_age_range = df.groupby(['Age-Range'])['EmployeeID'].count()
        attrition_by_age = round(inactive_by_age_range/emp_by_age_range*100,2).reset_index()
        # attrition_by_age = attrition_by_age.sort_values(by='EmployeeID')
        return attrition_by_age
    else:
    # data.drop('EducationLevelID',axis=1,inplace=True)
        Emp_by_Age = Employee.groupby(['Age-Range', 'Gender']).size().unstack(fill_value=0).reset_index()
        Emp_by_Age['Sum'] = Emp_by_Age[['Female','Male','Non-Binary','Prefer Not To Say']].sum(axis=1)
        Percent_Emp_By_Age = pd.DataFrame()
        Percent_Emp_By_Age['Age-Range'] = Emp_by_Age['Age-Range']

        for col in Emp_by_Age.columns[1:5]:
                # st.write(col)
            Percent_Emp_By_Age[col] = (Emp_by_Age[col] / Emp_by_Age['Sum']) * 100
            Percent_Emp_By_Age = Percent_Emp_By_Age.round(2)
            # st.write(Emp_by_Age)
            # st.write(Percent_Emp_By_Age)
        return Percent_Emp_By_Age   

    ############################################################# 
    # BAR CHART - deparment by employee count
    ###############################################################################
 
def attrition_by_department():
    Tree_Data = Employee.groupby(['Department','JobRole','Attrition']).size().reset_index(name='Count')
        # Tree_Data['Root'] = 'Departments'
    Tree_Data['Attrition'] = Tree_Data['Attrition'].replace({'Yes': 'Inactive', 'No': 'Active'})
    return Tree_Data
    ##########################################################################################################################
    # Grouped bar chart - total employees education level and departments
    ##########################################################################################################################
    
def total_emps_by_education(attrition_analysis:bool):
    Emp_Edu = pd.merge(Employee,Education_level,
                        left_on='Education',
                        right_on='EducationLevelID',
                        how='left')
    Emp_Edu = Emp_Edu[['Department','EducationLevel','Attrition']]
    if attrition_analysis==True:
        total_emps_edu = Emp_Edu.groupby(['EducationLevel']).size()
        df = Emp_Edu[Emp_Edu['Attrition']=='Yes']
        inactive_emp = df.groupby(['EducationLevel']).size()
        attrition_by_EduLevel = round(inactive_emp/total_emps_edu*100,2).reset_index()
        return attrition_by_EduLevel
    else:    
        chart_data = Emp_Edu.groupby(['Department','EducationLevel']).size().reset_index(name='Total Employees')
        return chart_data
     
########################################################################################################################
        # line and bar chart for ethinicity and salary
########################################################################################################################
def emps_by_ethnicity_salary():
    emp_count = Employee.groupby('Ethnicity')['EmployeeID'].count().reset_index()
    avg_salary = Employee.groupby('Ethnicity')['Salary'].mean().round(2).reset_index()
    chart_data = emp_count.merge(avg_salary,how='inner',on='Ethnicity')
    chart_data = chart_data.sort_values(by='EmployeeID',ascending=False)
    return chart_data

########################################################################################################################
        # attrition by salary range
######################################################################################################################## 
def attrition_by_salary_range():
    bins = [0,100000,200000,300000,400000,500000,600000]
    labels = ["<=100K","100K-200K","200K-300K","300K-400K","400K-500K",">500"]
    Employee['Salary-Range'] = pd.cut(Employee['Salary'],bins=bins,labels=labels)
    total_emps_by_salary_range = Employee.groupby(['Salary-Range'])['EmployeeID'].count()
    df = Employee[Employee['Attrition'] == 'Yes']
    inactive_emps = df.groupby(['Salary-Range'])['EmployeeID'].count()
    attrition_by_salary_range = round(inactive_emps/total_emps_by_salary_range*100,2).reset_index()
    return attrition_by_salary_range

########################################################################################################################
        # attrition by job satisfaction
######################################################################################################################## 
def attrition_by_job_satisfaction():
    df = data[['EmployeeID','JobSatisfaction','Attrition']]
    # total_emps_by_satlevel = df.groupby()
    df = data.groupby(['EmployeeID','Attrition'])['JobSatisfaction'].mean().reset_index()
    df['JobSatisfaction'] = round(df['JobSatisfaction'],0)
    total_emps = df.groupby(['JobSatisfaction'])['EmployeeID'].count()
    df1 = df[df['Attrition']=='Yes']
    inactive_emps = df1.groupby(['JobSatisfaction'])['EmployeeID'].count()
    inactive_emps = inactive_emps.reindex(total_emps.index, fill_value=0)
    attrition_rate = round(inactive_emps/total_emps*100,2).reset_index()
    return attrition_rate

########################################################################################################################
        # attrition by state
######################################################################################################################## 
def statewise_attrition():
    total_emp_state = Employee.groupby(['State'])['EmployeeID'].count()
    df = Employee[Employee['Attrition']=='Yes']
    inactive_emp_by_state = df.groupby(['State'])['EmployeeID'].count()
    attrition_by_state = round((inactive_emp_by_state/total_emp_state)*100,2)
    attrition_by_state = attrition_by_state.reset_index()
    return attrition_by_state

########################################################################################################################
        # details table
######################################################################################################################## 
def details_table():
    df = round(data.groupby(['JobRole','Department'])[['Salary','Age','YearsAtCompany']].mean(),2)
    unique_count_df = data.groupby(['JobRole', 'Department'])['EmployeeID'].nunique().rename('TotalEmployees')
    final_df = df.join(unique_count_df)
    
    attrited = data[data['Attrition']=='Yes'].groupby(['JobRole','Department'])['EmployeeID'].nunique().rename('AttritionCount')
    final_df = final_df.join(attrited)
    final_df['%Attrition'] = round(final_df['AttritionCount']/final_df['TotalEmployees']*100,2)

    df1 = data[data['Gender']=='Male'].groupby(['JobRole','Department'])['EmployeeID'].nunique().rename('Males').reset_index()
    df2 = data[data['Gender']=='Female'].groupby(['JobRole','Department'])['EmployeeID'].nunique().rename('Females').reset_index()
    df1 = pd.merge(df1, df2, on=['JobRole', 'Department'], how='outer').fillna(0)
    
    df1['GenderRatio'] = round(df1['Males']/df1['Females']*100,2)
    df1.set_index(['JobRole', 'Department'], inplace=True)
    final_df = final_df.join(df1['GenderRatio'])
    final_df.fillna(0,inplace=True)
    final_df.reset_index(inplace=True)
    final_df.sort_values(by=['Department'],inplace=True)
    return final_df

########################################################################################################################
        # grouped stacked chart
########################################################################################################################
def grouped_stacked_chart():
    df1 = data.drop_duplicates(subset=['EmployeeID'])
    df1['HireDate'] = pd.to_datetime(df1['HireDate'])
    df1['HireYear'] = df1['HireDate'].dt.year
    df1 = df1[['HireDate','HireYear','Department','Attrition','EmployeeID']]
        
    totalemps = df1.groupby(['HireYear','Department'])['EmployeeID'].count().rename('TotalEmps')
    attrited = df1[df1['Attrition']=='Yes'].groupby(['HireYear','Department'])['EmployeeID'].count().rename('Inactive')
    totalemps = pd.merge(totalemps,attrited,how='left',on=['HireYear','Department'])
    totalemps['Active'] = totalemps['TotalEmps'] - totalemps['Inactive']
    totalemps['%AttritionRate'] = round(totalemps['Inactive']/totalemps['TotalEmps']*100,2)
    totalemps.fillna(0,inplace=True)

    df2 = totalemps.reset_index()[['HireYear', 'Department', 'Active', 'Inactive']]
    df_wide = df2.pivot(index='HireYear', columns='Department')
    df_wide = df_wide.swaplevel(axis=1).sort_index(axis=1, level=0)
    df_wide = df_wide.rename(columns={'Human Resources': 'HR'}, level=0)
    return df_wide
########################################################################################

########################################################################################################################
        # prepare data for employee overview line charts
########################################################################################################################
def prepare_data(item,selected_emp_id):
    df = data[data["EmployeeID"]==selected_emp_id][[item,'ReviewDate']]
    df['ReviewYear'] = pd.to_datetime(df['ReviewDate']).dt.year
    chart_data = df.groupby(['ReviewYear'])[item].mean().reset_index()
    return chart_data
