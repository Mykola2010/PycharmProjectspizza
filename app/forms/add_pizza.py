from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, Length, URL

class PizzaForm(FlaskForm):
    name = StringField("Pizza Name", [DataRequired(), Length(max=80)])
    description = StringField("Description",[DataRequired(), Length(max=240)])
    price = FloatField("Price", [DataRequired()])
    image = StringField("Image URL", [DataRequired(), URL()])
    submit = SubmitField("Add Pizza")