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

"""Python binding for the hidapi library.

pyhidapi is a Python binding for the hidapi library, which provides a
platform-independent interface to USB Human Interface Device (HID)
hardware from user programs. The hidapi library itself is an external
dependency and is not included in the pyhidapi package. The hidapi
library may be found here:

    https://github.com/signal11/hidapi

Users of this module must call hid_init() before calling any other
functions defined by the module.

On the Mac, if the hidapi library is installed under /usr/local/lib,
it may be necessary to set the DYLD_LIBRARY_PATH environment variable
to '/usr/local/lib' so that find_library() will search there.

Public classes defined by this module:

    hid_device_info

Public functions defined by this module:

    hid_close(device)
    hid_enumerate(vendor_id=0, product_id=0)
    hid_error(device)
    hid_exit()
    hid_get_feature_report(device, data)
    hid_get_indexed_string(device, string_index)
    hid_get_manufacturer_string(device)
    hid_get_product_string(device)
    hid_get_serial_number_string(device)
    hid_init()
    hid_lib_path()
    hid_open(vendor_id, product_id, serial_number=None)
    hid_open_path(path)
    hid_read(device, length)
    hid_read_timeout(device, length, milliseconds)
    hid_send_feature_report(device, data)
    hid_set_nonblocking(device, nonblock)
    hid_write(device, data)
"""


from ctypes import *
from ctypes.util import find_library
import exceptions

# Define public classes:

class hid_device_info(object):
    """Describes an HID device found by hid_enumerate()."""

    path                = ''
    vendor_id           = 0
    product_id          = 0
    serial_number       = unicode('')
    release_number      = 0
    manufacturer_string = unicode('')
    product_string      = unicode('')
    usage_page          = 0
    usage               = 0
    interface_number    = 0

    def __init__(self, __hid_device = None):
        """Constructor for class hid_device_info.

        __hid_device argument is for internal use by this module."""
        
        if __hid_device is not None:
            if bool(__hid_device):
                self.path                = __hid_device.path
                self.vendor_id           = __hid_device.vendor_id
                self.product_id          = __hid_device.product_id
                self.serial_number       = __hid_device.serial_number
                self.release_number      = __hid_device.release_number
                self.manufacturer_string = __hid_device.manufacturer_string
                self.product_string      = __hid_device.product_string
                self.usage_page          = __hid_device.usage_page
                self.usage               = __hid_device.usage
                self.interface_number    = __hid_device.interface_number

    def description(self):
        """Return a printable string describing the device."""

        desc = ''
        desc = desc + 'path:                "{:s}"\n'.format(self.path)
        desc = desc + 'vendor_id:           0x{:04x}\n'.format(self.vendor_id)
        desc = desc + 'product_id:          0x{:04x}\n'.format(self.product_id)
        desc = desc + 'serial_number:       "{:s}"\n'.format(self.serial_number)
        desc = desc + 'release_number:      0x{:04x}\n'.format(self.release_number)
        desc = desc + 'manufacturer_string: "{:s}"\n'.format(self.manufacturer_string)
        desc = desc + 'product_string:      "{:s}"\n'.format(self.product_string)
        desc = desc + 'usage_page:          {:d}\n'.format(self.usage_page)
        desc = desc + 'usage:               {:d}\n'.format(self.usage)
        desc = desc + 'interface_number:    {:d}\n'.format(self.interface_number)
        return desc
    


# Define types for internal use only:

class __c_hid_device_info(Structure):
    """struct hid_device_info, ctypes version. For internal use by this binding."""
    pass

__c_hid_device_info_p = POINTER(__c_hid_device_info)

__c_hid_device_info._fields_ = [('path',                c_char_p),
                                ('vendor_id',           c_ushort),
                                ('product_id',          c_ushort),
                                ('serial_number',       c_wchar_p),
                                ('release_number',      c_ushort),
                                ('manufacturer_string', c_wchar_p),
                                ('product_string',      c_wchar_p),
                                ('usage_page',          c_ushort),
                                ('usage',               c_ushort),
                                ('interface_number',    c_int),
                                ('next',                __c_hid_device_info_p)]


# Variables for internal use only:
__hidapi  = None                          # libhidapi
__libpath = ''                            # library path
__BUFSIZE = 256                           # string buffer size


