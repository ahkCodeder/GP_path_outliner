bl_info = {
    "name": "GP Outliner",
    "author": "AHK <https://github.com/ahkCodeder>",
    "version": (1,0),
    "blender": (3,3,0),
    "category": "Add Grease Pencil",
    "location": "",
    "description": "Adds grease pencil strokes to you're animation",
    "warning": "",
    "doc_url": "",
    "tracer_url": ""
}

import bpy

def GP_outliner(MODE="DEFUALT",turn_default_into_one_animatable_object=False,add_subdivision = False,lagg_effect_amount = 1,fade_amount = 0.20, subdivison_level = 1, stroke_thickness = 20,stroke_opacity = 1,start_frame = 1,end_frame=30,output_collection = "g",R=0,B=0,G=0,A=0,frame_ons = 1):

    # MOVES THE STROKES AWAY FROM THE VIEW PRORT IN ANIMATION 
    away_from_frame_distance = (0,0,10000000)
    
    #Default color name SHOUDL BE A (R;G;B;A)
    color = (R,G,B,A)

    C = bpy.context
    D = bpy.data
    
    D.scenes[0].frame_current = start_frame
    
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
    
    area_type = "PROPERTIES"
    area = [area for area in C.screen.areas if area.type == area_type][0]
    
    window = C.window_manager.windows[0]
    region = area.regions[-1]
    
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
                if not obj == prev_obj:#and lagg_effect_amount < len(lagg_obj):
                    
                    prev_obj.hide_render = True
                    prev_obj.keyframe_insert("hide_render") 
    
                prev_obj = obj
    
            bpy.data.scenes[0].frame_current = bpy.data.scenes[0].frame_current + frame_ons
            
        if not turn_default_into_one_animatable_object:
            for obj in D.collections[output_collection].objects:
            
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
                GP_obj = D.collections[output_collection].objects[-1].name_full
            
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

class VIEW3D_PT_GP_Outliner(bpy.types.Panel):
    
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "GP Outliner"
    bl_label = "Stroke Animation"
    
    def draw(self,context):
        
        props = self.layout.operator("data.grease_pencils_outliner",text="Run")
        
        col = self.layout.column(align=True)
        
        col.prop(context.scene,'MODE')
        col.prop(context.scene,'output_collection')
        
        col.prop(context.scene,'turn_default_into_one_animatable_object')
        col.prop(context.scene,'add_subdivision')
        col.prop(context.scene,'subdivison_level')
        col.prop(context.scene,'lagg_effect_amount')
        col.prop(context.scene,'fade_amount')
        col.prop(context.scene,'stroke_thickness')
        col.prop(context.scene, 'stroke_opacity')
        
        col.prop(context.scene,'start_frame')
        col.prop(context.scene,'end_frame')
        
        col.prop(context.scene,'red_color')
        col.prop(context.scene,'green_color')
        col.prop(context.scene,'blue_color')
        col.prop(context.scene,'alpha_color')
        
        col.prop(context.scene,'frame_ons')
        
        props.MODE = context.scene.MODE
        props.turn_default_into_one_animatable_object = context.scene.turn_default_into_one_animatable_object
        props.add_subdivision = context.scene.add_subdivision
        props.subdivison_level = context.scene.subdivison_level
        props.lagg_effect_amount = context.scene.lagg_effect_amount
        props.fade_amount = context.scene.fade_amount
        props.stroke_thickness = context.scene.stroke_thickness
        props.stroke_opacity = context.scene.stroke_opacity
        
        props.start_frame = context.scene.start_frame
        props.end_frame = context.scene.end_frame
        
        props.output_collection = context.scene.output_collection
        
        props.red_color = context.scene.red_color
        props.green_color = context.scene.green_color
        props.blue_color = context.scene.blue_color
        props.alpha_color = context.scene.alpha_color
        
        props.frame_ons = context.scene.frame_ons    

