# GeoPython Conference 2018

**Processing Framework: Automating Tasks with Python**

A modified version of the [QGIS workshop for the GeoPython Conference 2018](https://giswiki.hsr.ch/Workshop_QGIS_Python_GeoPython_2018). The original workshop GitHub page can be found [here](https://github.com/geometalab/GeoPythonConf2018-QGIS-Processing-Workshop ).
 
## Getting started

To try out our hands on examples, the following is required:
* QGIS 3.x (We will be using QGIS 3.0)
* Python 3.x (We will be using Python 3.6)
* Qt
* PyQt

Downloading the standalone or OSGeo4W installer will automatically install the correct version of Python as well as Qt and PyQt.

1. [Download and install QGIS 3.x](https://www.qgis.org/en/site/forusers/download.html) (Only QGIS 3.0 and above is supported because of changes in the update from 2.18 to 3.0)
2. Get the sample data that we will be using from [this repository](https://github.com/robembd/GeoPythonConf2018-QGIS-Processing-Workshop)
	1. Option 1: go to repository click on **Code/Download ZIP**)
	2. Option 2 (in case you have Git installed): clone the repository using the command line (`cd` to the parent folder and type `git clone https://github.com/robembd/GeoPythonConf2018-QGIS-Processing-Workshop.git`)
3. Fire up QGIS and we're ready! 
 
**Notes:**

* This repository contains the hands-on problem sets and tasks that we will try out during the workshop. You can find the suggested solutions, master scripts, and graphic models for the tasks in the folder `Scripts` subfolder (read the readme for more information on the different files).
* For QGIS <2.99 users, these problem sets are still workable, but do take note that as QGIS upgraded from QGIS 2.18 to QGIS 3.0.0, there are a lot of changes, including the Python syntax to be upgrade from Python 2.6 to Python 3.6
* It is still possible to follow this workshop in QGIS 2.18, but do make sure that you are aware of the backwards incompatible changes as many methods and functions were made obsolete or renamed. You can see the [version changelog here](https://qgis.org/api/api_break.html#qgis_api_break_3_0_QgsGeometryAnalyzer)
* To be more specific and as a disclaimer, it is rather redundant if you are following this workshop using QGIS 2.18, as the LTR version of QGIS would soon be updated to QGIS 3.x, and the workshop here would still be very likely to work in the LTR
   
## Getting more sample data

If you want more sample data or resources to further try out QGIS on your own, look no further:
 
* [The PyQGIS Programmer's Guide](http://locatepress.com/ppg3)
* [The QGIS website also has some sample data](http://www.qgis.org)
* For raster layers to play around with, we can download one of the [Natural Earth rasters](http://www.naturalearthdata.com/downloads/)
* Various blogs, channels, etc.
 
## Using the QGIS Python Console

* With QGIS running, open the console by going to `Plugins -> Python Console`, clicking on the `Python Console` button from the `Plugin toolbar`, or simply press `Alt + Ctrl + P` on the keyboard
* The toolbar contains the tools **Clear console, Import Class, Run Command, Show Editor, Settings,** and **Help**
* The built-in code editor can be used alongside the console
* The QGIS API offers a large number of [Python classes](http://labs.webgeodatavore.com/partage/diagramme_principal.html) that we can use. See [Searchable documentation of PyQGIS classes](https://qgis.org/pyqgis/3.0/index.html)
* For the convenience of the user, the following statements are executed when the consoles is started
```python
from qgis.core import *
import qgis.utils
```
   
## Introduction to Processing Framework

More information can be found in the slides also available in this repository (file: **Workshop Slides/GeoPython Conference 2018.pdf**).

To summarize, it is a geoprocessing environment that can be used to call native and third-party algorithms from QGIS, making your spatial analysis tasks more productive and easy to accomplish. Its features include the algorithm **toolbox** as well as several **automation tools** including a graphic modeler and user-defined scripts.

As a Core plugin, Processing is installed by default but you need to activate it:

1. Go to `Plugins -> Manage and install plugins…`
2. Click on the Installed tab at the left
3. Check the box next to the Processing entry
4. Close the dialog.

## About PyQGIS

* QGIS 0.9.0 introduced Python to its client
* PyQGIS or Python Console in QGIS client
* Features of PyQGIS:
    * Automatically run Python code when QGIS starts
    * Create custom applications with Python API
    * Run Python code and commands on the Python Console
    * Create and use Python plugins

# **Task: Perform Geospatial Analysis on Protected Habitats in an Environment**

* **Problem**: The construction of an autobahn/expressway will have a detrimental impact on the habitats on its environment. The goal is to analyze the protected habitats (flora and fauna) that would be affected by the construction of a fictional expressway, and to determine how many species and biotypes in the impact area of building a highway are legally protected.
* **Source**: This task is based on Task 6 of the course _Introduction to GIS and Digital Cartography_ by Claas Leiner, University of Kassel, 2010.
	* Adapted to a class for Vector Analysis by Stefan Keller, FS 2017
	* Translated and adapted for QGIS 3.0 and the GeoPython Conference by Kang Zi Jing, 2018
* **Data**: provided are a polygon vector file (**umgebung.gpkg**) which maps Biotype habitats, a line vector file (**autobahn.gpkg**) for the fictional highway route, and a topographic map (**heli_georeferenced.tif**) scaled at 1:25,000 (Tk25) to be used as a basemap. 
* **Workflow**: The detailed workflow can be found in the repositor in **Workflow/Highway Construction Workflow English.doc**.

**As you can already guess, doing the same analysis over and over again on different files is very tedious, boring and repetitive. Is there a way to automate this? Yes! With the help of scripting and PyQGIS, we can!**

With the click of a button to run a script, we can automate this task in mere seconds.

This problem will be broken down into smaller problem sets and tasks to break the problem down. The tasks will be progressive, from getting familiar with the QGIS client to using its Processing toolbox tools, like the Graphical Modeler before moving on to creating your own custom script.


## **Task 1.** Adding GeoPackage as Layers into QGIS

- **Dataset used:** `Umgebung.gpkg`, `Autobahn.gpkg`
- **Tools used:** QGIS GUI, PyQGIS
- **Description:** To load `.gpkg` files into QGIS client
- **Objective:** Manually load vector layers on QGIS, and then using the Python console

#### Task 1.1. Manually adding the GeoPackage files into QGIS

1. Run QGIS 3.0 on your machine
2. The first step is to set the Project CRS to 31467 (DHDN/Gauss-Kruger Zone 3) which corresponds to the CRS of the `umgebung.gpkg` file which will be added first. All subsequent data (including `autobahn.gpkg` which uses another CRS) will be projected on the fly when added to the QGIS project.
3. You can do this manually by clicking on the CRS at the bottom-right of the window, or by clicking `Project -> Project Properties -> CRS` or you can press `Ctrl + Shift + P` to open up Project Properties and then clicking CRS
4. From there, change the CRS to `DHDN/Gauss-Kruger zone 3, EPSG: 31467`
5. Once you're done, check that it says 'EPSG:31467' at the bottom of the window on the CRS tab
6. Now on the browser panel, look for GeoPackage, right-click it and select `New Connection`
7. Navigate to the folder you saved the GeoPackage file `Dataset/umgebung.gpkg` in and add it
8. On the browser panel, show the child items of the newly created connection `umgebung.gpkg` and drag the vector layer onto the map canvas (or double-click it)
9. **(Optional)** you can play around with the Styling of the layer and classify it by the attribute `bfn_biotope_text` with different colors. To do this, right-click the environment layer and go to `Properties -> Symbology` and select `Categorized` from the drop-down menu at the top of the dialog box, selecting a color ramp (for example 'Random colors') and clicking on `Classify`.
10. As we are going to focus on scripting in Python, let's remove this layer: right-click the layer under Layers, and click on `Remove Layer`

#### Task 1.2. Creating a Dialog Box to ask for User Input on File to Add

We want to write a script to automate tasks, so let us explore asking for user input for file path:

1. On the Menu Toolbar, click `Plugins -> Python Console` or press `Ctrl + Alt + P` on your keyboard to open up the Python Console
2. You can run Python code on the console or in the editor. We'll choose the latter. To sho the editor click on the 'Show editor' button next to the `Run command button`. 
3. In the editor create a new file and save it somewhere, for example in a new folder `/Solution/My Solution.py`
4. In the previous step we set the CRS manually to EPSG:31467. This can also be done programmatically. First restore the default CRS by copy-pasting the command `QgsProject.instance().setCrs(QgsCoordinateReferenceSystem(4326))` in the script file.
5. Run the command by selecting and right-clicking on it and select `Run Selected`
6. Check that the CRS in the bottom right corner has changed back to EPSG:4326. Then restore the CRS to EPSG:31467 by running the command `QgsProject.instance().setCrs(QgsCoordinateReferenceSystem(31467))`.
7. Try creating a file dialog box that asks for user input on the file path by copy-pasting the following command in the script: `envPath = QFileDialog.getOpenFileName(QFileDialog(), 'Environment Layer Select', 'setDefaultPath')[0]`. The `[0]` is because the above returns a list, and we only need the first value of it, which is the file path
8. Check the stored user input path by printing it in the console: `print('Environment file path: ' + envPath)`


#### Task 1.3. Adding Vector Layers into QGIS

Now we can add the user input layer into QGIS

1. Add a new layer called `My Layer` to the project: `envLayer = iface.addVectorLayer(envPath, 'My Layer', 'ogr')`
2. Change the layer name to 'Environment': `envLayer.setName('Environment')`
3. Practice and do the same for the Autobahn (file: `autobahn.gpkg`) layer by first asking the GeoPackage file path user input and then adding it as a vector layer with name 'Autobahn'. If needed change the layer symbology manually to another color.

![Reference](https://github.com/bigzijing/Geopython-Conference-2018/blob/master/Workshop%20Presentation%20Slides/Workflow%20Example%20Images/Task%201.png)

## Task 2. Adding Buffers to Autobahn Layer

- **Dataset used:** `Autobahn.gpkg`
- **Tools used:** Processing Graphic Modeler, Python Console
- **Description:** To create buffer layers for the Autobahn to simulate the actual physical space of it
- **Objective:** Running Processing algorithms on the Graphic Modeler, and then with Pythonic code

#### Task 2.1. Introduction and Running the Graphic Modeler

The Graphic Modeler is a good introduction to scripting in PyQGIS because the coding and scripting is displayed for the user as something visual, which is easy on the beginners.

1. To start off, you need to open up your Processing Toolbox, on the menu toolbar, click `Processing -> Toolbox` or press `Ctrl + Alt + T` and see that the Processing Toolbox window now appears on the right side of the QGIS window
2. On the Toolbox's menu toolbar, click `Models -> Create New Model`
3. First, we need to visualize and get an idea of what we want to achieve (this helps us to form pseudo code before creating actual code in the future): Run through the Autobahn layer with a Buffer algorithm to create a new Autobahn layer that is 40m wide in diameter

#### Task 2.2. Create a 20m buffer for the Autobahn layer using the Graphic Modeler

With the Processing Graphic Modeler open, we can now visualize and build Task 2.1.3

1. Name the Model `Autobahn Buffer` and the Group `vector`
2. On the left, click on the `Inputs` tab (next to the `Algorithms` tab) if it is not already selected, and drag Vector Layer into the blank canvas
3. Name the parameter name `Input Layer Name` and under Geometry type select 'Line' as we only want it to exclusively deal with line geometries
4. Drag a Number under Input into the canvas, and name it `Buffer Distance`. The other fields can be left empty.
5. On the left, click on the `Algorithms` tab. In the search bar type 'Buffer' and drag the Algorithm called `Buffer` from the `Vector geometry` category into the canvas
6. In the 'Input layer' field change the type from 'Value' to 'Model Input'. Next, select the `Input Layer` input from the drop-down menu. Do the same for the 'Distance' field by changing the type to 'Model Input' and then selecting `Buffer Distance` as value. In the 'Buffered' field, select 'Model Output' as type and type 'Buffer Output'
7. On your canvas, you should see that **Autobahn** and **Buffer Distance** are connected as inputs to **Buffer** which gives an output named **Buffer Output**
8. On the menu toolbar, click on the green arrow Run Model or press F5 to run the model
	- Under `Input Layer`, select your Autobahn vector layer from the drop down menu. 
	- Under `Buffer Distance`, type in **20** 
	- Leave `Buffer Output` blank, which will create a temporary output layer
	- Leave the `Open output file after running algorithm` option checked
	- Run the model and inside the QGIS project rename the output layer 'Buffer Output' to **Autobahn 20** in the Layers panel
10. Let the Model run and after processing, you should see the output vector on your main QGIS window
11. **(Optional)** After creation your custom models can be added to the Processing Toolbox for later use. save the model as `AutobahnBuffer.model3` in a separate subfolder 'Solution'. On the Toolbox's menu toolbar, click `Models -> Add Model to Toolbox...` and navigate to the saved model file. It will be added to the toolbox under `Models -> vector` and saved in the QGIS app data.
12. **(Optional after Step 11)** Your model can be converted to a Python **Script Algorithm**, which itself can be imported to the Processing Toolbox. To do this:
	- Inside the `AutobahnBuffer.model3` Model Designer click on `Export as Script Algorithm` and save the script file as `AutobahnBufferPython.py`.
	- To be able to distinguish between the Modeler and Script names go to the bottom of the script and change the `name` and `displayName` return values to 'Autobahn Buffer Script'. For example `def displayName(self): return 'Autobahn Buffer Script'`
	- Close the script and on the Processing Toolbox's menu toolbar, click `Scripts -> Add Script to Toolbox...` and navigate to the saved Python script.
	- The script will be added under `Scripts -> vector`. If you run it with the same inputs you'll notice that the output layer name will be 'Buffered' rather than 'Buffer Output'. The former is the default output layer name of the standard Buffer tool.

![Reference](https://github.com/robembd/GeoPythonConf2018-QGIS-Processing-Workshop/blob/master/Workshop%20Slides/Slides%20Images/Graphic%20Modeler%20Example.png)

#### Task 2.3. Recreating the same function using a standalone script

Now that you visualized your steps, you can now try to translate them into actual Pythonic code.

1. Clean up by removing all copies of the buffered Autobahn layers from the previous task.
2. On the main QGIS window, at the Processing Toolbox, search for **Buffer**, this is the algorithm that we utilized in the Modeler
2. Double-click on it and you can do essentially the same thing as we did in the modeler, except with a few extra fields that we set to default in the Modeler
3. Enter the fields for **Input Layer (Autobahn), Distance (20)** while leaving the **Buffered** field empty (default 'Create temporary layer') and run it
4. At the top of the window, click on 'Log' and you will see a bunch of code. We will be needing this for our script.
5. Study the 'Input parameters' section of the log and copy its entire line of code (including the curly brackets)
6. On the PyQGIS console, type `inpLayer = QgsProject.instance().mapLayersByName('Autobahn')[0]`, this assigns the vector layer of your autobahn to the variable `inpLayer`
7. On the PyQGIS console, type `inpParam =` and paste the copied code, and edit the INPUT parameter from the file path to the referenced input layer. It should look something like this (may be slightly different depending on the used QGIS version, you can also see this in the screenshot):
``
inpParam = { 'INPUT' : inpLayer, 'DISTANCE' : 20, 'SEGMENTS' : 5, 'END_CAP_STYLE' : 0, 'JOIN_STYLE' : 0, 'MITER_LIMIT' : 2, 'DISSOLVE' : False, 'OUTPUT' : 'TEMPORARY_OUTPUT' }
``
8. Now to add the output as a map layer, type:
```
outAlgo = processing.run('qgis:buffer', inpParam)
outLayer = QgsProject.instance().addMapLayer(outAlgo['OUTPUT'])
outLayer.setName('Autobahn 20')
```

![Reference](https://github.com/bigzijing/Geopython-Conference-2018/blob/master/Workshop%20Presentation%20Slides/Slide%20Images/Buffer%20Log%20Example.png)

#### Task 2.4. Creating 2 more buffers

Oftentimes, the actual physical space that a highway construction takes up, is smaller than the actual impact that it causes to the environment.

For this we create 2 more buffers to depict 2 more impact zones that the construction of the Autobahn would cause. This can be done by copy-pasting the code from the previous task and modifying it.

1. Using `Autobahn` as input layer and 100m as buffer distance, create a new buffer named `Autobahn 100`
	- Hint: since the `Autobahn` layer doesn't change it doesn't have to be copied/reassigned anymore.
2. Using `Autobahn` as input layer and 300m as buffer distance, create a new buffer named `Autobahn 300`
3. Reorder the layers manually such that all layers are visible in the map canvas (we will later see how to do this in Python)

**Bonus**: rather than copy-pasting and modifying code you could write a reusable function `buffer_layer(inpLayerName, bufDist, outLayerName)` where `inpLayerName` is the input layer name (for getting input layer), `bufDist` the buffer distance in meters (buffer tool parameter) and `outLayerName` (for creation of output layer).


## Task 3. Performing Union on the Buffer Areas

- **Dataset used:** `Autobahn.gpkg`, and the 3 buffer results from previous task
- **Tools used:** Python Console, Script Editor
- **Description:** Now that we have 3 separate buffer layers to showcase the impact areas, we should perform an Union on them to create an overall area of impact from constructing the highway
- **Objective:** Get more familiar with using Pythonic code to run Processing algorithms

#### Task 3.1. Union-ing the Inner Impact Zone

Now that we have run our first Processing algorithms using a standalone script, let's try to run a different algorithm, the Union. 

This tool can be used to merge the 3 previously created layers `Autobahn 20`, `Autobahn 100` and `Autobahn 300` into a **single layer with non-overlapping geometries**. It will therefore represent 3 impact zones 0-20m, 20-100m and 100-300m. Unfortunately this tool only allows the combination of 2 layers at the same time which means that we'll have to execute it twice (first combining `Autobahn 20`, `Autobahn 100` which is finally combined with `Autobahn 300`)

1. On the main QGIS window in the Processing Toolbox search bar, search 'Union' and you can try running the Union algorithm under the 'Vector Overlay' category
2. The inputs will be `Autobahn 20` (Input layer) and `Autobahn 100` (Overlay layer), and name the output `Inner Impact Area`
3. Run the tool and use the same strategy from Task 2 by copying the input parameters from the Log window. Expand your script to perform the same operation.
	- Note: similar to the previous task you may want to replace some of the parameter values to layer references (for example for 'OVERLAY')
	- Note: if you have trouble doing it (or if you're interested), you can try using the Modeler to visualize your script

**Bonus**: similar to the Buffer tool from the previous task you can try to create a function `union_layers(inpLayerName1, inpLayerName2, outLayerName)` that performs the union of 2 layers with names `inpLayerName1` and `inpLayerName2` and outputs a temporary output layer with name `outLayerName`.

#### Task 3.2. Union-ing the Overall Impact Area

Next, we perform the Union algorithm on the result of the previous task, the Inner Impact Zone, with the Outer Impact Zone to aggregate the total Area of Impact
1. Do the same for the resulting layer, `Inner Impact Area` and `Autobahn 300` and name the output `Impact Area`
2. You will now have a layer that is the union of all 3 Autobahn buffers
3. You can see a screenshot of what your project should roughly look like below:

![Reference](https://github.com/bigzijing/Geopython-Conference-2018/blob/master/Workshop%20Presentation%20Slides/Slide%20Images/Task%203%20Example.png)

4. Verify that the merged features are indeed non-overlapping by examining the part related to the 300m buffer. 
	- Open the `Impact Area` attribute table. You see that 3 features have been created and that the attributes have been combined depending on overlapping and non-overlapping parts. The smallest feature for example corresponds to the part of the union that corresponds to the overlap of all 3 layers and has all attributes specified (non-NULL), while the other 2 features have missing values for at least 2 fields.
	- If `outLayer` references the `Impact Area` layer the following filter can be applied to only see the most outer feature: `outLayer.setSubsetString('fid IS NULL AND fid_2 IS NULL')`. You will see that this feature indeed has no overlap with the other features in the layer. *Note*: this particular filter will only work for temporary layers.
	- Remove the filter to see all features again: `outLayer.setSubsetString('')`

#### (Optional) Task 3.3. Modifying the attribute table

The new `Impact Area` layer does not have any meaningful attribute values for the individual impact zones. In order to determine the area of differently valued biotypes in the impact zone, we must assign some attribute values to the zones.

For this task we will replace the original attributes from the `Impact Area` layer by 3 new ones: 1) the feature ID (sequential number), 2) the area of the feature and 3) an indicator of the zone type ('Route', 'Inside' or 'Outside')

1. First we create 3 additional fields `fid_union`, `area` and `zone`
```
unionLayer = QgsProject.instance().mapLayersByName('Impact Area')[0]
layerProvider = unionLayer.dataProvider()
layerProvider.addAttributes([QgsField('fid_union', QVariant.Int)])
layerProvider.addAttributes([QgsField('zone', QVariant.String)])
layerProvider.addAttributes([QgsField('zone_area', QVariant.Double)])
unionLayer.updateFields()
```
2. Toggle the editing mode of the`Impact Area` layer and fill in the 3 new fields with resp. the feature ID, their polygon area and the zone indicator

```
unionFeatures = unionLayer.getFeatures()
unionLayer.startEditing()
for f in unionFeatures:
    # calculate feature zone type
    indFID = unionLayer.fields().indexFromName('fid')
    valFID = f.attributes()[indFID]
    indFID2 = unionLayer.fields().indexFromName('fid_2')
    valFID2 = f.attributes()[indFID2]
    if valFID is None and valFID2 is None:
        valZone = 'Outside'
    elif valFID is None:
        valZone = 'Inside'
    else: 
        valZone = 'Route'
    # calculate feature area
    valArea = f.geometry().area()
    # store attribute values   
    featID = f.id()
    indFIDUnion = unionLayer.fields().indexFromName('fid_union')
    indZone = unionLayer.fields().indexFromName('zone')
    indArea = unionLayer.fields().indexFromName('zone_area')
    valDict = {indFIDUnion: featID, indArea: valArea, indZone: valZone}
    layerProvider.changeAttributeValues({featID: valDict})
```

3. Save the changes: `unionLayer.commitChanges()`
4. Remove the original fields from the attribute table

```
fieldsAll = unionLayer.fields().names()
fieldsKeep = ['fid_union', 'zone', 'zone_area']
fieldsRemove = [i for i in fieldsAll if i not in fieldsKeep]
fieldsRemoveIndex = [unionLayer.fields().indexFromName(i) for i in fieldsRemove]
layerProvider.deleteAttributes(fieldsRemoveIndex)
unionLayer.updateFields()
```

5. Using the GUI open the layer properties, go to the 'Symbology' tab and apply a Categorized coloring using the new 'zone' field.

**Notes**: 

1. Naturally, for large attribute tables and/or more complex operations this loop-based editing can become slow/cumbersome. More compact/efficient functionality may be implemented in the future (e.g. data-frame like operations on attribute tables). This was mainly to illustrate one possible ways to modify attribute tables using Python.
2. Naturally (again), symbology can be set programmatically as well. We will briefly explore this for task 6.


## Task 4. Performing Intersection on Environment and Impact Area

- **Dataset used:** `Umgebung.gpkg`, union result from previous task (`Impact Area`)
- **Tools used:** Script Editor
- **Description:** Now that we have an overall impact area, we run an Intersection algorithm on it and the Environment layer to highlight the habitats that would be affected
- **Objectives:** More scripting with Processing algorithms

Now that we're getting more and more familiar with running geoprocessing tools in PyQGIS, we'll run an Intersection algorithm on the Environment layer as well as the Impact Zone layer. 

This tool will extract the overlapping portions of features (implying that they will be 'cut'!) from both layers and join their attributes.

1. Similar to Task 3, run the **Intersection** algorithm (found in the 'Vector overlay' group) on the `Impact Area` layer and the `Environment` layer
2. You will get an error that the `Environment` layer has invalid geometry. To fix this you first have to run an additional tool called **Fix geometries** found under the 'Vector geometry' group. After running the tool copy and paste the input parameters somewhere. Keep the temporary output layer `Fixed geometries`.
3. Try to run the Intersection algorithm again, now using the `Fixed geometries` layer rather than `Environment`. After running the tool copy and paste the input parameters somewhere.
4. Remove the 2 temporary layers `Fixed geometries` and `Intersection` and expand your script to
	- fix the geometry of the `Environment` layer using the 'Fix geometries' tool with output layer name `Environment Fixed` **without adding the fixed geometry layer to the project** (only store the layer reference: `envLayerFixed = outAlgo['OUTPUT']` instead of `QgsProject.instance().addMapLayer(...)`
	- make the intersection of `envLayerFixed` with `Impact Area` using the 'Intersection' tool with output layer name `Impact Area Intersect`.

**Bonus**: create a function `intersect_layers(inpLayerName1, inpLayerName2, outLayerName)` that first checks the validity of the layers with names `inpLayerName1` and `inpLayerName1` (and deriving a fixed geometry version of the layer **without adding it to the project**) and then creates an intersection with name `outputLayerName`. One possible way is to make use of a third tool in the Toolbox (find out which one... or check the solution file `Scripts/Workshop Solution.py`). You can use the same strategy as before to get the required inputs, parameters and outputs (note that some algorithm can have *multiple* outputs). Another way would involve more general Python exception handling of the thrown `QgsProcessingException` error (using `try`, `except` and/or `finally`).
5. Your result should look something like this: 

![Reference](https://github.com/bigzijing/Geopython-Conference-2018/blob/master/Workshop%20Presentation%20Slides/Slide%20Images/Task%204%20Example.png)


## Task 5. Selecting Features from Queries

- **Dataset used:** `Umgebung.gpkg`
- **Tools used:** Query Features and Script Editor
- **Description:** Now, we have to sieve out, from the impacted and affected habitats, those that are protected species from the others
- **Objectives:** Feature query on QGIS, feature query in PyQGIS, adding layers in PyQGIS

#### Task 5.1. Running a Query on the Environment Vector Layer Attributes

Query the attributes of the `Impact Area Intersect` layer from the previous task to determine the **features that are protected by law**.

1. To do this, right click on the Environment layer in the Layers panel, and select `Open Attribute Table`
2. On the top menu bar, click the button that says `Select features with an expression`
3. Write the expression for which you want to select queries with, for our case, we are looking for habitats where `ffh_typ_nr = 1`, `geschuetzt_biotop = 1`, or `bedeutend_gruenland_typ = 1`
4. Once you have written the expression, click on `Select Features`, you should have 40 features highlighted

![Reference](https://github.com/bigzijing/Geopython-Conference-2018/blob/master/Workshop%20Presentation%20Slides/Workflow%20Example%20Images/Task%206.1.png)

#### Task 5.2. Translating Query Feature into Pythonic Code

Now we do what we did in 5.1 using Pythonic code in our script

1. Remember, we are looking for habitats where `ffh_typ_nr = 1`, `geschuetzt_biotop = 1`, or `bedeutend_gruenland_typ = 1`
2. In your script, type:
```
intLayer = QgsProject.instance().mapLayersByName('Impact Area Intersect')[0]
selExpr = QgsExpression("ffh_typ_nr = 1 or geschuetzt_biotop = 1 or bedeutend_gruenland_typ = 1")
```
3. Next, we need to select all features that meet this query. The following expression will return an iterator for the selected features in the layer:
```
intSelFeatures = intLayer.getFeatures(QgsFeatureRequest(selExpr))
```
4. To show the selected features on the map canvas add and execute the following:
```
ids = [i.id() for i in intSelFeatures]
intLayer.selectByIds(ids)
```

![Reference](https://github.com/bigzijing/Geopython-Conference-2018/blob/master/Workshop%20Presentation%20Slides/Workflow%20Example%20Images/Task%206.2.png)

#### Task 5.3. Translating Vector Layer Adding into Pythonic Code

If we select features in QGIS the selected features can be exported by right-clicking on the layer and selecting `Save As...`, using the option `Save only selected features`.  Alternatively a new layer can be created from the feature selection by using plugins such as [Create Layer From Selected Features](https://plugins.qgis.org/plugins/create_layer_from_selected_features/) (surprisingly enough this standard function from ArcGIS is not yet present in vanilla QGIS).

Here however we will create a new layer `Environment Selection` using our script:

1. Materialize the feature selection into a new layer
```
selLayer = intLayer.materialize(QgsFeatureRequest().setFilterFids(ids))
selLayer.setName("Environment Selection")
QgsProject.instance().addMapLayer(valuable)
```
2. Clear the selection from the `Impact Area Intersect` source layer (deselect the highlighted features) with `intLayer.selectByIds([])`

## Task 6. Reordering and Stylizing

- **Dataset used:** All
- **Tools used:** Script Editor
- **Description:** Stylize the map layers to make results more obvious and reorder the layers in the project to make it more readable
- **Objectives:** Various styling tools and functions on QGIS, and then on PyQGIS

#### Task 6.1. Cleaning up Layers

At this point you should at least have the following results in the project: 
- `Environment` (original input)
- `Autobahn` (original input)
- `Autobahn 20/100/300` (buffered versions of `Autobahn`)
- `Inner Impact Area` (union of `Autobahn 20` and `Autobahn 100`)
- `Impact Area` (union of all buffered `Autobahn` layers)
- `Impact Area Intersect` (intersection of `Impact Area` and `Environment`)
- `Environment Selection` (selection of `Impact Area Intersect`, only keeping the protected features)

All other layers are not needed anymore and can be deleted:

1. Create a list of layers we want to keep: `lyrKeep = ['Environment', 'Autobahn', 'Autobahn 20', 'Autobahn 100', 'Autobahn 300', 'Inner Impact Area', 'Impact Area', 'Impact Area Intersect', 'Environment Selection']`
2. Create a list of layers to be removed using a list comprehension:
```
lyrAll = [layer.name() for layer in QgsProject.instance().mapLayers().values()]
lyrRemove = [i for i in lyrAll if i not in lyrKeep]
```
3. Remove all layers from the to-be-removed list:
```
for lyrName in lyrRemove:
    lyr = QgsProject.instance().mapLayersByName(lyrName)[0]
    QgsProject.instance().removeMapLayers([lyr.id()])
```

#### Task 6.2. Reordering and Hiding Layers

Some of the remaining intermediate results are useful, but too many layers visible on the project makes it hard to read.

Apart from that, layers are drawn on top of each other which means that the order matters. We can rearrange the layers for better visibility by for example putting the original Autobahn 20 and Autobahn vector files at the top of the order. 

For a limited number of layers the layer order and visibility can be set manually by reordering and checking/unchecking the layers. In case of a larger number of layers or an automated workflow this can also be done in PyQGIS:

For this we can uncheck their visibility using a script so that they are still available, but not visible on the Map Canvas

1. For now let's keep the 3 layers `Environment`, `Impact Area` and `Environment Selection` visible and store them in a list: `lyrVisible = ['Environment', 'Impact Area', 'Environment Selection']`
2. Let's use the following layer order to avoid that some layers are drawn on top of other layers: `lyrOrder = ['Environment Selection', 'Impact Area Intersect', 'Impact Area', 'Inner Impact Area', 'Autobahn 20', 'Autobahn 100', 'Autobahn 300', 'Autobahn', 'Environment']`
2. Loop over all project layers and set the order and visibility:

```
lyrTreeRoot = QgsProject.instance().layerTreeRoot()

for i in range(len(lyrOrder)):
    lyrOrig = QgsProject.instance().mapLayersByName(lyrOrder[i])[0] # QgsVectorLayer
    lyrTreeOrig = lyrTreeRoot.findLayer(lyrOrig.id()) # QgsLayerTreeLayer
    lyrClone = lyrTreeOrig.clone()
    lyrParent = lyrTreeOrig.parent() # QgsLayerTree
    lyrParent.insertChildNode(i, lyrClone)
    lyrParent.removeChildNode(lyrTreeOrig)
    # set layer visibility
    lyrName = lyrOrder[i]
    lyrID = QgsProject.instance().mapLayersByName(lyrName)[0].id()
    if lyrName in lyrVisible:
        QgsProject.instance().layerTreeRoot().findLayer(lyrID).setItemVisibilityChecked(True)
    else:
        QgsProject.instance().layerTreeRoot().findLayer(lyrID).setItemVisibilityChecked(False) 

print('Reordered and set visibility of ' + str(len(lyrOrder)) + ' layers')
```

#### Task 6.3. Stylizing Map Layers
There are many styles that can be utilized on the layers so that you can get information at a glance.

For today, we try to stylize them by categorizing different data in different colors and similar data in different shades:

1. First we have to choose the attributes we want to categorize our vector layer in, for this example, say we want to make all the valuable habitats that are impacted to be green, and we want to categorize it by the type of FFH classification it falls into
2. To do that, we have to find out how many unique FFH classifications we have in the layer:
```
layerName = 'Environment Selection'
colName = 'ffh_typ_text'
layer = QgsProject.instance().mapLayersByName(layerName)[0]
colIndex = layer.fields().indexFromName(colName)
uniqueVal = layer.uniqueValues(colIndex)
```
3. Now, we categorize the different types of attibutes with a different shade of color:
```
from random import randrange
categories = []
for unique_value in uniqueVal:
    # initialize the default symbol for this geometry type
    symbol = QgsSymbol.defaultSymbol(layer.geometryType())
    # configure a symbol layer
    layer_style = {}
    layer_style['color'] = '%d, %d, %d' % (randrange(0, 256), randrange(0, 256), randrange(0, 256))
    layer_style['outline'] = '#000000'
    symbol_layer = QgsSimpleFillSymbolLayer.create(layer_style)
    # replace default symbol layer with the configured one
    if symbol_layer is not None:
        symbol.changeSymbolLayer(0, symbol_layer)
    # create renderer object
    category = QgsRendererCategory(unique_value, symbol, str(unique_value))
    # entry for the list of category items
    categories.append(category)
```
4. Run the renderer and repaint:
```
renderer = QgsCategorizedSymbolRenderer(colName, categories)
if renderer is not None:
    layer.setRenderer(renderer)

layer.triggerRepaint()
```
5. **(Optional in case you did Task 3.3.)** Do the same for the `Impact Area` layer by applying a different color for each of the unique values of the `fid_union` field. Modify the coloring such that a **different shade of blue** is applied rather than a random color (Hints: you may have modify the for loop + you can for example use a list of RGB combinations you can iterate through in the for loop is used e.g. `rgbs = [[[30, 63, 102], [82, 138, 174], [188, 210, 232]]])` but you could also make it more challenging by trying to use a color ramp). You can check a possible solution in the solutions script `Scripts/Workshop Solution.py`.

#### Task 6.4. Adding a basemap

We can add a raster basemap as a reference for your geospatial data analysis:

1. Get a user input for the path which the raster map is stored as with did before with `QFileDialog.getOpenFileName()`. It is stored under `Dataset/heli_georeferenced.tif`
2. Use `addRasterLayer()` to add the raster layer
3. **Optional**: You may want to play around with the `renderer()` and `symbol()` to adjust the basemap stylization settings
4. Put the layer in the background by manually reordering it (or by modifying and rerunning the code from task 6.2)

The result should look like this (could be different in case you didn't do some of the optional steps):

![Reference](https://github.com/robembd/GeoPythonConf2018-QGIS-Processing-Workshop/blob/master/Workshop%20Slides/Slides%20Images/Task%207b.png)

**Note**: the `heli_georeferenced.tif` file is a manually georeferenced version of the original `heli.tif`. The result is not perfect (for example when you would lay it on top of another basemap like OpenStreetMap) but is sufficient for this exercise.

For comparing  this basemap with an OSM basemap you can optionally run the following code (or importing it manually using `Web -> QuickMapServices -> OSM -> OSM Standard`:
```
tms = 'type=xyz&url=https://tile.openstreetmap.org/{z}/{x}/{y}.png&zmax=19&zmin=0'
layer = QgsRasterLayer(tms,'OSM', 'wms')
QgsProject.instance().addMapLayer(layer)
```
5. Finally zoom to the extent of the `Environment` layer:

```
lyrEnv = QgsProject.instance().mapLayersByName('Environment')[0]
cnvs = iface.mapCanvas()
cnvs.setExtent(lyrEnv.extent())
cnvs.refresh()
```

## Task 7. Finishing Up

- **Dataset used:** (None)
- **Tools used:** Script Editor
- **Description:** Finish up and make sure that all your code is in a single script and everything works when you run it!
- **Objectives:** Finishing touches, making sure all is good

#### Task 7.1. Save and rerun the script on an empty project

In case all previous steps were executed correctly you could try to clear your map canvas and rerun the entire script as once to automatically recreate the workflow.

1. Make sure that all your functions and code are all properly ordered and functions properly. Remove any duplicate creation of outputs (for example once using individual commands and once with a function). You can also use the full solution script from `Scripts/Workshop Solution.py`.
2. **(Optional)** Rerun the full script from scratch:
	- Save your current project as a new one and clear the QGIS canvas in your current project by typing `QgsProject.instance().clear()` in the console
	- Run the full script from the editor by clicking on `Run Script` and make sure that the workflow progresses as intended (load input layers + run tools to create intermediate and output layers)
	- If your final results look like the end result, you just created an automated script that helps automate a workflow! 

#### (Optional) Task 7.2. Run the script from the Processing Toolbox

We have created many different functions to help us achieve our tasks.
The final goal would be to have a script that 
- is interactive and uses the user inputs to automate our tasks
- can be published and/or shared with others

There are many ways to customize your scripts and workflow processing in QGIS. We already know that we can execute our script from the Python Console (as individual commands or in the Editor window. We could however improve it by making the script available as a tool in the Processing Toolbox

While we won't do it here for the full script, we can however illustrate it for the simple buffering tool model you previously created during Task 2.2. and saved as `AutobahnBuffer.model3`:

1. Go to the Processing Toolbox and open the Model Designer of the model (right-click on model and then 'Edit Model'). If it's not there (anymore) import it again by clicking on `Model -> Open Existing Model...` and browsing to the `AutobahnBuffer.model3` model file.
2. Inside the Model Designer click on `Export as Script Algorithm...`
3. A new window will appear with the automatically generated script. Examine it carefully and you'll see that many things look familiar including input and parameter setting, running a tool using `processing.run` and returning its `Output` result. It is however in a slightly different form using classes and certain methods like `initAlgorithm` and `processAlgorithm` to be implemented.
4. Save the Python script
5. Go back to the Processing Toolbox and click on `Scripts -> Add Script to Toolbox...`. You'll see it under the `Scripts` group. It should work in exactly the same way as the model from the Graphic Modeler (same input and parameter names + same output)

#### Bonus: Running from toolbar + creating a Plugin or Main Script

1. We could modify our script to become available as a **tool in the Plugins Toolbar**.  For this the [ScriptRunner 3](https://plugins.qgis.org/plugins/scriptrunner3/) plugin can be installed and used.
2. Naturally there are more ways to convert your script for better execution and sharing, for example by converting it into a **plugin** so that it can be published and used by others .
2. For the more advanced coders, you might want to create a **Python class** and declare methods instead of just defining functions (similar to the code we have explored for converting the script to a Processing Toolbox tool).

The great thing about flexibility is you have the freedom to do as you please to suit your needs, so practice away! 

## Notes and Disclaimer

Note that there is no 'perfect' or 'only' solution when it comes to scripting, and as such, the scripts that were demonstrated and available in this workshop/repository are only for references and to guide you. With that said, always try to maintain good programming practices so that your code is clean, readable and easy to maintain. 

## References, Resources and Additional Help

* [Processing: A Python Framework for the Seamless Integration of Geoprocessing Tools in QGIS by Anita Graser](http://www.mdpi.com/2220-9964/4/4/2219/htm)
    * In-depth development history on Processing Framework
* [Anita Graser's blog](http://anitagraser.com)
* [Processing GitHub repository by Victor Olaya (developer of Processing)](https://github.com/qgis/QGIS-Processing)
* [QGIS Testing Documentation](https://docs.qgis.org/testing/en/docs/)
    * Contains a lot of resources and documentations
    * Links to tutorials and textbooks like the PyQGIS Cookbook, QGIS Developers Guide
* [QGIS Tutorials by Ujaval Gandhi](http://www.qgistutorials.com/en/)
    * Helpful step by step tutorials on many aspects of QGIS
* Vast amount of resources, forums and an active and helpful community online
* Special thanks to helpful developers like Anita Graser and other users on GIS Stack Exchange for answering my questions
* And of course, the wonderful people at Geometa Lab, HSR

## Contact

Kang Zi Jing, author and owner of this GitHub repository: zkang[at]hsr[dot]ch 