# For internal use only: Load the hidapi library.
def __load_hidapi():
    """Load the hidapi library. For internal use only."""

    global __hidapi
    global __libpath

    if __hidapi is None:
        # Search for the hidapi library.
        __libpath = find_library('hidapi-hidraw')
        if __libpath is None:
            raise RuntimeError('Could not find the hidapi shared library.')

        # Load the hidapi library.
        __hidapi = CDLL(__libpath)
        assert __hidapi is not None

        # Define argument and return types for the hidapi library functions.
        __hidapi.hid_close.argtypes                     = [c_void_p]
        __hidapi.hid_enumerate.argtypes                 = [c_ushort, c_ushort]
        __hidapi.hid_enumerate.restype                  = __c_hid_device_info_p
        __hidapi.hid_error.argtypes                     = [c_void_p]
        __hidapi.hid_error.restype                      = c_wchar_p
        __hidapi.hid_free_enumeration.argtypes          = [__c_hid_device_info_p]
        __hidapi.hid_get_feature_report.argtypes        = [c_void_p, c_void_p, c_int]
        __hidapi.hid_get_indexed_string.argtypes        = [c_void_p, c_int, c_wchar_p, c_int]
        __hidapi.hid_get_manufacturer_string.argtypes   = [c_void_p, c_wchar_p, c_int]
        __hidapi.hid_get_product_string.argtypes        = [c_void_p, c_wchar_p, c_int]
        __hidapi.hid_get_serial_number_string.argtypes  = [c_void_p, c_wchar_p, c_int]
        __hidapi.hid_open.argtypes                      = [c_ushort, c_ushort, c_wchar_p]
        __hidapi.hid_open.restype                       = c_void_p
        __hidapi.hid_open_path.argtypes                 = [c_char_p]
        __hidapi.hid_open_path.restype                  = c_void_p
        __hidapi.hid_read.argtypes                      = [c_void_p, c_void_p, c_int]
        __hidapi.hid_read_timeout.argtypes              = [c_void_p, c_void_p, c_int, c_int]
        __hidapi.hid_send_feature_report.argtypes       = [c_void_p, c_void_p, c_int]
        __hidapi.hid_set_nonblocking.argtypes           = [c_void_p, c_int]
        __hidapi.hid_write.argtypes                     = [c_void_p, c_void_p, c_int]


# Define Python wrappers for hidapi library functions:

def hid_close(device):
    """Close an HID device.

    Arguments:
        device: A device handle returned by hid_open().

    Returns:
        None"""

    global __hidapi
    assert __hidapi is not None
    __hidapi.hid_close(device)


def hid_enumerate(vendor_id=0, product_id=0):
    """Enumerate the HID devices.

    This function returns a list of hid_device_info objects
    describing all of the HID devices which match vendor_id and product_id.
    If vendor_id is set to the default of 0, then any vendor matches.
    If product_id is set to the default of 0, then any product matches.
    If both are set to the default of 0, then all HID devices will be returned.

    Arguments:
        vendor_id:  The 16-bit vendor ID (VID) of devices to be enumerated.

        product_id: The 16-bit product ID (PID) of devices to be enumerated.

    Returns:
        List of hid_device_info objects, or an empty list."""

    global __hidapi
    assert __hidapi is not None

    # Init empty list of hid_device_info objects to be returned
    hid_list   = []

    # Call hid_enumerate() to get linked list of struct hid_device_info
    hid_list_p = __hidapi.hid_enumerate(vendor_id, product_id)

    # Create a Python list of hid_device_info class instances
    if bool(hid_list_p):
        dev = hid_list_p[0]
        while dev is not None:
            hid_list.append(hid_device_info(dev))
            if bool(dev.next):
                dev = dev.next[0]
            else:
                dev = None
                
    # Free library resources and return
    __hidapi.hid_free_enumeration(hid_list_p)
    return hid_list


def hid_error(device):
    """Get a string describing the last error which occurred.

    Arguments:
        device: A device handle returned by hid_open().

    Returns:
        String describing the last error that occurred, or None if no
        error has occurred."""
    
    global __hidapi
    assert __hidapi is not None
    err = __hidapi.hid_error(device)
    return err


def hid_exit():
    """Clean up hidapi library resources.

    Arguments:
        None

    Returns:
        None"""
    
    global __hidapi
    assert __hidapi is not None
    if __hidapi.hid_exit() != 0:
        raise RuntimeError('hid_exit() failed.')


def hid_get_feature_report(device, data):
    """Get a feature report from a HID device.

    Set the first byte of data[] to the Report ID of the report to be read, and
    make the size of data equal to the size of the desired report plus one more byte
    for the report ID number.

    *** This function is not adequately tested, because the author has not yet
    *** identified a device which uses feature reports with which to test the
    *** code.

    Arguments:
        device: A device handle returned by hid_open().

        data: A bytearray to be sent to the device as the feature report
              request. Set the first byte to the desired report ID, or
              0x00 if the device does not use numbered reports.

    Returns:
        Bytearray containing report from device. The first byte
        will be the report number.
        Raises RuntimeError exception if an error occurs."""
    
    global __hidapi
    assert __hidapi is not None

    buf = create_string_buffer(len(data))
    for n in range(len(data)):
        buf[n] = chr(data[n])
    num = __hidapi.hid_get_feature_report(device, buf, len(data))
    if num < 0:
        raise RuntimeError('hid_get_feature_report() failed.')
    ba = bytearray(num)
    for n in range(num):
        ba[n] = buf[n]
    return ba


