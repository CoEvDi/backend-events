import copy


def exclude_dict_keys(original_dict, exclude_list):
    dict_data = copy.deepcopy(original_dict)
    for key, value in exclude_list:
        if key in dict_data:
            if value in dict_data[key]:
                del dict_data[key][value]
    return dict_data


def replace_dict_kyedata(original_dict, exclude_list):
    dict_data = copy.deepcopy(original_dict)
    for key, new_data in exclude_list:
        if key in dict_data:
            del dict_data[key]
            if new_data != '':
                new_key, new_value = new_data
                dict_data[new_key] = new_value                
    return dict_data


def add_dict_keys(original_dict, add_list):
    dict_data = copy.deepcopy(original_dict)
    for key, data in add_list:
        dict_data[key] = data
    return dict_data
