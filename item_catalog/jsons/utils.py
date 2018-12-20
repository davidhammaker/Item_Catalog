def json_prep(items):
    """Convert a model-type object into a JSON-serializable object.

    Keyword Arguments:
    items -- the model-type object to be converted.
    """

    # If the object is a list, convert it to a list of dictionaries.
    if type(items) == type([]):
        prepped = []
        for item in items:
            prepped_item = {
                'id': item.id,
                'name': item.name,
                'sport': item.sport,
                'category': item.category,
                'description': item.description,
                'date': item.date,
                'user': item.user.username
            }
            prepped.append(prepped_item)
        return {'items': prepped}

    # If the object is not a list, convert it to a dictionary.
    else:
        prepped = {
            'id': items.id,
            'name': items.name,
            'sport': items.sport,
            'category': items.category,
            'description': items.description,
            'date': items.date,
            'user': items.user.username
        }
        return {'item': prepped}
