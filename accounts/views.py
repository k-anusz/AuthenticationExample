import requests
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import City
from .models import Bank
from .models import BankAccount
from .forms import CityForm
from .forms import BankForm
from .forms import AccountForm
from .forms import UserRegistrationForm


# from django.contrib import messages


# @login_required decorator allows to limit access to the index page and check whether the user is authenticated
# if so, index page is rendered. If not, the user is redirected to the login page via login_url
@login_required(login_url='login')
def index(request):
    # Render the index page
    return render(request, 'accounts/index.html')


def register_view(request):
    # This function renders the registration form page and create a new user based on the form data
    if request.method == 'POST':
        # We use Django's UserCreationForm which is a model created by Django to create a new user.
        # UserCreationForm has three fields by default: username (from the user model), password1, and password2.
        # If you want to include email as well, switch to our own custom form called UserRegistrationForm
        form = UserCreationForm(request.POST)
        # check whether it's valid: for example it verifies that password1 and password2 match
        if form.is_valid():
            form.save()
            # if you want to login the user directly after saving, use the following two lines instead, and redirect to index
            # user = form.save()
            # login(user)
            # redirect the user to login page so that after registration the user can enter the credentials
            return redirect('login')
    else:
        # Create an empty instance of Django's UserCreationForm to generate the necessary html on the template.
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    # this function authenticates the user based on username and password
    # AuthenticationForm is a form for logging a user in.
    # if the request method is a post
    if request.method == 'POST':
        # Plug the request.post in AuthenticationForm
        form = AuthenticationForm(data=request.POST)
        # check whether it's valid:
        if form.is_valid():
            # get the user info from the form data and login the user
            user = form.get_user()
            login(request, user)
            # redirect the user to index page
            return redirect('index')
    else:
        # Create an empty instance of Django's AuthenticationForm to generate the necessary html on the template.
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    # This is the method to logout the user
    logout(request)
    # redirect the user to index page
    return redirect('index')


# view
@login_required(login_url='login')
def money_tracker_view(request):
    # direct the user to money tracker page
    banks = Bank.objects.all()
    context = {'banks': banks}
    return render(request, 'accounts/money-tracker.html', context)


# add
@login_required(login_url='login')
def add_bank(request):
    # Create a form instance and populate it with data from the request
    form = BankForm(request.POST or None)

    # if request.method == 'POST':
    # check whether it's valid:
    if form.is_valid():
        # save the record into the db
        form.save()
        print('form valid: true')
    else:
        print('form valid: false')
        print(form.errors)

    # after saving redirect to money-tracker page
    return redirect('money-tracker')


# view
@login_required(login_url='login')
def view_account(request, id):
    # direct the user to money tracker page
    account = Bank.objects.get(id=id)
    transactions = BankAccount.objects.all().filter(bankId=id)
    context = {'account': account, 'transactions': transactions}
    return render(request, 'accounts/accounts.html', context)


# add
@login_required(login_url='login')
def add_transaction(request, id):
    # Create a form instance and populate it with data from the request
    form = AccountForm(request.POST or None)
    form2 = BankForm(request.POST or None)

    if request.method == 'POST':
        # check whether it's valid:
        if form.is_valid():
            # save the record into the db
            form.save()
            print('form valid: true')
        else:
            print('form valid: false')
            print(form.errors)
        # this is currently broken, creates a new bank record instead of updating balance on exisiting record
        # if form2.is_valid():
        #     # save the record into the db
        #     form2.save()
        #     print('form2 valid: true')
        # else:
        #     print('form2 valid: false')
        #     print(form2.errors)

    # after saving redirect to money-tracker page
    return redirect('/account/' + str(id))


# view
@login_required(login_url='login')
def delete_account(request, id):
    # Get the bank account based on its id
    bank = Bank.objects.get(id=id)

    # if this is a POST request, we need to delete the form data
    if request.method == 'POST':
        bank.delete()
        # direct the user to money tracker page
        return redirect('money-tracker')

    # if the request is not post, render the page with the task's info
    return render(request, 'accounts/delete.html', {'bank': bank})


@login_required(login_url='login')
def weather_view(request):
    # the api url for getting the weather data
    # {} is a placeholder for the city we will query for
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=f1fe354b524a9755272446c089aaae23'

    err_msg = ''
    # message holds the message that the user sees
    message = ''
    # message_class holds a css class for the color of the message area
    message_class = ''

    if request.method == 'POST':
        # instantiates the form using the request data
        form = CityForm(request.POST)

        # checks if the city input is valid
        if form.is_valid():
            # this is the city name that is input by the user in the front end
            new_city = form.cleaned_data['name']
            # we query the database to make sure that there are no cities with the same name
            # because we dont want duplicate cities being added
            existing_city_count = City.objects.filter(name=new_city).count()
            # if the existing city count is 0 then it is added to the database
            if existing_city_count == 0:
                # r returns the data for the city that gets added
                r = requests.get(url.format(new_city)).json()
                # response 200 means success status from the api.
                # so if the city name entered is valid it will save to the database
                if r['cod'] == 200:
                    # validates and saves to the database
                    form.save()
                else:
                    err_msg = 'Error, The City entered is not a valid City name!'
            else:
                err_msg = 'Error, you already have this city in your list!'
        if err_msg:
            message = err_msg
            message_class = 'p-3 mb-2 bg-danger text-white rounded'
        else:
            message = 'City has been added successfully!'
            message_class = 'p-3 mb-2 bg-success text-white rounded'

    # instantiates the form
    # this goes under the request.method == 'POST' because it allows for it to be blank after it has been submitted
    form = CityForm()

    # Queries our database for all the cities that we have
    cities = City.objects.all()

    # list for our weather data
    weather_data = []

    # gets the weather for each city and appends it to a list
    # This loops over all the cities we have in the database and for each one its going to query the api, the data
    # that gets returned is going to be put into this dictionary called city_weather.
    # then that city_weather dictionary is going to be appended to our weather_data list
    # then it starts over from scratch for the next city and appends that city to the list.
    # ex. if we have 2 cities in the database then this list that we have will have a list of 2 elements
    for city in cities:
        # r is short for response. json() converts the result of the request into a json object
        r = requests.get(url.format(city)).json()

        # this will be our dictionary
        city_weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }

        # appends the city weather dictionary that we create for each city
        weather_data.append(city_weather)

    context = {
        'weather_data': weather_data,
        'form': form,
        'message': message,
        'message_class': message_class
    }
    # direct the user to weather page
    return render(request, 'accounts/weather.html', context)


@login_required(login_url='login')
def delete_city(request, city_name):
    # queries for the city and deletes it
    City.objects.get(name=city_name).delete()
    # redirect the user to weather page
    return redirect('weather')


@login_required(login_url='login')
def account_view(request):
    account = BankAccount.objects.all()
    context = {'account': account}
    return render(request, 'accounts/account.html', context)
