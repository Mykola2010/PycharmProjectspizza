from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import PizzaForm
from app.models import Pizza, Session, engine

@app.route('/')
def index():
    return render_template('index.html')


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