def hid_get_indexed_string(device, string_index):
    """Get a string from an HID device, based on its string index.

    Arguments:
        device: A device handle returned by hid_open().

        string_index: String index number to be fetched.

    Returns:
        Requested unicode string.
        Raises RuntimeError exception if error occurs."""

    
    global __hidapi
    assert __hidapi is not None

    buf = create_unicode_buffer(__BUFSIZE)
    val = __hidapi.hid_get_indexed_string(device, string_index, buf, __BUFSIZE)
    if val == -1:
        raise RuntimeError('Error getting indexed string.')
    else:
        return buf.value


    
def hid_get_manufacturer_string(device):
    """Get the manufacturer string from an HID device.

    Arguments:
        device: A device handle returned by hid_open().

    Returns:
        Manufacturer unicode string.
        Raises RuntimeError exception if error occurs."""
    
    global __hidapi
    assert __hidapi is not None

    buf = create_unicode_buffer(__BUFSIZE)
    val = __hidapi.hid_get_manufacturer_string(device, buf, __BUFSIZE)
    if val == -1:
        raise RuntimeError('Error getting manufacturer string.')
    else:
        return buf.value


def hid_get_product_string(device):
    """Get the product string from an HID device.

    Arguments:
        device: A device handle returned by hid_open().

    Returns:
        Product unicode string.
        Raises RuntimeError exception if error occurs."""
    
    global __hidapi
    assert __hidapi is not None

    buf = create_unicode_buffer(__BUFSIZE)
    val = __hidapi.hid_get_product_string(device, buf, __BUFSIZE)
    if val == -1:
        raise RuntimeError('Error getting product string.')
    else:
        return buf.value


def hid_get_serial_number_string(device):
    """Get the serial number string from an HID device.

    Arguments:
        device: A device handle returned by hid_open().

    Returns:
        Serial number unicode string.
        Raises RuntimeError exception if error occurs."""
    
    global __hidapi
    assert __hidapi is not None

    buf = create_unicode_buffer(__BUFSIZE)
    val = __hidapi.hid_get_serial_number_string(device, buf, __BUFSIZE)
    if val == -1:
        raise RuntimeError('Error getting serial number string.')
    else:
        return buf.value



def hid_init():
    """Initialize the hidapi library.

    User code must call this function before calling any other functions
    defined by this module."""

    global __hidapi
    if __hidapi is None:
        __load_hidapi()
    assert __hidapi is not None
    if __hidapi.hid_init() != 0:
        raise RuntimeError('hid_init() failed.')


def hid_open(vendor_id, product_id, serial_number=None):
    """Open an HID device by its VID and PID.

    Specify the desired device by vendor ID (VID), product ID (PID),
    and an optional serial number.

    If serial_number is None, open the first device found with the specified
    VID and PID.

    Arguments:
        vendor_id:  The 16-bit vendor ID (VID) of the device to be opened.

        product_id: The 16-bit product ID (PID) of the device to be opened.

        serial_number: Optional serial number Unicode string.

    Returns:
        Handle to opened device.
        Raises RuntimeError exception if device cannot be opened."""

    global __hidapi
    assert __hidapi is not None
    dev = __hidapi.hid_open(vendor_id, product_id, serial_number)
    if bool(dev):
        return dev
    else:
        raise RuntimeError('Could not open device.')
    

def hid_open_path(path):
    """Open an HID device by its path name.

    The path name be determined by calling hid_enumerate(), or a
    platform-specific path name can be used (eg: /dev/hidraw0 on Linux).

    Arguments:
        path: Path name of the device to open.

    Returns:
        Handle to opened device.
        Raises RuntimeError exception if device cannot be opened."""

    global __hidapi
    assert __hidapi is not None
    dev = __hidapi.hid_open_path(path)
    if bool(dev):
        return dev
    else:
        raise RuntimeError('Could not open device.')
    

def hid_read(device, length):
    """Read an Input report from a HID device.

    Input reports are returned to the host through the INTERRUPT IN endpoint.
    The first byte will contain the Report number if the device uses numbered
    reports.

    Arguments:
        device: A device handle returned by hid_open().

        length: Number of bytes to be read. For devices with multiple reports,
                include an extra byte for the report number.

    Returns:
        bytearray containing data that was read.
        Raises RuntimeError exception if an error occurs."""

    global __hidapi
    assert __hidapi is not None

    buf = create_string_buffer(length)
    num = __hidapi.hid_read(device, buf, length)
    if num < 0:
        raise RuntimeError('hid_write() failed.')
    ba = bytearray(num)
    for n in range(num):
        ba[n] = buf[n]
    return ba


