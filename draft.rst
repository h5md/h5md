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

Specifications for the H5MD file format - Draft
===============================================

Objective
---------

H5MD is aimed at becoming a specification to store molecular simulation data.
It is based on the `HDF5 <http://www.hdfgroup.org/HDF5/>`_ file format. H5MD
stands for "HDF5 for molecular data".

It should facilitate portability of said data amongst simulation and analysis
programs.

Notation
--------

The following notation is used:

* ``\-- item``: ``item`` is an element of a group. ``item`` can be a group
  itself. The elements within a group are indented by five spaces with respect
  to the group.
* ``+-- att``: ``att`` is an attribute. ``att`` can relate to a group or a
  dataset.
* ``\-- data [dim1][dim2]``: ``data`` has dimensions ``dim1`` by ``dim2``.


General organization
--------------------

H5MD defines an internal organization for an HDF5 file. A number of HDF5 groups
are defined at the root level of the file. Within the data groups, a number of
required fields exist and should possess a conforming name and shape.

Several groups of particles may exist in a file, allowing the description of several
subsystems. Multiple time steps are found inside a single HDF5 dataset. One can then
obtain either a snapshot of the system at a given time or extract a single
trajectory via dataset slicing.

The file is allowed to possess non-conforming groups that contain other
information such as simulation parameters. Only the "h5md" group is mandatory in
a H5MD file. The other data groups are optional, allowing the user to store only
relevant data. Inside each group, every dataset is again optional. Within
time-dependent groups, the "step", "time" and "value" datasets are however
mandatory as they form an important part of the specification.

The groups that are part of the H5MD specifications are

* h5md: Group containing, as attributes, information on the file itself.
* parameters: Group containing the parameters for a simulation/dataset, such as
  the spatial dimension of the system or simulation parameters.
* trajectory: Group containing the trajectory of the system (positions, ...).
* observables: Group containing all time-dependent variables in the system,
  except the ones found in the "trajectory group".

All time dependent data (whether in "trajectory" or "observables") is organized
into HDF5 groups that contain time information in addition to the data.

The root of the HDF5 file is organized as follows::

    file root
     \-- h5md
     \-- trajectory
     \-- observables
     \-- parameters

In the following, the examples of HDF5 organization may start at the group
level, omitting to display ``file root``.

Global attributes
-----------------

A few global attributes (in the HDF5 sense) are defined for convenience. These attributes are given
to the "h5md" group.

* creator: The name of the program that created the file.
* creator_version: The version of the program that created the file, as a string
  containing proper identification for the given program.
* version: The version of the H5MD specification that the file conforms
  to. "version" is a dimension \[2\] integer dataset. The first element is the
  major version number and the second element the minor version number.
* creation_time: The creation time of the file. It is an integer scalar dataset
  representing the number of seconds since the Epoch.
* author: The name of the author of the simulation/experiment. It is of the
  form "Real Name <email@domain.tld>", where the email is optional.

The content of this group is::

    h5md
     +-- creator
     +-- creator_version
     +-- version
     +-- creation_time
     +-- author


Storage of time-dependent data
------------------------------

To link time-dependent data to the time axis of the simulation, H5MD defines a
group structure containing, in addition to the data, the corresponding integer
time step information and physical time information.

The structure of such groups is ::

    data_group
     \-- value [var][...]
          +-- (unit)
     \-- step [var]
     \-- time [var]
          +-- (unit)

* The ``value`` dataset holds the actual data of the time series. Its
  dimensions depend on the type of data, ``[variable]`` for scalars and
  ``[variable][D]`` for vectors, etc.  The first dimension is variable and
  serves to accumulate samples during the course of the simulation.

* The ``step`` dataset has dimensions ``[variable]`` and contains the number of
  simulation steps (since a user-defined origin) when the corresponding data
  have been sampled. It is of integer datatype to allow exact temporal matching
  of data from one data group to another within the same file.

* The ``time`` dataset is as the ``step`` dataset, but is real-valued and
  contains the simulation time in simulation or physical units.

The first dimension of ``value`` must match the unique dimension of ``step``
and ``time``.

The datasets ``value`` and ``time`` may possess an optional string attribute
``unit`` that gives the physical unit of their respective data ("nm" for the
position, for instance).

