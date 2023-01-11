#Author: Adrian Melendrez
#Portfolio Project: Loan Calculator
# Course: CS 361

import importlib
from re import S
from flask import Flask, render_template, request, flash
from decimal import Decimal
from numpy import imag
import requests
import json
from urllib.request import urlopen

app = Flask(__name__)

#index route
@app.route('/')
def index():
    flash("Help page and Pie chart maker features now available. Help page answers FAQS and Pie Chart Maker creates pie charts with your input. CLICK Help below to learn how")
    return render_template('index.html')

@app.route('/payment_plan')
def payment_plan():
    return render_template('payment_plan.html')

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/pie_chart')
def pie():
    return render_template('pie.html')

def isChecked(loanType, amount, interestRate, years):
    """Function that checks for checked mark boxes and returns an array with checked marked fields  """
    outputTotal = []
    #Check if field checked marked. Checked marked items are displayed to the webpage. 
    loanTypeChecked = request.form.get("checkboxtype")
    loanType = " " if loanTypeChecked != "1" else f"Loan Type: {loanType}"
    if loanTypeChecked == "1": outputTotal.append(loanType)
 
    amountChecked = request.form.get("checkboxamount")
    amount = " " if amountChecked != "1" else f"Principal Amount: {amount}"
    if amountChecked == "1": outputTotal.append(amount)
  
    interestChecked = request.form.get("checkboxinterest")
    interestRate = " " if interestChecked != "1" else f"Interest Rate: {interestRate}"
    if interestChecked == "1": outputTotal.append(interestRate)
    
    yearsChecked = request.form.get("checkboxyears")
    years = " " if yearsChecked != "1" else f"Years: {years}"
    if yearsChecked == "1": outputTotal.append(years) 

    return outputTotal

#post request
# Function does the loan calculations and displays it on the webpage
@app.route('/form', methods=["POST"])
def form():
    loanType = request.form.get("loanType")
    amount = float(request.form.get("amount"))
    interestRate = float(request.form.get("interestRate"))
    interestRate = interestRate/100
    years = float(request.form.get("years"))
    totalAmount = float(amount * (1.00 + (interestRate*years)))
    totalAmountFloat = totalAmount
    amountFloat = amount
    str(totalAmount)

    outputTotal = isChecked(loanType, amount, interestRate, years)
    
    interestTotal = totalAmountFloat - amountFloat
    str(interestTotal)
   
    #POST JSON data from client to server(Nic Nolan's Microservice) 
    # via requests library and JSON parameter
    r = requests.post("https://mockdata-u.vercel.app/api/pie-chart", json={'Principal Amount': amountFloat, 'Interest Amount': interestTotal})

    #get the json object url
    json_object = json.loads(r.text)
    print(json_object["url"])
    imageLink = json_object["url"]
    
    return render_template('form.html', outputTotal=outputTotal, totalAmount=totalAmount, imageLink=imageLink)


def getSubjects():
    """ Get the subject input from user and return array of those values"""
    subjects = []
    subject1 = request.form.get("name1")
    subjects.append(subject1)
    subject2 = request.form.get("name2")
    subjects.append(subject2)
    subject3 = request.form.get("name3")
    subjects.append(subject3)
    subject4 = request.form.get("name4")
    subjects.append(subject4)
    subject5 = request.form.get("name5")
    subjects.append(subject5)
    subject6 = request.form.get("name6")
    subjects.append(subject6)
    subject7 = request.form.get("name7")
    subjects.append(subject7)

    return subjects

def getData(subjects):
    """get data that the user entered and return array of that data"""
    data = []

    #get the data input. Data is 0 if no input is provided
    data.append(float(request.form.get("data1"))) if subjects[0] != "" else data.append(0.0)
    data.append(float(request.form.get("data2"))) if subjects[1] != "" else data.append(0.0)
    data.append(float(request.form.get("data3"))) if subjects[2] != "" else data.append(0.0)
    data.append(float(request.form.get("data4"))) if subjects[3] != "" else data.append(0.0)
    data.append(float(request.form.get("data5"))) if subjects[4] != "" else data.append(0.0)
    data.append(float(request.form.get("data6"))) if subjects[5] != "" else data.append(0.0)
    data.append(float(request.form.get("data7"))) if subjects[6] != "" else data.append(0.0)

    return data


#post request
# Used to Display the data from user on a Pie chart(Nic Nolan's Microservice)
@app.route('/pieForm', methods=["POST"])
def pieForm():
    #get the subject input and data
    subjects = getSubjects()
    data = getData(subjects)
   
    #POST JSON data from client to server(Nic Nolan's Microservice) 
    # via requests library and JSON parameter
    r = requests.post("https://mockdata-u.vercel.app/api/pie-chart", json={subjects[0]: data[0], subjects[1]: data[1], subjects[2]: data[2], subjects[3]: data[3], subjects[4]: data[4], subjects[5]: data[5], subjects[6]: data[6]})

    #get the json object url
    json_object = json.loads(r.text)
    print(json_object["url"])
    imageLink = json_object["url"]
 
    return render_template('pieForm.html', imageLink=imageLink)


if __name__ == "__main__":
    app.config['SECRET_KEY'] = 'Tayler'
    app.run(debug=True)