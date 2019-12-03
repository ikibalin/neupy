"""
Defines SpaceGoupWyckoff class. 

"""
__author__ = 'ikibalin'
__version__ = "2019_12_03"

import os
import numpy

from pycifstar import Global


from typing import List, Tuple
from cryspy.f_common.cl_item_constr import ItemConstr
from cryspy.f_common.cl_loop_constr import LoopConstr


class AtomTypeScat(ItemConstr):
    """
SpaceGroupWyckoff
====================

Data items in the ATOM_TYPE_SCAT category describe atomic
scattering information used in crystallographic structure studies.
This category is fully defined in the core CIF dictionary.


Attributes:
-----------
- neutron_magnetic_j0_A1
- neutron_magnetic_j0_a2
- neutron_magnetic_j0_B1
- neutron_magnetic_j0_b2
- neutron_magnetic_j0_C1
- neutron_magnetic_j0_c2
- neutron_magnetic_j0_D
- neutron_magnetic_j0_e
- neutron_magnetic_j2_A1
- neutron_magnetic_j2_a2
- neutron_magnetic_j2_B1
- neutron_magnetic_j2_b2 
- neutron_magnetic_j2_C1
- neutron_magnetic_j2_c2
- neutron_magnetic_j2_D
- neutron_magnetic_j2_e
- neutron_magnetic_j4_A1
- neutron_magnetic_j4_a2
- neutron_magnetic_j4_B1
- neutron_magnetic_j4_b2
- neutron_magnetic_j4_C1
- neutron_magnetic_j4_c2
- neutron_magnetic_j4_D
- neutron_magnetic_j4_e
- neutron_magnetic_j6_A1
- neutron_magnetic_j6_a2
- neutron_magnetic_j6_B1
- neutron_magnetic_j6_b2
- neutron_magnetic_j6_C1
- neutron_magnetic_j6_c2
- neutron_magnetic_j6_D
- neutron_magnetic_j6_e
- neutron_magnetic_source

Methods:
---------
- 

reference: https://www.iucr.org/__data/iucr/cifdic_html/2/cif_sym.dic/Cspace_group_Wyckoff.html
    """
    MANDATORY_ATTRIBUTE = ("coord_xyz", )
    OPTIONAL_ATTRIBUTE = ("id", "letter", "multiplicity", "site_symmetry")
    INTERNAL_ATTRIBUTE = ("full_coord_xyz", "r", "b", "full_r", "full_b")
    PREFIX = "space_group_Wyckoff"
    def __init__(self, id=None, coord_xyz=None, letter=None, multiplicity=None, site_symmetry=None):
        super(SpaceGroupWyckoff, self).__init__(mandatory_attribute=self.MANDATORY_ATTRIBUTE, 
                                                optional_attribute=self.OPTIONAL_ATTRIBUTE, 
                                                internal_attribute=self.INTERNAL_ATTRIBUTE,
                                                prefix=self.PREFIX)

        self.id = id
        self.coord_xyz = coord_xyz
        self.letter = letter
        self.multiplicity = multiplicity
        self.site_symmetry = site_symmetry
        if self.is_defined:
            self.form_object

    @property
    def id(self) -> str:
        """
An arbitrary identifier that is unique to a particular Wyckoff posi-
tion.
        """
        return getattr(self, "__id")
    @id.setter
    def id(self, x):
        if x is None:
            x_in = None
        else:
            x_in = str(x)
        setattr(self, "__id", x_in)


    @property
    def coord_xyz(self) -> str:
        """
Coordinates of one site of a Wyckoff position expressed in terms
of its fractional coordinates (x, y, z) in the unit cell. To generate
the coordinates of all sites of this Wyckoff position, it is necessary
to multiply these coordinates by the symmetry operations stored in
_space_group_symop.operation_xyz.

Where no value is given, the assumed value is 'x,y,z'.

Example: 
-----------
'x,1/2,0' (coordinates of Wyckoff site with 2.. symmetry)
        """
        return getattr(self, "__coord_xyz")
    @coord_xyz.setter
    def coord_xyz(self, x):
        if x is None:
            x_in = None
        else:
            x_in = str(x)
        setattr(self, "__coord_xyz", x_in)

    @property
    def full_coord_xyz(self) -> List[str]:
        return getattr(self, "__full_coord_xyz")
    

    @property
    def letter(self) -> str:
        """
The Wyckoff letter associated with this position, as given in Inter-
national Tables for Crystallography Volume A. The enumeration
value \a corresponds to the Greek letter ‘α’ used in International
Tables.

Reference: 
------------
International Tables for Crystallography (2002).
Volume A, Space-group symmetry, edited by Th. Hahn, 5th ed.
Dordrecht: Kluwer Academic Publishers.

The data value must be one of the following:
a b c d e f g h i j k l m n o p q r s t u v w x
y z 
        """
        return getattr(self, "__letter")
    @letter.setter
    def letter(self, x):
        if x is None:
            x_in = None
        else:
            x_in = str(x)
        setattr(self, "__letter", x_in)


    @property
    def multiplicity(self) -> int:
        """
The multiplicity of this Wyckoff position as given in International
Tables Volume A. It is the number of equivalent sites per conven-
tional unit cell.

Reference:
------------
International Tables for Crystallography (2002).
Volume A, Space-group symmetry, edited by Th. Hahn, 5th ed.
Dordrecht: Kluwer Academic Publishers.
        """
        return getattr(self, "__multiplicity")
    @multiplicity.setter
    def multiplicity(self, x):
        if x is None:
            x_in = None
        else:
            x_in = int(x)
        setattr(self, "__multiplicity", x_in)


    @property
    def site_symmetry(self) -> str:
        """
The subgroup of the space group that leaves the point fixed. It is
isomorphic to a subgroup of the point group of the space group.
The site-symmetry symbol indicates the symmetry in the symme-
try direction determined by the Hermann–Mauguin symbol of the
space group (see International Tables for Crystallography Volume
A, Section 2.2.12).

Reference: 
-------------
International Tables for Crystallography (2002).
Volume A, Space-group symmetry, edited by Th. Hahn, 5th ed.
Dordrecht: Kluwer Academic Publishers.

Examples: 
------------
‘2.22’ (position 2b in space group No. 94, P4 2 2 1 2), ‘42.2’ (position 6b in space
group No. 222, Pn ¯ 3n), ‘2..’ (Site symmetry for the Wyckoff position 96f in space group No.
228, Fd ¯ 3c. The site-symmetry group is isomorphic to the point group 2 with the twofold axis
along one of the 100 directions.).

        """
        return getattr(self, "__site_symmetry")
    @site_symmetry.setter
    def site_symmetry(self, x):
        if x is None:
            x_in = None
        else:
            x_in = str(x)
        setattr(self, "__site_symmetry", x_in)

    
    @property
    def sg_id(self):
        """
A child of _space_group.id allowing the Wyckoff position to be
identified with a particular space group.
        """
        return getattr(self, "__sg_id")
    @sg_id.setter
    def sg_id(self, x):
        if x is None:
            x_in = None
        else:
            x_in = int(x)
        setattr(self, "__sg_id", x_in)


    @property
    def r(self):
        return getattr(self, "__r")
    @property
    def b(self):
        return getattr(self, "__b")

    @property
    def full_r(self):
        return getattr(self, "__full_r")
    @property
    def full_b(self):
        return getattr(self, "__full_b")

    @property
    def form_object(self)->bool:
        flag = True
        coord_xyz = self.coord_xyz
        if coord_xyz is None:
            return False
        r, b = CONSTANTS_AND_FUNCTIONS.transform_string_to_r_b(coord_xyz, labels=("x", "y", "z"))
        setattr(self, "__r", r)
        setattr(self, "__b", b)
        full_coord_xyz = self.full_coord_xyz
        if full_coord_xyz is not None:
            full_r, full_b = [], []
            for _coord_xyz in full_coord_xyz:
                r, b = CONSTANTS_AND_FUNCTIONS.transform_string_to_r_b(_coord_xyz, labels=("x", "y", "z"))
                full_r.append(r)
                full_b.append(b)
            setattr(self, "__full_r", full_r)
            setattr(self, "__full_b", full_b)
        return flag


    def is_valid_for_fract(self, fract_x:float, fract_y:float, fract_z:float, tol=10**-5) -> bool:
        flag = True
        nval = int(tol**-1)
        xyz = numpy.array([Fraction(fract_x).limit_denominator(nval), 
                           Fraction(fract_y).limit_denominator(nval), 
                           Fraction(fract_z).limit_denominator(nval)], dtype=Fraction)
        zeros = numpy.array([Fraction(0, 1), Fraction(0, 1), Fraction(0, 1)], dtype=Fraction)
        flag = [all(zeros == (CONSTANTS_AND_FUNCTIONS.mult_matrix_vector(r, xyz) + b - xyz)%1) for r, b in zip(self.full_r, self.full_b)]
        return any(flag)



