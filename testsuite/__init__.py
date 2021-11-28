def exclude_dict_keys(resp, exclude_list):
    for key, value in exclude_list:
        if key in resp:
            if value in resp[key]:
                del resp[key][value]
    return resp