If several data are sampled at equal times, ``step`` and ``time`` may be HDF5
hard links to the ``step`` and ``time`` datasets of a different data group. If
data are sampled at different times (for instance, one needs the positions more
frequently than the velocities), ``step`` and ``time`` are unique to each data
group.


Trajectory group
----------------

System trajectories, or more generally, time-dependent information for each
particle, are stored in the ``/trajectory`` group. The trajectory group itself
is only a container for groups that represent different subsets of the system
under consideration; it may hold one or several groups in ``/trajectory``, as
needed.  Inside of these subgroups, each kind of trajectory information is
stored in a group following the ``value``, ``step``, ``time`` scheme for
time-dependent data.

Standardized subgroups are ``position``, ``image``, ``velocity``, ``force``,
``mass``, ``species`` and ``id``.

* The ``value`` dataset in ``position``, ``image``, ``velocity``, and ``force``
  has dimensions ``[variable][N][D]``.

* The group ``position`` describes the particle positions within the (possibly
  periodic) simulation box.

* The ``image`` group represents the periodic image of the box in which each
  particle is actually located and allows one to unwrap periodically reduced
  positions. The ``image/value`` dataset is of the same shape as
  ``position/value`` and can be either of integer or real kind.

  Example: for a cuboid box with periodic boundaries, let :math:`\vec r_i` be
  the reduced position of particle :math:`i` taken from ``position``,
  :math:`\vec a_i` its image vector from ``image``, and :math:`\vec L` the
  space diagonal of the box, then component :math:`j` of the extended particle
  position is given by :math:`R_{ij} = r_{ij} + L_j a_{ij}`.

* The ``velocity`` and ``force`` groups contain the velocities and total forces
  (i.e., the accelerations multiplied by the particle mass) for each particle.

* The ``mass`` group holds the mass for each particle. Its ``value`` dataset
  has dimensions ``[N]`` if the masses do not change with time, or dimensions
  ``[variable][N]`` else.

* The ``species`` group describes the species of the particles, i.e., their
  atomic or chemical identity, and is of an integer datatype. Its ``value``
  dataset has dimensions ``[N]`` if the species do not change, or of dimensions
  ``[variable][N]`` if the species may change in the course of time, e.g., if
  chemical reactions occur or in semi-grandcanonical Monte-Carlo simulations.
  Also, as the species may change less often than other variables, if the
  species data is absent for a given time step, the most recent data for the
  species should be fetched instead.

* The ``id`` group holds a unique identifier for each particle, which is of
  integer kind.

All arrays are stored in C-order as enforced by the HDF5 file format (see `§
3.2.5 <http://www.hdfgroup.org/HDF5/doc/UG/12_Dataspaces.html#ProgModel>`_). A C
or C++ program may thus declare r\[N\]\[D\] for the coordinates array while the
Fortran program will declare a r(D,N) array (appropriate index ordering for a
system of N atoms in D dimensions) and the HDF5 file will be the same.

The content of the trajectory group is the following::

    trajectory
     \-- group1
          \-- box
          |    +-- dimension
          |    +-- geometry
          |    +-- boundary
          |    \-- ...
          \-- position
          |    \-- value [var][N][D]
          |    \-- step [var]
          |    \-- time [var]
          \-- image
          |    \-- value [var][N][D]
          |    \-- step [var]
          |    \-- time [var]
          \-- species
          |    \-- value [var][N]
          |    \-- step [var]
          |    \-- time [var]
          \-- ...


Specification of the simulation box
-----------------------------------

The specification of the simulation box is stored in a group ``box`` inside the
``/trajectory`` group, within each of its subgroups. The group ``box`` is
further stored in (or hard-linked to) the ``/observables`` group if present.
Storing the box information at several places reflects the fact that all root
groups are optional (except for ``/h5md``), different subgroups may further be
sampled at different time grids. This way, the box information remains
associated to a group of particles or the collection of observables.

The spatial dimension, the geometry and the boundary of the box are stored as
attributes to the ``box`` group, e.g., ::

    trajectory
     \-- group1
          \-- box
          |    +-- dimension
          |    +-- geometry
          |    +-- boundary [D]
          |    \-- ...
          \-- position
               \-- value
               \-- step
               \-- time

