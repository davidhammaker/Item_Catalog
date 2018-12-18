from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length


class ItemForm(FlaskForm):
    name = StringField('Item Name', validators=[DataRequired(), Length(max=64)])
    sport = SelectField('Sport', choices=[('Baseball', 'Baseball'),
                                          ('Basketball', 'Basketball'),
                                          ('Bowling', 'Bowling'),
                                          ('Boxing', 'Boxing'),
                                          ('Football', 'Football'),
                                          ('Golf', 'Golf'),
                                          ('Hockey', 'Hockey'),
                                          ('Soccer', 'Soccer'),
                                          ('Tennis', 'Tennis'),
                                          ('Other', 'Other')],
                        validators=[DataRequired()])
    category = SelectField('Category', choices=[('Accessories', 'Accessories'),
                                                ('Apparel', 'Apparel'),
                                                ('Equipment', 'Equipment'),
                                                ('Fan Gear', 'Fan Gear')],
                           validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Length(max=2048)])
    private = BooleanField('Private')
    submit = SubmitField('Submit')
