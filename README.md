# VSSettings_Sort

A Python utility to sort Visual Studio settings files (.vssettings) for diffing purposes

## Exporting your Visual Studio Settings
- Visual Studio -> View -> Other Windows -> Command Window
- % Tools.ImportandExportSettings /export:<path_export_file>
- Verify that your backup was taken
### Resetting your settings
- WARNING - Be sure you exported and backed up your settings first!
- % Tools.ImportandExportSettings /reset
- % Tools.ImportandExportSettings /export:<path_export_vanilla_file>
### Restore your settings
- % Tools.ImportandExportSettings /import:<path_export_file>


## Overview

VSSettings_Sort is a command-line tool that parses Visual Studio settings files and sorts specific XML elements alphabetically by their `name` attributes. This makes settings files more organized, easier to read, and produces cleaner diffs when committing to version control.

## Features

- **Sorts four key element types:**
  - `PropertyValue` tags by their `name` attribute
  - `ToolsOptionsCategory` tags by their `name` attribute  
  - `ToolsOptionsSubCategory` tags by their `name` attribute
  - `Category` tags by their `name` attribute (or `GUID` if no name exists)


## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/VSSettings_Sort.git
cd VSSettings_Sort
```

## Requirements

- Python 3.6 or higher
- No external dependencies (uses Python standard library only)

## Usage

### Basic Usage

Sort a settings file and save to a new file:
```bash
python3 sort_vs_settings.py settings.vssettings -o settings_sorted.vssettings
```

### Command-line Options

```
usage: sort_vs_settings.py [-h] -o OUTPUT input_file

Sort Visual Studio settings file by PropertyValue, ToolsOptionsCategory, ToolsOptionsSubCategory, and
Category name attributes

positional arguments:
  input_file            Path to the input .vssettings file

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Path to the output file (required)
```

### Examples


**Use with Git pre-commit hooks:**
```bash
python3 sort_vs_settings.py settings.vssettings -o settings_sorted.xml
```

## How It Works

The script performs the following operations:

1. **Parses the XML** using Python's built-in `xml.etree.ElementTree`
2. **Recursively traverses** the XML tree structure
3. **Identifies sortable elements** (PropertyValue, ToolsOptionsCategory, ToolsOptionsSubCategory, Category)
4. **Sorts elements alphabetically** by their `name` or `GUID` attributes
5. **Preserves all other elements** in their original order and structure
6. **Formats the output** with proper indentation using tabs

### Before Sorting
```xml
<ToolsOptionsSubCategory name="Documents">
    <PropertyValue name="ShowMiscFilesProject">false</PropertyValue>
    <PropertyValue name="AutoloadExternalChanges">true</PropertyValue>
    <PropertyValue name="DetectFileChangesOutsideIDE">true</PropertyValue>
    <PropertyValue name="AllowEditingReadOnlyFiles">true</PropertyValue>
</ToolsOptionsSubCategory>
```

### After Sorting
```xml
<ToolsOptionsSubCategory name="Documents">
    <PropertyValue name="AllowEditingReadOnlyFiles">true</PropertyValue>
    <PropertyValue name="AutoloadExternalChanges">true</PropertyValue>
    <PropertyValue name="DetectFileChangesOutsideIDE">true</PropertyValue>
    <PropertyValue name="ShowMiscFilesProject">false</PropertyValue>
</ToolsOptionsSubCategory>
```

## Benefits

- **Version Control Friendly:** Sorted settings produce cleaner, more predictable diffs
- **Easier Navigation:** Alphabetically ordered settings are easier to find and review
- **Team Consistency:** Standardized ordering across team members' settings files
- **Visual Studio Compatible:** Output files work seamlessly with Visual Studio

## Supported Elements

The script specifically sorts these XML elements when they have a `name` or `GUID` attribute:

| Element | Sorting Attribute | Description |
|---------|------------------|-------------|
| `PropertyValue` | `name` | Individual setting values |
| `ToolsOptionsCategory` | `name` | Major setting categories (Environment, Projects, etc.) |
| `ToolsOptionsSubCategory` | `name` | Setting subcategories within major categories |
| `Category` | `name` or `GUID` | Setting categories and subcategories |

All other elements maintain their original order and structure.

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


---

**Note:** Always backup your original settings files before running any sorting operations. While this tool is designed to preserve all data, it's good practice to maintain backups of important configuration files.
