import maya.cmds as cmds


sides = ['L','R']
loc_names = ['locs_base_neck','locs_base_neck_end','locs_base_head','locs_base_head_end','locs_base_jaw','locs_base_jaw_end']


def locator_pivot(*arguments):
    posX = posY = posZ = 0
    selection = cmds.ls(sl=True, fl=True)

    # Condition for if nothing is selected
    try:
        obj = cmds.ls(sl=True)[0]

    except IndexError:
        cmds.error("No object or vertices selected")

    # Stores all vertices in a list if a mesh is selected
    vert_selection = cmds.ls(obj + ".vtx[*]", fl=True)

    # Stores all vertices in a list if individual vertices are selected instead of a mesh
    for i in cmds.ls(sl=True, fl=True):
        if ".vtx" in i:
            vert_selection = selection
            break

    # Adds up all the 'X', 'Y', and 'Z' positions of all selected vertices
    for i in vert_selection:
        position = cmds.xform( i, q=True, translation=True, ws=True )
        posX+=position[0]
        posY+=position[1]
        posZ+=position[2]

    position[0] = posX/len(vert_selection)
    position[1] = posY/len(vert_selection)
    position[2] = posZ/len(vert_selection)

    # Creates a locator and moves it to the average position of all vertices selected
    for loc in arguments:
        cmds.move(position[0], position[1], position[2], cmds.spaceLocator(n=loc))

    # Show Axis for Joints
def show_axis_display(display=True):
    cmds.listRelatives(allDescendents=True, type='joint')
    cmds.select(hi=True,add=True)
    cmds.ls(sl=True,type='joint')
    if len(cmds.ls(sl=1, type="joint")) == 0: # if no joints are selected, do it for all the joints in the scene
        jointList = cmds.ls(type="joint")
    else:
        jointList = cmds.ls(sl=1, type="joint")
    for jnt in jointList:
        cmds.setAttr(jnt + ".displayLocalAxis", display) # set the displayLocalAxis attribute to what the user specifies.

    # Hide Axis for Joints
def hide_axis_display(display=False):
    cmds.listRelatives(allDescendents=True, type='joint')
    cmds.select(hi=True,add=True)
    cmds.ls(sl=True,type='joint')
    if len(cmds.ls(sl=1, type="joint")) == 0: # if no joints are selected, do it for all the joints in the scene
        jointList = cmds.ls(type="joint")
    else:
        jointList = cmds.ls(sl=1, type="joint")
    for jnt in jointList:
        cmds.setAttr(jnt + ".displayLocalAxis", display) # set the displayLocalAxis attribute to what the user specifies.
       
def eye_loc():
    try:
        l_eye = cmds.select('L_eye') # if "L_eye" and "R_eye" exist, if not user get a warning saying to change for the correct name convention
        r_eye = cmds.select('R_eye')
        sel = cmds.ls(sl=True,type='transform')
        sideMultiplyer = 1
        for side in sides:
            eye_center_loc = cmds.spaceLocator(n='locs_base_' + side + '_eye_center')#creating locator
            cmds.scale(1,1,1, eye_center_loc)#scaling the locators
            
            eye_position = cmds.xform(cmds.ls(side  + '_eye.rotatePivot'), q=True,t=True,ws=True) #using "cmds.xform" to have the position of eyes
            cmds.move(eye_position[0], eye_position[1], eye_position[2], eye_center_loc)#moving the locators to the eyes position
            
            #repeat the same process for all the "facial curves"
            eye_aim_loc = cmds.spaceLocator(n='locs_base_' + side + '_eye_aim')
            cmds.scale(1,1,1, eye_aim_loc)
            
            cmds.move(eye_position[0], eye_position[1], eye_position[2]+0.250, eye_aim_loc)
            upper_lid = cmds.curve(p=[(0,0,0), (0.05 * sideMultiplyer, 0.02, 0), (0.1 * sideMultiplyer,0.04,0), (0.15 * sideMultiplyer, 0.02,0), (0.2 * sideMultiplyer,0,0)],n= 'cv_' + 'L' + '_upper_eye_lid')
            cmds.scale(4,4,4, upper_lid)
            
            eye_aim_pos = cmds.xform(eye_aim_loc,q=True,t=True,ws=True)
            cmds.move(eye_aim_pos[0]-0.1,eye_aim_pos[1]+0.004,eye_aim_pos[2]+0.1,upper_lid)
            
            
            lower_lid = cmds.curve(p=[(0,0,0), (0.05 * sideMultiplyer, -0.02, 0), (0.1 * sideMultiplyer,-0.04,0), (0.15 * sideMultiplyer, -0.02,0), (0.2 * sideMultiplyer,0,0)],n= 'cv_' + 'L' + '_lower_eye_lid')
            cmds.scale(4,4,4, lower_lid)
            cmds.move(eye_aim_pos[0]-0.1,eye_aim_pos[1]-0.004,eye_aim_pos[2]+0.1,lower_lid)
            

            
        cmds.rename('cv_L_upper_eye_lid1','cv_R_upper_eye_lid')
        cmds.rename('cv_L_lower_eye_lid1','cv_R_lower_eye_lid')
        L_eyes_lid = cmds.ls('cv_L_*_eye_lid')    
        L_eye_lid_lower = cmds.xform(L_eyes_lid[0],q=True,t=True,ws=True) 
        L_eye_lid_upper = cmds.xform(L_eyes_lid[1],q=True,t=True,ws=True)  
        cmds.move(L_eye_lid_lower[0]-0.250,L_eye_lid_lower[1],L_eye_lid_lower[2],'cv_L_lower_eye_lid')
        cmds.move(L_eye_lid_upper[0]-0.250,L_eye_lid_upper[1],L_eye_lid_upper[2],'cv_L_upper_eye_lid')    
        R_eyes_lid = cmds.ls('cv_R_*_eye_lid')    
        R_eye_lid_lower = cmds.xform(R_eyes_lid[0],q=True,t=True,ws=True) 
        R_eye_lid_upper = cmds.xform(R_eyes_lid[1],q=True,t=True,ws=True)  
        cmds.move(R_eye_lid_lower[0]-0.370,R_eye_lid_lower[1],R_eye_lid_lower[2],'cv_R_lower_eye_lid')
        cmds.move(R_eye_lid_upper[0]-0.370,R_eye_lid_upper[1],R_eye_lid_upper[2],'cv_R_upper_eye_lid')
        cmds.makeIdentity(L_eyes_lid,apply=True, t=True,r=True,s=True,n=False,pn=True) 
        cmds.makeIdentity(R_eyes_lid,apply=True, t=True,r=True,s=True,n=False,pn=True)
        
       
            
    except:
        cmds.warning('change eyes names to: L_eye and R_eye')
         
def mouth_cv():
    sideMultiplyer = 1
    for side in sides:
        jaw_position = cmds.xform(cmds.ls('locs_base_jaw_end',type='transform'),q=True,t=True,ws=True)
        upper_mouth = cmds.curve(p=[(0,0,0), (0.04 *sideMultiplyer, -0.001,-0.001), (0.02*sideMultiplyer,-0.002,-0.002), (0.06*sideMultiplyer, -0.004,-0.003)],n='cv_' + side + '_upper_mouth')
        cmds.scale(15,15,15, upper_mouth)
        cmds.move(jaw_position[0], jaw_position[1]+1.1, jaw_position[2]+0.2, upper_mouth)
        cmds.makeIdentity(upper_mouth,apply=True, t=True,r=True,s=True,n=False,pn=True)
        lower_mouth = cmds.curve(p=[(0,0,0), (0.04 *sideMultiplyer, 0.001,-0.001), (0.02*sideMultiplyer,0.002,-0.002), (0.06*sideMultiplyer, 0.004,-0.003)],n='cv_' + side + '_lower_mouth')
        cmds.scale(15,15,15, lower_mouth)
        cmds.move(jaw_position[0], jaw_position[1]+0.8, jaw_position[2] + 0.2, lower_mouth)
        cmds.makeIdentity(lower_mouth,apply=True, t=True,r=True,s=True,n=False,pn=True)
        sideMultiplyer = -1

def smile_cv():
    sideMultiplyer = 1
    for side in sides:
        jaw_position = cmds.xform(cmds.ls('locs_base_jaw_end',type='transform'),q=True,t=True,ws=True)
        smile_muscle = cmds.curve(p=[(0,0,0), (0.15 *sideMultiplyer, -0.2,0), (0.2*sideMultiplyer,-0.4,0), (0.25*sideMultiplyer, -0.6,0)],n='cv_' + 'L' + '_smile_muscle')
        cmds.scale(2,2,2, smile_muscle)
        cmds.move(jaw_position[0]+0.4, jaw_position[1]+2.1, jaw_position[2]-0.008, smile_muscle)
        cmds.select('cv_L_smile_muscle*')
        cmds.makeIdentity(apply=True, t=True,r=True,s=True,n=False,pn=True)
    cmds.select('cv_L_smile_muscle1')
    cmds.duplicate(rr=True)
    cmds.scale(-1,1,1,r=True)
    cmds.move(0.8,0,0,r=True,os=True,wd=True)
    cmds.makeIdentity(apply=True, t=True,r=True,s=True,n=False,pn=True)
    cmds.rename('cv_L_smile_muscle2','cv_R_smile_muscle')
    cmds.delete('cv_L_smile_muscle1')
    cv_smile = cmds.xform(cmds.ls('cv_L_smile_muscle.cv[0]'),q=True,t=True,ws=True)
    loc_cheek = cmds.spaceLocator(n='loc_face_L_cheek')
    cmds.move(cv_smile[0]+ 0.2, cv_smile[1], cv_smile[2], loc_cheek)
    cmds.select('loc_face_L_cheek')
    cmds.duplicate(rr=True)
    cmds.move(-0.4,0,0,r=True,os=True,wd=True)
    cmds.rename('loc_face_L_cheek1','loc_face_R_cheek')
    cmds.parent('loc_face_L_cheek','cv_L_smile_muscle')
    cmds.parent('loc_face_R_cheek','cv_R_smile_muscle')