def hid_read_timeout(device, length, milliseconds):
    """Read an Input report from a HID device with timeout.

    Input reports are returned to the host through the INTERRUPT IN endpoint.
    The first byte will contain the Report number if the device uses numbered
    reports.

    Arguments:
        device: A device handle returned by hid_open().

        length: Number of bytes to be read. For devices with multiple reports,
                include an extra byte for the report number.

        milliseconds: Timeout in milliseconds, or -1 for blocking read.

    Returns:
        bytearray containing data that was read.
        If no packet was available to be read within the timeout,
        returns an empty bytearray.
        Raises RuntimeError exception if an error occurs."""

    global __hidapi
    assert __hidapi is not None

    buf = create_string_buffer(length)
    num = __hidapi.hid_read_timeout(device, buf, length, milliseconds)
    if num < 0:
        raise RuntimeError('hid_write() failed.')
    ba = bytearray(num)
    for n in range(num):
        ba[n] = buf[n]
    return ba


def hid_send_feature_report(device, data):
    """Send a Feature report to the device.

    Feature reports are sent over the Control endpoint as a Set_Report
    transfer. The first byte of data[] must contain the Report ID. For
    devices which only support a single report, this must be set to 0x00.
    The remaining bytes contain the report data. Since the Report ID is
    mandatory, calls to hid_send_feature_report() will always contain one
    more byte than the report contains. For example, if a hid report is
    16 bytes long, 17 bytes must be passed to hid_send_feature_report():
    the Report ID (or 0x00, for devices which do not use numbered reports),
    followed by the report data (16 bytes). In this example, the length
    passed in would be 17.

    *** This function is not adequately tested, because the author has not yet
    *** identified a device which uses feature reports with which to test the
    *** code.

    Arguments:
        device: A device handle returned by hid_open().

        data: A bytearray containing the data to be written.

    Returns:
        Actual number of bytes written.
        Raises RuntimeError exception if an error occurs."""
    
    global __hidapi
    assert __hidapi is not None

    buf = create_string_buffer(len(data))
    for n in range(len(data)):
        buf[n] = chr(data[n])
    num = __hidapi.hid_send_feature_report(device, buf, len(data))
    if num == -1:
        raise RuntimeError('hid_send_feature_report() failed.')
    return num


def hid_set_nonblocking(device, nonblock):
    """Set the device handle to be non-blocking.

    In non-blocking mode calls to hid_read() will return immediately with
    a value of 0 if there is no data to be read. In blocking mode,
    hid_read() will wait (block) until there is data to read before
    returning. Nonblocking can be turned on and off at any time.

    Arguments:
        device: A device handle returned by hid_open().

        nonblock: Set to True or 1 to enable nonblocking mode.
                  Set to False or 0 to disable nonblocking mode.

    Returns:
        None
        Raises RuntimeError exception if error occurs."""

    global __hidapi
    assert __hidapi is not None

    if nonblock:
        nb = 1
    else:
        nb = 0

    if __hidapi.hid_set_nonblocking(device, nb) == -1:
        raise RuntimeError('Error while changing nonblocking mode.')

    

def hid_write(device, data):
    """Write an Output report to a HID device.

    The first byte of the data argument  must contain the Report ID. For
    devices which only support a single report, this must be set to 0x00.
    The remaining bytes contain the report data. Since the Report ID is
    mandatory, calls to hid_write() will always contain one more byte
    than the report contains. For example, if a hid report is 16 bytes
    long, 17 bytes must be passed to hid_write(), the Report ID (or 0x00,
    for devices with a single report), followed by the report data (16
    bytes). In this example, the length passed in would be 17.

    hid_write() will send the data on the first OUT endpoint, if one
    exists. If it does not, it will send the data through the Control
    Endpoint (Endpoint 0).

    Arguments:
        device: A device handle returned by hid_open().

        data: A bytearray containing the data to be written.

    Returns:
        Actual number of bytes written.
        Raises RuntimeError exception if an error occurs."""
    
    global __hidapi
    assert __hidapi is not None

    buf = create_string_buffer(len(data))
    for n in range(len(data)):
        buf[n] = chr(data[n])
    num = __hidapi.hid_write(device, buf, len(data))
    if num == -1:
        raise RuntimeError('hid_write() failed.')
    return num


# Define additional convenience functions:

def hid_lib_path():
    """Return path of loaded hidapi library.

    Arguments:
        none

    Returns:
        String containing path of loaded hidapi library."""
    
    global __hidapi
    global __libpath
    assert __hidapi is not None

    return __libpath
