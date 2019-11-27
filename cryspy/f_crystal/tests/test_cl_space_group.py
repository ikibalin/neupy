import pytest
from cryspy.f_crystal.cl_space_group_new import SpaceGroup




STR_FROM_CIF_1 = """
    _space_group.IT_number             15
    _space_group.id                    1
    _space_group.Bravais_type          mS
    _space_group.Laue_class            2/m
    _space_group.Patterson_name_HM  'C 2/m'
    _space_group.centring_type         C
    _space_group.crystal_system        monoclinic
    _space_group.name_HM_ref            'C 2/c'
    _space_group.name_Hall           '-C 2yc'
    _space_group.name_Schoenflies      C2h.6
    """  # TODO: temporary test, it should be: _space_group.Patterson_name_H-M-M_ref            'C 2/m'
    #                                          _space_group.name_H-M_ref            'C 2/c'

def test_init():
    _object = SpaceGroup()
    try:
        flag = True
    except:
        flag = False
    assert flag

def test_to_cif():
    _object = SpaceGroup()
    _str = _object.to_cif()
    try:
        flag = True
    except:
        flag = False
    assert flag


def test_from_cif():
    _obj = SpaceGroup.from_cif(STR_FROM_CIF_1)
    assert _obj is not None
    assert _obj.id == "1"
    assert _obj.it_number == 15
    assert _obj.name_hm_ref == 'C 2/c'
    
    _str_1 = STR_FROM_CIF_1.replace(" ","").replace("\n","").lower()
    _str_2 = _obj.to_cif(separator=".").replace(" ","").replace("\n","").lower()
    print(_obj.to_cif(separator="."))
    assert _str_1 == _str_2 

