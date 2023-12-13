import os
import subprocess
import pip

def get_dependencies(file_path):
    """Function to extract the dependencies from a .py file"""
    with open(file_path, 'r') as file:
        dependencies = []
        for line in file:
            if line.startswith('import') or line.startswith('from'):
                # Extract the dependency name from the line
                dependency = line.split()[1].split('.')[0]
                dependencies.append(dependency)
        return dependencies

def install_dependencies(dependencies):
    """Function to install the dependencies using pip"""
    for dependency in dependencies:
        try:
            # Skip the installation if the dependency is already installed
            if dependency in [package.project_name for package in pip.get_installed_distributions()]:
                continue
            subprocess.check_call(['pip', 'install', dependency])
        except subprocess.CalledProcessError as error:
            print(f"Error installing {dependency}: {error}")

# Find all the .py files in the current directory
py_files = [file for file in os.listdir() if file.endswith('.py')]

# Find the dependencies for each .py file and install them
for py_file in py_files:
    dependencies = get_dependencies(py_file)
    install_dependencies(dependencies)
    print(f"installing {dependencies}")
