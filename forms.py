from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class NewItemForm(FlaskForm):
    name = StringField('Item Name', validators=[DataRequired(), Length(max=64)])
    sport = SelectField('Sport', choices=['Baseball',
                                          'Basketball',
                                          'Bowling',
                                          'Boxing',
                                          'Football',
                                          'Golf',
                                          'Hockey',
                                          'Soccer',
                                          'Tennis',
                                          'Other'],
                        validators=[DataRequired()])
    category = SelectField('Category', choices=['Accessories',
                                                'Apparel',
                                                'Equipment',
                                                'Fan Gear'],
                           validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=1024)])
    date = StringField('Date', validators=[DataRequired()])
    submit = SubmitField('Submit')