def eye_brow_loc():
    sideMultiplyer = 1
    for side in sides:
        eye_pos = cmds.xform(cmds.ls('locs_base_L_eye_aim'),q=True,t=True,ws=True)
        eye_brow = cmds.curve(p=[(0,0,0), (0.1 *sideMultiplyer, 0.1,0), (0.2*sideMultiplyer,0.15,0), (0.3*sideMultiplyer, 0.1,0)],n='cv_' + 'L' + '_eye_brow')
        cmds.scale(4,4,4, eye_brow)
        cmds.move(eye_pos[0]-0.40, eye_pos[1]+0.06, eye_pos[2]+0.80, eye_brow)
        cmds.select('cv_L_eye_brow*')
        cmds.makeIdentity(apply=True, t=True,r=True,s=True,n=False,pn=True)
    cmds.select('cv_L_eye_brow1')
    cmds.duplicate(rr=True)
    cmds.scale(-1,1,1,r=True)
    cmds.move(0.3,0,0,r=True,os=True,wd=True)
    cmds.makeIdentity(apply=True, t=True,r=True,s=True,n=False,pn=True)
    cmds.rename('cv_L_eye_brow2','cv_R_eye_brow')
    cmds.delete('cv_L_eye_brow1')
  

#Create clusters on each "cv" point of all curves
def clusters():
    cmds.parent('loc_face_L_cheek',w=True)
    cmds.parent('loc_face_R_cheek',w=True)
    cmds.select('cv_*')
    cmds.makeIdentity(apply=True, t=True,r=True,s=True,n=False,pn=True)
    grp_face_loc = cmds.group(em=True, n='face_loc')
    all_curves = cmds.ls('cv_*') # list of all cvs
    for cv in all_curves:
        curve_cv = cmds.ls(cv+'.cv[0:]',fl=True)
        for i, xcv in enumerate(curve_cv):
            tmp_name = str(xcv).split('cv_') #temporary cvs name
            loc_name = tmp_name[1].split('.cv')[0]#cv name without cv numbers "[0],[1],..."
            face_cluster = cmds.cluster(xcv,xcv,n='cluster_face_'+ loc_name + '_' + str(i))# create cluster on each cv selected
            
            if (xcv=='cv_R_upper_mouth.cv[0]'or xcv=='cv_R_lower_mouth.cv[0]'):
                pass
                
        #Here I create locator and I parent the clusters on them so I can move the clusters when I move the locators
        #So user can shape the cvs with diferent shapes.
            else:
                face_loc = cmds.spaceLocator(n='loc_face_'+ loc_name + '_' + str(i))
                cmds.scale(0.04,0.04,0.04,face_loc)
                cluster_pos = cmds.xform(xcv,q=True,t=True,ws=True)
                cmds.move(cluster_pos[0],cluster_pos[1],cluster_pos[2],face_loc)
                cmds.parent(face_loc,grp_face_loc)
            if (face_cluster[0] == 'cluster_face_R_upper_mouth_0'):
                cmds.parent(cmds.ls(face_cluster, type='transform')[0], 'loc_face_L_upper_mouth_0')
            elif(face_cluster[0] =='cluster_face_R_lower_mouth_0'):
                cmds.parent(cmds.ls(face_cluster, type='transform')[0],'loc_face_L_lower_mouth_0')
            else:
                cmds.parent(cmds.ls(face_cluster, type='transform')[0],'loc_face_'+ loc_name + '_' + str(i))

#Base joints (created by user as a guide to build the facial rigging skeleton)
def base_joints():
    all_head_locs = cmds.ls('locs_base_*',type='transform')
    for locs in all_head_locs:
        locs_pos = cmds.xform(locs,q=True,t=True,ws=True) #get locs postion 
        cmds.select(d=True)
        cmds.joint(radius=0.01,p=locs_pos,n='base'+str(locs+'_jnt').split('locs_base')[1])#create joints on loc position
    cmds.parent('base_neck_end_jnt','base_neck_jnt')
    cmds.parent('base_head_jnt','base_neck_end_jnt')
    cmds.parent('base_jaw_jnt','base_head_jnt')
    cmds.parent('base_jaw_end_jnt','base_jaw_jnt')
    cmds.parent('base_head_end_jnt','base_head_jnt')
    cmds.parent('base_L_eye_aim_jnt','base_L_eye_center_jnt')
    cmds.parent('base_L_eye_center_jnt','base_head_jnt')
    cmds.parent('base_R_eye_aim_jnt','base_R_eye_center_jnt')
    cmds.parent('base_R_eye_center_jnt','base_head_jnt')

    
#Parent all the joints from face to the "base_head_jnt"
def head_joints():
    all_head_locs = cmds.ls('loc_face_*',type='transform')
    for locs in all_head_locs:
        locs_pos = cmds.xform(locs,q=True,t=True,ws=True)
        cmds.select(d=True)
        cmds.joint(radius=0.01,p=locs_pos,n='face'+str(locs+'_jnt').split('loc_face')[1])
        
    all_left_eye_joints = cmds.ls('face_L_*_eye_lid_*')
    all_right_eye_joints = cmds.ls('face_R_*_eye_lid_*')
    all_smile_joints = cmds.ls('face_*_smile_muscle_*')
    all_brow_joints = cmds.ls('face_*_eye_brow_*')
    all_mouth_joints = cmds.ls('face_*_*_mouth_*')
    all_cheek_joints = cmds.ls('face_*_cheek_*')
    for lef_joints in all_left_eye_joints:
        cmds.select(d=True)
        center_loc_pos = cmds.xform(cmds.ls('locs_base_L_eye_center'),q=True,t=True,ws=True)
        rotate_joint = cmds.joint(radius = 0.01,p=center_loc_pos,n=(str(lef_joints) + '_rotate_joint'))
        
        cmds.parent(lef_joints,rotate_joint)
        cmds.parent(rotate_joint,'base_L_eye_center_jnt')
        
    for right_joints in all_right_eye_joints:
        cmds.select(d=True)
        center_loc_pos = cmds.xform(cmds.ls('locs_base_R_eye_center'),q=True,t=True,ws=True)
        rotate_joint = cmds.joint(radius = 0.01,p=center_loc_pos,n=(str(right_joints) + '_rotate_joint'))
        
        cmds.parent(right_joints,rotate_joint)
        cmds.parent(rotate_joint,'base_R_eye_center_jnt')
        
    for smile in all_smile_joints:
        cmds.select(d=True)
        cmds.parent(smile,'base_head_jnt')
        
    for brow in all_brow_joints:
        cmds.select(d=True)
        cmds.parent(brow,'base_head_jnt')
        
    for mouth in all_mouth_joints:
        cmds.select(d=True)
        cmds.parent(mouth,'base_head_jnt')
        
    for cheek in all_cheek_joints:
        cmds.select(d=True)
        cmds.parent(cheek,'base_head_jnt')
        
    cmds.rename('face_R_lower_eye_lid_4_jnt','face_R_lower_eye_lid_0_jnt1')
    cmds.rename('face_R_lower_eye_lid_0_jnt','face_R_lower_eye_lid_4_jnt')
    cmds.rename('face_R_lower_eye_lid_0_jnt1','face_R_lower_eye_lid_0_jnt')
    cmds.rename('face_R_lower_eye_lid_3_jnt','face_R_lower_eye_lid_1_jnt1')
    cmds.rename('face_R_lower_eye_lid_1_jnt','face_R_lower_eye_lid_3_jnt')
    cmds.rename('face_R_lower_eye_lid_1_jnt1','face_R_lower_eye_lid_1_jnt')
  
      
    cmds.rename('face_R_upper_eye_lid_4_jnt','face_R_upper_eye_lid_0_jnt1')
    cmds.rename('face_R_upper_eye_lid_0_jnt','face_R_upper_eye_lid_4_jnt')
    cmds.rename('face_R_upper_eye_lid_0_jnt1','face_R_upper_eye_lid_0_jnt')
    cmds.rename('face_R_upper_eye_lid_3_jnt','face_R_upper_eye_lid_1_jnt1')
    cmds.rename('face_R_upper_eye_lid_1_jnt','face_R_upper_eye_lid_3_jnt')
    cmds.rename('face_R_upper_eye_lid_1_jnt1','face_R_upper_eye_lid_1_jnt')




