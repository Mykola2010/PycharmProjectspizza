from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import PizzaForm
from app.models import Pizza, Session, engine
from app.models import API_KEY
import requests

weather_type = {
    "Clear": "Ясно \U00002600",
    "Clouds": "Хмарно \U00002601",
    "Rain": "Дощ \U00002614",
    "Thunderstorm": "Гроза \U000026A1",
    "Snow": "Сніг \U0001F328",
    "Mist": "Туман \U0001F32B"
}

pizza_recommendations = {
    "Clear": "Спробуй класичну Маргариту",
    "Clouds": "Зігрійся гострою папероні",
    "Rain": "Гаряча піца з чотирма сирами в цей дощовий день.",
    "Thunderstorm": "Як щодо гавайської піци?",
    "Snow": "Побалуйте себе піццою Діаволо, щоб зігрітися.",
    "Mist": "Для баварської піци підійде туманний день"
}


@app.route('/', methods=['GET', 'POST'])
def index():
    weather_message = None
    pizza_suggestion = None

    if request.method == 'POST':
        city_name = request.form.get('city_name', '').strip()
        if city_name:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name.lower()}&appid={API_KEY}&units=metric&lang=ua"
            response = requests.get(url)

            if response.status_code == 200:
                weather_data = response.json()

                weather_condition = weather_data['weather'][0]['main']
                weather_icon = weather_type.get(weather_condition, "Невідомо")
                temp = weather_data['main']['temp']
                weather_message = f"{weather_icon} {temp}°C"

                pizza_suggestion = pizza_recommendations.get(weather_condition, pizza_recommendations)
            else:
                weather_message = "Не вдалося отримати дані про погоду. Спробуйте ще раз."
        else:
            weather_message = "Будь ласка, введіть назву міста."

    return render_template('index.html', weather_data=weather_message, pizza_suggestion=pizza_suggestion)


@app.route('/add-pizza/', methods=['GET', 'POST'])
def add_pizza():
    form = PizzaForm()
    if form.validate_on_submit():
        session = Session(bind=engine)
        new_pizza = Pizza(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            image=form.image.data
        )
        try:
            session.add(new_pizza)
            session.commit()
            flash("Pizza added successfully!", "success")
            return redirect(url_for('add_pizza'))
        except Exception as exception:
            session.rollback()
            flash(f"Error: {exception}", "danger")
        finally:
            session.close()

    return render_template('add_pizza.html', form=form)


@app.route('/menu/')
def menu():
    session = Session(bind=engine)
    pizzas = session.query(Pizza).all()
    session.close()
    return render_template('menu.html', pizzas=pizzas)
