###############################
####### SETUP (OVERALL) #######
###############################

## Import statements
# Import statements
import os
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField, ValidationError, SelectMultipleField, widgets # Note that you may need to import more here! Check out examples that do what you want to figure out what.
from wtforms.validators import Required, Length # Here, too
from flask_sqlalchemy import SQLAlchemy
import requests
import json

## App setup code
app = Flask(__name__)
app.debug = True
app.use_reloader = True

## All app.config values
app.config['SECRET_KEY'] = 'hard to guess string for midterm'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hsurkamer:hogansurk5@localhost/recipes1'
app.config['SQLACHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
## Statements for db setup (and manager setup if using Manager)
db = SQLAlchemy(app)


######################################
######## HELPER FXNS (If any) ########
######################################
def check_diet(form, field):
    diet_list = ['balanced','high-protien','low-fat','low-carb']
    if field.data not in diet_list:
        raise ValidationError('Diet name must be one of the options listed.')

def one_word(form, field):
    if len(field.data.split())<1:
        raise ValidationError('Username Can Not Contain Spaces')

def create_food(food, diet, allergy_health, user_id):
    food1 = Food.query.filter_by(food_name=food,diet=diet,health=allergy_health).first()
    if food1 is None:
        food_enter = Food(food_name=food,diet=diet,health=allergy_health,user_id=user_id)
        db.session.add(food_enter)
        db.session.commit()
        find_recipe(food, diet, allergy_health, user_id)
    else:
        return food1

def find_recipe(food, diet, allergy_health, user_id):
    base_url = "https://api.edamam.com/search?"
    re = requests.get(base_url, params={'q':food,'app_id':'c32dd9d7','app_key':'3a1dc96c14fb8d3a339815d072d89fbb','diet':diet,'health':allergy_health})
    r = json.loads(re.text)
    print(r)
#curl "https://api.edamam.com/search?q=chicken&app_id=${c32dd9d7}&app_key=${3a1dc96c14fb8d3a339815d072d89fbb}&from=0&to=3&calories=gte%20591,%20lte%20722&health=alcohol-free"
    
##################
##### MODELS #####
##################

class Food(db.Model):
    __tablename__ = "foods"
    id = db.Column(db.Integer,primary_key=True)
    food_name = db.Column(db.String(64))
    health = db.Column(db.String(64))
    diet = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    recipe = db.relationship('Recipes', backref='Food')
    def __repr__(self):
        return "{} (ID: {})".format(self.food_name, self.id, )

class Recipes(db.Model):
    __tablename__ = "recipes"
    id = db.Column(db.Integer,primary_key=True)
    recipe = db.Column(db.String(500))
    food = db.Column(db.Integer, db.ForeignKey('foods.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    def __repr__(self):
        return "{} | ID: {}".format(self.recipe, self.id)

class User(db.Model):
    __tablename__="users"
    id = db.Column(db.Integer,primary_key=True)
    user_name = db.Column(db.String(64))
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    fav_recipe = db.relationship('Favorites', backref='User')
    called_recipes = db.relationship('Recipes', backref='User')
    food_entered = db.relationship('Food',backref='User')
    def __repr__(self):
        return "{} (ID: {})".format(self.user_name,self.id)

class Favorites(db.Model):
    __tablename__ = "favorite recipes"
    id = db.Column(db.Integer, primary_key=True)
    recipe = db.Column(db.String(500))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    def __repr__(self):
        return "{} | ID:{}".format(self.recipe,self.user_id)

###################
###### FORMS ######
###################

class FoodForm(FlaskForm):
    user_name = StringField("Enter your Username here: ", validators=[Required(),one_word])
    food_name = StringField("Please name of food you would like a recipe for: ",validators=[Required(), Length(max=64)])
    diet = StringField("Enter the diet you would like the recipe to follow (i.e. balanced, high-protien, low-carb, low-fat): ", validators=[Required(),check_diet])
    health = RadioField("Check the name of the allergies you have: ", validators=[Required()], choices=[('alchohol-free','Alcohol'),('peanut-free','Peanut'),('sugar-conscious','Sugar Conscious'),('tree-nut-free','Tree Nuts'),('vegan','Vegan'),('vegetarian','Vegetarian'),('None','none')],default='None')
    submit = SubmitField('Submit')

class NameForm(FlaskForm):
    username = StringField("Enter your Username here: ", validators=[Required(),one_word])
    first = StringField("Enter your First Name: ", validators=[Required()])
    last = StringField("Enter your Last Name: ", validators=[Required()])
    submit = SubmitField('Submit')

class FavoriteForm(FlaskForm):
    username = StringField("Enter your Username here: ", validators=[Required(),one_word])
    fav = SelectMultipleField("Choose Favorite Recipes: ", choices = ['PUT RECIPE USER HAS RETURNED HERE'], option_widget = widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False)) #this code I found on http://www.ergo.io/tutorials/persuading-wtforms/persuading-wtforms-to-generate-checkboxes/
    submit = SubmitField('Submit')

#######################
###### VIEW FXNS ######
#######################

@app.route('/', methods=['GET','POST'])
def home():
    form = NameForm() # User should be able to enter name after name and each one will be saved, even if it's a duplicate! Sends data with 
    user_n,firs_n,last_n = None,None,None
    if request.method == 'POST' and form.validate_on_submit():
        user_n = form.username.data
        first_n = form.first.data
        last_n = form.last.data
        #print(user_n,first_n,last_n)
        user = User.query.filter_by(user_name = user_n).first()
        if user is None:
            username = User(user_name = user_n,first_name = first_n,last_name = last_n)
            db.session.add(username)
            db.session.commit()
            flash('User Successfully Created')
            return redirect(url_for('enter_food'))
        else:
            user = User.query.filter_by(user_name = user_n).first()
            print(user)
            flash('Username is taken, please enter a new name')
            return redirect(url_for('enter_food'))
        
    else:
        print('i wont work')
    errors = [x for x in form.errors.values()]
    if len(errors) > 0:
        flash('Error in the submission of the form - '+str(errors))
    return render_template('name.html',form=form)

@app.route('/food_entry', methods=['POST','GET'])
def enter_food():
    form = FoodForm() # User should be able to enter name after name and each one will be saved, even if it's a duplicate! Sends data with GET
    if request.method == 'POST' and form.validate_on_submit():
        name = form.user_name.data
        food = form.food_name.data.lower()
        diet = form.diet.data

        allergy_health = form.health.data
        print(food,diet,allergy_health)
        username1 = User.query.filter_by(user_name=name).first()
        user_id = username1.id
        create_food(food,diet,allergy_health,user_id)
        food1 = Food.query.filter_by(food_name=food,diet=diet,health=allergy_health).first()
        if food1:
            print(food1)
            flash('Food Added Successfully')

    else:
        print("I won't work")


    errors = [x for x in form.errors.values()]
    if len(errors) > 0:
        flash('Error in the submission of the form - '+str(errors))
    return render_template('foods.html',form=form)

# @app.route('/recipes')
# def recipes():
#     inputs = Food.query.



## Code to run the application...

if __name__ == '__main__':
    db.create_all()
    app.run(use_reloader=True,debug=True)
# Put the code to do so here!
# NOTE: Make sure you include the code you need to initialize the database structure when you run the application!