def json_prep(items):
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
