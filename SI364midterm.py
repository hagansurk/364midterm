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
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hsurkamer:hogansurk5@localhost/recipes'
app.config['SQLACHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
## Statements for db setup (and manager setup if using Manager)
db = SQLAlchemy(app)


######################################
######## HELPER FXNS (If any) ########
######################################
def check_diet(form, field):
    diet_list = ['balanced','high-protein','low-fat','low-carb']
    if field.data not in diet_list:
        raise ValidationError('Diet name must be one of the options listed.')

def one_word(form, field):
    if len(field.data.split())<1:
        raise ValidationError('Username Can Not Contain Spaces')

def create_food(food, diet, allergy_health, user_id):
    food1 = Food.query.filter_by(food_name=food,diet=diet,health=allergy_health,user_id = user_id).first()
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
    food2 = Food.query.filter_by(food_name=food,diet=diet,health=allergy_health).first()
    food_id = food2.id
    for dic in r['hits']:
        for k,v in dic['recipe'].items():
            recipe_name = dic['recipe']['label']
            health_lab = str(dic['recipe']['healthLabels'])
            ingr = str(dic['recipe']['ingredientLines'])
            cals = dic['recipe']['calories']
        rec = Recipes.query.filter_by(recipe = recipe_name).first()
        if rec is None:
            rec_enter = Recipes(recipe=recipe_name,ingredients=ingr,health_labels=health_lab, cals=cals, user_id=user_id, food=food_id)
            db.session.add(rec_enter)
            db.session.commit()
        else:
            return rec

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
        return "{} (ID: {})".format(self.food_name, self.id)

class Recipes(db.Model):
    __tablename__ = "recipes"
    id = db.Column(db.Integer,primary_key=True)
    recipe = db.Column(db.String(64))
    ingredients = db.Column(db.String())
    health_labels = db.Column(db.String())
    cals = db.Column(db.Float)
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
    #fav_recipe = db.relationship('Favorites', backref='User')
    called_recipes = db.relationship('Recipes', backref='User')
    food_entered = db.relationship('Food',backref='User')
    def __repr__(self):
        return "{} (ID: {})".format(self.user_name,self.id)

# class Favorites(db.Model):
#     __tablename__ = "favorite recipes"
#     id = db.Column(db.Integer, primary_key=True)
#     recipe = db.Column(db.String(500))
#     user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
#     def __repr__(self):
#         return "{} | ID:{}".format(self.recipe,self.user_id)

###################
###### FORMS ######
###################

class FoodForm(FlaskForm):
    user_name = StringField("Enter your Username here: ", validators=[Required(),one_word])
    food_name = StringField("Please name of food you would like a recipe for: ",validators=[Required(), Length(max=64)])
    diet = StringField("Enter the diet you would like the recipe to follow (i.e. balanced, high-protein, low-carb, low-fat): ", validators=[Required(),check_diet])
    health = RadioField("Check the name of the allergies you have: ", validators=[Required()], choices=[('alchohol-free','Alcohol'),('peanut-free','Peanut'),('sugar-conscious','Sugar Conscious'),('tree-nut-free','Tree Nuts'),('vegan','Vegan'),('vegetarian','Vegetarian'),('None','none')],default='None')
    submit = SubmitField('Submit')

class NameForm(FlaskForm):
    username = StringField("Enter your Username here: ", validators=[Required(),one_word])
    first = StringField("Enter your First Name: ", validators=[Required()])
    last = StringField("Enter your Last Name: ", validators=[Required()])
    submit = SubmitField('Submit')

# class FavoriteForm(FlaskForm):
#     username = StringField("Enter your Username here: ", validators=[Required(),one_word])
#     fav = SelectMultipleField("Choose Favorite Recipes: ", choices = ['Hey','hello','whats up'], option_widget = widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False)) #this code I found on http://www.ergo.io/tutorials/persuading-wtforms/persuading-wtforms-to-generate-checkboxes/
#     submit = SubmitField('Submit')

#######################
###### VIEW FXNS ######
#######################
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/')
def home():
    form = NameForm() 
    return render_template('name.html',form=form)

@app.route('/home1',methods=['GET','POST'])
def answers():
    form = NameForm()
    if request.args:
        user_name = request.args.get('username')
        first = request.args.get('first')
        last = request.args.get('last')
        print(user_name,first,last)
        
        user = User.query.filter_by(user_name = user_name).first()
        if user is None:
            username = User(user_name = user_name,first_name = first,last_name = last)
            db.session.add(username)
            db.session.commit()
            flash('User successfully created')
            return redirect(url_for('enter_food'))
        else:
            user = User.query.filter_by(user_name = user_name).first()
            print(user)
            flash('Username is taken, please enter a new name')
            return redirect(url_for('home'))

    

@app.route('/food_entry', methods=['POST','GET'])
def enter_food():
    form = FoodForm() # User should be able to enter name after name and each one will be saved, even if it's a duplicate! Sends data with GET
    # name_entries = request.args.get()
    # print(name_entries)
    if request.method == 'POST' and form.validate_on_submit():
        name = form.user_name.data
        food = form.food_name.data.lower()
        diet = form.diet.data
        allergy_health = form.health.data
        username1 = User.query.filter_by(user_name=name).first()
        user_id = username1.id
        create_food(food,diet,allergy_health,user_id)
        food1 = Food.query.filter_by(food_name=food,diet=diet,health=allergy_health).first()
        if food1:
            flash('Food Added Successfully')
            return redirect(url_for('see_all_recipes'))

    else:
        print("I won't work")


    errors = [x for x in form.errors.values()]
    if len(errors) > 0:
        flash('Error in the submission of the form - '+str(errors))
    return render_template('foods.html',form=form)

@app.route('/recipes')
def see_all_recipes():
    all_recipes=[]
    rec = Recipes.query.all()
    for elem in rec:
        rec_name = elem.recipe
        ingr = elem.ingredients
        cals = elem.cals
        u_id = elem.user_id
        user = User.query.filter_by(id=u_id).all()
        for elem1 in user:
            user_name = elem1.user_name
            tupl = (rec_name,ingr,cals,user_name)
            all_recipes.append(tupl)

    return render_template('all_recipes.html', all_recipes=all_recipes)

@app.route('/all_users')
def see_users():
    all_users = []
    users = User.query.all()
    for elem in users:
        name = elem.user_name
        user_id = elem.id
        foods = Food.query.filter_by(user_id = user_id).all()
        recipes = Recipes.query.filter_by(user_id=user_id).all()
        for elem1 in foods:
            food_name = elem1.food_name
            for elem2 in recipes:
                recipe_name = elem2.recipe
                tupl = (name,food_name,recipe_name)
                all_users.append(tupl)
    return render_template('all_users.html', all_users=all_users)


## Code to run the application...

if __name__ == '__main__':
    db.create_all()
    app.run(use_reloader=True,debug=True)
# Put the code to do so here!
# NOTE: Make sure you include the code you need to initialize the database structure when you run the application!
