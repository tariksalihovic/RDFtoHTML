# RDF to HTML converter

The RDF to HTML converter aims to provide documentation for RDF files by generating
a more human readable version of the data.

The converter currently supports splitting all subjects of an RDF file into separate paragraphs,
each with a title, type and description. Each paragraph can then be expanded to show all data
contained in the file.

To further improve the readability, the converter also tries to download the specification
for all predicates in the file. This allows it to generate a more readable version of the predicates
as well.

The HTML files output by the converter will be HTML files with a language suffix (.en, .sv, etc.)
to allow tools such as Apache mod_negotiation to serve different languages based on the users
preferences.

## Setup
* Create a virtual environment and activate it `virtualenv venv; . venv/bin/activate`
* Run `python setup.py install` you will now have an executable named `rdf-to-html` in your path
* Or install it via PyPi `pip install rdf-to-html`

## Run

    usage: rdf-to-html [-h] [--languages LANGUAGES] [--watch] [--verbose]
                       [--log-file LOG_FILE]
                       DCAT_FILE [DCAT_FILE ...] OUTPUT_DIR

    RDF to HTML converter.

    positional arguments:
      DCAT_FILE             DCAT file
      OUTPUT_DIR            Output directory

    optional arguments:
      -h, --help            show this help message and exit
      --languages LANGUAGES
                            Languages (on ISO-369-* format) to generate separated
                            by comma (,). If omitted all encountered languages are
                            generated.
      --watch               Watch input files for changes and run the conversion
                            when a change occurs.
      --verbose             Only log critical events
      --log-file LOG_FILE   File to log to. If omitted logging will be sent to
                            stdout


### Examples
The easiest way to run the converter is to simply run in on a single file.
Which will create one HTML file for each language present in the DCAT file.

    rdf-to-html DCAT_FILE OUTPUT_DIR

If you only want to generate HTML for specific languages you can specify them as
flags to the application. If the languages specified aren't exactly the same those encountered in the DCAT file, the program will exit.
This functionallity is mainly included to avoid to generate output for DCAT files containing typos in the language tags.

    rdf-to-html --languages en,sv DCAT_FILE OUTPUT_DIR

The typical use case is to setup the script to watch for changes in one or more RDF files.
This will enable you to always have an up to date human readable version of your datafile.
To do this setup the following code to be run when the server starts.

    rdf-to-html --watch DCAT_FILE [DCAT_FILE ...] OUTPUT_DIR

**Note** The watch is bound to a specific inode, not a filename, which means that the script
will still monitor the same file if you move/rename it.

An example HTML page generated by the converter can be found [here](http://opennorth.se/datasets/dcat).

## Develop
The generated files can of course be opened manually, but for convenience
a development web server is included at `devel/webserver.py`.

Just run `python webserver.py` in the folder where you have your
generated HTML-files and you can view them in your browser `localhost:8080/YOUR_FILE`.

## CKAN extension
This repository includes code to upload data from an RDF file to CKAN in order to show metadata about datasets. The upload script will utilize the extras field in CKAN to store this data. To 
display the data nicely you should install [this](https://github.com/openumea/ckanext-rdf-to-html) extension.

To upload data to CKAN run the following command `ckan-uploader CKAN_URL API_KEY RDF_FILE`.
The `RDF_FILE` can be either a local file or a file accessible by HTTP. For the script to work you must use an `API_KEY` for a user with edit right for all the datasets you want to upload data to.

## Acknowledgements

This application was developed by [Dohi Agency](http://dohi.se/agency) in cooperation with
[Umeå Kommun](http://umea.se) in a project financed by
[Internetfonden](https://www.iis.se/vad-vi-gor/internetfonden/).
