from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    mealType = StringField('Meal Type', validators=[DataRequired()])
    mainIngredient = StringField('Protein')
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')
