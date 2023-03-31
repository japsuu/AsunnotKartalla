import json

import config


# def clear_all_listings():
#     file_to_delete = open(listings_file, 'w')
#     file_to_delete.close()


def overwrite_listings_file(data):
    try:
        with open(config.ioService_LISTINGS_FILENAME, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except:
        return


def read_listings_file() -> []:
    with open(config.ioService_LISTINGS_FILENAME, 'r', encoding='utf-8') as f:
        return json.load(f)


def overwrite_map_file(data):
    try:
        with open(config.ioService_MAP_FILENAME, 'w', encoding='utf-8') as f:
            f.write(data)
    except:
        return


def read_map_file():
    try:
        with open(config.ioService_MAP_FILENAME, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return 'Could not read map file :('


def overwrite_listings_metadata_file(data):
    try:
        with open(config.ioService_LISTINGS_METADATA_FILENAME, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except:
        return -1


def read_listings_metadata_file() -> []:
    try:
        with open(config.ioService_LISTINGS_METADATA_FILENAME, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return -1