def eye_lid_ctrls():
    eye_curv = cmds.curve(n='test_ctrl_eye_lid',d=3,p=[(0.392,0.392,-0.000),
    (-0.000,0.554,-0.000),(-0.392,0.392,-0.000),(-0.554,0.000,-0.000),(-0.392,0,-0.000),
    (-0.000,0,-0.000),(0.392,0,-0.000),(0.554,-0.000,0.000),(0.392,0.392,-0.000),
    (-0.000,0.554,-0.000),(-0.392,0.392,-0.000)],k=[-0.25,-0.125,0.0,
    0.125,0.25,0.375,0.5,0.625,0.75,0.875,1.0,1.125,1.25])
    eye_pos = cmds.xform(cmds.ls('base_L_eye_center_jnt'), q=True,t=True,ws=True)
    cmds.move(eye_pos[0]+ 0.895, eye_pos[1]+ 0.41, eye_pos[2] + 3.519, eye_curv)
    cmds.makeIdentity(apply=True, t=True,r=True,s=True,n=False,pn=True)
    cmds.duplicate('test_ctrl_eye_lid')
    cmds.setAttr('test_ctrl_eye_lid1.rotateZ',-180)
    cmds.move(0,-0.817,0)
    cmds.makeIdentity(apply=True, t=True,r=True,s=True,n=False,pn=True)
    cmds.rename('test_ctrl_eye_lid','L_eye_upper_lid_ctrl')
    cmds.rename('test_ctrl_eye_lid1','L_eye_lower_lid_ctrl')
    cmds.parent('L_eye_upper_lid_ctrl','eyes_box_ctrl')
    cmds.parent('L_eye_lower_lid_ctrl','eyes_box_ctrl')
    cmds.select('face_ctrl_L_lower_eye_lid_1_jnt')
    cmds.group(n='SDK_face_ctrl_L_lower_eye_lid_1',em=False)
    cmds.select('face_ctrl_L_lower_eye_lid_2_jnt')
    cmds.group(n='SDK_face_ctrl_L_lower_eye_lid_2',em=False)
    cmds.select('face_ctrl_L_lower_eye_lid_3_jnt')
    cmds.group(n='SDK_face_ctrl_L_lower_eye_lid_3',em=False)
    lower_lid_sel = cmds.ls('SDK_face_ctrl_L_lower_eye_lid_*')

    for i in lower_lid_sel:
        cmds.setDrivenKeyframe(i+'.translateY',cd='L_eye_lower_lid_ctrl.translateY')
        
    cmds.move(0,0.422,0,'L_eye_lower_lid_ctrl')
    cmds.select(lower_lid_sel)
    cmds.move(0,0.3,0,lower_lid_sel)

    for i in lower_lid_sel:
        cmds.setDrivenKeyframe(i+'.translateY',cd='L_eye_lower_lid_ctrl.translateY')

    cmds.select('face_ctrl_L_upper_eye_lid_1_jnt')
    cmds.group(n='SDK_face_ctrl_L_upper_eye_lid_1',em=False)
    cmds.select('face_ctrl_L_upper_eye_lid_2_jnt')
    cmds.group(n='SDK_face_ctrl_L_upper_eye_lid_2',em=False)
    cmds.select('face_ctrl_L_upper_eye_lid_3_jnt')
    cmds.group(n='SDK_face_ctrl_L_upper_eye_lid_3',em=False)
    upper_lid_sel = cmds.ls('SDK_face_ctrl_L_upper_eye_lid_*')
    for i in upper_lid_sel:
        cmds.setDrivenKeyframe(i+'.translateY',cd='L_eye_upper_lid_ctrl.translateY')
        
    cmds.move(0,-0.382,0,'L_eye_upper_lid_ctrl')
    cmds.select(upper_lid_sel)
    cmds.move(0,-0.266,0,upper_lid_sel)
    for i in upper_lid_sel:
        cmds.setDrivenKeyframe(i+'.translateY',cd='L_eye_upper_lid_ctrl.translateY')
        

    cmds.setAttr('L_eye_lower_lid_ctrl.translateY',0)
    cmds.setAttr('L_eye_upper_lid_ctrl.translateY',0)
    cmds.select(cl=True)


            

    cmds.select('L_eye_lower_lid_ctrl')
    cmds.transformLimits(tx=(0, 0), ty=(0, 0.422), tz=(0, 0),etx = (1,1),ety = (1,1),etz = (1,1))
    cmds.transformLimits(rx=(0, 0), ry=(0, 0), rz=(0, 0),erx = (1,1),ery = (1,1),erz = (1,1))
    cmds.transformLimits(sx=(1, 1), sy=(1, 1), sz=(1, 1),esx = (1,1),esy = (1,1),esz = (1,1))

    cmds.select('L_eye_upper_lid_ctrl')
    cmds.transformLimits(tx=(0, 0), ty=(-0.382, 0), tz=(0, 0),etx = (1,1),ety = (1,1),etz = (1,1))
    cmds.transformLimits(rx=(0, 0), ry=(0, 0), rz=(0, 0),erx = (1,1),ery = (1,1),erz = (1,1))
    cmds.transformLimits(sx=(1, 1), sy=(1, 1), sz=(1, 1),esx = (1,1),esy = (1,1),esz = (1,1))






    eye_curv = cmds.curve(n='R_test_ctrl_eye_lid',d=3,p=[(0.392,0.392,-0.000),
    (-0.000,0.554,-0.000),(-0.392,0.392,-0.000),(-0.554,0.000,-0.000),(-0.392,0,-0.000),
    (-0.000,0,-0.000),(0.392,0,-0.000),(0.554,-0.000,0.000),(0.392,0.392,-0.000),
    (-0.000,0.554,-0.000),(-0.392,0.392,-0.000)],k=[-0.25,-0.125,0.0,
    0.125,0.25,0.375,0.5,0.625,0.75,0.875,1.0,1.125,1.25])
    eye_pos = cmds.xform(cmds.ls('base_R_eye_center_jnt'), q=True,t=True,ws=True)
    cmds.move(eye_pos[0]- 0.950, eye_pos[1]+ 0.41, eye_pos[2] + 3.519, eye_curv)
    cmds.makeIdentity(apply=True, t=True,r=True,s=True,n=False,pn=True)
    cmds.duplicate('R_test_ctrl_eye_lid')
    cmds.setAttr('R_test_ctrl_eye_lid1.rotateZ',-180)
    cmds.move(0,-0.817,0)
    cmds.makeIdentity(apply=True, t=True,r=True,s=True,n=False,pn=True)
    cmds.rename('R_test_ctrl_eye_lid','R_eye_upper_lid_ctrl')
    cmds.rename('R_test_ctrl_eye_lid1','R_eye_lower_lid_ctrl')
    cmds.parent('R_eye_upper_lid_ctrl','eyes_box_ctrl')
    cmds.parent('R_eye_lower_lid_ctrl','eyes_box_ctrl')
    cmds.select('face_ctrl_R_lower_eye_lid_1_jnt')
    cmds.group(n='SDK_face_ctrl_R_lower_eye_lid_1',em=False)
    cmds.select('face_ctrl_R_lower_eye_lid_2_jnt')
    cmds.group(n='SDK_face_ctrl_R_lower_eye_lid_2',em=False)
    cmds.select('face_ctrl_R_lower_eye_lid_3_jnt')
    cmds.group(n='SDK_face_ctrl_R_lower_eye_lid_3',em=False)
    R_lower_lid_sel = cmds.ls('SDK_face_ctrl_R_lower_eye_lid_*')

    for i in R_lower_lid_sel:
        cmds.setDrivenKeyframe(i+'.',cd='R_eye_lower_lid_ctrl.translateY')
        
    cmds.move(0,0.422,0,'R_eye_lower_lid_ctrl')
    cmds.select(R_lower_lid_sel)
    cmds.move(0,0.3,0,R_lower_lid_sel)

    for i in R_lower_lid_sel:
        cmds.setDrivenKeyframe(i+'.',cd='R_eye_lower_lid_ctrl.translateY')

    cmds.select('face_ctrl_R_upper_eye_lid_1_jnt')
    cmds.group(n='SDK_face_ctrl_R_upper_eye_lid_1',em=False)
    cmds.select('face_ctrl_R_upper_eye_lid_2_jnt')
    cmds.group(n='SDK_face_ctrl_R_upper_eye_lid_2',em=False)
    cmds.select('face_ctrl_R_upper_eye_lid_3_jnt')
    cmds.group(n='SDK_face_ctrl_R_upper_eye_lid_3',em=False)
    R_upper_lid_sel = cmds.ls('SDK_face_ctrl_R_upper_eye_lid_*')
        
    for i in R_upper_lid_sel:
        cmds.setDrivenKeyframe(i+'.',cd='R_eye_upper_lid_ctrl.translateY')
        
    cmds.move(0,-0.382,0,'R_eye_upper_lid_ctrl')
    cmds.select(R_upper_lid_sel)
    cmds.move(0,-0.266,0,R_upper_lid_sel)
    for i in R_upper_lid_sel:
        cmds.setDrivenKeyframe(i+'.',cd='R_eye_upper_lid_ctrl.translateY')
    cmds.setAttr('R_eye_lower_lid_ctrl.translateY',0)
    cmds.setAttr('R_eye_upper_lid_ctrl.translateY',0)


    cmds.select('R_eye_lower_lid_ctrl')
    cmds.transformLimits(tx=(0, 0), ty=(0, 0.422), tz=(0, 0),etx = (1,1),ety = (1,1),etz = (1,1))
    cmds.transformLimits(rx=(0, 0), ry=(0, 0), rz=(0, 0),erx = (1,1),ery = (1,1),erz = (1,1))
    cmds.transformLimits(sx=(1, 1), sy=(1, 1), sz=(1, 1),esx = (1,1),esy = (1,1),esz = (1,1))

    cmds.select('R_eye_upper_lid_ctrl')
    cmds.transformLimits(tx=(0, 0), ty=(-0.382, 0), tz=(0, 0),etx = (1,1),ety = (1,1),etz = (1,1))
    cmds.transformLimits(rx=(0, 0), ry=(0, 0), rz=(0, 0),erx = (1,1),ery = (1,1),erz = (1,1))
    cmds.transformLimits(sx=(1, 1), sy=(1, 1), sz=(1, 1),esx = (1,1),esy = (1,1),esz = (1,1))
    cmds.select(cl=True)

