.. |cog| image:: ../../../icons/cog-outline_mdi.svg

Installation and setup
++++++++++++++++++++++
Installation instructions for GMS-uploader on Windows, Linux and Mac


Installation
^^^^^^^

**Windows**

For Windows, GMS-uploader releases are provided as a Windows installer (setup.exe), created using the `Inno Setup Compiler <https://jrsoftware.org/>`_.


* Grab the lastest release:

  https://github.com/genomic-medicine-sweden/GMS-uploader/releases

* Copy GMS-uploader to the correct location

    * If the zip file was downloaded, unpack it to a suitable location; e.g. ``<C:\Apps>``
    * If the windows installer was downloaded, run it and follow instructions provided
* Start by double-clicking the ``gms-uploader.exe`` in the GMS-uploader folder or (if properly installed) from the Windows start menu.

**Linux**

Will be added.

Setup
^^^^^^^

After GMS-uploader has been installed, the program settings need to be entered.

* Click the COG button |cog| on the sidebar to enter the settings view
* Set paths, for simple navigation:

    * ``seq_base_path`` sequence data root
    * ``csv_base_path`` where you may store csv metadata (import)
    * ``metadata_output_path`` where metadata json files will be stored before upload
    * ``metadata_docs_path`` where ``*.pkl`` metadata files can be saved to and loaded from
    * ``pseudo_id_filepath`` where the pseudo_id file is to be stored (keeping a record of used pseudo ids)
    * ``credentials_filepath`` where the credentials json file is located

* Set ``submitter`` name (your name?)
* Set ``bucket``, which hpc bucket to use on the NGP
* Set default ``seq_technology``, sequencing technology used
* Set default ``host``, what type of sample is it?
* Set default ``library_method`` to be used
* Set ``paste_fx``, custom clipboard parser function

* In the settings tab section, select allowed values for delegates when entering metadata

    * ``region``
    * ``selection_criterion``
    * ``patient_sex``
    * ``patient_details_history``
    * ``type``
    * ``patient_status``

**target**

