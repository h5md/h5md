.. Copyright © 2011-2013 Pierre de Buyl, Peter Colberg and Felix Höfling
   
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

Specifications for the H5MD file format version 1.0
===================================================

Objective
---------

H5MD stands for "HDF5 for molecular data". H5MD is a
specification to store molecular simulation data and is based on the `HDF5`_
file format. The primary goal is to facilitate the portability of said data
amongst scientific simulation and analysis programs.

.. _HDF5: http://www.hdfgroup.org/HDF5/


File format
-----------

A H5MD file is stored in the `HDF5 file format`_ version 0 or later.
It is recommended to store H5MD files in the HDF5 file format version 2,
which includes the implicit tracking of the creation and modification times
of the file and of each of its objects.

.. _HDF5 file format: http://www.hdfgroup.org/HDF5/doc/H5.format.html


Notation
--------

HDF5 files are organized into groups and datasets, which form a tree structure.
Attributes can be attached to each group or dataset. The following notation is
used to depict the tree or its subtrees:

``\-- item``
    An element of a group, that is either a dataset or a group. If it is a
    group itself, the elements within the group are indented by five spaces
    with respect to the group name.

``+-- attribute``
    An attribute, that relates either to a group or a dataset.

``\-- data [dim1][dim2]``
    A dataset with array dimensions ``dim1`` by ``dim2``.

``(identifier)``
    An optional element.

``<identifier>``
    An optional element with unspecified name.


General organization
--------------------

H5MD defines an organization of the HDF5 file into groups, datasets, and
attributes. A number of groups are defined at the root level of the file.
Several levels of subgroups may exist in a file, allowing the storage and
description of subsystems.

The file is allowed to possess non-specified groups, datasets or attributes that
contain additional information such as application-specific parameters or data
structures, leaving scope for future extensions. Only the ``h5md`` group is
mandatory in a H5MD file. All other root groups are optional, allowing the user
to store only relevant data. Inside each group, every group or dataset is again
optional, unless specified differently.

H5MD supports equally the storage of time-dependent and time-independent data,
i.e., data that change in the course of the simulation or that do not. The
choice between those storage types is not made explicit for the elements in the
specification, it has to be made according to the situation. For instance, the
species and mass of the particles are often fixed in time, but in chemically
reactive systems this might not be appropriate.

Time-dependent data
^^^^^^^^^^^^^^^^^^^

Time-dependent data consist of a series of samples (or frames) referring to
multiple time steps. Such data are found inside a single dataset and are
accessed via dataset slicing. In order to link the samples to the time axis of
the simulation, H5MD defines a *data group* as a group that contains, in
addition to the actual data, information on the corresponding integer time step
and on the physical time. The structure of such a group is::

    <data_group>
     \-- step [variable]
     \-- time [variable]
     \-- value [variable][...]

``step``
    A dataset with dimensions ``[variable]`` that contains the time steps
    at which the corresponding data were sampled. It is of integer data type to
    allow exact temporal matching of data from one data group to another within
    the same file.

``time``
    A dataset that is the same as the ``step`` dataset, except it is
    real-valued and contains the simulation time.

``value``
    A dataset that holds the data of the time series. Its shape is the shape
    of the stored data prepended by a ``[variable]`` dimension that allows the
    accumulation of samples. (``[variable]`` for scalars, ``[variable][D]`` for
    ``D``-dimensional vectors, etc.). The first dimension of ``value`` must match
    the unique dimension of ``step`` and ``time``, and serves to accumulate
    samples during the course of the simulation.

If several data groups are sampled at equal times, ``step`` and ``time`` of one
data group may be hard links to the ``step`` and ``time`` datasets of a
different data group. If data groups are sampled at different times (for
instance, if one needs the positions more frequently than the velocities),
``step`` and ``time`` are unique to each data group.

Time-independent data
^^^^^^^^^^^^^^^^^^^^^

Time-independent data is stored as a dataset or as an attribute.
As for the ``value`` dataset in the case of time-dependent data, data type
and array shape are implied by the stored data, where the ``[variable]``
dimension is omitted.

Storage as attributes is preferred over datasets for small amounts of data, in
particular when the size of the data is known *a priori* and does not scale with
the system size (i.e., the particle number or the simulation volume).

Storage order of arrays
^^^^^^^^^^^^^^^^^^^^^^^