def controllers():
    l_eye_ctrl_pos = []
    r_eye_ctrl_pos = []
    all_joints = cmds.ls('face_*',type='joint') #list all "face joints"
    for joints in all_joints:
        ctrl = cmds.polyCylinder(r=0.06,h=0.01,ax=[0,0,1],n='face_ctrl_' + str(joints).split('face_')[1]) #creates a cylinder to use as controller 
        ctrl_grp = cmds.group(em=True,n='grp_face_offset_' + str(joints).split('face_')[1])
        face_joints_pos = cmds.xform(joints,q=True,t=True,ws=True)# get "face joints" position 
        cmds.move(face_joints_pos[0],face_joints_pos[1],face_joints_pos[2] + 0.001,ctrl)#move all the cylinder controllers to each "face joint" position
        cmds.move(face_joints_pos[0],face_joints_pos[1],face_joints_pos[2] + 0.001,ctrl_grp)
        cmds.parent(cmds.ls(ctrl, type='transform')[0],ctrl_grp)
        if 'eye_lid' in joints:
            if 'rotate_joint' in joints:
                pass
            else:
                if '_L_' in joints:
                    l_eye_ctrl_pos.append([(face_joints_pos[0]),(face_joints_pos[1]),(face_joints_pos[2])])
                else:
                    r_eye_ctrl_pos.append([(face_joints_pos[0]),(face_joints_pos[1]),(face_joints_pos[2])])
                cmds.pointConstraint(ctrl, str(joints))
    if (len(l_eye_ctrl_pos) > 0):
        L_eye_ctrl = cmds.curve(p=[(l_eye_ctrl_pos[0]),(l_eye_ctrl_pos[1]),(l_eye_ctrl_pos[2]),(l_eye_ctrl_pos[3]),(l_eye_ctrl_pos[4]),(l_eye_ctrl_pos[9]),(l_eye_ctrl_pos[8]),(l_eye_ctrl_pos[7]),(l_eye_ctrl_pos[6]),(l_eye_ctrl_pos[5]),(l_eye_ctrl_pos[0])],degree=1,n='face_ctrl_L_aim_cvs')
        cmds.xform(L_eye_ctrl,cp=True)
    if (len(r_eye_ctrl_pos) > 0):
        R_eye_ctrl = cmds.curve(p=[(r_eye_ctrl_pos[0]),(r_eye_ctrl_pos[1]),(r_eye_ctrl_pos[2]),(r_eye_ctrl_pos[3]),(r_eye_ctrl_pos[4]),(r_eye_ctrl_pos[9]),(r_eye_ctrl_pos[8]),(r_eye_ctrl_pos[7]),(r_eye_ctrl_pos[6]),(r_eye_ctrl_pos[5]),(r_eye_ctrl_pos[0])],degree=1,n='face_ctrl_R_aim_cvs')
        cmds.xform(R_eye_ctrl,cp=True)
        both_sides = ['L','R']
        for both in both_sides:
            #Upper mouth controllers
            
            upper_ctrl_pos1 = cmds.xform(cmds.ls('face_'+ both + '_upper_mouth_3_jnt'), q = True, t= True, ws=True)
            upper_ctrl_pos2 = cmds.xform(cmds.ls('face_'+ both + '_smile_muscle_3_jnt'), q = True, t= True, ws=True)
            upper_mouth_ctrl = cmds.polyCylinder(r=0.08,h=0.02,ax=[0,0,1],n='face_ctrl_'+ both + '_mouth_corner')
            upper_mouth_dis = [(upper_ctrl_pos2[0] - upper_ctrl_pos1[0]),(upper_ctrl_pos2[1] - upper_ctrl_pos1[1]),(upper_ctrl_pos2[2] - upper_ctrl_pos1[2])]
            cmds.move(upper_ctrl_pos1[0] + (upper_mouth_dis[0]/2), upper_ctrl_pos1[1] + (upper_mouth_dis[1]/2),upper_ctrl_pos1[2] + 0.003,upper_mouth_ctrl)
            upper_ctrl_grp = cmds.group(em=True,n='grp_face_ctrl_'+ both + '_mouth_corner')
            cmds.move(upper_ctrl_pos1[0] + (upper_mouth_dis[0]/2), upper_ctrl_pos1[1] + (upper_mouth_dis[1]/2),upper_ctrl_pos1[2] + 0.003,upper_ctrl_grp)
            cmds.parent(cmds.ls(upper_mouth_ctrl,type='transform')[0],upper_ctrl_grp)
            
            #Smile and cheek controllers
            cheek_ctrl_pos1 = cmds.xform(cmds.ls('face_'+ both + '_smile_muscle_1_jnt'), q = True, t= True, ws=True)
            cheek_ctrl_pos2 = cmds.xform(cmds.ls('face_'+ both + '_cheek_jnt'), q = True, t= True, ws=True)
            cheek_mouth_ctrl = cmds.polyCylinder(r=0.08,h=0.02,ax=[0,0,1],n='face_ctrl_'+ both + '_smile_cheek')
            cheek_smile_dis = [(cheek_ctrl_pos2[0] - cheek_ctrl_pos1[0]),(cheek_ctrl_pos2[1] - cheek_ctrl_pos1[1]),(cheek_ctrl_pos2[2] - cheek_ctrl_pos1[2])]
            cmds.move(cheek_ctrl_pos1[0] + (cheek_smile_dis[0]/2), cheek_ctrl_pos1[1] + (cheek_smile_dis[1]/2),cheek_ctrl_pos1[2],cheek_mouth_ctrl)
            cheek_ctrl_grp = cmds.group(em=True,n='grp_face_ctrl_'+ both + '_smile_cheek')
            cmds.move(cheek_ctrl_pos1[0] + (cheek_smile_dis[0]/2), cheek_ctrl_pos1[1] + (cheek_smile_dis[1]/2),cheek_ctrl_pos1[2],cheek_ctrl_grp)
            cmds.parent(cmds.ls(cheek_mouth_ctrl,type='transform')[0],cheek_ctrl_grp)
            
            #Eyebrow controllers
            eyebow_ctrl_pos1 = cmds.xform(cmds.ls('face_'+ both + '_eye_brow_0_jnt'), q = True, t= True, ws=True)
            eyebow_ctrl_pos2 = cmds.xform(cmds.ls('face_'+ both + '_eye_brow_1_jnt'), q = True, t= True, ws=True)
            eyebow_ctrl = cmds.polyCylinder(r=0.08,h=0.02,ax=[0,0,1],n='face_ctrl_'+ both + '_eyebrow1')
            eyebow_dis = [(eyebow_ctrl_pos2[0] - eyebow_ctrl_pos1[0]),(eyebow_ctrl_pos2[1] - eyebow_ctrl_pos1[1]),(eyebow_ctrl_pos2[2] - eyebow_ctrl_pos1[2])]
            cmds.move(eyebow_ctrl_pos1[0] + (eyebow_dis[0]/2), eyebow_ctrl_pos1[1] + (eyebow_dis[1]/2),eyebow_ctrl_pos1[2],eyebow_ctrl)
            eyebow_ctrl_grp = cmds.group(em=True,n='grp_face_ctrl_'+ both + '_eyebrow')
            cmds.move(eyebow_ctrl_pos1[0] + (eyebow_dis[0]/2), eyebow_ctrl_pos1[1] + (eyebow_dis[1]/2),eyebow_ctrl_pos1[2],eyebow_ctrl_grp)
            cmds.parent(cmds.ls(eyebow_ctrl,type='transform')[0],eyebow_ctrl_grp)
            
            eyebow_middle_ctrl_pos1 = cmds.xform(cmds.ls('face_'+ both + '_eye_brow_1_jnt'), q = True, t= True, ws=True)
            eyebow_middle_ctrl_pos2 = cmds.xform(cmds.ls('face_'+ both + '_eye_brow_2_jnt'), q = True, t= True, ws=True)
            eyebow_middle_ctrl = cmds.polyCylinder(r=0.08,h=0.02,ax=[0,0,1],n='face_ctrl_'+ both + '_eyebrow2')
            eyebow_middle_dis = [(eyebow_middle_ctrl_pos2[0] - eyebow_middle_ctrl_pos1[0]),(eyebow_middle_ctrl_pos2[1] - eyebow_middle_ctrl_pos1[1]),(eyebow_middle_ctrl_pos2[2] - eyebow_middle_ctrl_pos1[2])]
            cmds.move(eyebow_middle_ctrl_pos1[0] + (eyebow_middle_dis[0]/2), eyebow_middle_ctrl_pos1[1] + (eyebow_middle_dis[1]/2),eyebow_middle_ctrl_pos1[2],eyebow_middle_ctrl)
            cmds.parent(cmds.ls(eyebow_middle_ctrl,type='transform')[0],eyebow_ctrl_grp)

    #Create controllers for eyes
    face_ctrl_geo = cmds.ls('face_ctrl*',type='transform')
    cmds.makeIdentity(face_ctrl_geo,apply=True, t=True,r=True,s=True)
    for side in sides:
        eye_loc_position = cmds.xform(cmds.ls('base_'+ side +'_eye_center_jnt'), q=True,t=True,ws=True)
        eye_ctrl = cmds.circle(n='ctrl_base_' + side + '_eye',nr=(0, 0, 1), c=(0, 0, 0))
        cmds.scale(0.3,0.3,0.3, eye_ctrl)
        cmds.move(eye_loc_position[0], eye_loc_position[1], eye_loc_position[2]+ 3.52, eye_ctrl)
        cmds.makeIdentity(eye_ctrl,apply=True, t=True,r=True,s=True)
    eyes_box_curv = cmds.curve(n='eyes_box_ctrl',d=1, p=[(1,-1,1), (-1,-1,1), (-1,-1,-1), (1,-1,-1),(1,-1,1)])
    cmds.scale(0.96,0.48,0.48, eyes_box_curv)
    cmds.setAttr('eyes_box_ctrl.rotateX',90)
    cmds.CenterPivot(eyes_box_curv)
    cmds.move(eye_loc_position[0]+0.6, eye_loc_position[1], eye_loc_position[2]+ 4, eyes_box_curv)
    cmds.makeIdentity(eyes_box_curv,apply=True, t=True,r=True,s=True)
    cmds.select(eyes_box_curv)
    cmds.transformLimits(tx=(-1.82, 1.82), ty=(-2.02, 2.02), tz=(0, 0),etx = (1,1),ety = (1,1),etz = (1,1))
    cmds.transformLimits(rx=(0, 0), ry=(0, 0), rz=(0, 0),erx = (1,1),ery = (1,1),erz = (1,1))
    cmds.transformLimits(sx=(1, 1), sy=(1, 1), sz=(1, 1),esx = (1,1),esy = (1,1),esz = (1,1))
    #Here I create a main control for the facial rigging
    #With this control you can just mantain the main controllers of the face
    control_curv = cmds.curve(n='ctrl_facial_rig',d=3,p=[(0.392,0.392,-0.000),
    (-0.000,0.554,-0.000),(-0.392,0.392,-0.000),(-0.554,0.000,-0.000),(-0.392,0.228,-0.000),(-0.000,0.323,-0.000),
    (0.392,0.228,-0.000),(0.554,-0.000,0.000),(0.392,0.392,-0.000),(-0.000,0.554,-0.000),(-0.392,0.392,-0.000)],k=[-0.25,-0.125,0.0,
    0.125,0.25,0.375,0.5,0.625,0.75,0.875,1.0,1.125,1.25])
    cmds.scale(3,3,3, control_curv)
    cmds.addAttr(shortName='SC',longName='Show_Secondary',attributeType='enum',en='False:True',k=True) #here I crate the attributes
    head_loc_position = cmds.xform(cmds.ls('locs_base_head_end'), q=True,t=True,ws=True)
    cmds.move(head_loc_position[0], head_loc_position[1]+0.6, head_loc_position[2], control_curv)
    cmds.CenterPivot(control_curv)
    cmds.makeIdentity(control_curv,apply=True, t=True,r=True,s=True)


