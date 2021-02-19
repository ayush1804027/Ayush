--[[
*****************************************************************************************
*
*        		===============================================
*           		Nirikshak Bot (NB) Theme (eYRC 2020-21)
*        		===============================================
*
*  This Lua script is to implement Task 2B of Nirikshak Bot (NB) Theme (eYRC 2020-21).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*  
*  e-Yantra - An MHRD project under National Mission on Education using ICT (NMEICT)
*
*****************************************************************************************
]]--


--[[
# Team ID:			[ NB_1209 ]
# Author List:		[ Pushkar Prashant , Ayush Kumar ]
# Filename:			task_2b
# Functions:        createWall, saveTexture, retrieveTexture, reapplyTexture, receiveData, generateHorizontalWalls, 
#                   generateVerticalWalls, deleteWalls, createMaze, sysCall_init, sysCall_beforeSimulation
#                   sysCall_afterSimulation, sysCall_cleanup
# 					[ Comma separated list of functions in this file ]
# Global variables:	
# 					[ List of global variables defined in this file ]
]]--

--[[
##################### GLOBAL VARIABLES #######################
## You can add global variables in this section according   ##
## to your requirement.                                     ##
## DO NOT TAMPER WITH THE ALREADY DEFINED GLOBAL VARIABLES. ##
##############################################################
]]--

maze_array = {}
baseHandle = -1       --Do not change or delete this variable
textureID = -1        --Do not change or delete this variable
textureData = -1       --Do not change or delete this variable
--############################################################

--[[
##################### HELPER FUNCTIONS #######################
## You can add helper functions in this section according   ##
## to your requirement.                                     ##
## DO NOT MODIFY OR CHANGE THE ALREADY DEFINED HELPER       ##
## FUNCTIONS                                                ##
##############################################################
]]--
function binary(num)
    s = ""
    
    while(num>0)
    do
        rem = num%2
        s = s..tostring(rem)
        num = math.floor(num/2)
    end

    n = string.len(s)
    m = 4-n
    
    while(m>0)
    do
        s = s..tostring(0)
        m = m-1
    end
    
    t = string.reverse(s)
    return t
    
    
end

function walls(s)
    myWalls = {}
    n = string.len(s)
    
    for i=1,4
    do
        if(string.sub(s,i,i)=="1")
        then
            w = math.pow(2,4-i)
            table.insert(myWalls,w)
        end
    end
    return myWalls
end

function carveMaze(s,i,j)
    
    if(s=="H")
    then
    objectName = "H_wallSegment_"..tostring(i).."x"..tostring(j)
    else
    objectName = "V_wallSegment_"..tostring(i).."x"..tostring(j)
    end
    
    objHandle = sim.getObjectHandle(objectName)
    if(objHandle~=-1)
    then
        sim.removeObject(objHandle)
    end

end

--[[
**************************************************************
	Function Name : createWall()
    Purpose:
	---
	Creates a black-colored wall of dimensions 90cm x 10cm x 10cm

	Input Arguments:
	---
	None
	
	Returns:
	---
	wallObjectHandle : number
    
    returns the object handle of the created wall
	
	Example call:
	---
	wallObjectHandle = createWall()
**************************************************************	
]]--
function createWall()
    wallObjectHandle = sim.createPureShape(0, 26, {0.09, 0.01, 0.1}, 0, nil)
    sim.setShapeColor(wallObjectHandle, nil, sim.colorcomponent_ambient_diffuse, {0, 0, 0})
    sim.setObjectSpecialProperty(wallObjectHandle, sim.objectspecialproperty_collidable)
    sim.setObjectSpecialProperty(wallObjectHandle, sim.objectspecialproperty_measurable)
    sim.setObjectSpecialProperty(wallObjectHandle, sim.objectspecialproperty_detectable_all)
    sim.setObjectSpecialProperty(wallObjectHandle, sim.objectspecialproperty_renderable)
    return wallObjectHandle
end

--[[
**************************************************************
  YOU ARE NOT ALLOWED TO MODIFY OR CALL THIS HELPER FUNCTION
**************************************************************
	Function Name : saveTexture()
    Purpose:
	---
	Reads and initializes the applied texture to Base object
    and saves it to a file.

	Input Arguments:
	---
	None
	
	Returns:
	---
	None
	
	Example call:
	---
	saveTexture()
**************************************************************	
]]--
function saveTexture()
    baseHandle = sim.getObjectHandle("Base")
    textureID = sim.getShapeTextureId(baseHandle)
    textureData=sim.readTexture(textureID ,0,0,0,0,0)
    sim.saveImage(textureData, {512,512}, 0, "models/other/base_template.png", -1)
