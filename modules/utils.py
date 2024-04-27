import os

import bpy


def make_pairs(items):
    return [items[i:i + 2] for i in range(0, len(items)-1, 2)]


def make_elements(name):
    home = os.path.expanduser('~')
    working = os.path.join(home, 'PycharmProjects', 'coaster',  'coasterobjects')
    filepath = os.path.join(working, name + '.blend')
    directory = os.path.join(filepath, 'Object')
    filename = name
    return filepath, directory, filename


def activate_object_by_name(partial_name):
    for obj in bpy.context.scene.objects:
        if partial_name in obj.name:
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
            return
    print("didn't find it")
