import pip
pip.main(['install', 'kinparse', '--user'])
import bpy
import sys
sys.path.insert(0, '/home/malhaar/development/augmentia')
from parse import parse
from ref_value import ref_value

# Clear existing objects
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete()

# Path to the .blend file
blend_path = {"LED":"static/blend_files/LED_2.blend", "R":"static/blend_files/resistor.blend"}
blend_file_path_arduino = "static/blend_files/arduino.blend"

# Load Arduino objects
with bpy.data.libraries.load(blend_file_path_arduino) as (data_from, data_to):
    data_to.objects = [name for name in data_from.objects]

for obj in data_to.objects:
    bpy.context.collection.objects.link(obj)

ref_val = ref_value('static/netlist_file/circuit.net')
con = parse('static/netlist_file/circuit.net')
inc_obj = list(ref_val.values())

if len(inc_obj) == 1:
    # Get reference object from Arduino
    reference_object = bpy.data.objects[list(con.items())[0][0]]
    cord = reference_object.location.copy()
    place = 0
    for j in con.items():
        if j[0].split("_")[0] == "A1" and int(j[0].split("_")[1]) in range(15,31):
            try:
                if one_side != True:
                    place = 1
                    break
            except NameError:
                one_side = True
        elif j[0].split("_")[0] == "A1" and int(j[0].split("_")[1]) not in range(15,31):
            try:
                if one_side != False:
                    place = 1
                    break
            except NameError:
                one_side = False
    
    if place == 0:
        coeff = 1
        if inc_obj[0] == "R":
            coeff = -1
        if int(list(con.items())[0][0].split("_")[1]) in range(15,31):
            cord.y += coeff*50 # Malhaar- decide + or - based on which side the port on arduino is (add if cond)
        else:
            cord.y -= coeff*50
    else:
        reference_object = bpy.data.objects['arduino']
        cord = reference_object.location.copy()
        cord.x += 100

    cord.z += 40

    with bpy.data.libraries.load(blend_path[inc_obj[0]]) as (data_from, data_to):
        data_to.objects = [name for name in data_from.objects]

    relative_positions = {}
    bpy.ops.object.select_all(action='DESELECT')

    for obj in data_to.objects:
        # Calculate the offset of each object from the reference object
        offset = obj.location * 5
        # Store the offset in the dictionary
        relative_positions[obj.name] = offset
        # Set the location of the object to the new position
        obj.location = cord + offset
        obj.scale *= 5

        bpy.context.collection.objects.link(obj)

    for obj in data_to.objects:
        obj.select_set(True)

    # Rotate selected objects by 90 degrees along the Z-axis
    bpy.ops.transform.rotate(value=1.5708, orient_axis='Z', orient_type='GLOBAL')

    # Update the scene
    bpy.context.view_layer.update()
    
bpy.ops.object.select_all(action='DESELECT')
# deselect all the objects to avoid to edit all together
#bpy.ops.object.mode_set(mode='OBJECT')
#bpy.ops.object.mode_set(mode='EDIT')

for link in list(con.items()):

    # select the first plane by name
    plane1 = bpy.data.objects[link[0]] # Malhaar- change from
    plane1.select_set(True)
    #bpy.context.view_layer.objects.active = plane1

    # select the second plane by name
    plane2 = bpy.data.objects[link[1]] # Malhaar- change to
    plane2.select_set(True)
    #bpy.context.view_layer.objects.active = plane2c

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

### Exporting the file
export_path = "static/models/final_model.glb"

# Select all objects in the scene
bpy.ops.object.select_all(action='SELECT')

# Export the scene to .glb format
bpy.ops.export_scene.gltf(filepath=export_path, export_format='GLB')