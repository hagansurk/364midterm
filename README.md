My application lets a user create an identity for themselves and allows them to find recipes they may enjoy given the food they wish to be included in the recipe (i.e. chicken, steak, pork, onions, etc.), the diet they perfer the recipe to follow, and any allergies or other parameters they need to be conscious of using the edamam recipe search API.

To save all of the entered data, I ctreated a user table to save data on the user, a table for foods entered for the API request (id, food name, diet, health concerns, and user id from user table), a recipe table to save the outputs of the API request in (the recipe name, ingridents, calories, health concerns the recipe falls under, and the food_id and user_id the recipe was linked to), as well as a review table for people to let me know what they liked and dislked about the application (id, star rating, description, and user_id from user table).  There is a relationship between the user table and each of the other tables as well as another relationship between the food and the recipe table.

The API required a key and application id, which I have included in my file for ease of use.

** Routes and templates: **

/ --> name.html which I changed from name_example.html.
/home1 --> answers.html which I was used to get the data from name.html using GET request and save it to the user data base.
/food_entry --> foods.html which was a form to get the food request data using a POST method, save to db in a helper function create_food and save to db in that same helper function.
/recipes --> all_recipes.html allows for the user to view all the recipes found from the API request by querying all data from recipes table using jinja for loop to iterate through the data.
/all_users --> all_users.html allows for the user to see all users of the system, food they looked up and some of the recipes they got back.
/review --> review.html allows for the user to submit a review from a form and save it to the db table Reviews.
/all_reviews --> all_reviews.html allows for the user to see all the reviews left on the page.
404 --> 404.html to handle a 404 error.

### Requirements ###
I have completed all requirements to the best of my ability as well as the additional 2 requirements.

### - [ ] Ensure that the `SI364midterm.py` file has all the setup (`app.config` values, import statements, code to run the app if that file is run, etc) necessary to run the Flask application, and the application runs correctly on `http://localhost:5000` (and the other routes you set up) ###
### - [ ] Add navigation in `base.html` with links (using `a href` tags) that lead to every other viewable page in the application. (e.g. in the lecture examples from the Feb 9 lecture, [like this](https://www.dropbox.com/s/hjcls4cfdkqwy84/Screenshot%202018-02-15%2013.26.32.png?dl=0) ) ###
### - [ ] Ensure that all templates in the application inherit (using template inheritance, with `extends`) from `base.html` and include at least one additional `block`. ###
### - [ ] Include at least 2 additional template `.html` files we did not provide. ###
### - [ ] At least one additional template with a Jinja template for loop and at least one additional template with a Jinja template conditional. ###
    - These could be in the same template, and could be 1 of the 2 additional template files.
### - [ ] At least one errorhandler for a 404 error and a corresponding template. ###
### - [ ] At least one request to a REST API that is based on data submitted in a WTForm. ###
### - [ ] At least one additional (not provided) WTForm that sends data with a `GET` request to a new page. ###
### - [ ] At least one additional (not provided) WTForm that sends data with a `POST` request to the *same* page. ###
### - [ ] At least one custom validator for a field in a WTForm. ###
### - [ ] At least 2 additional model classes. ###
### - [ ] Have a one:many relationship that works properly built between 2 of your models. ###
### - [ ] Successfully save data to each table. ###
### - [ ] Successfully query data from each of your models (so query at least one column, or all data, from every database table you have a model for). ###
### - [ ] Query data using an `.all()` method in at least one view function and send the results of that query to a template. ###
### - [ ] Include at least one use of `redirect`. (HINT: This should probably happen in the view function where data is posted...) ###
### - [ ] Include at least one use of `url_for`. (HINT: This could happen where you render a form...)) ###
### - [ ] Have at least 3 view functions that are not included with the code we have provided. (But you may have more! *Make sure you include ALL view functions in the app in the documentation and ALL pages in the app in the navigation links of `base.html`.*) ###

### Additional Requirements for an additional 200 points (to reach 100%) -- an app with extra functionality!

### (100 points) Include an *additional* model class (to make at least 4 total in the application) with at least 3 columns. Save data to it AND query data from it; use the data you query in a view-function, and as a result of querying that data, something should show up in a view. (The data itself should show up, OR the result of a request made with the data should show up.) **

** (100 points) Write code in your Python file that will allow a user to submit duplicate data to a form, but will *not* save duplicate data (like the same user should not be able to submit the exact same tweet text for HW3). ###