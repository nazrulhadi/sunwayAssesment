from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import Form
from wtforms import TextField
from encryption import *
from decryption import *
import pandas as  pd
import numpy as np
import datetime
import csv
import os 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'our very hard to guess secretfir'

def create_directory():
    current_dir = os.getcwd()
    folder_name =  'Clean_Data'
    path = os.path.join(current_dir , folder_name) 
    os.mkdir(path)
    return path
    

def datatype_validation(data):#change the data types
    df = data
    if df['Name'].dtypes != object:
        df['Name'] = df['Name'].astypes (object)
    

    if df['Mobile No.'].dtypes != object:
        df['Mobile No.']= df['Mobile No.'].astypes(object)

    if df['IC No.'].dtypes != object:
        df['IC No.'] = df['IC No.'].astypes(object)

    if df['Transaction Date'].dtypes != 'datetime64[ns]':
        df['Transaction Date'] = df['Transaction Date'].astype('datetime64[ns]')

    if df['Business Unit ID'].dtypes != int:
        df['Business Unit ID'] = df['Business Unit ID'].astypes (int)

    if df['Race'].dtypes != object:
        df['Race'] = df['Race'].astypes (object)

    




def data_cleaning(df):
    mobile_num = df['Mobile No.']
    for i in range (len(mobile_num)): #to clean the data

        if  (df.loc[i,'Mobile No.'] == '@#asdjvn' or df.loc[i,'Mobile No.'] == '!_qzksj_' ):
            df.loc[i,'Mobile No.'] = np.nan

        if (df.loc[i,'IC No.'] == 'No Data' or df.loc[i,'IC No.'] == 'asdadj' or df.loc[i,'IC No.'] == '!#@$'):
            df.loc[i,'IC No.'] = np.nan

        if (df.loc[i,'Race'] == 'Info not found in database'):
            df.loc[i,'Race'] = np.nan
    return df


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/decryption_page')
def thank_you():
    return render_template('decryption_page.html')


# Simple form handling using raw HTML forms
@app.route('/process', methods=['GET', 'POST'])
def process():
    error = ""
    if request.method == 'POST':
        # Form being submitted; grab data from form.
        path = request.form['path']
       

        # Validate form data
        if len(path) == 0 :
            # Form data failed validation; try again
            error = "Please supply path for the file"
            
        else:

            data = pd.read_csv(path)
            datatype_validation(data)
            df = data_cleaning(data)

            # sorting by  name 
            df.sort_values("Name", inplace = True) 

            # dropping ALL duplicte values 
            df.drop_duplicates(subset ="Name", 
                                keep = False, inplace = True)

            # to remove the Remove irrelevant values / null values
            df1=df.dropna()

            folder = create_directory()
            outfile = os.path.join(folder, 'clean.csv')
            
            df1.to_csv (outfile, index = False, header=True)
            encrypt(outfile)
            
            return redirect(url_for('index'))

    # Render the process page
    return render_template('process.html', message=error)


@app.route('/decryption_page', methods=['GET', 'POST'])
def decryption():
    error = ""
    if request.method == 'POST':

        decrypt_key = request.form['decrypt_key']
        if len(decrypt_key) == 0  :
            error = "Please insert the decryption key"
        else:
            decrypt(decrypt_key)
            return 'Decryption complete!'

    return render_template('decryption_page.html', message=error)


# Run the application
app.run(debug=True)
