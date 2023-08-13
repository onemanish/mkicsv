import streamlit as st
import pandas as pd
import plotly.express as px

def main():
    col1, col2 = st.columns(2)
    uploaded_file = col1.file_uploader('Upload IAS CSV file') 
    if uploaded_file:
        with uploaded_file as f:
            df = pd.read_csv(f, encoding='latin1', skiprows=6, dtype='unicode')
        df = df.drop(range(0,7)) # drop intial rows after the column names
        df = df.drop(columns=df.columns[0:2]) # drop the first two columns
        # get header names and replace 'Unnamed:' in the name
        headers = [x[-1] if 'Unnamed' in x else x for x in df.columns ]
        df.columns = headers
        df['datetime'] = df['2'] + ' ' + df['3']
        df['datetime'] = df['datetime'].astype('datetime64[ns]')
        df = df.drop(['2', '3', '4'], axis=1) # drop the first three columns
        headers = headers[3:]
        df[headers] = df[headers].apply(pd.to_numeric)
        options = ['30S', '15S', '5S', '1T', '3T', '5T', '10T', '30T', 'H', '2H', 'D']
        optPrompt = 'Select Time period for averaging... (S=Seconds, T=minuTes, H=Hours, D=Day)'
        time_period = col2.selectbox(label=optPrompt, options=options)
        df = df.resample(time_period, on='datetime').mean()
        col2.write(f'Data points: {df.shape}')
        fig1 = px.line(df, x=df.index, y=headers[:-1], title='Data Timeline')
        fig1.update_layout(height=600, legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
        st.plotly_chart(fig1, use_container_width=True, theme='streamlit')
        
if __name__ == '__main__':
    st.set_page_config(layout='wide')
    st.title('IAS CSV Viewer')
    main()