from flask import Flask,url_for,redirect,render_template,request
from flask_bootstrap import Bootstrap
import csv
from months import list_of_months,months
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
app = Flask(__name__)
Bootstrap(app)
app.config["SECRET_KEY"]="12321312421412412"


class Day():
    def __init__(self,number,month):
        self.number=number
        self.month=month
        self.todo=[]

class AddForm(FlaskForm):
    todo = StringField('Todo',validators=[DataRequired()])
    submit = SubmitField('Add')

            

month_index=0
days=[]
with open('todo.csv',newline='') as file :
    data = csv.reader(file,delimiter=',')
    for key in list_of_months:
        i=1
        while i<= list_of_months[key]:
            days.append(Day(i,key))
            i+=1
    for row in data:
        if row[0]!='number':
            number = int(row[0])
            month = row[1]
            todo = row[2].split(';')
            for day in days:
                if day.number == number and day.month == month:
                    day.todo = todo

@app.route('/')
def home():
    global month_index
    global days
    days=[]
    with open('todo.csv',newline='') as file :
        data = csv.reader(file,delimiter=',')
        for key in list_of_months:
            i=1
            while i<= list_of_months[key]:
                days.append(Day(i,key))
                i+=1
        for row in data:
            if row[0]!='number':
                number = int(row[0])
                month = row[1]
                todo = row[2].split(';')
                for day in days:
                    if day.number == number and day.month == month:
                        day.todo = todo
    return render_template('index.html',days=days,list_of_months=list_of_months,month_index=month_index,months=months,flag=False,number=0,month='')

@app.route('/<int:number_x>/<string:month_x>')
def list(number_x,month_x):
    global month_index
    global days
    days=[]
    with open('todo.csv',newline='') as file :
        data = csv.reader(file,delimiter=',')
        for key in list_of_months:
            i=1
            while i<= list_of_months[key]:
                days.append(Day(i,key))
                i+=1
        for row in data:
            if row[0]!='number':
                number = int(row[0])
                month = row[1]
                todo = row[2].split(';')
                for day in days:
                    if day.number == number and day.month == month:
                        day.todo = todo
    return render_template('index.html',days=days,list_of_months=list_of_months,month_index=month_index,months=months,flag=True,number=number_x,month=month_x)

@app.route('/month_down')
def month_down():
    global month_index
    if month_index>0:
        month_index-=1
    return redirect(url_for('home'))
@app.route('/month_up')
def month_up():
    global month_index
    if month_index<11:
        month_index+=1
    return redirect(url_for('home'))

@app.route('/add/<int:number_x>/<string:month_x>',methods=['GET','POST'])
def add(number_x,month_x):
    global days
    global month_index
    form = AddForm()
    if form.validate_on_submit():
        with open('todo.csv','w') as file:
            file.write('number,month,todo\n')
            for day in days:
                if(day.number == number_x and day.month == month_x and day.todo.count(form.todo.data)==0):
                    day.todo.append(form.todo.data)
                if(day.todo!=[]):
                    file.write(f"{day.number},{day.month},")
                    for todo in day.todo:
                        file.write(f"{todo}")
                        if(todo!=day.todo[len(day.todo)-1]):
                            file.write(";")
                    file.write('\n')
        return redirect(url_for('list',number_x=number_x,month_x=month_x))
    return render_template('add.html',days=days,list_of_months=list_of_months,month_index=month_index,months=months,flag=True,number=number_x,month=month_x,form =form)


@app.route('/delete/<int:number_x>/<string:month_x>/<string:item>')
def delete(number_x,month_x,item):
    with open('todo.csv','w') as file:
            file.write('number,month,todo\n')
            for day in days:
                if(day.number == number_x and day.month == month_x):
                    day.todo.remove(item)
                if(day.todo!=[]):
                    file.write(f"{day.number},{day.month},")
                    for todo in day.todo:
                        file.write(f"{todo}")
                        if(todo!=day.todo[len(day.todo)-1]):
                            file.write(";")
                    file.write('\n')
    return redirect(url_for('list',number_x=number_x,month_x=month_x))



if(__name__=='__main__'):
    app.run(debug=True)