end
--[[
**************************************************************
  YOU ARE NOT ALLOWED TO MODIFY OR CALL THIS HELPER FUNCTION
**************************************************************
	Function Name : retrieveTexture()
    Purpose:
	---
	Loads texture from file.

	Input Arguments:
	---
	None
	
	Returns:
	---
	None
	
	Example call:
	---
	retrieveTexture()
**************************************************************	
]]--
function retrieveTexture()
    textureData, resolution = sim.loadImage(0, "models/other/base_template.png") 
end

--[[
**************************************************************
  YOU ARE NOT ALLOWED TO MODIFY OR CALL THIS HELPER FUNCTION
**************************************************************
	Function Name : reapplyTexture()
    Purpose:
	---
	Re-applies texture to Base object

	Input Arguments:
	---
	None
	
	Returns:
	---
	None
	
	Example call:
	---
    reapplyTexture()
**************************************************************	
]]--
function reapplyTexture()
    plane, textureID = sim.createTexture("", 0, nil, {1.01, 1.01}, nil, 0, {512, 512})
    sim.writeTexture(textureID, 0, textureData, 0, 0, 0, 0, 0)
    sim.setShapeTexture(baseHandle, textureID, sim.texturemap_plane, 0, {1.01, 1.01},nil,nil)
    sim.removeObject(plane)
end

--############################################################

--[[
**************************************************************
	Function Name : receiveData()
    Purpose:
	---
	Receives data via Remote API. This function is called by 
    simx.callScriptFunction() in the python code (task_2b.py)

	Input Arguments:
	---
	inInts : Table of Ints
    inFloats : Table of Floats
    inStrings : Table of Strings
    inBuffer : string
	
	Returns:
	---
	inInts : Table of Ints
    inFloats : Table of Floats
    inStrings : Table of Strings
    inBuffer : string
    
    These 4 variables represent the data being passed from remote
    API client(python) to the CoppeliaSim scene
	
	Example call:
	---
	N/A
    
    Hint:
    ---
    You might want to study this link to understand simx.callScriptFunction()
    better 
    https://www.coppeliarobotics.com/helpFiles/en/remoteApiExtension.htm
**************************************************************	
]]--
function receiveData(inInts,inFloats,inStrings,inBuffer)

    --*******************************************************
    --               ADD YOUR CODE HERE
    
    
    row = 10
    col = 10
    k = 1
    maze_array = {}
    for i=1,row
    do
        myTables = {}
        for j=1,col
        do
            table.insert(myTables,inInts[k])
            k = k+1
        end
        table.insert(maze_array,myTables)
    end
    --*******************************************************
    return inInts, inFloats, inStrings, inBuffer
end

--[[
**************************************************************
	Function Name : generateHorizontalWalls()
    Purpose:
	---
	Generates all the Horizontal Walls in the scene.

	Input Arguments:
	---
	None
	
	Returns:
	---
    None
	
	Example call:
	---
	generateHorizontalWalls()
**************************************************************	
]]--
function generateHorizontalWalls()

    --*******************************************************
    --               ADD YOUR CODE HERE
    
    x_pos = -0.450
    y_pos = 0.5
    z_pos = 0.0640
    row = 10
    col = 10
    
    for i=1,11
    do
        for j=1,10
        do
            wall_objectHandle = createWall()
            parent_objectHandle = sim.getObjectHandle("Base")
            res_set_parent = sim.setObjectParent(wall_objectHandle,parent_objectHandle,False)
            objName = "H_wallSegment_"..tostring(i).."x"..tostring(j)
            res_set_name = sim.setObjectName(wall_objectHandle,objName)
            draw_objectHandle = sim.addDrawingObject(wall_objectHandle,1,0.0,parent_objectHandle,1,NULL,NULL,NULL,NULL)
            res_set_pos = sim.setObjectPosition(wall_objectHandle,parent_objectHandle,{x_pos,y_pos,z_pos})
            x_pos = x_pos+0.10
        end
        if(x_pos==0.550)
        then
            x_pos = -0.450
        end
        y_pos = y_pos-0.10
    end


        
    --*******************************************************
end

--[[
**************************************************************
	Function Name : generateVerticalWalls()
    Purpose:
	---
	Generates all the Vertical Walls in the scene.

	Input Arguments:
	---
	None
	
	Returns:
	---
    None
	
	Example call:
	---
	generateVerticalWalls()
**************************************************************	
]]--
function generateVerticalWalls()

    --*******************************************************
    --               ADD YOUR CODE HERE
    x_pos = -0.50
    y_pos = 0.45
    z_pos = 0.0640
    row = 10
    col = 10
    
    for i=1,10
    do
        for j=1,11
        do
            wall_objectHandle = createWall()
            parent_objectHandle = sim.getObjectHandle("Base")
            res_set_parent = sim.setObjectParent(wall_objectHandle,parent_objectHandle,False)
            objName = "V_wallSegment_"..tostring(i).."x"..tostring(j)
            res_set_name = sim.setObjectName(wall_objectHandle,objName)
            draw_objectHandle = sim.addDrawingObject(wall_objectHandle,1,0.0,parent_objectHandle,1,NULL,NULL,NULL,NULL)
            res_set_orien = sim.setObjectOrientation(wall_objectHandle,parent_objectHandle,{0,0,-1.5707960128784})
            res_set_pos = sim.setObjectPosition(wall_objectHandle,parent_objectHandle,{x_pos,y_pos,z_pos})
            x_pos = x_pos+0.10
        end
        if(x_pos==0.60)
        then
            x_pos = -0.50
        end
        y_pos = y_pos-0.10
    end
    


        
    --*******************************************************
