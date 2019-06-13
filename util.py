import hashlib
import os


def hash_password(password):
    salt = str(os.urandom(50))
    hashed_password = hashlib.sha512((password + salt).encode()).hexdigest()
    return hashed_password, salt


def hash_password_with_custom_salt(password, salt):
    hashed_password = hashlib.sha512((password + str(salt)).encode()).hexdigest()
    return hashed_password


def convert_data_structure(list_of_dicts):
    data = dict()
    for entry in list_of_dicts:
        id = entry.pop('id')
        data.update({id: entry})
    return data


def sorted_dict(dict_, by=None, direction='asc'):
    """
    :param dict_:
        nested dictionary of questions or answers
    :param by:
        order parameter
    :param direction:
        asc or desc
    :return:
        same data structure as dict_, nested dictionary, ordered
    """
    ordered_dict = dict()
    if not by:
        by = 'submission_time'
    sorted_dict = sorted(dict_, key=lambda x: dict_[x][by], reverse=True if direction == 'desc' else False)
    for element in sorted_dict:
        ordered_dict.update({element: dict_[element]})
    return ordered_dict