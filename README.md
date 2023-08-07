## AutoWxs

This script generates an XML file in WiX Toolset format for creating an MSI package installer. The WiX Toolset is a set of tools that allow you to create Windows Installer (MSI) packages for software installation.

### Purpose

The script aims to automate the process of generating the XML structure required for creating an MSI installer package. It walks through a specified directory, identifies files and subdirectories, and generates the necessary XML elements for each component and directory in the structure.

### Prerequisites

To use this script, you need:

1. Python installed on your system (version 3.0 or higher).
2. Knowledge of the WiX Toolset and MSI package creation.

### Usage

1. **Run the Script:** Execute the script in a Python environment, preferably in a command-line interface.

2. **Input Details:**
   - **Package Name:** Provide a name for the package.
   - **Version:** Specify the version of the package.
   - **Owner:** Enter the name of the package owner.
   - **Path:** Provide the path to the root directory of the files you want to include in the package.

3. **Output:**
   The script will generate an XML file named "output.wxs" that contains the necessary structure for the MSI package.

### Script Overview

The script is composed of several functions:

- `generate_guid()`: Generates a unique identifier (GUID) for components.
- `sanitize_id(text)`: Sanitizes a text string to create valid XML identifiers.
- `generate_component(file_path, existing_ids)`: Generates XML for a file component.
- `generate_directory(path, indent="", existing_ids=None)`: Generates XML for a directory and its components.
- `__main__`: The main part of the script where user inputs are collected, and the XML output is generated.

### Output XML Structure

The generated XML output follows the WiX Toolset schema and includes the package details, directories, components, and component references necessary for creating an MSI package.

### Customization

You can customize the generated XML by modifying the script's structure, adding additional attributes, or adjusting the generated XML elements to fit your specific requirements.

### Note

- The script generates a unique ID for each file and directory by sanitizing their names. It also handles scenarios where multiple files or directories have the same name.
- The script assumes that the files and directories are located in the specified path and its subdirectories.

### Disclaimer

The script provided is a simplified example, and it's recommended to review and adapt it based on your project's requirements and WiX Toolset's capabilities.

Remember that generating MSI packages involves understanding how Windows Installer works, the WiX Toolset's documentation, and best practices for software deployment on Windows systems.
