#!/usr/bin/env python
# ----------------------------------------------------------------------------
# Copyright 2015 Nervana Systems Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ----------------------------------------------------------------------------
# pylint: skip-file


def get_compute_capability(device_id=None, verbose=False):
    """
    Query compute capability through PyCuda and check it's 5.0 (Maxwell) or
    greater.
    5.0 (GTX750 Ti) only fp32 support
    5.2 (GTX9xx series) required for fp16
    By default, check all devices and return the highest compute capability.

    Arguments:
        device_id (int): CUDA device id. Default to None, will iterate over
                         all devices if None.
        verbose (bool): prints verbose logging if True, default False.

    Returns:
        float: Zero if no GPU is found, otherwise highest compute capability.
    """
    try:
        import pycuda
        import pycuda.driver as drv
    except ImportError:
        if verbose:
            print("PyCUDA module not found")
        return 0
    try:
        drv.init()
    except pycuda._driver.RuntimeError as e:
        print("PyCUDA Runtime error: {0}".format(str(e)))
        return 0

    major_string = pycuda._driver.device_attribute.COMPUTE_CAPABILITY_MAJOR
    minor_string = pycuda._driver.device_attribute.COMPUTE_CAPABILITY_MINOR
    full_version = []
    if device_id is None:
        device_id = range(drv.Device.count())
    elif isinstance(device_id, int):
        device_id = [device_id]

    for i in device_id:
        major = drv.Device(i).get_attribute(major_string)
        minor = drv.Device(i).get_attribute(minor_string)
        full_version += [major + minor / 10.]

    if verbose:
        print "Found GPU(s) with compute capability:", full_version

    return max(full_version)


def get_device_count(verbose=False):
    """
    Query device count through PyCuda.

    Arguments:
        verbose (bool): prints verbose logging if True, default False.

    Returns:
        int: Number of GPUs available.
    """
    try:
        import pycuda
        import pycuda.driver as drv
    except ImportError:
        if verbose:
            print("PyCUDA module not found")
        return 0
    try:
        drv.init()
    except pycuda._driver.RuntimeError as e:
        print("PyCUDA Runtime error: {0}".format(str(e)))
        return 0

    count = drv.Device.count()

    if verbose:
        print "Found %d GPU(s)", count

    return count

if __name__ == '__main__':
    print get_compute_capability(verbose=False)
