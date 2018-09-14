# rbfgenerator

> This project helps to generate the organized structure of Web automation testing using RobotFramework. There are two type: 1. Sample project 2. Skeleton project

## How to start

1. Requirement:

    Python 3

1. Install Robot Framework

    Refer to [Robot Installation Instructions](https://github.com/robotframework/robotframework/blob/master/INSTALL.rst)

2. Install Selenium Library

    Refer to [Selenium Library Installation Instruction](https://github.com/robotframework/Selenium2Library)


    automation#  pip install robotframework-seleniumlibrary


3. Install PYYAML


    automation#  pip install pyyaml


4. Install Webcolors

    automation#  pip install webcolors


5. Run Test

    automation#  robot -pythonpath ./Libs Tests


## Robot Framework Document


1. Refer to [Robot Framework Userguide](https://github.com/robotframework/robotframework/tree/master/doc/userguide/src)

2. Refer to [How To Write Good Test Cases](https://github.com/robotframework/HowToWriteGoodTestCases/blob/master/HowToWriteGoodTestCases.rst)

3. Refer to [Selenium2Library Doc](http://robotframework.org/Selenium2Library/Selenium2Library.html)

## Project Structure

    automation
        |- Libs                 # Library directory (defined custom python libraries here)
        |- Pages                # Contains Robot Resource that defined keywords for related pages in WebUI
        |- Resources            # Contains Another Resources file
            |- Data             # Contains Input Data files for Testcases
            |- settings.robot   # Contains global settings
        |- Tests                # Contains All Test Suite files


## PyCharm plugin:

You need to install the intellibot plugin in $automation/intellibot.zip manually (install plugin from disk) in order to support Yaml resource file.
