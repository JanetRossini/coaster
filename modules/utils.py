import os

import bpy


def make_pairs(items):
    return [items[i:i + 2] for i in range(0, len(items)-1, 2)]


def coaster_base_path():
    home = os.path.expanduser('~')
    return os.path.join(home, 'coaster')


def coaster_data_in_path():
    return os.path.join(coaster_base_path(), 'data-in')


def coaster_objects_in_path():
    return os.path.join(coaster_base_path(), 'objects-in')


def coaster_scripts_out_path():
    return os.path.join(coaster_base_path(), 'scripts-out')


def activate_object_by_name(partial_name):
    for obj in bpy.context.scene.objects:
        if partial_name in obj.name:
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
            return obj
    return None
