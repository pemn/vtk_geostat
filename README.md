## 📌 Description
full open source workflow for generating a geostatistics block model  
this script integrates multiple generic tools and modules in a single graphical desktop application  
the target audience is academic use by geostatistic professionals or industrial proof of concepts projects  
its not suited for production use  
## 📸 Screenshot
![screenshot1](https://github.com/pemn/assets/blob/main/vtk_geostats1.png?raw=true)
## 🧩 Implementation
This implementations uses a jupyter notebook. Check my other project, bm_geostat_process for a desktop based implementation.
This geostatistics estimation process consists of the following steps:
 1. Data and parameter input
 2. Sample database postprocess
 3. Grid creation
 4. Flag litho solids
 5. Multivariate grade estimation
 6. Estimation Postprocess
 7. QA checks
 8. Reserve Report
## 📦 Installation
In case a python distribution is not already available, the recomended distribution is [Winpython](https://winpython.github.io/) 3.8+.  
Download the installer from the link above.  
Extract into this windows special folder:  
`%APPDATA%`  
The correct path to the python executable should be similar to this example:  
`C:\Users\user\AppData\Roaming\WPy64-31131\python-3.12.3.amd64\python.exe`  
Download this entire repository as zip and extract to a valid folder.  
Windows blocks executables in protected folders (and subfolders) such as:
 - Desktop
 - Downloads
 - Documents
 - OneDrive Synced folders

Also, its not recomended to use the winpython install folder to save this script.  
So you may need to create a new valid folder directly in the C: drive. Ex.:  
`c:\scripts\geostat`
## 🎬 Run
Start jupyter Notebook or jupyter Lab.
If you dont already have a shortcut, the auxiliary script jupyter_localhost.bat is provided for easily starting jupyter on Microsoft Windows systems.
Follow the instructions provided on the notebook.
## 📓 Notes
## 📚 Examples
### db checks
![screenshot2](https://github.com/pemn/assets/blob/main/vtk_geostats2.png?raw=true)
### grade checks
![screenshot3](https://github.com/pemn/assets/blob/main/vtk_geostats3.png?raw=true)
### grade voxel view
![screenshot4](https://github.com/pemn/assets/blob/main/vtk_geostats4.png?raw=true)
### reserves calculation
![screenshot5](https://github.com/pemn/assets/blob/main/vtk_geostats5.png?raw=true)
## 🧰 Tools
 - jupyter_localhost.bat: (optional) starts jupyter
 - wf01_main.ipynb: notebook with the complete workflow. will call the other tools which should be on the same folder.
 - db_assay_runlength.py: helper script for sample compositing
 - db_linear_model.py: default linear regressor using scikit
## 🙋 Support
Any question or problem contact:
 - paulo.ernesto
## 💎 License
Apache 2.0  
Copyright ![vale_logo_only](https://github.com/pemn/assets/blob/main/vale_logo_only_r.svg?raw=true) Vale 2023
