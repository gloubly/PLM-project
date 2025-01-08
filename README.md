## Login
* You need an username and a password both valid to acces the tool
* Pressing **Return** on the password entry is a faster alternative to clicking on `Login`

## Users Page
Some user have the admin privilege and have access to the user control panel. 
- They can:
    * Add/Delete an user
    * Promote/Downgrade an user to admin
- They can't:
    * View passwords
    * Edit email/username/passwords

## Products Page
* **Double-click** on a line in the table show the ingredients list and recipe of the product
* **Right-click** pops a menu relative to the line in the table:
    * `Edit`: a *Product* page will appear to edit the product. Warning, it will overwrite any existing one
    * `Remove`: a dialog box will appear and the item will be removed only after clicking on `OK`
    * When clicking on `Add a product`, an empty *Product* page will appear. Warning, it will overwrite any existing one

## Product Page
##### General Informations
* *Quantity* and *Price* fields only accept float numbers
* **Left-click** on *Launching Date* field pops a calendar. You can validate the chosen date by either clicking on `Validate`

##### Ingredients Table
* **Left-click** on `Add an ingredient`
* **Double-click** on a cell opens a popup for editing:
    * To save press **Return**
    * **Left-click/Double-click** anywhere close it without saving
    * All fields are editable

##### Add a product
* The version is automatically added
* No change it saved before clicking on `Add a product`
##### Edit a product
* Depending on the *Change Type* (Major, Minor or Patch) chosen, the new version is automatically changed when saving
* Restoring a previous version:
    * The "Edit fonctionalities" will be disabled to prevent editing while restoring a version
    * You can't edit any previous version before restoring it
    * Choose the version from the list above
    * clicking `Restore this version` will show a warning, if `YES` is clicked:
        * The "chosen version" replace the "current version" (saved in the history)
        * The new version is the "current version"'s with a Major change
    * **Warning**: any unsaved change on the current version won't be saved before moving it to history
* No change it saved before clicking on `Edit product`


## Stock Page
You can either view 'product' or 'ingredients' items (selected above the table).
##### Stock Management
* Expired items will appear in red in the table and athere will be a warning below the table
* **Right-click** pops a menu:
    * `Remove`: a dialog box will appear and the item will be removed only after clicking on `OK`
* **Double-click** on a cell opens a popup for editing:
    * To save press **Return**
    * **Left-click/Double-click** anywhere close it without saving
    * All fields are editable
    * *Quantity* and *Price* fields only accept float numbers
##### Add an item:
* Based on the items type selected above the table, the type (*Product* or *Ingredient*) is autommatically added
* *Quantity* and *Price* fields only accept float numbers
* **Left-click** on *Expiry Date* field pops a calendar. You can validate the chosen date by either clicking on `Validate` or **Double-click** on the date
* The item is only added after clicking on `Add Ingredient/Product`