def uttilites():
    cmds.group(n='character_geo',em=True)
    #Rename Controllers
    eye_aim_L_m = cmds.ls('face_ctrl_L_upper_eye_lid_4_jnt_rotate_joint')
    for eye_aim_L in eye_aim_L_m:
        cmds.rename(eye_aim_L,'face_ctrl_L_eye_aim')

    eye_aim_grp_L = cmds.ls('grp_face_offset_L_upper_eye_lid_4_jnt_rotate_joint')
    for eye_aim_L_grp in eye_aim_grp_L:
        cmds.rename(eye_aim_L_grp,'grp_face_ctrl_L_eye_aim')

    eye_aim_R_m = cmds.ls('face_ctrl_R_upper_eye_lid_4_jnt_rotate_joint')
    for eye_aim_R in eye_aim_R_m:
        cmds.rename(eye_aim_R,'face_ctrl_R_eye_aim')

    eye_aim_grp_R = cmds.ls('grp_face_offset_R_upper_eye_lid_4_jnt_rotate_joint')
    for eye_aim_R_grp in eye_aim_grp_R:
        cmds.rename(eye_aim_R_grp,'grp_face_ctrl_R_eye_aim')
    grp_eyebrow_L = cmds.ls('grp_face_ctrl_L_eyebrow')
    for name_eye_L in grp_eyebrow_L:
        cmds.rename(name_eye_L,'grp_face_ctrl_L_eye_brow_1_'+ '+2')

    grp_eyebrow_R = cmds.ls('grp_face_ctrl_R_eyebrow')
    for name_eye_R in grp_eyebrow_R:
        cmds.rename(name_eye_R,'grp_face_ctrl_R_eye_brow_1_'+ '+2')
    grp_mouth_upper = cmds.ls('grp_face_offset_L_upper_mouth*')
    for names_up in grp_mouth_upper:
        cmds.rename(names_up,'grp_face_offset_L_upper_mouth_4'+ '+5')

    grp_mouth_lower = cmds.ls('grp_face_offset_L_lower_mouth*')
    for names_down in grp_mouth_lower:
        cmds.rename(names_down,'grp_face_offset_L_lower_mouth_1' + '+1') 
        
    grp_mouth_upper = cmds.ls('grp_face_offset_R_upper_mouth*')
    for names_up in grp_mouth_upper:
        cmds.rename(names_up,'grp_face_offset_R_upper_mouth_1' + '+4')

    grp_mouth_lower = cmds.ls('grp_face_offset_R_lower_mouth*')
    for names_down in grp_mouth_lower:
        cmds.rename(names_down,'grp_face_offset_R_lower_mouth_1' + '+1')    
        
    grp_mouth_upper = cmds.ls('grp_face_offset_L_smile_muscle*')
    for names_up in grp_mouth_upper:
        cmds.rename(names_up,'grp_face_offset_L_smile_muscle_1')

    grp_mouth_lower = cmds.ls('grp_face_offset_R_smile_muscle*')
    for names_down in grp_mouth_lower:
        cmds.rename(names_down,'grp_face_offset_R_smile_muscle_5') 
        
    grp_L = cmds.ls('grp_face_offset_L_eye_brow*')
    for L_grps in grp_L:
        cmds.rename(L_grps,'grp_face_offset_L_eye_brow_1_' + '1')

    grp_R = cmds.ls('grp_face_offset_R_eye_brow*')
    for R_grps in grp_R:
        cmds.rename(R_grps,'grp_face_offset_R_eye_brow_1_' + '1')
        
    #Eyes controller, the main "eye box" control the transaltion of each eye ball controller
    #when he moves the other two eyes controllers move with him
    all_ctrl_grp = cmds.ls('grp_face*')
    cmds.select(all_ctrl_grp)
    cmds.group(n='main_grp_face',em=True)
    cmds.parent(all_ctrl_grp,'main_grp_face')
    cmds.connectAttr('eyes_box_ctrl.translate','ctrl_base_L_eye.translate')
    cmds.connectAttr('eyes_box_ctrl.translate','ctrl_base_R_eye.translate')    
    
    for i,grp in enumerate(all_ctrl_grp):
        cmds.makeIdentity(grp,apply=True, t=True,r=True,s=True) #frezee all transformations
        mult_div = cmds.shadingNode('multiplyDivide',asUtility=True,n='face_node_' + str(i) )#the multiplyDivide node will have influence between the "muscle controllers", known as "main facial controllers", moving the "small facial controllers"
        unit_conv_01 = cmds.shadingNode('unitConversion',asUtility=True,n='face_node_unit_conversion_in_' + str(i) )#the unitConversion "in" goes before the multiplyDivide
        unit_conv_02 = cmds.shadingNode('unitConversion',asUtility=True,n='face_node_unit_conversion_out_' + str(i) )#the unitConversion "out" goes after the multiplyDivide and will be connected to the ".translate" input of the offset group of the "small facial controllers"
        cmds.setAttr(mult_div + '.operation',1)
        if 'eye_aim' in grp:
                cmds.setAttr(mult_div + '.input2X', 0.1) # here I set how much influence the multiplyDivide node will have on the "small facial controllers"
                cmds.setAttr(mult_div + '.input2Y', 0.1)
                cmds.setAttr(mult_div + '.input2Z', 0.1)   
                if '_L_' in grp:
                    cmds.connectAttr('ctrl_base_L_eye.translate', unit_conv_01 + '.input')
                else:
                    cmds.connectAttr('ctrl_base_R_eye.translate', unit_conv_01 + '.input')
                cmds.connectAttr(unit_conv_01 + '.output', mult_div + '.input1')
                cmds.connectAttr(mult_div + '.output', unit_conv_02 + '.input')
                cmds.connectAttr(unit_conv_02 + '.output', grp + '.translate')
                
                
        if 'eye_lid' in grp:
                cmds.setAttr(mult_div + '.input2X', 0.01)
                cmds.setAttr(mult_div + '.input2Y', 0.01)
                cmds.setAttr(mult_div + '.input2Z', 0.01)   
                if '_L_' in grp:
                    cmds.connectAttr('eyes_box_ctrl.translate', unit_conv_01 + '.input')
                else:
                    cmds.connectAttr('eyes_box_ctrl.translate', unit_conv_01 + '.input')
                cmds.connectAttr(unit_conv_01 + '.output', mult_div + '.input1')
                cmds.connectAttr(mult_div + '.output', unit_conv_02 + '.input')
                cmds.connectAttr(unit_conv_02 + '.output', grp + '.translate')
            
        if 'eye_brow' in grp:
            if '0' in grp:
                cmds.setAttr(mult_div + '.input2X', 0.8)
                cmds.setAttr(mult_div + '.input2Y', 0.8)
                cmds.setAttr(mult_div + '.input2Z', 0.8)
                        
                if '_L_' in grp:
                    cmds.connectAttr('face_ctrl_L_eyebrow1.translate', unit_conv_01 + '.input')
                else:
                    cmds.connectAttr('face_ctrl_R_eyebrow1.translate', unit_conv_01 + '.input')
                cmds.connectAttr(unit_conv_01 + '.output', mult_div + '.input1')
                cmds.connectAttr(mult_div + '.output', unit_conv_02 + '.input')
                cmds.connectAttr(unit_conv_02 + '.output', grp + '.translate')
                
            elif '1' in grp:
                cmds.setAttr(mult_div + '.input2X', 0.6)
                cmds.setAttr(mult_div + '.input2Y', 0.6)
                cmds.setAttr(mult_div + '.input2Z', 0.6)
                if '_L_' in grp:
                    cmds.connectAttr('face_ctrl_L_eyebrow1.translate', unit_conv_01 + '.input')
                else:
                    cmds.connectAttr('face_ctrl_R_eyebrow1.translate', unit_conv_01 + '.input')
                cmds.connectAttr(unit_conv_01 + '.output', mult_div + '.input1')
                cmds.connectAttr(mult_div + '.output', unit_conv_02 + '.input')
                cmds.connectAttr(unit_conv_02 + '.output', grp + '.translate')
                        
            elif '2' in grp:
                cmds.setAttr(mult_div + '.input2X', 0.3)
                cmds.setAttr(mult_div + '.input2Y', 0.3)
                cmds.setAttr(mult_div + '.input2Z', 0.3)
                if '_L_' in grp:
                    cmds.connectAttr('face_ctrl_L_eyebrow2.translate', unit_conv_01 + '.input')
                else:
                    cmds.connectAttr('face_ctrl_R_eyebrow2.translate', unit_conv_01 + '.input')
                cmds.connectAttr(unit_conv_01 + '.output', mult_div + '.input1')
                cmds.connectAttr(mult_div + '.output', unit_conv_02 + '.input')
                cmds.connectAttr(unit_conv_02 + '.output', grp + '.translate')
                
                     
                
        if 'cheek' in grp:
            if 'smile_cheek' in grp:
                if '_L_' in grp:
                        cmds.setAttr(mult_div + '.input2X', 0.15)
                        cmds.setAttr(mult_div + '.input2Y', 0.15)
                        cmds.setAttr(mult_div + '.input2Z', 0.15)
                        
                        cmds.connectAttr('face_ctrl_L_mouth_corner.translate', unit_conv_01 + '.input')
                        cmds.connectAttr(unit_conv_01 + '.output', mult_div + '.input1')
                        cmds.connectAttr(mult_div + '.output', unit_conv_02 + '.input')
                        cmds.connectAttr(unit_conv_02 + '.output', grp + '.translate')
                else:
                        cmds.setAttr(mult_div + '.input2X', 0.15)
                        cmds.setAttr(mult_div + '.input2Y', 0.15)
                        cmds.setAttr(mult_div + '.input2Z', 0.15)
                        
                        cmds.connectAttr('face_ctrl_R_mouth_corner.translate', unit_conv_01 + '.input')
                        cmds.connectAttr(unit_conv_01 + '.output', mult_div + '.input1')
                        cmds.connectAttr(mult_div + '.output', unit_conv_02 + '.input')
                        cmds.connectAttr(unit_conv_02 + '.output', grp + '.translate')
                        
            else:
                if '_L_' in grp:
                        cmds.setAttr(mult_div + '.input2X', 0.5)
                        cmds.setAttr(mult_div + '.input2Y', 0.5)
                        cmds.setAttr(mult_div + '.input2Z', 0.5)
                        
                        cmds.connectAttr('face_ctrl_L_smile_cheek.translate', unit_conv_01 + '.input')
                        cmds.connectAttr(unit_conv_01 + '.output', mult_div + '.input1')
                        cmds.connectAttr(mult_div + '.output', unit_conv_02 + '.input')
                        cmds.connectAttr(unit_conv_02 + '.output', grp + '.translate')
                else:
                        cmds.setAttr(mult_div + '.input2X', 0.5)
                        cmds.setAttr(mult_div + '.input2Y', 0.5)
                        cmds.setAttr(mult_div + '.input2Z', 0.5)
                        
                        cmds.connectAttr('face_ctrl_R_smile_cheek.translate', unit_conv_01 + '.input')
                        cmds.connectAttr(unit_conv_01 + '.output', mult_div + '.input1')
                        cmds.connectAttr(mult_div + '.output', unit_conv_02 + '.input')
                        cmds.connectAttr(unit_conv_02 + '.output', grp + '.translate')
                    
        if 'smile_muscle' in grp:
            if '_L_' in grp:
                if '0' in grp:
                        cmds.setAttr(mult_div + '.input2X', 0.15)
                        cmds.setAttr(mult_div + '.input2Y', 0.15)
                        cmds.setAttr(mult_div + '.input2Z', 0.15)
                        
                        cmds.connectAttr('face_ctrl_L_mouth_corner.translate', unit_conv_01 + '.input')
                        cmds.connectAttr(unit_conv_01 + '.output', mult_div + '.input1')
                        cmds.connectAttr(mult_div + '.output', unit_conv_02 + '.input')
                        cmds.connectAttr(unit_conv_02 + '.output', grp + '.translate')
                        
                elif '1' in grp:
                        cmds.setAttr(mult_div + '.input2X', 0.4)
                        cmds.setAttr(mult_div + '.input2Y', 0.4)
                        cmds.setAttr(mult_div + '.input2Z', 0.4)
                        
                        cmds.connectAttr('face_ctrl_L_mouth_corner.translate', unit_conv_01 + '.input')
                        cmds.connectAttr(unit_conv_01 + '.output', mult_div + '.input1')
                        cmds.connectAttr(mult_div + '.output', unit_conv_02 + '.input')
                        cmds.connectAttr(unit_conv_02 + '.output', grp + '.translate')
                        
                elif '2' in grp:
                        cmds.setAttr(mult_div + '.input2X', 0.4)
                        cmds.setAttr(mult_div + '.input2Y', 0.4)
                        cmds.setAttr(mult_div + '.input2Z', 0.4)
                        
                        cmds.connectAttr('face_ctrl_L_mouth_corner.translate', unit_conv_01 + '.input')
                        cmds.connectAttr(unit_conv_01 + '.output', mult_div + '.input1')
                        cmds.connectAttr(mult_div + '.output', unit_conv_02 + '.input')
                        cmds.connectAttr(unit_conv_02 + '.output', grp + '.translate')
                        
                else:

                        cmds.setAttr(mult_div + '.input2X', 0.35)
                        cmds.setAttr(mult_div + '.input2Y', 0.35)
                        cmds.setAttr(mult_div + '.input2Z', 0.35)
                        
                        cmds.connectAttr('face_ctrl_L_mouth_corner.translate', unit_conv_01 + '.input')
                        cmds.connectAttr(unit_conv_01 + '.output', mult_div + '.input1')
                        cmds.connectAttr(mult_div + '.output', unit_conv_02 + '.input')
                        cmds.connectAttr(unit_conv_02 + '.output', grp + '.translate')
                        
            if '_R_' in grp:
                if '0' in grp:
                        cmds.setAttr(mult_div + '.input2X', 0.15)
                        cmds.setAttr(mult_div + '.input2Y', 0.15)
                        cmds.setAttr(mult_div + '.input2Z', 0.15)
                        
                        cmds.connectAttr('face_ctrl_R_mouth_corner.translate', unit_conv_01 + '.input')
                        cmds.connectAttr(unit_conv_01 + '.output', mult_div + '.input1')
                        cmds.connectAttr(mult_div + '.output', unit_conv_02 + '.input')
                        cmds.connectAttr(unit_conv_02 + '.output', grp + '.translate')
                        
                elif '1' in grp:
                        cmds.setAttr(mult_div + '.input2X', 0.4)
                        cmds.setAttr(mult_div + '.input2Y', 0.4)
                        cmds.setAttr(mult_div + '.input2Z', 0.4)
                        
                        cmds.connectAttr('face_ctrl_R_mouth_corner.translate', unit_conv_01 + '.input')
                        cmds.connectAttr(unit_conv_01 + '.output', mult_div + '.input1')
                        cmds.connectAttr(mult_div + '.output', unit_conv_02 + '.input')
                        cmds.connectAttr(unit_conv_02 + '.output', grp + '.translate')
                        
                elif '2' in grp:
                        cmds.setAttr(mult_div + '.input2X', 0.4)
                        cmds.setAttr(mult_div + '.input2Y', 0.4)
                        cmds.setAttr(mult_div + '.input2Z', 0.4)
                        
                        cmds.connectAttr('face_ctrl_R_mouth_corner.translate', unit_conv_01 + '.input')
                        cmds.connectAttr(unit_conv_01 + '.output', mult_div + '.input1')
                        cmds.connectAttr(mult_div + '.output', unit_conv_02 + '.input')
                        cmds.connectAttr(unit_conv_02 + '.output', grp + '.translate')
                        
                else:
                        cmds.setAttr(mult_div + '.input2X', 0.35)
                        cmds.setAttr(mult_div + '.input2Y', 0.35)
                        cmds.setAttr(mult_div + '.input2Z', 0.35)
                        
                        cmds.connectAttr('face_ctrl_R_mouth_corner.translate', unit_conv_01 + '.input')
                        cmds.connectAttr(unit_conv_01 + '.output', mult_div + '.input1')
                        cmds.connectAttr(mult_div + '.output', unit_conv_02 + '.input')
                        cmds.connectAttr(unit_conv_02 + '.output', grp + '.translate')
                    
                
        if 'mouth' in grp:
            if 'mouth_corner' in grp:
                pass
            else:
                grp_value = str(all_ctrl_grp[i]).split('mouth_')
                print (grp_value)
                cmds.setAttr(mult_div + '.input2X', float(grp_value[1]) *0.02)
                cmds.setAttr(mult_div + '.input2Y', float(grp_value[1]) *0.02)
                cmds.setAttr(mult_div + '.input2Z', float(grp_value[1]) *0.02)
                if '_R_' in grp:
                    cmds.setAttr(mult_div + '.input2X', float(grp_value[1]) *0.07)
                    cmds.setAttr(mult_div + '.input2Y', float(grp_value[1]) *0.07)
                    cmds.setAttr(mult_div + '.input2Z', float(grp_value[1]) *0.07)
                    cmds.connectAttr('face_ctrl_R_mouth_corner.translate', unit_conv_01 + '.input')
                    cmds.connectAttr(unit_conv_01 + '.output', mult_div + '.input1')
                    cmds.connectAttr(mult_div + '.output', unit_conv_02 + '.input')
                    cmds.connectAttr(unit_conv_02 + '.output', grp + '.translate')
                    
                else:
                    cmds.connectAttr('face_ctrl_L_mouth_corner.translate', unit_conv_01 + '.input')
                    cmds.connectAttr(unit_conv_01 + '.output', mult_div + '.input1')
                    cmds.connectAttr(mult_div + '.output', unit_conv_02 + '.input')
                    cmds.connectAttr(unit_conv_02 + '.output', grp + '.translate')  

                    
        
    all_ctrls = cmds.ls('face_ctrl_*',type='transform')       
    ctrl_grps = []

    for ctrls in all_ctrls:
        if '_rotate_joint' in ctrls:
            pass
        elif 'eye_lid' in ctrls:
            pass
        elif 'mouth_corner' in ctrls:
            pass
        elif 'smile_cheek' in ctrls:
            pass
        elif 'eyebrow' in ctrls:
            pass
        elif 'eye_aim' in ctrls:
            pass
        else:
            cmds.connectAttr('ctrl_facial_rig.Show_Secondary', ctrls + '.visibility')
            ctrl_grps.append(ctrls)
        
    #Here I parentConstraint some facial controllers
    parentList = []
    constrainedList = []
    ctrls_sel = cmds.ls('face_ctrl_L_upper_mouth_*',type='transform')

    for ctrls in ctrls_sel :
        parentList.append(ctrls)


    joint_sel = cmds.ls('face_L_upper_mouth_*_jnt',type='joint') 

    for joints in joint_sel :
        constrainedList.append(joints)

    for parentJoints, constrainedJoints in zip(parentList, constrainedList):
        cmds.parentConstraint ( parentJoints , constrainedJoints, mo=True)


    ctrls_sel = cmds.ls('face_ctrl_R_upper_mouth_*',type='transform')

    for ctrls in ctrls_sel :
        parentList.append(ctrls)


    joint_sel = cmds.ls('face_R_upper_mouth_*_jnt',type='joint') 
    for joints in joint_sel :
        constrainedList.append(joints)
        
        
        
        
    ctrls_sel = cmds.ls('face_ctrl_L_lower_mouth_*',type='transform')

    for ctrls in ctrls_sel :
        parentList.append(ctrls)


    joint_sel = cmds.ls('face_L_lower_mouth_*_jnt',type='joint') 

    for joints in joint_sel :
        constrainedList.append(joints)

    for parentJoints, constrainedJoints in zip(parentList, constrainedList):
        cmds.parentConstraint ( parentJoints , constrainedJoints, mo=True)
        


    ctrls_sel = cmds.ls('face_ctrl_R_lower_mouth_*',type='transform')

    for ctrls in ctrls_sel :
        parentList.append(ctrls)


    joint_sel = cmds.ls('face_R_lower_mouth_*_jnt',type='joint') 
    for joints in joint_sel :
        constrainedList.append(joints)

    for parentJoints, constrainedJoints in zip(parentList, constrainedList):
        cmds.parentConstraint ( parentJoints , constrainedJoints, mo=True)




    ctrls_sel = cmds.ls('face_ctrl_L_smile_muscle_*_jnt',type='transform')

    for ctrls in ctrls_sel :
        parentList.append(ctrls)


    joint_sel = cmds.ls('face_L_smile_muscle_*_jnt',type='joint') 
    for joints in joint_sel :
        constrainedList.append(joints)

    for parentJoints, constrainedJoints in zip(parentList, constrainedList):
        cmds.parentConstraint ( parentJoints , constrainedJoints, mo=True)


    ctrls_sel = cmds.ls('face_ctrl_R_smile_muscle_*_jnt',type='transform')

    for ctrls in ctrls_sel :
        parentList.append(ctrls)


    joint_sel = cmds.ls('face_R_smile_muscle_*_jnt',type='joint') 
    for joints in joint_sel :
        constrainedList.append(joints)

    for parentJoints, constrainedJoints in zip(parentList, constrainedList):
        cmds.parentConstraint ( parentJoints , constrainedJoints, mo=True)


    ctrls_sel = cmds.ls('face_ctrl_L_eye_brow_*_jnt',type='transform')

    for ctrls in ctrls_sel :
        parentList.append(ctrls)


    joint_sel = cmds.ls('face_L_eye_brow_*_jnt',type='joint') 
    for joints in joint_sel :
        constrainedList.append(joints)

    for parentJoints, constrainedJoints in zip(parentList, constrainedList):
        cmds.parentConstraint ( parentJoints , constrainedJoints, mo=True)


    ctrls_sel = cmds.ls('face_ctrl_R_eye_brow_*_jnt',type='transform')

    for ctrls in ctrls_sel :
        parentList.append(ctrls)


    joint_sel = cmds.ls('face_R_eye_brow_*_jnt',type='joint') 
    for joints in joint_sel :
        constrainedList.append(joints)

    for parentJoints, constrainedJoints in zip(parentList, constrainedList):
        cmds.parentConstraint ( parentJoints , constrainedJoints, mo=True)


    cmds.parent('grp_face_offset_R_eye_brow_1_4','grp_face_offset_R_eye_brow_1_3')

    cmds.parent('grp_face_offset_R_eye_brow_1_3','face_ctrl_R_eyebrow2')

    cmds.parent('grp_face_offset_L_eye_brow_1_4','grp_face_offset_L_eye_brow_1_3')

    cmds.parent('grp_face_offset_L_eye_brow_1_3','face_ctrl_L_eyebrow2')

    #Create the neck control
    neck_ctrl = cmds.circle(n='ctrl_neck',nr=(0, 0, 1), c=(0, 0, 0))
    cmds.group(n='grp_ctrl_base_neck_offset',em=True)
    cmds.group(n='grp_ctrl_base_neck_SDK',em=True)
    cmds.parent('grp_ctrl_base_neck_SDK','grp_ctrl_base_neck_offset')
    cmds.parent('ctrl_neck','grp_ctrl_base_neck_SDK')
    cmds.parentConstraint ( 'base_neck_end_jnt' , 'grp_ctrl_base_neck_offset', mo=False)


    cmds.scale(2,2,2, 'ctrl_neck')
    cmds.rotate(-46.61, 0, 0, 'ctrl_neck')
    cmds.makeIdentity('ctrl_neck',apply=True, t=True,r=True,s=True)
    cmds.delete('grp_ctrl_base_neck_offset_parentConstraint1')
    cmds.parentConstraint ('ctrl_neck' , 'base_neck_end_jnt', mo=True)
    cmds.rename('main_grp_face','grp_face_offset')
    cmds.parent('grp_face_offset','ctrl_neck')

    #create the jaw control
    jaw_ctrl = cmds.circle(n='ctrl_base_jaw',nr=(0, 0, 1), c=(0, 0, 0))
            


    cmds.group(n='grp_ctrl_base_jaw_offset',em=True)
    cmds.group(n='grp_ctrl_base_jaw_SDK',em=True)
    cmds.parent('grp_ctrl_base_jaw_SDK','grp_ctrl_base_jaw_offset')
    cmds.parent('ctrl_base_jaw','grp_ctrl_base_jaw_SDK')
    cmds.parentConstraint ( 'base_jaw_jnt' , 'grp_ctrl_base_jaw_offset', mo=False)


    cmds.scale(1.5,3,0, 'ctrl_base_jaw')
    cmds.rotate(-59.514916, 0, 0, 'ctrl_base_jaw')
    cmds.makeIdentity('ctrl_base_jaw',apply=True, t=True,r=True,s=True)
    cmds.delete('grp_ctrl_base_jaw_offset_parentConstraint1')
    cmds.parentConstraint ('ctrl_base_jaw' , 'base_jaw_jnt', mo=True)
    
    
    L_grp_lower_mouth = cmds.ls('grp_face_offset_L_lower_mouth_*_*')
    R_grp_lower_mouth = cmds.ls('grp_face_offset_R_lower_mouth_*_*')
    lower_mouth = L_grp_lower_mouth + R_grp_lower_mouth
    cmds.group(n='grp_lower_mouth_offset',em=True)
    cmds.parent(lower_mouth,'grp_lower_mouth_offset')
    cmds.parent('grp_lower_mouth_offset','ctrl_base_jaw')
    cmds.parent('grp_ctrl_base_jaw_offset','ctrl_neck')
    cmds.setAttr('ctrl_facial_rig.Show_Secondary',1)
    locs_selc = cmds.ls('locs_*',type='transform')
    loc_selc = cmds.ls('loc_*',type='transform')
    cvs_selc = cmds.ls('cv_*',type='transform')
    face_cvs_selc = cmds.ls('face_ctrl_*_aim_cvs',type='transform')
    cmds.delete(face_cvs_selc)
    cmds.delete(locs_selc)
    cmds.delete(loc_selc)
    cmds.delete(cvs_selc)
    cmds.delete('character_geo1')
    


    eyes_selc = cmds.ls('ctrl_base_*_eye',type='transform')
    eyes_box_selc = cmds.ls('eyes_box_ctrl',type='transform')
    ctrl_facial_selc = cmds.ls('ctrl_facial_rig',type='transform')
    extra_ctrl_sel = eyes_selc + eyes_box_selc + ctrl_facial_selc
    cmds.group(n='grp_extra_ctrls',em=True)
    cmds.parent(extra_ctrl_sel,'grp_extra_ctrls')
    cmds.parent('grp_extra_ctrls','ctrl_neck')
    cmds.delete('face_loc')

    cmds.parentConstraint('face_ctrl_L_cheek_jnt','face_L_cheek_jnt',mo=True)

    cmds.parentConstraint('face_ctrl_R_cheek_jnt','face_R_cheek_jnt',mo=True)
    
    cmds.select('face_ctrl_L_eye_aim')
    cmds.move(0,0,0.439,r=True,os=True,wd=True)
    cmds.makeIdentity(apply=True, t=True,r=True,s=True,n=False,pn=True)
    cmds.select('face_ctrl_R_eye_aim')
    cmds.move(0,0,0.439,r=True,os=True,wd=True)
    cmds.makeIdentity(apply=True, t=True,r=True,s=True,n=False,pn=True)
    
    cmds.aimConstraint('face_ctrl_L_eye_aim', 'base_L_eye_center_jnt', weight=1, mo=True, aimVector=(0, 0, 1), upVector=(0, 1, 0), worldUpType="vector", worldUpVector=(0, 1, 0))
    cmds.aimConstraint('face_ctrl_R_eye_aim', 'base_R_eye_center_jnt', weight=1, mo=True, aimVector=(0, 0, 1), upVector=(0, 1, 0), worldUpType="vector", worldUpVector=(0, 1, 0))

    
    #Group joints/controllers and meshe
    cmds.group(n='grp_ctrls',em=True)
    cmds.group(n='grp_joints',em=True)
    cmds.group(n='grp_geo',em=True)
    cmds.group(n='grp_christopher',em=True)
    cmds.parent('base_neck_jnt','grp_joints')
    cmds.parent('grp_ctrl_base_neck_offset','grp_ctrls')
    cmds.parent('character_geo','grp_geo')
    cmds.parent('grp_joints','grp_christopher')
    cmds.parent('grp_ctrls','grp_christopher')
    cmds.parent('grp_geo','grp_christopher')
    cmds.select(cl=True)
    
