#!/usr/bin/env python3
"""
Visual Studio Settings XML Sorter

This script parses a Visual Studio settings (.vssettings) file and sorts:
- PropertyValue tags by their 'name' attribute
- ToolsOptionsCategory tags by their 'name' attribute  
- ToolsOptionsSubCategory tags by their 'name' attribute
- Category tags by their 'name' attribute (or 'GUID' if no name)

The output is a cleanly formatted XML with the specified tags sorted alphabetically.
"""
import os
import xml.etree.ElementTree as ET
import argparse
import sys
from typing import Optional


def sort_key_for_element(element: ET.Element) -> str:
    """
    Get the sorting key for an element.
    Uses 'name' attribute if available, otherwise 'GUID', otherwise empty string.
    """
    return element.get('name', element.get('GUID', ''))


def sort_children_recursively(element: ET.Element) -> None:
    """
    Recursively sort children elements that have 'name' or 'GUID' attributes.
    Sorts PropertyValue, ToolsOptionsCategory, ToolsOptionsSubCategory, and Category tags.
    """
    # Tags we want to sort by their name/GUID attribute
    sortable_tags = {'PropertyValue', 'ToolsOptionsCategory', 'ToolsOptionsSubCategory', 'Category'}
    
    # Get children that should be sorted
    children_list = list(element)
    sortable_children = []
    other_children = []
    
    for child in children_list:
        if child.tag in sortable_tags and (child.get('name') or child.get('GUID')):
            sortable_children.append(child)
        else:
            other_children.append(child)
    
    # Sort the sortable children by their name/GUID attribute
    sortable_children.sort(key=sort_key_for_element)
    
    # Remove all children and re-add them in the correct order
    for child in children_list:
        element.remove(child)
    
    # Add non-sortable children first (to maintain structure)
    for child in other_children:
        element.append(child)
    
    # Add sorted children
    for child in sortable_children:
        element.append(child)
    
    # Recursively sort children of all elements
    for child in list(element):
        sort_children_recursively(child)


def format_xml_output(root: ET.Element) -> str:
    """
    Format XML with proper indentation.
    """
    def indent_xml(elem: ET.Element, level: int = 0) -> None:
        """Add whitespace to XML elements for pretty printing."""
        indent_str = "\t" * level
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = f"\n{indent_str}\t"
            if not elem.tail or not elem.tail.strip():
                elem.tail = f"\n{indent_str}"
            for child in elem:
                indent_xml(child, level + 1)
            if not child.tail or not child.tail.strip():
                child.tail = f"\n{indent_str}"
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = f"\n{indent_str}"
    
    indent_xml(root)
    return ET.tostring(root, encoding='unicode')


def process_settings_file(input_file: str, output_file: Optional[str] = None) -> None:
    """
    Process the Visual Studio settings file and sort the specified elements.
    
    Args:
        input_file: Path to the input .vssettings file
        output_file: Path to the output file (optional, defaults to stdout)
    """
    try:
        # Parse the XML file preserving namespaces
        ET.register_namespace('', 'http://www.w3.org/XML/1998/namespace')
        tree = ET.parse(input_file)
        root = tree.getroot()
        
        # Sort elements recursively
        sort_children_recursively(root)
        
        # Format the output (no XML declaration to maintain VS compatibility)
        xml_output = format_xml_output(root)
        
        # Write output
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(xml_output)

        print(f"Sorted settings written to: {output_file}")
            
    except ET.ParseError as e:
        print(f"Error parsing XML file: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Sort Visual Studio settings file by PropertyValue, ToolsOptionsCategory, ToolsOptionsSubCategory, and Category name attributes"
    )
    parser.add_argument(
        'input_file',
        help='Path to the input .vssettings file'
    )
    parser.add_argument(
        '-o', '--output',
        required=True,
        help='Path to the output file (required)'
    )
    
    args = parser.parse_args()

    # Verify that args.input_file is valid
    args.input_file = args.input_file.strip()
    if not args.input_file:
        print("Error: Input file must be specified", file=sys.stderr)
        sys.exit(1)
    if not args.input_file.endswith('.vssettings'):
        print("Error: Input file must be a .vssettings file", file=sys.stderr)
        sys.exit(1)
    
    # Expand paths before checking file existence
    if args.input_file.startswith('~'):
        args.input_file = os.path.expanduser(args.input_file)
    elif args.input_file.startswith('./'):
        args.input_file = os.path.abspath(args.input_file)
    
    # check that input file exists in filesystem
    if not os.path.isfile(args.input_file):
        print(f"Error: Input file '{args.input_file}' does not exist", file=sys.stderr)
        sys.exit(1)

    input_dir, input_file = os.path.split(args.input_file)
    if input_dir == "": 
        input_dir = os.getcwd()  # If no directory is specified, use current working directory

    # check the output file...
    if not args.output:
        print("Error: Output file must be specified", file=sys.stderr)
        sys.exit(1)
        
    args.output = args.output.strip()
    if not args.output:
        print("Error: Output file must be specified", file=sys.stderr)
        sys.exit(1)

    # Expand ~ if its in the output
    if args.output.startswith('~'):
        args.output = os.path.expanduser(args.output)
    elif args.output.startswith('./'):
        args.output = os.path.abspath(args.output)

    # Split path and file
    output_dir, output_file = os.path.split(args.output)
    if not(output_dir):
        output_dir = input_dir
    elif output_dir and not os.path.isdir(output_dir):
        print(f"Error: Output directory '{output_dir}' does not exist", file=sys.stderr)
        sys.exit(1)

    if output_file.endswith(".vssettings"):
        print("Error: Output file should not have a .vssettings extension", file=sys.stderr)
        sys.exit(1)

    process_settings_file(args.input_file, output_file=os.path.join(output_dir, output_file))


if __name__ == '__main__':
    main()
