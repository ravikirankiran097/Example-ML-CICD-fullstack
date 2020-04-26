from operator import methodcaller

from s2geometry.pywraps2 import S2LatLng, S2CellId


def convert_lat_long_into_s2_cells_level(latitude: float, longitude: float, level: int):
    s2_geometry = S2LatLng.FromDegrees(latitude, longitude)
    s2_cell = S2CellId(s2_geometry)

    s2_cell_correct_level = traverse_s2_cell_to_level(s2_cell, level)
    return s2_cell_correct_level


def traverse_s2_cell_to_level(s2_cell: S2CellId, level: int):
    current_level = s2_cell.level()
    traverse = methodcaller('parent')

    if current_level == level:
        return s2_cell
    elif current_level > level:
        return s2_cell  # Because we do not have a means to traverse down yet

    while current_level != level:
        s2_cell = traverse(s2_cell)
        current_level = s2_cell.level()
    return s2_cell
