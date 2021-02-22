from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.validators import DataRequired

class If_form(FlaskForm):
    interface = SelectField("Please select Interface",choices=[])