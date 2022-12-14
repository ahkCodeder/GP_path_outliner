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

# OUTPUTS IT INTO A GREASE PENCIL WITH ONE LAYER THAT CAN BE ANIMATED ON EASYLY
turn_default_into_one_animatable_object = True

# THIS ADDS MORE POINTS ONTO THE GP OUTPUT OBJECT 
add_subdivision = False

# THIS DOSNT WORK WITH turn_default_into_one_animatable_object = True unless its set to 0
# THE AMOMUNT OF LAGG EFFECT 
lagg_effect_amount = 7

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

#Default color name SHOUDL BE A (R;G;B;A)
color = (0.02,1,0,1)

# on's this will be sett to on 1's by default for the smoothest animations
frame_ons =  1

""" 
VARIABLES END
"""

C = bpy.context
D = bpy.data

D.scenes[0].frame_current = start_frame

area_type = "PROPERTIES"
area = [area for area in C.screen.areas if area.type == area_type][0]

window = C.window_manager.windows[0]
region = area.regions[-1]

def config_and_draw(GP_obj): 
    
    C.view_layer.objects.active = bpy.data.objects[GP_obj]
    D.objects[GP_obj].select_set(True)
        
    D.objects[GP_obj].active_material_index = 0
    target_material_name = output_collection
    D.objects[GP_obj].active_material.name = target_material_name
    target_material_name = D.objects[GP_obj].active_material.name
        
    bpy.ops.object.gpencil_modifier_add(type='GP_LINEART')
    D.objects[GP_obj].grease_pencil_modifiers['Line Art'].source_type = 'SCENE'
    D.objects[GP_obj].grease_pencil_modifiers["Line Art"].target_layer = "GP_Layer"
    D.objects[GP_obj].grease_pencil_modifiers["Line Art"].target_material = bpy.data.materials[target_material_name]
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

            bpy.data.scenes[0].frame_current = bpy.data.scenes[0].frame_current + frame_ons

    bpy.data.scenes[0].frame_current = start_frame

    prev_obj = D.collections[output_collection].objects[0]

    lagg_obj = []
    
    for obj in D.collections[output_collection].objects:
        
        lagg_obj.append(obj)
        
        C.view_layer.objects.active = D.objects[obj.name_full]
        C.object.active_material.grease_pencil.color = color
        C.view_layer.objects.active = None
        
        obj.hide_render = False
        obj.keyframe_insert("hide_render")
        
        if not turn_default_into_one_animatable_object: 
            try:
                obj.select_set(True)
                obj.keyframe_insert(bpy.ops.transform.translate(value=(0, 0, 0),orient_axis_ortho='X',orient_type='GLOBAL',orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),orient_matrix_type='GLOBAL',mirror=False, use_proportional_edit=False,proportional_edit_falloff='SMOOTH',proportional_size=1, use_proportional_connected=False,use_proportional_projected=False))
            except:
                obj.select_set(False)
                print("keyfram failed")

            if (not (obj == prev_obj)) and lagg_effect_amount < len(lagg_obj) - 1:

                re_obj = lagg_obj.pop(0)
                re_obj.select_set(True)
                re_obj.hide_render = True
                re_obj.keyframe_insert("hide_render") 
                re_obj.select_set(False)
                
                try:
                    re_obj.select_set(True)
                    re_obj.keyframe_insert(bpy.ops.transform.translate(value=away_from_frame_distance,orient_axis_ortho='X',orient_type='GLOBAL',orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),orient_matrix_type='GLOBAL',mirror=False, use_proportional_edit=False,proportional_edit_falloff='SMOOTH',proportional_size=1, use_proportional_connected=False,use_proportional_projected=False))
                except:
                    re_obj.select_set(False)
                    print("keyframe failed")

            prev_obj = obj
        
        else:

            if not obj == prev_obj:

                prev_obj.hide_render = True
                prev_obj.keyframe_insert("hide_render") 

            prev_obj = obj


        bpy.data.scenes[0].frame_current = bpy.data.scenes[0].frame_current + frame_ons
    
    if not turn_default_into_one_animatable_object:
        for obj in D.collections['g'].objects:
        
            obj.select_set(True)
        
            area_type = "DOPESHEET_EDITOR"
            area = [area for area in C.screen.areas if area.type == area_type][0]

            window = C.window_manager.windows[0]
            region = area.regions[-1]
            with C.temp_override(window=window,area=area,region=region):
            
                bpy.ops.action.interpolation_type(type='CONSTANT')

            obj.select_set(False)
    
    if turn_default_into_one_animatable_object: 
        for obj in D.collections[output_collection].objects:
            obj.select_set(True)
        
        C.view_layer.objects.active = D.collections[output_collection].objects[0]
        
        bpy.ops.object.join()
        
        D.scenes[0].frame_current = -1
        GP_name = D.collections[output_collection].objects[0].name_full
        D.grease_pencils[GP_name].layers[0].select = True
        bpy.ops.gpencil.layer_merge(mode='ALL')
        
if MODE == "TRACE_1":
    with C.temp_override(window=window,area=area,region=region):

        while True:

            current_frame = D.scenes[0].frame_current

            if end_frame < current_frame:
                break
        
            bpy.ops.object.gpencil_add(align='WORLD', location=(0, 0, 0), scale=(1, 1, 1), type='EMPTY')
            GP_obj = D.collections['g'].objects[-1].name_full
        
            config_and_draw(GP_obj=GP_obj)
    
            bpy.data.scenes[0].frame_current = bpy.data.scenes[0].frame_current + frame_ons

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
    
            bpy.data.scenes[0].frame_current = bpy.data.scenes[0].frame_current + frame_ons
