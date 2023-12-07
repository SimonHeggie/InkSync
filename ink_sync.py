#!/usr/bin/env python
# coding=utf-8
#
# Copyright (C) [2023] [Simon Heggie], [simon.p.heggie@gmail.com]
# Copyright (C) [2021] [Matt Cottam (quick_export)], [mpcottam@raincloud.co.uk]
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
#
# #############################################################################
#  Quick Export - Quickly sync Inkscape svg, plain svg, and png
#  Overwrite existing file provides the syncing behavior
#  After setting the options in the main dialogue
#  Assign a shortcut in Inkscape Edit>Preferences>Interface>Keyboard to org.inkscape.simonh.ink_sync.noprefs
#  For shortcut triggered quick export
#  It does require that you have saved
#  Your svg file at least once before using (will not work on an unsaved svg)
#  Requires Inkscape 1.1+ (1.3 tested)
# #############################################################################

import inkex
from inkex import command
from pathlib import Path
from datetime import datetime
import sys
import os

def command_line_call(self):
    # Current date and time to time stamp
    timestamp = datetime.today().replace(microsecond=0)
    timestamp_suffix = str(timestamp.strftime('%Y-%m-%d-%H-%M-%S'))

    # Get output directory
    my_file_path = self.options.input_file

    # Collect export format options
    my_export_path = self.options.save_path

    # Get name of currently open Inkscape file
    my_filename = self.svg.name

    # Check to see if user has saved file at least once
    if len(my_filename) < 2:
        inkex.errormsg('Please Save Your File First')
        return

    # Build a formatted string for command line actions
    my_actions = '--actions='

    # Use the original filename without timestamp if overwrite is true
    if self.options.overwrite_existing_file == 'true':
        my_svg_export_filename_path = my_export_path + '/' + my_filename
        my_svg_plain_export_filename_path = my_export_path + '/' + my_filename.replace('.svg', '_plain.svg')
        my_png_export_filename_path = my_export_path + '/' + my_filename.replace('.svg', '.png')
        my_pdf_export_filename_path = my_export_path + '/' + my_filename.replace('.svg', '.pdf')
        my_html5_export_filename_path = my_export_path + '/' + my_filename.replace('.svg', '.html')
    else:
        my_svg_export_filename_path = my_export_path + '/' + my_filename.replace('.svg', '_' + timestamp_suffix + '.svg')
        my_svg_plain_export_filename_path = my_export_path + '/' + my_filename.replace('.svg', '_' + timestamp_suffix + '_plain.svg')
        my_png_export_filename_path = my_export_path + '/' + my_filename.replace('.svg', '_' + timestamp_suffix + '.png')
        my_pdf_export_filename_path = my_export_path + '/' + my_filename.replace('.svg', '_' + timestamp_suffix + '.pdf')
        my_html5_export_filename_path = my_export_path + '/' + my_filename.replace('.svg', '_' + timestamp_suffix + '.html')

    # Get png dpi setting
    png_dpi = self.options.png_dpi

    # Check which export file formats have been selected by user
    if self.options.export_svg_cb == 'true':
        export_svg_actions = f'export-filename:{my_svg_export_filename_path};export-do;'
        my_actions = my_actions + export_svg_actions

    if self.options.export_svg_plain_cb == 'true':
        export_svg_plain_actions = f'export-filename:{my_svg_plain_export_filename_path};export-plain-svg;export-do;'
        my_actions = my_actions + export_svg_plain_actions

    if self.options.export_png_cb == 'true':
        export_png_actions = f'export-filename:{my_png_export_filename_path};export-dpi:{png_dpi};export-do;'
        my_actions = my_actions + export_png_actions

    if self.options.export_pdf_cb == 'true':
        export_pdf_actions = f'export-filename:{my_pdf_export_filename_path};export-do;'
        my_actions = my_actions + export_pdf_actions

    if self.options.export_html5_cb == 'true':
        export_html5_actions = f'export-filename:{my_html5_export_filename_path};export-do;'
        my_actions = my_actions + export_html5_actions

    # Any text to path export actions need to be at end of action list
    if self.options.export_svg_ttp_cb == 'true':
        export_svg_actions = f'export-text-to-path;export-filename:{my_svg_export_filename_path};export-do;'
        my_actions = my_actions + export_svg_actions

    if self.options.export_svg_plain_ttp_cb == 'true':
        export_svg_actions = f'export-text-to-path;export-filename:{my_svg_plain_export_filename_path};export-do;'
        my_actions = my_actions + export_svg_actions

    # Exit if no export file formats have been selected
    if my_actions == '--actions=':
        inkex.errormsg('Please Select At Least One Export Format')
        return

    # Redirect standard error to suppress warnings and errors
    original_stderr = sys.stderr
    sys.stderr = open('/dev/null', 'w')

    # Set the path for the log file to the user's home directory to avoid permission issues
    log_file_path = os.path.join(os.path.expanduser('~'), 'ink_sync_error.log')

    try:
        # Check to make sure export directory exists
        if Path(my_export_path).is_dir():
            inkex.command.inkscape(my_file_path, my_actions)
        else:
            inkex.errormsg('Please Select An Export Folder')
    except Exception as e:
        # Log the exception to a file in the user's home directory
        with open(log_file_path, "a") as log_file:
            log_file.write(f"An error occurred: {e}\n")
    finally:
        # Restore original stderr
        sys.stderr.close()
        sys.stderr = original_stderr

class InkSync(inkex.EffectExtension):
    def add_arguments(self, pars):
        pars.add_argument("--notebook_main", type=str, dest="notebook_main", default=0)

        pars.add_argument("--export_svg_cb", type=str, dest="export_svg_cb", default='true')
        pars.add_argument("--export_svg_ttp_cb", type=str, dest="export_svg_ttp_cb", default='true')

        pars.add_argument("--export_svg_plain_cb", type=str, dest="export_svg_plain_cb", default='true')
        pars.add_argument("--export_svg_plain_ttp_cb", type=str, dest="export_svg_plain_ttp_cb", default='true')

        pars.add_argument("--export_png_cb", type=str, dest="export_png_cb", default='true')
        pars.add_argument("--png_dpi", type=int, dest="png_dpi", default=96)

        pars.add_argument("--export_pdf_cb", type=str, dest="export_pdf_cb", default='true')
        pars.add_argument("--export_html5_cb", type=str, dest="export_html5_cb", default='true')

        pars.add_argument("--save_path", type=str, dest="save_path", default=str(Path.home()))
        pars.add_argument("--overwrite_existing_file", type=str, dest="overwrite_existing_file", default='false')

    def effect(self):
        command_line_call(self)

if __name__ == '__main__':
    InkSync().run()

