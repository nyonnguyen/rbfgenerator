import optparse
import os
import shutil
from os import path
from os import walk
import sys
import enum
import re

CUSTOMIZED_LIB_DEFAULT_NAME = "MyCustomizedLibrary"

DIRECTORIES = ['Libs', 'Pages', 'Tests/Data', 'Tests', "Utilities", 'Webdrivers']
DIRECTORY_PATHS = {}

DEMO_URL = "http://automationpractice.com"


def create_options_parser():
    desc = """This tool generates a template project of Robotframework for WebUI Testing."""

    parser = MyParser(description=desc)

    group1 = optparse.OptionGroup(parser, 'Test related options')
    group2 = optparse.OptionGroup(parser, 'Common options')

    group1.add_option("--libs", dest="libs", help="Name of customized library [default: %d]",
                      default=CUSTOMIZED_LIB_DEFAULT_NAME)
    group2.add_option("-i", "--initialize", dest="init",
                      help="Initialize a blank new RobotFramework Project [default: %d]", action="store_true",
                      default=False)
    group2.add_option("--dir", dest="dir", help="Target directory for the test project [default: %d]",
                      default=os.path.join(".", "MyProject"))
    group2.add_option("--url", dest="url", help="Web App URL [default: %d]", default=DEMO_URL)
    group2.add_option("--browser", dest="browser", help="Web browser is used for testing [default: %d]",
                      default="chrome")
    group2.add_option("-e", "--headless", dest="headless", help="Start browser with HEADLESS mode [default: %d]",
                      action="store_true", default=False)

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


def _clone_blank_files(project_dir):
    print("Generate blank project....")
    shutil.copytree("blank/", project_dir)
    print("DONE!")


def _clone_template_files(project_dir, lib_name):
    print("Cloning from template....")

    shutil.copytree("templates/", project_dir)

    libs_path = os.path.join(project_dir, "Libs")
    mylib_path = os.path.join(libs_path, lib_name)

    print(os.listdir(libs_path))
    children = os.listdir(libs_path)

    if not os.path.exists(mylib_path):
        os.makedirs(mylib_path)

    for child in children:
        old_path = os.path.join(libs_path, child)
        shutil.move(old_path, mylib_path)

    # old_keywords_path = os.path.join(libs_path, "keywords")
    # old_utils_path = os.path.join(libs_path, "utilities")
    # old_init_file_path = os.path.join(libs_path, "__init__.py")

    # shutil.move(old_keywords_path, mylib_path)
    # shutil.move(old_utils_path, mylib_path)
    # shutil.move(old_init_file_path, mylib_path)

    keywords_path = os.path.join(mylib_path, "keywords")

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
    new_file = os.path.join(keywords_path, lib_name.lower() + "keywords.py")
    os.rename(old_file, new_file)
    print("DONE!")


def _init_setting(dir, url, browser, headless):
    print("Configuring setting .... ", end="")
    setting_file_path = os.path.join(dir, "settings.yaml")
    write_on_template(setting_file_path, DEMO_URL, url)
    write_on_template(setting_file_path, "<BROWSER>", browser)
    write_on_template(setting_file_path, "<HEADLESS>", headless)
    print("DONE!")


def _generate_blank_project(project_name):
    _clone_blank_files(project_name)


def main(options=None):
    parser = create_options_parser()
    (options, args) = parser.parse_args()

    # 1. setup options
    is_blank_project = options.init or False
    project_name = options.dir or sys.exit("Error: No path was defined")
    shutil.rmtree(project_name, ignore_errors=True)

    if not is_blank_project:
        lib_name = options.libs or CUSTOMIZED_LIB_DEFAULT_NAME
        url = options.url or DEMO_URL
        browser = options.browser or "chrome"
        is_headless = options.headless or False

        # 2. setup paths
        for dir in DIRECTORIES:
            DIRECTORY_PATHS.update({dir: os.path.join(project_name, dir)})

        # 3. Clone template files
        _clone_template_files(project_name, lib_name)

        # 4. Initialize template files
        _init_library(DIRECTORY_PATHS['Libs'], project_name, lib_name)
        # # _create_resources(DIRECTORY_PATHS['Resources'])
        # # _create_tests(DIRECTORY_PATHS['Tests'])
        _init_setting(DIRECTORY_PATHS['Tests/Data'], url, browser, "True" if is_headless else "False")
        # _create_webdriver(DIRECTORY_PATHS['Webdrivers'], browser)

    # 2. Generate a blank project
    else:
        _generate_blank_project(project_name)


if __name__ == '__main__':
    main()
