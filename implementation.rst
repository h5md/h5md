.. Copyright © 2013 Pierre de Buyl, Peter Colberg and Felix Höfling
   
   This file is part of H5MD.
   
   H5MD is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.
   
   H5MD is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.
   
   You should have received a copy of the GNU General Public License
   along with H5MD.  If not, see <http://www.gnu.org/licenses/>.

Implementation of the H5MD file format
======================================

While the H5MD specification is agnostic towards the software used to write and
read H5MD files, this document provides implementation hints for common HDF5
libraries.

Language-independent
^^^^^^^^^^^^^^^^^^^^

Compact datasets
----------------

For storage efficiency, small-sized time-independent data should be stored
using the compact dataset layout (see `§5.4.5
<http://www.hdfgroup.org/HDF5/doc/UG/UG_frame10Datasets.html>`_). The raw data
of a compact dataset, which may `not exceed 64 kb
<http://www.hdfgroup.org/HDF5/doc/RM/RM_H5P.html#Property-SetLayout>`_, is
stored in the header block of the dataset object.

The enum datatype for the ``species`` data
------------------------------------------

The ``species`` data group in the ``particles`` group of a H5MD file may use the
enum datatype (see `§6.5.3
<http://www.hdfgroup.org/HDF5/doc/UG/11_Datatypes.html#NonNumDtypes>`_) that is
compatible with the integer datatype. This allows to map numerical species
identifiers to a string while keeping the performance of integer data.

An enumerated-type dataset can be read using, e.g., ``H5T_NATIVE_INT`` as the
memory datatype. For writing, however, the memory datatype needs to be an
enumerated type. A program extending an existing enumerated-type dataset needs
to be aware of this.

C
^

This section describes the usage of the `HDF5 C API`_.

.. _HDF5 C API: http://www.hdfgroup.org/HDF5/doc/RM/RM_H5Front.html

.. code-block:: c

   #include <hdf5.h>

File format
-----------

The H5MD specification recommends HDF5 file format version 2. This format is
supported by HDF5 library version 1.8 or later, but needs to be enabled
explicitly when creating or opening an HDF5 file for writing.

This is achieved using the function `H5Pset_libver_bounds`_.

.. _H5Pset_libver_bounds: http://www.hdfgroup.org/HDF5/doc/RM/RM_H5P.html#Property-SetLibverBounds

.. code-block:: c

   /* Create HDF5 file with HDF5 file format version 2. */
   hid_t fapl_id = H5Pcreate(H5P_FILE_ACCESS);
   H5Pset_libver_bounds(fapl_id, H5F_LIBVER_18, H5F_LIBVER_18);
   hid_t file_id = H5Fcreate("name.h5", H5F_ACC_TRUNC, H5P_DEFAULT, fapl_id);

Compact datasets
----------------

Compact datasets are created by setting the layout property of the dataset
creation property list.

.. code-block:: c

  hid_t dcpl_id = H5Pcreate(H5P_DATASET_CREATE);
  H5Pset_layout(dcpl_id, H5D_COMPACT);
  hid_t dset_id = H5Dcreate(loc_id, "name", type_id, space_id, H5P_DEFAULT, dcpl_id, H5P_DEFAULT);

Object time tracking
--------------------

For HDF5 file format version 2 or later, the HDF5 library automatically tracks
access, modification, change, and birth time of an object, which applies to the
file, and its groups and datasets.

The function `H5Oget_info`_ may be used to query object times in seconds since
the epoch.

.. _H5Oget_info: http://www.hdfgroup.org/HDF5/doc/RM/RM_H5O.html#Object-GetInfo

.. code-block:: c

   H5O_info_t info;
   H5Oget_info(file_id, &info);
   printf("atime %ld\n", info.atime);
   printf("mtime %ld\n", info.mtime);
   printf("ctime %ld\n", info.ctime);
   printf("btime %ld\n", info.btime);

Python
^^^^^^

This section describes the usage of `HDF5 for Python`_.

.. _HDF5 for Python: http://www.h5py.org/docs/

.. code-block:: python

   import h5py

File format
-----------

The class ``h5py.File`` takes a `"libver" argument`_ to set the file format.

.. _"libver" argument: http://www.h5py.org/docs/high/file.html#version-bounding

.. code-block:: python

   f = h5py.File("name.h5", libver="18")

.. note::

   h5py up to version 2.1.3 lacks a binding for the ``H5F_LIBVER_18`` constant.

Object time tracking
--------------------

The low-level function `h5py.h5o.get_info`_ retrieves object times.

.. _h5py.h5o.get_info: http://www.h5py.org/docs/low/h5o.html#h5py.h5o.get_info

.. code-block:: python

   info = h5py.h5o.get_info(f.id)
   print(info.atime)
   print(info.mtime)
   print(info.ctime)
   print(info.btime)

.. note::

   h5py up to version 2.1.3 lacks bindings for the above mentioned ``H5O_info_t`` members.
