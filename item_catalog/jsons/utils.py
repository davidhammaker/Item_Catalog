def json_prep(items):
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
