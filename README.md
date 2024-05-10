## 📌 Description
full open source geostatistics workflow for generating a block model.  
this script integrates multiple generic tools and modules in a full process.  
the result is a complete block model in the vtk file format, that can be easily converted to other formats like csv, bmf, dm, etc.  
the target audience is geologists and other mining industry professionals or students.  
this is a proof of concept not intended for production use. most steps are placeholders which should be replaced with real tools. check notes.
the idea is to provide a common backbone for custom processes tailored for each situation.
## 📸 Screenshot
![screenshot1](https://github.com/pemn/assets/blob/main/vtk_geostats1.png?raw=true)
## 🧩 Implementation
This implementations uses a jupyter notebook. Check my other project, bm_geostat_process, for a desktop based implementation.
This geostatistics estimation process consists of the following steps:
 1. Data and parameter input
 2. Sample database preprocess
 3. Grid creation
 4. Flag litho solids
 5. Multivariate grade estimation
 6. Estimation Postprocess
 7. QA checks
 8. Reserve Report
## 📦 Installation
In the case a python distribution is not already available, the recomended distribution is [Winpython](https://winpython.github.io/) 3.8+.  
Download the installer from the link above.  
Extract into this windows special folder:  
`%APPDATA%`  
The correct path to the python executable should be similar to this example:  
`C:\Users\user\AppData\Roaming\WPy64-31131\python-3.12.3.amd64\python.exe`  
Download this entire repository as zip and extract to the notebooks subfolder in the Winpython installations. Ex.:  
`C:\Users\user\AppData\Roaming\WPy64-31230\notebooks`

## 🎬 Run
Start jupyter Notebook or jupyter Lab.
If you dont already have a shortcut, the auxiliary script jupyter_localhost.bat is provided for easily starting jupyter on Microsoft Windows systems.
Follow the instructions provided on the notebook.
## 📓 Notes
This proof of concept uses linear regression as the interpolation engine. Real products will require [Pykrig](https://geostat-framework.readthedocs.io/projects/pykrige/en/stable/index.html) or the isatis python module (isatis.py).
The reserves calculation step is also a simple pivot table placeholder. For a real reserves calculation, use a commercial software or check my other project, vtk_reserves for a open source tool.
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
