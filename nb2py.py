#!/usr/bin/env python3
"""Create a python script from a jupyter notebook.

Run as:  python nb2py my_notebook.ipynb

Can also be imported as a module:
    import nb2py
    nb2py.convert('notebook.ipynb')
    nb2py.convert('notebook.ipynb', output_name='script.py')
"""
import os
import argparse
import json

# Export main functions for module use
__all__ = ['convert']


def convert(notebook_name, output_name=None):
    """ Convert the jupyter notebook to python script"""
    if output_name:
        script_name = output_name
        if not script_name.endswith('.py'):
            script_name += '.py'
    else:
        script_name = os.path.splitext(notebook_name)[0] + '.py'
    with open(notebook_name, 'r', encoding='utf-8') as f_in:
        with open(script_name, 'w', encoding='utf-8') as f_out:
            last_source = ''
            f_in = json.load(f_in)
            for cell in f_in['cells']:
                if last_source == 'code' and cell['cell_type'] == 'code':
                    # Check if this is a command cell
                    is_command_cell = 'command' in cell.get('metadata', {}).get('tags', [])
                    if not is_command_cell:
                        f_out.write('#-------------------------------\n\n')
                        
                for line in cell['source']:
                    if cell['cell_type'] == 'markdown':
                        line = '#| ' + line.lstrip()
                    elif cell['cell_type'] == 'code':
                        # Check if this is a command cell
                        is_command_cell = 'command' in cell.get('metadata', {}).get('tags', [])
                        if is_command_cell:
                            # Remove leading ! if present (from py2nb conversion)
                            stripped_line = line.lstrip()
                            if stripped_line.startswith('!'):
                                stripped_line = stripped_line[1:].lstrip()
                            line = '#! ' + stripped_line
                    line = line.rstrip() + '\n'
                    f_out.write(line)
                f_out.write('\n')
                last_source = cell['cell_type']
    
    return script_name


def parse_args():
    """Argument parsing for nb2py"""
    description = "Convert a jupyter notebook to a python script"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("notebook_name", help="name of notebok (.ipynb) to convert to script (.py)")
    parser.add_argument(
        "--output", 
        help="specify output script filename (default: notebook_name.py)")
    return parser.parse_args() 


def main():
    args = parse_args()
    script_name = convert(args.notebook_name, output_name=args.output)
    print(f"✓ Successfully converted {args.notebook_name} to {script_name}")
    return script_name


if __name__ == '__main__':
    main()