* The ``dimension`` attribute stores the spatial dimension ``D`` of the
  simulation box and is of integer type.

* The ``geometry`` attribute can be "cuboid" or "triclinic". Depending on this
  information, additional data is stored:

  **Cuboid box**

  + edges: A ``D``-dimensional vector specifying the space diagonal of the
    box. The box is not restricted to having the same edges in the different
    dimensions.

  + offset: A ``D``-dimensional vector specifying the lower coordinate
    for all directions.

  **Triclinic box**

  + edges: A ``D`` × ``D`` matrix with the rows specifying the edge vectors
    of the box.

  + offset: A ``D``-dimensional vector specifying the lower coordinate
    for all directions.

* The ``boundary`` attribute is a vector of length ``D`` that specifies the
  boundary of the box in each dimension. The elements of ``boundary`` can be
  either "open" or "periodic".

Time dependence
^^^^^^^^^^^^^^^

If the simulation box is fixed in time, ``edges`` and ``offset`` are stored as
attributes of the ``box`` group for all box kinds. Else, ``edges`` and
``offset`` are stored as datasets following the ``value``, ``step``, ``time``
organization.  A specific requirement for ``box`` groups inside ``/trajecory``
is that the ``step`` and ``time`` datasets must match exactly those of the
corresponding ``position`` datasets; this may be accomplished by hard linking
in the HDF5 sense.

Examples:

* A cuboid box that changes in time would appear as ::

    trajectory
     \-- group1
          \-- box
               +-- dimension
               +-- geometry
               +-- boundary
               \-- edges
                    \-- value [var][D]
                    \-- step [var]
                    \-- time [var]
               \-- offset
                    \-- value [var][D]
                    \-- step [var]
                    \-- time [var]

where ``dimension`` is equal to ``D`` and ``geometry`` is set to "cuboid".

* A fixed-in-time triclinic box would appear as ::

    trajectory
     \-- group1
          \-- box
               +-- dimension
               +-- geometry
               +-- boundary
               +-- edges [D][D]
               +-- offset [D]

where ``dimension`` is equal to ``D`` and ``geometry`` is set to "triclinic".


Observables group
-----------------

Macroscopic observables, or more generally, averages over many particles, are
stored as time series in the root group ``/observables``.  Observables
representing only a subset of the particles may be stored in appropriate
subgroups similarly to the ``/trajectory`` tree.  Each observable is stored as
a group obeying the ``value``, ``step``, ``time`` organization outlined above.
The shape of ``value`` depends on the tensor rank of the observable prepended
by a ``[variable]`` dimension allowing the accumulation of samples during the
course of time. For scalar observables, ``value`` has the shape ``[variable]``,
observables representing ``D``-dimensional vectors have shape
``[variable][D]``, and so on.  In addition, each group may carry an optional integer
attribute ``particles`` stating the number of particles involved in the
average.  If this number varies, the attribute is replaced by a dataset
``particles`` of ``[variable]`` dimension.

The following names should be obeyed for the corresponding observables:

* total_energy
* potential_energy
* kinetic_energy
* pressure
* temperature

Note that "temperature" refers to the instantaneous temperature as obtained
from the kinetic energy, not to the thermodynamic quantity.

The content of the observables group has the following structure ::

    observables
     \-- box
     |    +-- dimension
     |    +-- geometry
     |    +-- boundary
     |    \-- ...
     \-- obs1
     |    +-- (particles)
     |    \-- value [var]
     |    \-- step [var]
     |    \-- time [var]
     \-- obs2
     |    \-- (particles) [var]
     |    \-- value [var][D]
     |    \-- step [var]
     |    \-- time [var]
     \-- group1
     |    \-- obs3
     |         +-- (particles)
     |         \-- value [var][D][D]
     |         \-- step [var]
     |         \-- time [var]
     \-- ...


Parameters group
----------------

The "parameters" group stores user-defined simulation parameters.

The content of the parameters group is the following::

    parameters
     +-- user_data1
     \-- user_group1
     |    +-- user_data2
     |    \-- ...
     \-- ...