def adjust_R_mouth():
    cmds.setAttr('face_node_216.input2X', 0.26)
    cmds.setAttr('face_node_216.input2Y', 0.26)
    cmds.setAttr('face_node_216.input2Z', 0.26)   
    cmds.setAttr('face_node_215.input2X', 0.24)
    cmds.setAttr('face_node_215.input2Y', 0.24)
    cmds.setAttr('face_node_215.input2Z', 0.24)  
    cmds.setAttr('face_node_217.input2X', 0.28)
    cmds.setAttr('face_node_217.input2Y', 0.28)
    cmds.setAttr('face_node_217.input2Z', 0.28) 

    # Function that will open the bind skin options of maya, so user can have all the options
def fun_bin_skin():
    joint_sel = cmds.ls(sl=True, type='joint')
    sel = cmds.ls(sl=True,type='transform')
    if (len(sel) == 0):
        cmds.confirmDialog(title = "Empty Selection", message= "You have to select a mesh", button = ['OK'])
    
    if (len(joint_sel) == 0):
       cmds.confirmDialog(title = "Empty Selection", message= "You have to select a joint", button = ['OK']) 
        
    else:
        cmds.SmoothBindSkinOptions()
            
    # Function to unbind all(select all the skinClusters on scene)
def fun_unbind_skin():
    sel_mesh = cmds.ls(sl=True,type='transform')[0]
    if (len(sel_mesh) == 0):
        cmds.confirmDialog(title = "Empty Selection", message= "You have to select a mesh", button = ['OK'])
        
    else:
        skin_cluster  = cmds.select('skinCluster*')
        list_skin = cmds.ls(sl=True,type='skinCluster')
        for each in list_skin:
            cmds.skinCluster(each,e=True,ub = True)