All arrays are stored in C-order as enforced by the HDF5 file format (see `§
3.2.5 <http://www.hdfgroup.org/HDF5/doc/UG/12_Dataspaces.html#ProgModel>`_). A
C or C++ program may thus declare ``r[N][D]`` for the array of particle
coordinates while the Fortran program will declare a ``r(D,N)`` array
(appropriate index ordering for a system of ``N`` particles in ``D`` spatial
dimensions) and the HDF5 file will be the same.


Root level of the file
----------------------

The root of the HDF5 file holds a number of groups and is organized as
follows::

    file root
     \-- h5md
     \-- (particles)
     \-- (observables)
     \-- (parameters)

``h5md``
    A group that contains metadata and information on the file itself. It
    is the only mandatory root group.

``particles``
    An optional group that contains information on each particle in the system,
    e.g., a snapshot of the positions or the full trajectory in phase space.
    The size of stored data scales linearly with the number of particles under
    consideration.

``observables``
    An optional group that contains other quantities of interest, e.g.,
    physical observables that are derived from the system state at given points
    in time. The size of stored data is typically independent of the system size.

``parameters``
    An optional group that contains application-specific, custom data such as
    control parameters or simulation scripts.

In subsequent sections, the examples of HDF5 organization may start at the group
level, omitting the display of ``file root``.


H5MD metadata
-------------

A set of global metadata describing the file is stored in the ``h5md`` group as
attributes. The contents of the group is::

    h5md
     +-- version
     \-- author
     |    +-- name
     |    +-- (email)
     \-- creator
          +-- name
          +-- version

``version``
    An attribute that states the version of the H5MD specification that
    the file conforms to. It is an integer attribute of dimension \[2\], with the
    first element as the major version number ``1`` and the second element as the
    minor version number ``0``.

``author``
    A group that contains metadata on the person responsible for the simulation
    (or the experiment) as follows:

    ``name``
        An attribute that holds the author's real name as a string.

    ``email``
        An optional attribute that holds the author's email address as a string of
        the form ``email@domain.tld``.

``creator``
    A group that contains metadata on the program that created the file
    as follows:

    ``name``
        An attribute that stores the name of the program as a string.

    ``version``
        An attribute that yields the version of the program, as a string
        containing a proper identification for the given program.


Particles group
---------------

Information on each particle, i.e., particle trajectories, is stored in the
``particles`` group. The ``particles`` group is a container for subgroups that
represent different subsets of the system under consideration, and it may hold
one or several subgroups, as needed. These subgroups contain the trajectory
data per particle as time-dependent or time-independent data, depending on the
situation. Each subgroup contains a specification of the simulation box, see
below. For each dataset, the particle index is accommodated by the second
(first, in the case of time-independence) array dimension.

An example of contents for the ``particles`` group assuming ``N`` particles in
``D``-dimensional space is the following::

    particles
     \-- <group1>
          \-- box
          \-- position
          |    \-- value [variable][N][D]
          |    \-- step [variable]
          |    \-- time [variable]
          \-- image
          |    \-- value [variable][N][D]
          |    \-- step [variable]
          |    \-- time [variable]
          \-- species [N]
          \-- ...

The following identifiers for data groups are standardized:

``position``
    A group that describes the particle positions within the simulation
    box, as periodically wrapped or unwrapped coordinate vectors.

``image``
    A group that represents the periodic image of the box in which each
    particle is actually located and allows one to unwrap periodically wrapped
    positions. For the case of time-dependent data, the ``image/value`` dataset is
    of the same shape as ``position/value`` and is either of integer or real kind.

    For instance, given a cuboid box with periodic boundaries, let :math:`\vec
    r_i` be the reduced position of particle :math:`i` taken from ``position``,
    :math:`\vec a_i` its image vector from ``image``, and :math:`\vec L` the
    space diagonal of the box, then component :math:`j` of the extended particle
    position :math:`\vec R_i` is given by :math:`R_{ij} = r_{ij} + L_j a_{ij}`.

``velocity``
    A group that contains the velocities for each particle as a vector.

``force``
    A group that contains the total forces (i.e., the accelerations multiplied
    by the particle mass) for each particle as a vector.

``mass``
    A group that holds the mass for each particle as a scalar.

``species``
    A group that describes the species of the particles, i.e., their
    atomic or chemical identity, and is of scalar integer data type. ``species``
    is typically time-dependent if chemical reactions occur or in
    semi-grandcanonical Monte-Carlo simulations.

``id``
    A group that holds a unique scalar identifier for each particle, which is
    of integer kind.


