def convert_data_structure(list_of_dicts):
    data = dict()
    for entry in list_of_dicts:
        id = entry.pop('id')
        data.update({id: entry})
    return data