def delete_clusters():
    face_loc_cluster_grp = cmds.ls('face_loc',type='transform')
    cmds.delete(face_loc_cluster_grp)
    cmds.parent('loc_face_L_cheek','cv_L_smile_muscle')
    cmds.parent('loc_face_R_cheek','cv_R_smile_muscle')


def R_mouth_c():
    cmds.setAttr('face_node_216.input2X',0.26)
    cmds.setAttr('face_node_216.input2Y',0.26)
    cmds.setAttr('face_node_216.input2Z',0.26)
    cmds.setAttr('face_node_215.input2X',0.24)
    cmds.setAttr('face_node_215.input2Y',0.24)
    cmds.setAttr('face_node_215.input2Z',0.24)
    cmds.setAttr('face_node_217.input2X',0.28)
    cmds.setAttr('face_node_217.input2Y',0.28)
    cmds.setAttr('face_node_217.input2Z',0.28)


def create_ctrls():
    base_joints()
    head_joints()
    controllers()
    uttilites()
    eye_lid_ctrls()
    R_mouth_c()

def create_cvs():
    eye_loc()
    mouth_cv()
    smile_cv()
    eye_brow_loc()
    



def create_clusters():
    clusters()

### Window UI ###
def window_maker():
    pass
    
win_name = 'Auto_Facial_Rig'
if cmds.window(win_name, query=True, exists=True):
    cmds.deleteUI(win_name)
   