class DATA_OT_GP_outliner(bpy.types.Operator):
    
    bl_idname = "data.grease_pencils_outliner"
    bl_label = "GP Outliner"
    bl_options = {'REGISTER','UNDO'}

    MODE: bpy.props.EnumProperty(items=[("DEFAULT","DEFAULT",""),("TRACE_1","TRACE_1",""),("TRACE_2","TRACE_2","")])
            
    turn_default_into_one_animatable_object: bpy.props.BoolProperty(
                                                    name="one animation",
                                                    description="This moves the animantion into one GP object so it can be animated",
                                                    default=False)
    
    add_subdivision: bpy.props.BoolProperty(
                                    name="add subdivision",
                                    description="This adds subdivion on the GP object(s) so that you can apply noise f.e",
                                    default=False)
    
    subdivison_level: bpy.props.IntProperty(
                                    name="subdivion amount",
                                    description="This setting adds the amount of subdivisions",
                                    default=1,
                                    min=1,
                                    max=5)
                                       
    lagg_effect_amount: bpy.props.IntProperty(
                                    name="after image",
                                    description="This setting adds an after image of the frames before the current one.",
                                    default=0,
                                    min=0,
                                    max=50)
    
    fade_amount: bpy.props.FloatProperty(
                                name="fade strokes",
                                description="This adds opasity to strokes",
                                default=1.0,
                                min=0.0,
                                max=1.0)
    
    stroke_thickness: bpy.props.IntProperty(
                                name="stroke thickness",
                                description="This adds the stroke thickness",
                                default=15,
                                min=1,
                                max=300)
    
    stroke_opacity: bpy.props.FloatProperty(
                                name="stroke opacity",
                                description="opacity storkes",
                                default=1.0,
                                min=0.0,
                                max=1.0)
    
    start_frame: bpy.props.IntProperty(
                                name="start frame",
                                description="This sets the start frame to run on",
                                default=1,
                                min=0,
                                max=2000000000)
                                
    end_frame: bpy.props.IntProperty(
                            name="end frame",
                            description="This sets the end frame",
                            default=30,
                            min=1,
                            max=2000000001)
    
    output_collection: bpy.props.StringProperty(
                                    name="output collection",
                                    description="This sets the collection to output to",
                                    default="sdf")
        
    red_color: bpy.props.FloatProperty(
                                name="red color",
                                description="red color for storkes",
                                default=1.0,
                                min=0.0,
                                max=1.0)
                                
    green_color: bpy.props.FloatProperty(
                                name="green color",
                                description="green color for storkes",
                                default=1.0,
                                min=0.0,
                                max=1.0)
                                
    blue_color: bpy.props.FloatProperty(
                                name="blue color",
                                description="blue color for storkes",
                                default=1.0,
                                min=0.0,
                                max=1.0)
                                
    alpha_color: bpy.props.FloatProperty(
                                name="alpha color",
                                description="alpha color for storkes",
                                default=1.0,
                                min=0.0,
                                max=1.0)
        
    frame_ons: bpy.props.IntProperty(
                            name="frame ons",
                            description="This setting controlls frame rate of the animation",
                            default=1,
                            min=1,
                            max=24)
      
    @classmethod
    def poll(cls, context):   
        if bpy.context.scene.start_frame >= bpy.context.scene.end_frame:
            return False
        
        try:
            bpy.data.collections[bpy.context.scene.output_collection]
        except:
            return False

        return True
    
    # SIMPLE JUST RUNS SOMETHING
    def execute(self, context):
        
        if self.poll(self):
            GP_outliner(MODE = self.MODE, turn_default_into_one_animatable_object = self.turn_default_into_one_animatable_object, add_subdivision = self.add_subdivision,
            lagg_effect_amount = self.lagg_effect_amount,fade_amount = self.fade_amount, subdivison_level = self.subdivison_level, stroke_thickness = self.stroke_thickness,
            stroke_opacity = self.stroke_opacity, start_frame = self.start_frame, end_frame = self.end_frame, output_collection = self.output_collection,
            R = self.red_color, B = self.blue_color, G = self.green_color, A = self.alpha_color,
            frame_ons = self.frame_ons)
        
            return {'FINISHED'}
        
        return {'CANCELED'}

