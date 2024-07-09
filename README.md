# Fusion 360 Material Sync #

---

This Add-In provides Fusion 360 with the ability to poll an external library 
source to check for changes and reload automatically.

Fusion 360 Allows the user to interact with many cloud based features, but 
there is no core functionality to share a live material library. While the 
"Manage Materials" tool allows the user to source .adsklib files from their 
storage system, other users sourcing the same files will need to manually 
remove and reload the files to view changes.

This Add-In takes advantage of the MaterialLibraries handle provided by 
Fusion 360's Python API. When Material-Sync is loaded into the Add-In 
runtime, it starts a daemon that polls the file every 12 seconds. If the 
file's metadata shows a new modification date, Material-Sync will 
automatically remove the material library and reload it. Should a user wish 
to share a live material-library with teammates, it is best to have the 
source document saved in a shared network location or on Google Drive.

### Note: ###
Currently, the name of the shared material library is hard coded, and it 
MUST be titled "Material-Sync.adsklib"

This Add-In provides a single command located in the Utilities tab which 
allows the user to select the file path of the desired library. Once the 
user sets a file with the "Source Material Library" tool, Material-Sync will 
set the path as the polling target.