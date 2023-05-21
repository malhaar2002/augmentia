import os
import bpy

def make_glb():
    # Clear existing objects
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

    # Path to the .blend file
    blend_files_dir = "static/blend_files"
    blend_file_path_arduino = os.path.join(blend_files_dir, "arduino.blend")
    blend_file_path_led = os.path.join(blend_files_dir, "LED_2.blend")
    blend_file_path_resistor = os.path.join(blend_files_dir, "resistor.blend")

    # Load Arduino objects
    with bpy.data.libraries.load(blend_file_path_arduino) as (data_from, data_to):
        data_to.objects = [name for name in data_from.objects]

    for obj in data_to.objects:
        bpy.context.collection.objects.link(obj)

    # Get reference object from Arduino
    pin_ref = 'A1-23'
    reference_object = bpy.data.objects[pin_ref]
    cord = reference_object.location.copy()
    pin_num = int(pin_ref.split('-')[1])
    if pin_num >= 15 and pin_num <= 30:
        cord.y += 50 # Malhaar- decide + or - based on which side the port on arduino is (add if cond)
    else:
        cord.y -= 50
    cord.z += 20

    # Malhaar- choose which components to load into the file
    # Load LED objects and place them at the modified reference location
    with bpy.data.libraries.load(blend_file_path_led) as (data_from, data_to):
        data_to.objects = [name for name in data_from.objects]

    relative_positions = {}

    for obj in data_to.objects:
        # Calculate the offset of each object from the reference object
        offset = obj.location * 5
        # Store the offset in the dictionary
        relative_positions[obj.name] = offset

        # Set the location of the object to the new position
        obj.location = cord + offset
        obj.scale *= 5

        bpy.context.collection.objects.link(obj)
        
    bpy.ops.object.select_all(action='DESELECT')
    # deselect all the objects to avoid to edit all together
    #bpy.ops.object.mode_set(mode='OBJECT')
    #bpy.ops.object.mode_set(mode='EDIT')

    # select the first plane by name
    plane1 = bpy.data.objects['A1-23'] # Malhaar- change from
    plane1.select_set(True)
    #bpy.context.view_layer.objects.active = plane1

    # select the second plane by name
    plane2 = bpy.data.objects['D1_K'] # Malhaar- change to
    plane2.select_set(True)
    #bpy.context.view_layer.objects.active = plane2

    bpy.context.view_layer.objects.active = plane1
    bpy.context.view_layer.objects.active = plane2

    # enter edit mode
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type="FACE")
    bpy.ops.mesh.select_all(action = 'DESELECT')
    bpy.ops.object.mode_set(mode = 'OBJECT')
    plane1.data.polygons[0].select = True
    plane2.data.polygons[0].select = True
    bpy.ops.object.mode_set(mode = 'EDIT') 

    # creating the tube between the two planes
    bpy.ops.mesh.add_curvebased_tube(generated_name="Wire", subdiv=16, tube_resolution_u=30, handle_ext_1=8, handle_ext_2=8, show_smooth=True, point1_scale=0.4, point2_scale=0.4, flip_v=False, flip_u=False)

    # back to edit mode
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')

    # Malhaar- Work to do

    # 1- use your net file programme to get the connections then place the components in the right place based on
    # left or right place of the port.
    # 2- make changes to the wiring code so that the connections extracted from the .net file have wires between them

    # Extracting the .glb from the .blend file

    # Set the file path and name for the exported .glb file
    export_path = "final_model.glb"

    # Select all objects in the scene
    bpy.ops.object.select_all(action='SELECT')

    # Export the scene to .glb format
    bpy.ops.export_scene.gltf(filepath=export_path, export_format='GLB')