cmds.window(win_name, sizeable=False, height=250, width=260, backgroundColor=(0.1,0.1,0.1))


# Create the tabLayout
tabControls = cmds.tabLayout()

# Arm tab
tab1Layout = cmds.columnLayout()
    # Button for Locators
msg_002 = cmds.text('Mesh must face Z axis!')
msg_002_cont = cmds.text('Locators goes to the avarage vertex selection')
cmds.separator(height=10)
cmds.rowLayout (cw3 = (50, 280, 40), nc = 5)
neck_loc = cmds.button(label='Neck', w=80, h=20,enable=True, command='locator_pivot(loc_names[0])', backgroundColor=(0.3,0.3,0.3))
cmds.separator(w=20,height=1)
head_loc = cmds.button(label='Neck End', w=80, h=20,enable=True, command='locator_pivot(loc_names[1])', backgroundColor=(0.3,0.3,0.3))
cmds.separator(w=20,height=1)
jaw_loc = cmds.button(label='Head', w=80, h=20,enable=True, command='locator_pivot(loc_names[2])', backgroundColor=(0.3,0.3,0.3))
cmds.setParent( '..' )  
cmds.rowLayout (cw3 = (50, 280, 40), nc = 6)
cmds.separator(height=50)
jaw_loc = cmds.button(label='Head End', w=80, h=20,enable=True, command='locator_pivot(loc_names[3])', backgroundColor=(0.3,0.3,0.3))
cmds.separator(w=20,height=1)
jaw_loc = cmds.button(label='Jaw', w=80, h=20,enable=True, command='locator_pivot(loc_names[4])', backgroundColor=(0.3,0.3,0.3))
cmds.separator(w=20,height=1)
jaw_loc = cmds.button(label='Jaw End', w=80, h=20,enable=True, command='locator_pivot(loc_names[5])', backgroundColor=(0.3,0.3,0.3))
cmds.setParent( '..' )  

    # Button to create clusters/face joints and controllers
cmds.separator(height=10)
msg_005 = cmds.text('Place the curves where they belong and scale as much as you need!') 
cmds.separator(height=10)
msg_005_cont = cmds.text('After the curves you can create clusters and arrange then to the face')
cmds.separator(height=10)
msg_005_cont = cmds.text('Then you can create the controllers.')
cmds.separator(height=10)
cmds.rowLayout (cw3 = (50, 280, 40), nc = 5)
make_joint_btn = cmds.button(l='Create Curves', w=90, h=20,enable=True,c='create_cvs()', backgroundColor=(0.3,0.3,0.3))
cmds.separator(w=10,height=1)
create_controllers = cmds.button(label='Create Clusters', w=110, h=20,enable=True, command='create_clusters()', backgroundColor=(0.3,0.3,0.3))
cmds.separator(w=10,height=1)
create_controllers = cmds.button(label='Create Controllers', w=110, h=20,enable=True, command='create_ctrls()', backgroundColor=(0.3,0.3,0.3))
cmds.setParent( '..' )  
cmds.separator(height=20)
msg_005 = cmds.text('If you need you can undo clusters before you create the controllers') 
cmds.rowLayout (cw3 = (50, 280, 40), nc = 6)
cmds.separator(height=50)
create_controllers = cmds.button(label='Undo Clusters', w=110, h=20,enable=True, command='delete_clusters()', backgroundColor=(0.3,0.3,0.3))
cmds.setParent( '..' )

    # Button to bind or unbind skin
cmds.separator(height=10)
msg_006 = cmds.text('Skinning')
cmds.rowLayout (cw3 = (50, 280, 40), nc = 5)
bind_skin = cmds.button(l='Bind Skin', w=70, h=20,enable=True,c='fun_bin_skin()', backgroundColor=(0.3,0.3,0.3))
cmds.separator(w=10,height=1)
unbind_skin = cmds.button(l='Unbind Skin', w=70, h=20,enable=True,c='fun_unbind_skin()', backgroundColor=(0.3,0.3,0.3))
cmds.setParent( '..' )

cmds.separator(height=10)
cmds.iconTextButton("lblCopyright1", l="All Rights Reserved.", w=370, h=20, style="textOnly", c="cmds.showHelp(\"http://www.arthurmeirelles.com\", a=1)",backgroundColor=(0.3,0.3,0.3))
cmds.setParent('..')


# Create appropriate labels for the tabs
cmds.tabLayout(tabControls, edit=True, tabLabel=(
(tab1Layout, "FACIAL OPTIONS")))


cmds.showWindow('Auto_Facial_Rig')