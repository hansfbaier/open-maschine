#!/usr/bin/env python
#
##########################################################################
# Copyright (C) 2014 Mark J. Blair, NF6X
#
# This file is part of pyhidapi.
#
#  pyhidapi is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  pyhidapi is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with pyhidapi.  If not, see <http://www.gnu.org/licenses/>.
##########################################################################

"""Enumerate all HID devices on the system."""

import hidapi

if __name__ == '__main__':
    hidapi.hid_init()
    
    print 'Loaded hidapi library from: {:s}\n'.format(hidapi.hid_lib_path())

    for dev in hidapi.hid_enumerate():
        print '------------------------------------------------------------'
        print dev.description()