def register():
    
    bpy.types.Scene.MODE = bpy.props.EnumProperty(items=[("DEFAULT","DEFAULT",""),("TRACE_1","TRACE_1",""),("TRACE_2","TRACE_2","")])
            
    bpy.types.Scene.turn_default_into_one_animatable_object = bpy.props.BoolProperty(
                                                    name="one animation",
                                                    description="This moves the animantion into one GP object so it can be animated",
                                                    default=False)
    
    bpy.types.Scene.add_subdivision = bpy.props.BoolProperty(
                                    name="add subdivision",
                                    description="This adds subdivion on the GP object(s) so that you can apply noise f.e",
                                    default=False)
    
    bpy.types.Scene.subdivison_level = bpy.props.IntProperty(
                                    name="subdivion amount",
                                    description="This setting adds the amount of subdivisions",
                                    default=1,
                                    min=1,
                                    max=5)
                                       
    bpy.types.Scene.lagg_effect_amount = bpy.props.IntProperty(
                                    name="after image",
                                    description="This setting adds an after image of the frames before the current one.",
                                    default=0,
                                    min=0,
                                    max=50)
    
    bpy.types.Scene.fade_amount = bpy.props.FloatProperty(
                                name="fade strokes",
                                description="This adds opasity to strokes",
                                default=1.0,
                                min=0.0,
                                max=1.0)
    
    bpy.types.Scene.stroke_thickness = bpy.props.IntProperty(
                                name="stroke thickness",
                                description="This adds the stroke thickness",
                                default=15,
                                min=1,
                                max=300)
                                
    bpy.types.Scene.stroke_opacity =  bpy.props.FloatProperty(
                                name="stroke opacity",
                                description="opacity storkes",
                                default=1.0,
                                min=0.0,
                                max=1.0)
                                
    bpy.types.Scene.start_frame = bpy.props.IntProperty(
                                name="start frame",
                                description="This sets the start frame to run on",
                                default=1,
                                min=0,
                                max=2000000000)
                                
    bpy.types.Scene.end_frame = bpy.props.IntProperty(
                            name="end frame",
                            description="This sets the end frame",
                            default=30,
                            min=1,
                            max=2000000001)
    
    bpy.types.Scene.output_collection = bpy.props.StringProperty(
                                    name="output collection",
                                    description="This sets the collection to output to",
                                    default="sdf")
        
    bpy.types.Scene.red_color = bpy.props.FloatProperty(
                                name="red color",
                                description="red color for storkes",
                                default=1.0,
                                min=0.0,
                                max=1.0)
                                
    bpy.types.Scene.green_color = bpy.props.FloatProperty(
                                name="green color",
                                description="green color for storkes",
                                default=1.0,
                                min=0.0,
                                max=1.0)
                                
    bpy.types.Scene.blue_color = bpy.props.FloatProperty(
                                name="blue color",
                                description="blue color for storkes",
                                default=1.0,
                                min=0.0,
                                max=1.0)
                                
    bpy.types.Scene.alpha_color = bpy.props.FloatProperty(
                                name="alpha color",
                                description="alpha color for storkes",
                                default=1.0,
                                min=0.0,
                                max=1.0)
        
    bpy.types.Scene.frame_ons = bpy.props.IntProperty(
                            name="frame ons",
                            description="This setting controlls frame rate of the animation",
                            default=1,
                            min=1,
                            max=24)
                            
    bpy.utils.register_class(VIEW3D_PT_GP_Outliner)
    bpy.utils.register_class(DATA_OT_GP_outliner)
    
def unregister():
    
    del bpy.types.Scene.MODE 
            
    del bpy.types.Scene.turn_default_into_one_animatable_object 
    
    del bpy.types.Scene.add_subdivision 
    
    del bpy.types.Scene.subdivison_level                   
                                       
    del bpy.types.Scene.lagg_effect_amount 
                                    
    del bpy.types.Scene.fade_amount 
                                
    del bpy.types.Scene.stroke_thickness 
                                
    del bpy.types.Scene.stroke_opacity
    
    del bpy.types.Scene.start_frame 
                                
    del bpy.types.Scene.end_frame 
    
    del bpy.types.Scene.output_collection 
        
    del bpy.types.Scene.red_color 
                                
    del bpy.types.Scene.green_color
                                
    del bpy.types.Scene.blue_color 
                                
    del bpy.types.Scene.alpha_color 
    
    del bpy.types.Scene.frame_ons 
                            
    bpy.utils.unregister_class(VIEW3D_PT_GP_Outliner)
    bpy.utils.unregister_class(DATA_OT_GP_outliner)
       
if __name__ == "__main__":
    register()
