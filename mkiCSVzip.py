import streamlit as st
import zipfile, py7zr, os, shutil
import pandas as pd
import plotly.express as px

def clear_temp_dir():
    if os.path.exists('temp_dir'):
        shutil.rmtree('temp_dir')

def extract_zip(file):
    extracted_filenames = []
    os.makedirs('temp_dir', exist_ok=True)
    with zipfile.ZipFile(file, 'r') as zip_ref:
        for member in zip_ref.namelist():
            if member.lower().endswith('.csv'):
                extracted_filename = os.path.join('temp_dir', os.path.basename(member))
                zip_ref.extract(member, 'temp_dir')
                os.rename(os.path.join('temp_dir', member), extracted_filename)
                extracted_filenames.append(extracted_filename)
    return extracted_filenames

def extract_7z(file):
    extracted_filenames = []
    os.makedirs('temp_dir', exist_ok=True)
    with py7zr.SevenZipFile(file, mode='r') as archive:
        for member in archive.getnames():
            if member.lower().endswith('.csv'):
                extracted_filename = os.path.join('temp_dir', os.path.basename(member))
                archive.extract(member, path='temp_dir')
                os.rename(os.path.join('temp_dir', member), extracted_filename)
                extracted_filenames.append(extracted_filename)
    return extracted_filenames

def display_data(data_file):
    col1, col2 = st.columns(2)
    df = pd.read_csv(os.path.join('temp_dir',data_file), encoding='latin1', skiprows=6, dtype='unicode')
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
    optPrompt = 'Select Time period for averaging... 30sec is default. (S=Seconds, T=minuTes, H=Hours, D=Day)'
    time_period = col1.selectbox(label=optPrompt, options=options)
    df = df.resample(time_period, on='datetime').mean()
    col2.write(f'Data points: {df.shape}')
    fig1 = px.line(df, x=df.index, y=headers[:-1], title='Data Timeline')
    fig1.update_layout(height=600, legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
    st.plotly_chart(fig1, use_container_width=True, theme='streamlit')


def main():
    st.set_page_config(layout='wide')
    st.sidebar.header('MKI IAS CSV Viewer')
    
    # Place the file uploader in the sidebar
    uploaded_file = st.sidebar.file_uploader("Upload a file", type=["zip", "7z"])

    if uploaded_file is not None:
        clear_temp_dir()  # Clear existing files in temp_dir
        file_extension = os.path.splitext(uploaded_file.name)[1].lower()

        if file_extension == '.zip':
            extracted_filenames = extract_zip(uploaded_file)
        elif file_extension == '.7z':
            extracted_filenames = extract_7z(uploaded_file)

        if extracted_filenames:
            st.sidebar.success(f"Extracted {len(extracted_filenames)} files.")
            extracted_filenames = [x.split('/')[1] for x in extracted_filenames]
            selected_file = st.sidebar.selectbox("Select a file", extracted_filenames)
            st.subheader(selected_file)
            display_data(selected_file)
        else:
            st.sidebar.info("No files found in the uploaded archive.")

if __name__ == "__main__":
    main()
