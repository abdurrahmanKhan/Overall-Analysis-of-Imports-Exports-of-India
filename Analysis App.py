import streamlit as st
import pandas as pd
import codecs
import streamlit.components.v1 as components
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objs as go
from wordcloud import WordCloud,STOPWORDS
from scipy.stats import norm
st.set_option('deprecation.showPyplotGlobalUse', False)
st.cache()

def main():
	menu = ["Overall","About"]
	choice = st.sidebar.selectbox("Menu",menu)
	if choice == "Overall":
                st.title("Overall Analysis of Imports & Exports")
                st.write('')
                st.subheader("**Attribute Information**")
                st.write('')
                st.write("**HSCode** - HS stands for Harmonized System.It is a multipurpose international product nomenclature that\
                        describes the type of good that is shipped")
                st.write(" **Commodity** - It is defined as a tangible good that can be bought and sold or exchanged for products of similar value")
                st.write("**Value** - values for export and import of commodities in million US $")
                st.write("**Country** - Country Imported From/ Exported To")
                st.write("**Year** -Year in which comodities where Imported/Exported which is in between 2010 to 2018")
                st.write("**Import** - Imports are foreign goods and services bought by residents of a country. Residents include citizens, businesses, and the government")
                st.write("**Export** - Exports are the goods and services produced in one country and purchased by residents of another country")
                st.write('')
                expander1 = st.beta_expander("Summary Statistics of Imports & Exports") ## Summary
                with expander1:      
                        st.subheader("IMPORTS")
                        data_file = st.file_uploader("Upload Import data",type=['csv'])
                        if data_file is not None:
                                df_i = pd.read_csv(data_file)
                                st.dataframe(df_i.head())
                                if st.button("Pre-Process imports"):
                                        mean_value = df_i.value.mean()
                                        df_i.value.fillna(mean_value, inplace = True )
                                        df_i.drop_duplicates(keep="first",inplace=True)
                                        df_i['country']= df_i['country'].apply(lambda x : np.NaN if x == "UNSPECIFIED" else x)
                                        df_i = df_i[df_i.value!=0]
                                        df_i.dropna(inplace=True)
                                        st.write("Checking Nulls: " ,df_i.isnull().sum())
                                        st.write("After Pre-processing")
                                        st.dataframe(df_i.head())
                        col8, col9= st.beta_columns(2)
                        st.write('')
                        with col8:
                                if st.button("Summary Statistics of Continuous Variables (Imports)"):
                                        desi = df_i[['HSCode','value']].describe() 
                                        st.table(desi.style.highlight_max(axis=1))
                        with col9:
                                if st.button("Summary Statistics of Categorical Variables (Imports)"):
                                        cati = df_i.dtypes[df_i.dtypes == 'object'].index
                                        st.table(df_i[cati].describe(include = ['O']))
                                        

                        st.subheader("EXPORTS")
                        data_file = st.file_uploader("Upload Export Data",type=['csv'])
                        if data_file is not None:
                                df_e = pd.read_csv(data_file)
                                st.dataframe(df_e.head())                                      
                                if st.button("Pre-Process exports"):
                                        mean_value = df_e.value.mean()
                                        df_e.value.fillna(mean_value, inplace = True )
                                        df_e.drop_duplicates(keep="first",inplace=True)
                                        df_e['country']= df_e['country'].apply(lambda x : np.NaN if x == "UNSPECIFIED" else x)
                                        df_e = df_e[df_e.value!=0]
                                        df_e.dropna(inplace=True)
                                        st.write("Checking Nulls: " ,df_e.isnull().sum())
                                        st.write("After Pre-processing")
                                        st.dataframe(df_e.head())
                        col6, col7= st.beta_columns(2)
                        st.write('')
                        with col6:
                                if st.button("Summary Statistics of Continuous Variables (Exports)"):
                                        dese = df_e[['HSCode','value']].describe() 
                                        st.table(dese.style.highlight_max(axis=1))
                        with col7:
                                if st.button("Summary Statistics of Categorical Variables (Exports)"):
                                        cate = df_e.dtypes[df_e.dtypes == 'object'].index
                                        st.table(df_e[cate].describe(include = ['O']))


                # Analysis
                st.write('')
                if st.button("Overview Analysis"):
                        st.write('')
                        #Deficit 
                        expander_trade = st.beta_expander("Trade Deficit over the years")
                        with expander_trade:
                                st.write("")
                                st.write("**Trade Deficit** - It is an amount by which the cost of imports exceeds its exports.")
                                df3 = df_i.groupby('year').agg({'value': 'sum'})
                                df4 = df_e.groupby('year').agg({'value': 'sum'})
                                df3['value_ex'] = df4.value
                                df3['deficit'] = df4.value - df3.value
                                years = ['2010','2011','2012','2013','2014','2015','2016','2017','2018']
                                fig4 = go.Figure(data = [
                                go.Bar(x = years, y= df3.value , name= 'import'),
                                go.Bar(x=years, y =df3.deficit , name = 'deficit'),
                                go.Bar(x=years, y = df3.value_ex , name= 'export')],
                                layout= {'barmode':'group'})
                                st.plotly_chart(fig4)
                                st.write('')
                                st.write('')
                        #Growth Rate
                        st.write('')
                        expander_growth = st.beta_expander("Growth Rate Overall over the years")
                        with expander_growth:
                                st.write("")
                                st.write("**Growth Rate** - It is the percentage change of a specific variable within a specific time period and given a certain context. we calucate the annual growth rate")
                                ###Coverting dataset in year wise
                                exp_year = df_e.groupby('year').agg({'value': 'sum'})
                                exp_year = exp_year.rename(columns={'value': 'Export'})
                                imp_year = df_i.groupby('year').agg({'value': 'sum'})
                                imp_year = imp_year.rename(columns={'value': 'Import'})
                                ###Calculating the growth of export and import'''
                                exp_year['Growth Rate(E)'] = exp_year.pct_change()
                                imp_year['Growth Rate(I)'] = imp_year.pct_change()
                                total_year = pd.concat([exp_year, imp_year], axis = 1)
                                ###Visualization of Export/Import Growth Rate'''
                                # create trace1
                                trace1 = go.Scatter(x = total_year.index,
                                y = total_year['Growth Rate(E)'],name = "Growth Rate(E)",line_color='deepskyblue',opacity=0.8,
                                        text = total_year['Growth Rate(E)'])
                                # create trace2 
                                trace2 = go.Scatter(
                                x = total_year.index,
                                y = total_year['Growth Rate(I)'],name = "Growth Rate(I)",line_color='dimgray',opacity=0.8,
                                        text = total_year['Growth Rate(I)'])

                                layout = go.Layout(hovermode= 'closest', title = 'Export/Import Growth Rate of Indian Trade from 2010 to 2018' , xaxis = dict(title = 'Year'), yaxis = dict(title = 'Growth Rate'))
                                fig6 = go.Figure(data = [trace1, trace2], layout = layout)
                                st.plotly_chart(fig6)
                                st.write('')

                        st.write('')
                        col1, col2= st.beta_columns(2)
                        st.write('')
                        with col1:
                                #Import
                                im_expander = st.beta_expander("Top 5 sources of Import for India")
                                with im_expander:
                                        im_bar = df_i.groupby('country').agg({'value':'sum'}) #for analysing imports
                                        im_bar = im_bar.sort_values(by='value',ascending = False)
                                        im_bar = im_bar.head(5) 
                                        fig = px.bar(im_bar, y='value', x=im_bar.index, text='value',color = im_bar.index)
                                        fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
                                        fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide',width=500, height=400, bargap=0.60)
                                        st.plotly_chart(fig)

                        with col2:
                                #Export
                                ex_expander = st.beta_expander("Top 5 countries of export")
                                with ex_expander:
                                        ex_bar = df_e.groupby('country').agg({'value': 'sum'}) #for analysing exports
                                        ex_bar = ex_bar.sort_values(by='value',ascending = False)
                                        ex_bar = ex_bar.head(5)
                                        fig = px.bar(ex_bar, y='value', x=ex_bar.index, text='value',color = ex_bar.index)
                                        fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
                                        fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide',width=500, height=400, bargap=0.70)
                                        st.plotly_chart(fig)
          #for 5 countries over time
                        expander_ani_imp = st.beta_expander("Top 5 countries of import over the years")
                        with expander_ani_imp:
                                dc_i = df_i.groupby(['country','year']).agg({'value': 'sum'})
                                dc_i = dc_i.reset_index()
                                c_i = dc_i.sort_values(by='year')
                                list_of_values = ['CHINA P RP','U ARAB EMTS','SAUDI ARAB','U S A','SWITZERLAND']
                                c_i = c_i[c_i['country'].isin(list_of_values)]
                                fig2 = px.scatter(c_i, x='country', y='value',
                                color = c_i.index,size = 'value',size_max=40, hover_name = 'country',range_x=[-1,5],range_y=[1,80000],
                                   animation_frame = 'year',animation_group='country',log_x=False)
                                st.plotly_chart(fig2)

                        st.write('')  #for 5 countries over time
                        expander_ani_exp = st.beta_expander("Top 5 countries of export over the years")
                        with expander_ani_exp:
                                dc_e = df_e.groupby(['country','year']).agg({'value': 'sum'})
                                dc_e = dc_e.reset_index()
                                c_e = dc_e.sort_values(by='year')
                                list_of_values = ['CHINA P RP','U ARAB EMTS','SINGAPORE','U S A','HONG KONG']
                                c_e = c_e[c_e['country'].isin(list_of_values)]
                                fig2 = px.scatter(c_e, x='country', y='value',
                                color= c_e.index,size = 'value',size_max=40, hover_name = 'country',range_x=[-1,5],range_y=[1,80000],
                                   animation_frame = 'year',animation_group='country',log_x=False)
                                st.plotly_chart(fig2)
                                st.write('')


                        #top 5 commodities
                        st.write('')
                        col3, col4= st.beta_columns(2)
                        st.write('')
                        with col3:
                                #Import
                                im_expander = st.beta_expander("Top 5 Commodities India import\'s")
                                with im_expander:
                                        trade_commodities_i = df_i.groupby(['Commodity']).sum().sort_values(by = 'value', ascending = False).head()
                                        trade_commodities_i = trade_commodities_i.reset_index()
                                        fig6 = px.pie(trade_commodities_i, values='value', names='Commodity', color_discrete_sequence=px.colors.sequential.Oryel)
                                        fig6.update_layout(width=1550,height=400)
                                        st.plotly_chart(fig6)

                        with col4:
                                #Export
                                ex_expander = st.beta_expander("Top 5 Commodities India export\'s")
                                with ex_expander:
                                        trade_commodities_e = df_e.groupby(['Commodity']).sum().sort_values(by = 'value', ascending = False).head()
                                        trade_commodities_e= trade_commodities_e.reset_index()
                                        fig7 = px.pie(trade_commodities_e, values='value', names='Commodity', color_discrete_sequence=px.colors.sequential.Oryel)
                                        fig7.update_layout(width=1550,height=400)
                                        st.plotly_chart(fig7)
	elif choice == "About":
                st.markdown("## About Author")
                st.markdown("### Abdurrahman")
                st.markdown("Currently pursuing Masters in Big Data Analytics. Keen to work with data. Completed many projects on Data Analysis & Machine Learning")
                st.markdown("### Reach out to me at -")
                st.markdown("LinkedIn - www.linkedin.com/in/abdurrahman-163a63127" )
                st.markdown("Gmail - mailtoabdurrahman24x7@gmail.com" )

if __name__ == '__main__':
	main()