end

--[[
**************************************************************
	Function Name : deleteWalls()
    Purpose:
	---
	Deletes all the walls in the given scene

	Input Arguments:
	---
	None
	
	Returns:
	---
    None
	
	Example call:
	---
	deleteWalls()
**************************************************************	
]]--
function deleteWalls()

    --*******************************************************
    --               ADD YOUR CODE HERE
    row = 10
    col = 10
    for i=1,row
    do
        for j=1,col
        do
            cell_value = maze_array[i][j]
            TrueWalls = walls(binary(cell_value))
            for key,wall in ipairs(TrueWalls)
            do
                if(wall==1.0)
                then
                    carveMaze("V",i,j)--delete v_ixj
                elseif(wall==2.0)
                then
                    carveMaze("H",i,j)--delete h_ixj
                elseif(wall==4.0 and j==col)
                then
                    carveMaze("V",i,j+1)--delete v_ix(j+1)
                elseif(wall==8.0 and i==row)
                then
                    carveMaze("H",i+1,j)--delete h_(i+1)xj
                end
            end
        end
    end
    


        
    --*******************************************************
end


--[[
**************************************************************
  YOU CAN DEFINE YOUR OWN INPUT AND OUTPUT PARAMETERS FOR THIS
                          FUNCTION
**************************************************************
	Function Name : createMaze()
    Purpose:
	---
	Creates the maze in the given scene by deleting specific 
    horizontal and vertical walls

	Input Arguments:
	---
	None
	
	Returns:
	---
    None
	
	Example call:
	---
	createMaze()
**************************************************************	
]]--
function createMaze()
    
    --*******************************************************
    --               ADD YOUR CODE HERE
    
    row = 10
    col = 10
    for i=1,row
    do
        for j=1,col
        do
            cell_value = 15-maze_array[i][j]
            falseWalls = walls(binary(cell_value))
            for key,wall in ipairs(falseWalls)
            do
                if(wall==1.0)
                then
                    carveMaze("V",i,j)--delete v_ixj
                elseif(wall==2.0)
                then
                    carveMaze("H",i,j)--delete h_ixj
                end
            end
        end
    end
            
        


        
    --*******************************************************
end



--[[
**************************************************************
	Function Name : sysCall_init()
    Purpose:
	---
	Can be used for initialization of parameters
    
	Input Arguments:
	---
	None
	
	Returns:
	---
    None
	
	Example call:
	---
	N/A
**************************************************************	
]]--
function sysCall_init()
    
    if pcall(saveTexture) then -- Do not delete or modify this section
        print("Successfully saved texture")
    else
        print("Texture does not exist. Importing texture from file..")
        retrieveTexture()
        reapplyTexture()
    end     
end

--[[
**************************************************************
        YOU ARE NOT ALLOWED TO MODIFY THIS FUNCTION. 
**************************************************************
	Function Name : sysCall_beforeSimulation()
    Purpose:
	---
	This is executed before simulation starts
    
	Input Arguments:
	---
	None
	
	Returns:
	---
    None
	
	Example call:
	---
	N/A
**************************************************************	
]]--
function sysCall_beforeSimulation()
    
    sim.setShapeTexture(baseHandle, -1, sim.texturemap_plane, 0, {1.01, 1.01},nil,nil) -- Do not delete or modify this line
    
    generateHorizontalWalls()
    generateVerticalWalls()
    createMaze()
end

--[[
**************************************************************
        YOU ARE NOT ALLOWED TO MODIFY THIS FUNCTION. 
**************************************************************
	Function Name : sysCall_afterSimulation()
    Purpose:
	---
	This is executed after simulation ends
    
	Input Arguments:
	---
	None
	
	Returns:
	---
    None
	
	Example call:
	---
	N/A
**************************************************************	
]]--
function sysCall_afterSimulation()
    -- is executed after a simulation ends
    deleteWalls()
    reapplyTexture() -- Do not delete or modify this line
end

function sysCall_cleanup()
    -- do some clean-up here
end

-- See the user manual or the available code snippets for additional callback functions and details