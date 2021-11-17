.. GMS-uploader documentation master file, created by
   sphinx-quickstart on Fri Oct  1 13:07:55 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to GMS-uploader's documentation!
========================================
GUI utility for compiling metadata and uploading sequence and metadata to the Swedish National Genomics Platform.

Features
-----------------------
* Simple and intuitive construction of metadata files
   * Should be simpler, faster and less error-prone than using e.g. MS Excel
   * Prevents errors
      * Many fields are restricted to predefined accepted values
      * Delegate functions provide allowed values in comboboxes (drop-downs)
      * Pasted data is validated before entered into the data model
   * Tries to mimic MS Excel shortcuts
   * Supports filtering and sorting of metadata
   * Use arrow-keys for moving around
   * Auto-population of fields
   * Filldown on empty cells
   * Cut-and-paste from other sources using CTRL-C, CTRL-V
   * Import metadata from CSV files
   * Paste-FX function provides method to import/paste metadata from the clipboard using custom parsers
* Generates and stores serial pseudo-id numbers for uploaded samples
* Saves, stores and uploads metadata in json format
* Saving and opening of metadata files in pickle format
* Final data validation step before upload
* Upload to different targets and different protocols
   * Supports upload via SFTP and S3
   * Upload to i.e. NGP using S3
   * Upload to other locations using SFTP


TODO
-----------------------
* Add a viewer or editor for stored pseudo_id data (csv)



.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: installation and setup:

   installation/installation_and_setup

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Creating custom import functions:

   installation/custom_import_functions


.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: usage:

   usage/workflow

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: development:

   development/code_structure
   development/contribute