class SpaceGroupWyckoffL(LoopConstr):
    """
SpaceGroupWyckoffL
====================

Contains information about Wyckoff positions of a space group.
Only one site can be given for each special position but the
remainder can be generated by applying the symmetry operations
stored in _space_group_symop.operation_xyz.

Description in cif file:
-------------------------

loop_
_space_group_Wyckoff.id
_space_group_Wyckoff.multiplicity
_space_group_Wyckoff.letter
_space_group_Wyckoff.site_symmetry
_space_group_Wyckoff.coord_xyz
   1  192   h   1      x,y,z
   2   96   g   ..2    1/4,y,-y
   3   96   f   2..    x,1/8,1/8
   4   32   b   .32    1/4,1/4,1/4

Attributes:
-----------
- id
- coord_xyz
- letter
- multiplicity
- site_symmetry


Mandatory attribute: 
---------------------
 - id (category key, 1st)
 - coord_xyz

Optional attribute: 
---------------------
 - letter
 - multiplicity
 - site_symmetry
 - sg_id


Methods:
---------
 - get_id_for_fract(fract_x, fract_y, fract_z)
 - get_letter_for_fract(fract_x, fract_y, fract_z)

reference: https://www.iucr.org/__data/iucr/cifdic_html/2/cif_sym.dic/Cspace_group_Wyckoff.html
    """
    CATEGORY_KEY = ("id", )
    ITEM_CLASS = SpaceGroupWyckoff
    def __init__(self, item = [], label=""):
        super(SpaceGroupWyckoffL, self).__init__(category_key=self.CATEGORY_KEY, item_class=self.ITEM_CLASS, label=label)
        self.item = item

    def get_id_for_fract(self, fract_x:float, fract_y:float, fract_z:float, tol=10**-5)->str:
        l_res = []
        for _item in self.item:
            if _item.is_valid_for_fract(fract_x, fract_y, fract_z, tol):
                l_res.append((_item.id, _item.multiplicity))
        out = sorted(l_res, key=lambda x: x[1])   # sort by multiplicity
        return out[0][0]

    def get_letter_for_fract(self, fract_x:float, fract_y:float, fract_z:float, tol=10**-5)->str:
        _id = self.get_id_for_fract(fract_x, fract_y, fract_z)
        res = self[_id].letter
        return res


