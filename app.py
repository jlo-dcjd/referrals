import streamlit as st
import pandas as pd 
import plotly.express as ex
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import datetime

months = ['Jan.', 'Feb.', 'Mar.', 'Apr.', 'May', 'Jun.', 'Jul.', 'Aug.', 'Sep.', 'Oct.', 'Nov.', 'Dec.']
monthsf = ['Oct.', 'Nov.', 'Dec.', 'Jan.', 'Feb.', 'Mar.', 'Apr.', 'May', 'Jun.', 'Jul.', 'Aug.', 'Sep.']
year_list = ['2018', '2019', '2020', '2021']


def percentage_change(col1,col2):
    return ((col2 - col1) / col1)

refs_2016 = pd.read_csv(r'C:\Users\Juan.Lomeli\OneDrive - Dallas County\Documents\streamlit-app\multipage-app\apps\data\Referrals_2016_2021.csv',
    index_col='Referral_Date')

formal_refs = refs_2016['Formal'][24:] + refs_2016['Paper_Formalized'][24:] # start jan 2017

col_names = ['Pid', 'Sex', 'Race', 'Ref_Date', 'Paper_Date', 'Referral_Date', 'Stat', 'Category', 'Offense',
        'General_Category', 'OffenseDescription', 'Referral_Type']

refs = pd.read_csv(r'C:\Users\Juan.Lomeli\OneDrive - Dallas County\Documents\streamlit-app\multipage-app\apps\data\Referrals 2010-2021.csv', names=col_names, skiprows=1)
refs['Referral_Date'] = pd.to_datetime(refs['Referral_Date'])

def det_perc_df():
    df_perc = pd.DataFrame(index=list(range(1,13)))
    df_perc.index.names = ['Month']
    df_perc['2018'] = formal_refs.iloc[12:24].values
    df_perc['2019'] = formal_refs.iloc[24:36].values
    df_perc['2020'] = formal_refs.iloc[36:48].values

    c2021 = pd.Series(formal_refs.iloc[48:60].values)
    c2021.index += 1 
    df_perc['2021'] = c2021
    
    df_perc = df_perc.round(2)
    return df_perc

def det_perc_df_fy():
    df_perc = pd.DataFrame(index=list(range(1,13)))
    df_perc.index.names = ['Month']
    df_perc['2018'] = formal_refs.iloc[9:21].values
    df_perc['2019'] = formal_refs.iloc[21:33].values
    df_perc['2020'] = formal_refs.iloc[33:45].values

    c2021 = pd.Series(formal_refs.iloc[45:57].values)
    c2021.index += 1 
    df_perc['2021'] = c2021
    
    df_perc = df_perc.round(2)
    return df_perc


year1 = st.selectbox('Select Year 1', year_list, index=1) 
year2 = st.selectbox('Select Year 2', year_list, index=2) 

fig = make_subplots(rows=2, cols=1, shared_yaxes=True)
fig.add_trace(
    go.Scatter(x=months, y=formal_refs[12:24], name='2018'),
    row=1, col=1
)
fig.add_trace(
    go.Scatter(x=months, y=formal_refs[24:36], name='2019'),
    row=1, col=1
)
fig.add_trace(
    go.Scatter(x=months, y=formal_refs[36:48], name='2020'),
    row=1, col=1
)
fig.add_trace(
    go.Scatter(x=months, y=formal_refs[48:60], name='2021'),
    row=1, col=1
)

fig.add_trace(
go.Bar(x=months, y=percentage_change(det_perc_df()[year1], det_perc_df()[year2]), name='% Change {} vs {}'.format(year1, year2)),
row=2, col=1
)

fig.update_layout(title_text="Formal & Paper Formalized Combined")

# ----------------- FY ---------------------- 
figf = make_subplots(rows=2, cols=1, shared_yaxes=True)
figf.add_trace(
    go.Scatter(x=monthsf, y=formal_refs[9:21], name='2018'),
    row=1, col=1
)
figf.add_trace(
    go.Scatter(x=monthsf, y=formal_refs[21:33], name='2019'),
    row=1, col=1
)
figf.add_trace(
    go.Scatter(x=monthsf, y=formal_refs[33:45], name='2020'),
    row=1, col=1
)
figf.add_trace(
    go.Scatter(x=monthsf, y=formal_refs[45:57], name='2021'),
    row=1, col=1
)

figf.add_trace(
go.Bar(x=monthsf, y=percentage_change(det_perc_df_fy()[year1], det_perc_df_fy()[year2]), name='% Change {} vs {}'.format(year1, year2)),
row=2, col=1
)

figf.update_layout(title_text="Formal & Paper Formalized Combined - Fiscal Year")




# Radio Button
status = st.radio("Select Type: ", ('Calendar Year', 'Fiscal Year'))
if (status == 'Calendar Year'):
    st.success("Calendar Year")
    st.plotly_chart(fig)
else:
    st.success("Fiscal Year")
    st.plotly_chart(figf)

fig1 = ex.line(refs_2016, x=refs_2016.index, y=refs_2016.columns, title='Monthly Referrals 2016-2021')
fig2 = ex.bar(refs['General_Category'].value_counts(), x=refs['General_Category'].value_counts().index, y=refs['General_Category'].value_counts().values, 
    title='Referral Offenses 2016-2021')

st.plotly_chart(fig1)
st.plotly_chart(fig2)