Specification of the simulation box
-----------------------------------

The specification of the simulation box is stored in the group ``box``, which
must be contained within each of the subgroups of the ``particles`` group.
The group ``box`` must further be stored in (or hard-linked to) the
``observables`` group, if present.
Storing the box information at several places reflects the fact that all root
groups are optional (except for ``h5md``), and further that different subgroups
may be sampled at different time grids. This way, the box information remains
associated to a group of particles or the collection of observables.
A specific requirement for ``box`` groups inside ``particles`` is that the
``step`` and ``time`` datasets exactly match those of the corresponding
``position`` groups, which may be accomplished by hard-linking the datasets.

The spatial dimension and the boundary conditions of the box are stored as
attributes to the ``box`` group, e.g., ::

    particles
     \-- <group1>
          \-- box
               +-- dimension
               +-- boundary [D]
               \-- ...

``dimension``
    An attribute that stores the spatial dimension ``D`` of the
    simulation box and is of integer type.

``boundary``
    An attribute that is a string-valued array of size ``D`` that
    specifies the boundary condition of the box along each dimension.
    The elements of ``boundary`` are either ``periodic`` or ``none``.

Information on the geometry of the box edges and on the coordinate offset is
stored as attributes or as data groups, depending on whether the box is fixed
in time or not.

``edges``
    A ``D``-dimensional vector, or a ``D`` × ``D`` matrix, depending on the
    geometry of the box. If ``edges`` is a vector, it specifies the space
    diagonal of a cuboid-shaped box. If ``edges`` is a matrix, the box is of
    triclinic shape with the edge vectors given by the rows of the matrix.

``offset``
    A ``D``-dimensional vector specifying the lower coordinate
    for all directions.

For instance, a cuboid box that changes in time would appear as::

    particles
     \-- <group1>
          \-- box
               +-- dimension
               +-- boundary [D]
               \-- edges
                    \-- value [variable][D]
                    \-- step [variable]
                    \-- time [variable]
               \-- offset
                    \-- value [variable][D]
                    \-- step [variable]
                    \-- time [variable]

where ``dimension`` is equal to ``D``.
A triclinic box that is fixed in time would appear as::

    particles
     \-- <group1>
          \-- box
               +-- dimension
               +-- boundary [D]
               +-- edges [D][D]
               +-- offset [D]

where ``dimension`` is equal to ``D``.


Observables group
-----------------

Macroscopic observables, or more generally, averages over many particles, are
stored as time series in the root group ``observables``. Observables
representing only a subset of the particles may be stored in appropriate
subgroups similarly to the ``particles`` tree. Each observable is stored as a
group obeying the ``value``, ``step``, ``time`` organization outlined above.
As for all time-dependent data, the shape of ``value`` depends on the tensor
rank of the observable prepended by a ``[variable]`` dimension.  In addition,
each group may carry an optional integer attribute ``particles`` stating the
number of particles involved in the average. If this number varies, the
attribute is replaced by a dataset ``particles`` of ``[variable]`` dimension.

The contents of the observables group has the following structure::

    observables
     \-- box
     \-- <observable1>
     |    +-- (particles)
     |    \-- value [variable]
     |    \-- step [variable]
     |    \-- time [variable]
     \-- <observable2>
     |    \-- (particles) [variable]
     |    \-- value [variable][D]
     |    \-- step [variable]
     |    \-- time [variable]
     \-- <group1>
     |    \-- <observable3>
     |         +-- (particles)
     |         \-- value [variable][D][D]
     |         \-- step [variable]
     |         \-- time [variable]
     \-- ...

The following identifiers should be obeyed for the corresponding thermodynamic
observables: ``total_energy``, ``potential_energy``, ``kinetic_energy``,
``pressure``, and ``temperature``. These quantities are understood as "per
particle", i.e., they are intensive quantities in the thermodynamic limit.
(Note that ``temperature`` refers to the instantaneous temperature as obtained
from the kinetic energy, not to the thermodynamic variable.)


Parameters group
----------------

The ``parameters`` group stores application-specific, custom data such as
control parameters or simulation scripts. The group consists of groups,
datasets, and attributes. However, the detailed structure of the group is left
unspecified.

The contents of the ``parameters`` group could be the following::

    parameters
     +-- <user_attribute1>
     \-- <user_data1>
     \-- <user_group1>
     |    \-- <user_data2>
     |    \-- ...
     \-- ...

