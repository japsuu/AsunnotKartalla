from Services import dataService, ioService


def process():
    data = dataService.get_data_cache()
    assign_default_geocode_provider_to_cache(data)


# Jesus, that's a long function name.
def assign_default_geocode_provider_to_cache(data):
    # Hacky wacky way to insert an element in to the dict.
    for i, entry in enumerate(data):
        if 'geocode_provider' in entry:
            continue
        if entry['geocode'] is not None:
            provider = 'unknown'
        else:
            provider = None

        new_entry = insert_dict_item(entry, item_to_insert={'geocode_provider': provider}, position_to_insert_before='url')
        data[i] = new_entry

    ioService.overwrite_listings_file(data)


def insert_dict_item(target_dict, item_to_insert=None, position_to_insert_before=None):
    """
    Insert a key, value pair into an ordered dictionary.
    Insert before the specified position.
    """
    if item_to_insert is None:
        item_to_insert = {}
    from collections import OrderedDict
    d = OrderedDict()
    # abort early if not a dictionary:
    if not item_to_insert or not isinstance(item_to_insert, dict):
        print('Aborting. Argument item must be a dictionary.')
        return target_dict
    # insert anywhere if argument pos not given:
    if not position_to_insert_before:
        target_dict.update(item_to_insert)
        return target_dict
    for item_k, item_v in item_to_insert.items():
        for k, v in target_dict.items():
            # insert key at stated position:
            if k == position_to_insert_before:
                d[item_k] = item_v
            d[k] = v
    return d
