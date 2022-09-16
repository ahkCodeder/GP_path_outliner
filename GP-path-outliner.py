import bpy
"""
INSTRUCTION 
"""
"""

!!IMPORTANT!!  ONLY WORKS ON OBJECTS AND PART OF OBJECTS ARE SEEN IN CAMERA VIEW  

0. WINDOWS THAT NEED TO BE ALL BE OPEN WHEN SCRIPT RUNS  :: 3D VIEW-(object mode) , OUTLINER, PROPERTIES
1. create a collection to out put to 
2. figure out what the defualt name is for the new grease pencil that is created 
3. animate the object you want to trace the path of 
4. set the settings right and run the script  
5. OPTIONAL :: after things are done you can go into grease pencil and remove linse and things you dont want with remove points with the e

"""
""" 
END INSTRUCTION 
"""
"""
VARIABLES 
"""
"""
MODES :: 
"DEFAULT"
:: this mode just adds outlines to the object and animation
    
"TRACE_1"
:: TRACES THE OBJECT PATH AND LEAVES STROKES AFTER IT INTO ANIMAION(ONLY STROKES THAT ARE VISSABLE FROM CAMERAS VIEW GET DRAWN)

"TRACE_2"
:: TRACES PATH INTO ONE GREASE PENCIL OBJECT (STROKES ONLY FROM CAMERA VIEW)
"""
MODE = "DEFAULT"

# THIS ADDS MORE POINTS ONTO THE GP OUTPUT OBJECT 
add_subdivision = False

# TIP :: START LOWEST THEN GO HIGHER IF YOU NEED MORE 
#this gose from 1-5 subdivision amount higher is more and takes more time and harder to run 
subdivison_level = 1

# defualt 25 
stroke_thickness = 50

#defualt = 1.0 down to 0.0
stroke_opacity = 1.0

# start frame 
start_frame = 0

# end frame
end_frame = 30

# output collection name 
output_collection = "g"

# MOVES THE STROKES AWAY FROM THE VIEW PRORT IN ANIMATION 
away_from_frame_distance = (0,0,10000000000000000)

# Default color name 
color = "Black"

# name for the grease pencil object being created 'GPencil' is the first one if that one exist new once might be 'GPencil.001' or 'GPencil.002' or more
#GP_obj = 'GPencil'

""" 
VARIABLES END
"""

C = bpy.context
D = bpy.data

D.scenes[0].frame_current = start_frame

area_type = "OUTLINER"
area = [area for area in C.screen.areas if area.type == area_type][0]

window = C.window_manager.windows[0]
region = area.regions[-1]

area_type = "PROPERTIES"
area = [area for area in C.screen.areas if area.type == area_type][0]

window = C.window_manager.windows[0]
region = area.regions[-1]

def config_and_draw(GP_obj): 
    
    C.view_layer.objects.active = bpy.data.objects[GP_obj]
    D.objects[GP_obj].select_set(True)
        
    D.objects[GP_obj].active_material_index = 0
    D.objects[GP_obj].active_material.name = "Black"
        
    bpy.ops.object.gpencil_modifier_add(type='GP_LINEART')
    D.objects[GP_obj].grease_pencil_modifiers['Line Art'].source_type = 'SCENE'
    D.objects[GP_obj].grease_pencil_modifiers["Line Art"].target_layer = "GP_Layer"
    D.objects[GP_obj].grease_pencil_modifiers["Line Art"].target_material = bpy.data.materials["Black"]
    D.objects[GP_obj].grease_pencil_modifiers["Line Art"].thickness = stroke_thickness
    D.objects[GP_obj].grease_pencil_modifiers["Line Art"].opacity = stroke_opacity
    bpy.ops.object.gpencil_modifier_apply(modifier="Line Art")

if MODE == "DEFAULT":
    with C.temp_override(window=window,area=area,region=region):

        while True:

            current_frame = D.scenes[0].frame_current

            if end_frame + 1 < current_frame:
                break

            bpy.ops.object.gpencil_add(align='WORLD', location=(0, 0, 0), scale=(1, 1, 1), type='EMPTY')

            GP_obj = D.collections[output_collection].objects[-1].name_full

            config_and_draw(GP_obj=GP_obj)

            bpy.ops.object.gpencil_modifier_apply(modifier="Line Art")

            bpy.data.scenes[0].frame_current = bpy.data.scenes[0].frame_current + 1

    bpy.data.scenes[0].frame_current = start_frame

    prev_obj = D.collections[output_collection].objects[0]

    for obj in D.collections[output_collection].objects:

        obj.hide_render = False
        obj.keyframe_insert("hide_render")

        try:
            obj.select_set(True)
            obj.keyframe_insert(bpy.ops.transform.translate(value=(0, 0, 0),orient_axis_ortho='X',orient_type='GLOBAL',orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),orient_matrix_type='GLOBAL',mirror=False, use_proportional_edit=False,proportional_edit_falloff='SMOOTH',proportional_size=1, use_proportional_connected=False,use_proportional_projected=False))
        except:
            obj.select_set(False)
            print("keyfram failed")

        if not obj == prev_obj:

            prev_obj.hide_render = True
            prev_obj.keyframe_insert("hide_render")

            try:
                prev_obj.select_set(True)
                prev_obj.keyframe_insert(bpy.ops.transform.translate(value=away_from_frame_distance,orient_axis_ortho='X',orient_type='GLOBAL',orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),orient_matrix_type='GLOBAL',mirror=False, use_proportional_edit=False,proportional_edit_falloff='SMOOTH',proportional_size=1, use_proportional_connected=False,use_proportional_projected=False))
            except:
                prev_obj.select_set(False)
                print("keyframe failed")

        prev_obj = obj


        bpy.data.scenes[0].frame_current = bpy.data.scenes[0].frame_current + 1
        
if MODE == "TRACE_1":
    with C.temp_override(window=window,area=area,region=region):

        while True:

            current_frame = D.scenes[0].frame_current

            if end_frame < current_frame:
                break
        
            bpy.ops.object.gpencil_add(align='WORLD', location=(0, 0, 0), scale=(1, 1, 1), type='EMPTY')
            GP_obj = D.collections['g'].objects[-1].name_full
        
            config_and_draw(GP_obj=GP_obj)
    
            bpy.data.scenes[0].frame_current = bpy.data.scenes[0].frame_current + 1

if MODE == "TRACE_2":            
    with C.temp_override(window=window,area=area,region=region):
    
        while True:

            current_frame = D.scenes[0].frame_current

            if end_frame < current_frame:
                break  
            
            if len(D.collections[output_collection].objects) == 0:
                bpy.ops.object.gpencil_add(align='WORLD', location=(0, 0, 0), scale=(1, 1, 1), type='EMPTY')
                
            GP_obj = D.collections[output_collection].objects[-1].name_full  
            
            config_and_draw(GP_obj=GP_obj)
    
            bpy.data.scenes[0].frame_current = bpy.data.scenes[0].frame_current + 1
