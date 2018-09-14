
import optparse
import os
import shutil
from os import path
from os import walk
import sys
import enum
import re

CUSTOMIZED_LIB_DEFAULT_NAME = "MyCustomizedLibrary"

DIRECTORIES = ['Libs', 'Pages', 'Resources', 'Tests', "Utilities", 'Webdrivers']
DIRECTORY_PATHS = {}

DEMO_URL = "http://automationpractice.com"



def create_options_parser():
    desc = """This tool generates a template project of Robotframework for WebUI Testing."""

    parser = MyParser(description=desc)

    group1 = optparse.OptionGroup(parser, 'Test related options')
    group2 = optparse.OptionGroup(parser, 'Common options')

    group1.add_option("-l", "--libs", dest="libs",help="Name of customized library [default: %d]", default=CUSTOMIZED_LIB_DEFAULT_NAME)
    group2.add_option("-d", "--dir", dest="dir",help="Target directory for the test project [default: %d]", default=os.path.join(".","MyProject"))
    group2.add_option("-u", "--url", dest="url",help="Web App URL [default: %d]", default=DEMO_URL)
    group2.add_option("-b", "--browser", dest="browser",help="Web browser is used for testing [default: %d]", default="chrome")

    parser.add_option_group(group1)
    parser.add_option_group(group2)

    return parser

class MyParser(optparse.OptionParser):

    def format_epilog(self, formatter):
        return self.epilog
    def format_help(self, formatter=None):
        if formatter is None:
            formatter = self.formatter
        result = []
        if self.usage:
            result.append(self.get_usage() + "\n")
        if self.description:
            result.append(self.format_description(formatter) + "\n")
        result.append(self.format_option_help(formatter))
        return "".join(result)

def copy_template(src_file, des_file):
    with open(src_file, "r") as file:
        data = file.read()
        file2 = open(des_file, "w")
        file2.write(data)

def get_all_files_in_dir(dir, includes):
    files = []
    for (dirpath, dirnames, filenames) in walk(dir):
        for f in filenames:
            if includes != []:
                if os.path.splitext(f)[1] in includes:
                    files.append(os.path.join(dirpath, f))
            else:
                files.append(os.path.join(dirpath, f))
    return files


def write_on_template(filename, search_string, replace_string):

    with open(filename) as f:
        s = f.read()
        if search_string not in s:
            return

    with open(filename, 'w') as f:
        s = s.replace(search_string, replace_string)
        f.write(s)

def _clone_template_files(project_dir, lib_name):
    print("Cloning from template....")

    shutil.copytree("templates/", project_dir)

    libs_path = os.path.join(project_dir, "Libs")
    mylib_path = os.path.join(libs_path, lib_name)

    if not os.path.exists(mylib_path):
        os.makedirs(mylib_path)

    keywords_path = os.path.join(mylib_path, "keywords")

    old_keywords_path = os.path.join(libs_path, "keywords")
    old_utils_path = os.path.join(libs_path, "utilities")
    old_init_file_path = os.path.join(libs_path, "__init__.py")

    shutil.move(old_keywords_path, mylib_path)
    shutil.move(old_utils_path, mylib_path)
    shutil.move(old_init_file_path, mylib_path)


    files = get_all_files_in_dir(project_dir, ['.py', '.robot'])
    for file in files:
        write_on_template(file, "MyCustomizedLibrary", lib_name)
        write_on_template(file, "LIBRARY_PATH_TO_DEFINE", keywords_path.replace(project_dir, ""))
        write_on_template(file, "CustomizedLibraryFile", lib_name.lower())
        print("Cloning: {} ... DONE!".format(file))

def _init_library(dir, project_name, lib_name):
    print("Initalizing library ... ", end="")
    mylib_path = os.path.join(dir, lib_name)
    keywords_path = os.path.join(mylib_path, "keywords")
    old_file = os.path.join(keywords_path, "mycustomizedlibrarywords.py")
    new_file = os.path.join(keywords_path, lib_name.lower()+"keywords.py")
    os.rename(old_file, new_file)
    print("DONE!")


def _init_setting(dir, url, browser):
    print("Configuring setting .... ", end="")
    setting_file_path = os.path.join(dir, "settings.yaml")
    write_on_template(setting_file_path, DEMO_URL, url)
    write_on_template(setting_file_path, "<BROWSER>", browser)
    print("DONE!")

def main(options = None):

    parser = create_options_parser()
    (options, args) = parser.parse_args()

#1. setup options
    project_name = options.dir or sys.exit("Error: No path was defined")
    shutil.rmtree(project_name, ignore_errors=True)
    lib_name = options.libs or CUSTOMIZED_LIB_DEFAULT_NAME
    url = options.url or DEMO_URL
    browser = options.browser or "chrome"

#2. setup paths
    for dir in DIRECTORIES:
        DIRECTORY_PATHS.update({dir : os.path.join(project_name, dir)})

#3. Clone template files
    _clone_template_files(project_name, lib_name)


#4. Initialize template files
    _init_library(DIRECTORY_PATHS['Libs'], project_name, lib_name)
    # # _create_resources(DIRECTORY_PATHS['Resources'])
    # # _create_tests(DIRECTORY_PATHS['Tests'])
    _init_setting(DIRECTORY_PATHS['Resources'], url, browser)
    # _create_webdriver(DIRECTORY_PATHS['Webdrivers'], browser)

if __name__ == '__main__':
    main()
