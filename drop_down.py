import bpy

# Define the items for the dropdown menu
dropdown_items = [
    ("OPTION1", "Option 1", "Select Option 1"),
    ("OPTION2", "Option 2", "Select Option 2"),
    ("OPTION3", "Option 3", "Select Option 3")
]


# Define a property group to store the selected value
class MyAddonProperties(bpy.types.PropertyGroup):
    # noinspection SqlNoDataSourceInspection
    dropdown_property: bpy.props.EnumProperty(
        items=dropdown_items,
        name="Dropdown Menu",
        description="Select an option from the dropdown menu",
        update=lambda self, context: print("Selected Option:", self.dropdown_property)
    )


# Define the panel to display the dropdown menu
class DropdownPanel(bpy.types.Panel):
    bl_label = "Dropdown Menu"
    bl_idname = "OBJECT_PT_dropdown_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tools"

    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene.my_addon_properties, "dropdown_property")

# Register the property group and panel

def register():
    bpy.utils.register_class(MyAddonProperties)
    bpy.types.Scene.my_addon_properties = bpy.props.PointerProperty(type=MyAddonProperties)
    bpy.utils.register_class(DropdownPanel)


def unregister():
    bpy.utils.unregister_class(MyAddonProperties)
    del bpy.types.Scene.my_addon_properties
    bpy.utils.unregister_class(DropdownPanel)


# Run register function
if __name__ == "__main__":
    register()