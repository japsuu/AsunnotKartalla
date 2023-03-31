import folium

from Services import ioService, dataService


def re_render_map_from_cached_data():
    # Get cached data.
    re_render_map(dataService.get_data_cache())


def re_render_map(data):
    # Center to Finland.
    m = folium.Map(location=[65.34910944263534, 26.425770683543483], zoom_start=5)

    # Add markers.
    for listing in data:
        tooltip = listing['title']
        geocode = listing['geocode']

        # Skip non-geocoded entries.
        if geocode is None:
            continue

        folium.Marker(
            geocode, popup=f'''
                        <i>{listing['address']}</i>
                        </br>
                        <i>{listing['rooms']}</i>
                        </br>
                        <i>{listing['price']}</i>
                        </br>
                        <a href="{listing['url']}">Link</a>
                        ''', tooltip=tooltip
        ).add_to(m)

    # Save the map.
    ioService.overwrite_map_file(m.get_root().render())


def get_latest_map():
    return ioService.read_map_file()

