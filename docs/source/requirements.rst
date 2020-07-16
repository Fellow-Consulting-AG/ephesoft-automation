===============
Requirements
===============

You need following information and documents before you can create flows

- Credentials

    - Access to MS-SQL Server
        - Server name
        - Username
        - Password
        - Source Database name (Database from which data will be transfered to M3)
        - Staging Database name (Database where data will store after transformation)

    - Access to Prefect cloud
        - Token for Prefect cloud
        - Project name

    - Access to M3
        - M3 URL
        - ION API File

    All these credential informations should be provided in **credentials.yml**


- Modules information

    For every module you want to export data from MS-SQL Server to M3 you need following information and add this to a csv file. Ideally it should be named **modules.csv**.

    - Module name (You can put any name here. This is only used to create flows)
    - Program name (This should be valid M3 program name where data will be exported)
    - Mapping excel file path (Full path for the excel file which contains the sheet used for data tranformation)
    - Sheet name (Name of the sheet which contains all the transformation information)
    - Source table name: Table name from which data will be extracted.
    - Stage table name: Table name where data will stored after transformation.

- Modules dependencies information

    You should know if a module you are exporting already depends on another module. e.g. OrderLineItems is dependent on Orders and should be transferred after Orders are transferred.
    This dependencies need to be provided in a csv file in a parent-child format, ideally named **module_dependencies.csv**