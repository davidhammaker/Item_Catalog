from flask_wtf import FlaskForm
from wtforms import (StringField, SelectField, TextAreaField, SubmitField,
                     BooleanField)
from wtforms.validators import DataRequired, Length


class ItemForm(FlaskForm):
    """Item creation and update form.

    Inherits from:
    FlaskForm

    Attributes:
    name -- a StringField specifying the name of the item
    sport -- a SelectField specifying the sport associated with the
        item
    category -- a SelectField specifying the category associated with
        the item
    description -- a TextAreaField specifying the item description
    private -- a BooleanField indicating whether the item is private
    submit -- a SubmitField for submitting the form
    """
    name = StringField('Item Name', validators=[DataRequired(),
                                                Length(max=64)])
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
    category = SelectField('Category',
                           choices=[('Accessories', 'Accessories'),
                                    ('Apparel', 'Apparel'),
                                    ('Equipment', 'Equipment'),
                                    ('Fan Gear', 'Fan Gear')],
                           validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Length(max=2048)])
    private = BooleanField('Private')
    submit = SubmitField('Submit')


class DeleteItemForm(FlaskForm):
    """Item deletion form.

    Attributes:
    submit -- a SubmitField for submitting the form
    """
    submit = SubmitField('Delete')
