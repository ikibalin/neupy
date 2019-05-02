"""
define classes to describe crystal 
"""
__author__ = 'ikibalin'
__version__ = "2019_04_06"
import os
import numpy

def calc_mRmCmRT(r11, r12, r13, r21, r22, r23, r31, r32, r33,
                 c11, c12, c13, c21, c22, c23, c31, c32, c33):
    """
    calculate matrix multiplication R*C*RT, when matrices are expressed througn 
    its component and can be expressed as nD-array
    """
    rc_11, rc_12 = r11*c11+r12*c21+r13*c31, r11*c12+r12*c22+r13*c32
    rc_13 = r11*c13+r12*c23+r13*c33
    rc_21, rc_22 = r21*c11+r22*c21+r23*c31, r21*c12+r22*c22+r23*c32
    rc_23 = r21*c13+r22*c23+r23*c33
    rc_31, rc_32 = r31*c11+r32*c21+r33*c31, r31*c12+r32*c22+r33*c32
    rc_33 = r31*c13+r32*c23+r33*c33

    #dimension (atoms, symmetry)
    rcrt_11 = (rc_11*r11+rc_12*r12+rc_13*r13)
    rcrt_12 = (rc_11*r21+rc_12*r22+rc_13*r23)
    rcrt_13 = (rc_11*r31+rc_12*r32+rc_13*r33)

    rcrt_21 = (rc_21*r11+rc_22*r12+rc_23*r13)
    rcrt_22 = (rc_21*r21+rc_22*r22+rc_23*r23)
    rcrt_23 = (rc_21*r31+rc_22*r32+rc_23*r33)

    rcrt_31 = (rc_31*r11+rc_32*r12+rc_33*r13)
    rcrt_32 = (rc_31*r21+rc_32*r22+rc_33*r23)
    rcrt_33 = (rc_31*r31+rc_32*r32+rc_33*r33)
    return rcrt_11, rcrt_12, rcrt_13, rcrt_21, rcrt_22, rcrt_23, rcrt_31, rcrt_32, rcrt_33

class Cell(dict):
    """
    Cell parameters
    """
    def __init__(self, a = 1.0, b = 1.0, c = 1.0, alpha = 90.0, beta = 90.0, 
                 gamma= 90., singony = "Triclinic"):
        super(Cell, self).__init__()
        self._p_a = None
        self._p_b = None
        self._p_c = None
        self._p_alpha = None
        self._p_beta = None
        self._p_gamma = None
        self._p_singony = None
        
        self._p_cos_a = None
        self._p_cos_b = None
        self._p_cos_g = None
        self._p_cos_a_sq = None
        self._p_cos_b_sq = None
        self._p_cos_g_sq = None
        self._p_sin_a = None
        self._p_sin_b = None
        self._p_sin_g = None
        self._p_sin_a_sq = None
        self._p_sin_b_sq = None
        self._p_sin_g_sq = None
        
        self._p_ia = None
        self._p_ib = None
        self._p_ic = None
        self._p_ialpha = None
        self._p_ibeta = None
        self._p_igamma = None        

        self._p_cos_ia = None
        self._p_cos_ib = None
        self._p_cos_ig = None
        self._p_cos_ia_sq = None
        self._p_cos_ib_sq = None
        self._p_cos_ig_sq = None
        self._p_sin_ia = None
        self._p_sin_ib = None
        self._p_sin_ig = None
        self._p_sin_ia_sq = None
        self._p_sin_ib_sq = None
        self._p_sin_ig_sq = None
        
        self._p_vol = None
        self._p_ivol = None
        self._p_m_b = None
        self._p_m_ib = None

        self._refresh(a, b, c, alpha, beta, gamma, singony)
        self.set_val()
        
    def __repr__(self):
        lsout = """Cell: \n a: {:}\n b: {:}\n c: {:}\n alpha: {:}
 beta: {:}\n gamma: {:}\n singony: {:}""".format(self._p_a, self._p_b, 
                 self._p_c, self._p_alpha, self._p_beta, self._p_gamma, 
                 self._p_singony)
        return lsout
    
    def _refresh(self, a, b, c, alpha, beta, gamma, singony):
        """
        refresh variables
        """
        if a != None:
            self._p_a = a
        if b != None:
            self._p_b = b
        if c != None:
            self._p_c = c
        if alpha != None:
            self._p_alpha = alpha
        if beta != None:
            self._p_beta = beta
        if gamma != None:
            self._p_gamma = gamma
        if singony != None:
            self._p_singony = singony

        cond = any([hh != None for hh in [a, b, c, alpha, beta, gamma, 
                                          singony]])
        if cond:
            self._constr_singony()
            self._calc_cos_abc()
            self._calc_volume()
            self._calc_iucp()
            self._calc_cos_iabc()
            self._calc_m_b()
            self._calc_m_ib()
    
    def _constr_singony(self):
        singony = self._p_singony
        if singony == "Cubic":
            self._p_b = self._p_a
            self._p_c = self._p_a
            self._p_alpha = 90.
            self._p_beta = 90.
            self._p_gamma = 90.
        elif singony == "Hexagonal":
            self._p_b = self._p_a
            self._p_alpha = 90.
            self._p_beta = 90.
            self._p_gamma = 120.        
        elif singony == "Trigonal":
            self._p_b = self._p_a
            self._p_c = self._p_a
        elif singony == "Tetragonal":
            self._p_b = self._p_a
            self._p_alpha = 90.
            self._p_beta = 90.
            self._p_gamma = 90.
        elif singony == "Orthorhombic":
            self._p_alpha = 90.
            self._p_beta = 90.
            self._p_gamma = 90.
        elif singony == "Monoclinic":
            self._p_alpha = 90.
            self._p_gamma = 90.

    def set_val(self, a = None, b = None, c = None, alpha = None, 
                   beta = None, gamma= None, singony = None):
        self._refresh(a, b, c, alpha, beta, gamma, singony)


    def get_val(self, label):
        lab = "_p_"+label
        
        if lab in self.__dict__.keys():
            val = self.__dict__[lab]
            if isinstance(val, type(None)):
                self.set_val()
                val = self.__dict__[lab]
        else:
            print("The value '{:}' is not found".format(lab))
            val = None
        return val
    
    def list_vals(self):
        """
        give a list of parameters with small descripition
        """
        lsout = """
Parameters:
a, b, c - unit cell parameters in Angstrems
alpha, beta, gamma - angles in degrees

singony - singony: "Triclinic", "Monoclinic", "Orthorhombic", "Tetragonal", 
                   "Trigonal", "Hexagonal" or "Cubic"

ia, ib, ic - inverse unit cell parameters in Angstrems**-1
ialpha, ibeta, igamma - angles of inverse cell in degrees

vol - volume of unit cell in Angstrems**3
ivol - volume of inverse cell in Angstrems**3

m_b - matrix B (x is along ia, y is in (ia,ib) plane, z is vector product x, y)
m_ib - inverse B matrix 
        """
        print(lsout)
            
    def _calc_cos_abc(self):
        rad=numpy.pi/180.
        self._p_cos_a = numpy.cos(self._p_alpha*rad)
        self._p_cos_b = numpy.cos(self._p_beta*rad)
        self._p_cos_g = numpy.cos(self._p_gamma*rad)
        
        self._p_sin_a = numpy.sin(self._p_alpha*rad)
        self._p_sin_b = numpy.sin(self._p_beta*rad)
        self._p_sin_g = numpy.sin(self._p_gamma*rad)
        
        self._p_cos_a_sq = self._p_cos_a**2
        self._p_cos_b_sq = self._p_cos_b**2
        self._p_cos_g_sq = self._p_cos_g**2

        self._p_sin_a_sq = 1.-self._p_cos_a_sq
        self._p_sin_b_sq = 1.-self._p_cos_b_sq
        self._p_sin_g_sq = 1.-self._p_cos_g_sq
        
    def _calc_cos_iabc(self):
        rad=numpy.pi/180.
        self._p_cos_ia = numpy.cos(self._p_ialpha*rad)
        self._p_cos_ib = numpy.cos(self._p_ibeta*rad)
        self._p_cos_ig = numpy.cos(self._p_igamma*rad)
        
        self._p_sin_ia = numpy.sin(self._p_ialpha*rad)
        self._p_sin_ib = numpy.sin(self._p_ibeta*rad)
        self._p_sin_ig = numpy.sin(self._p_igamma*rad)
        
        self._p_cos_ia_sq = self._p_cos_ia**2
        self._p_cos_ib_sq = self._p_cos_ib**2
        self._p_cos_ig_sq = self._p_cos_ig**2

        self._p_sin_a_sq = 1.-self._p_cos_a_sq
        self._p_sin_b_sq = 1.-self._p_cos_b_sq
        self._p_sin_g_sq = 1.-self._p_cos_g_sq

    def _calc_volume(self):
        a = self._p_a
        b = self._p_b
        c = self._p_c
        c_a = self._p_cos_a
        c_b = self._p_cos_b
        c_g = self._p_cos_g
        c_a_sq = self._p_cos_a_sq
        c_b_sq = self._p_cos_b_sq
        c_g_sq = self._p_cos_g_sq
        vol = a*b*c*(1.-c_a_sq-c_b_sq-c_g_sq+2.*c_a*c_b*c_g)**0.5
        self._p_vol = vol
        
    
    def _calc_iucp(self):
        """
        calculate inverse unit cell
        """
        irad = 180./numpy.pi

        a = self._p_a
        b = self._p_b
        c = self._p_c
        c_a = self._p_cos_a
        c_b = self._p_cos_b
        c_g = self._p_cos_g
        s_a = self._p_sin_a
        s_b = self._p_sin_b
        s_g = self._p_sin_g
        vol = self._p_vol
        
        self._p_ialpha = numpy.arccos((c_b*c_g-c_a)/(s_b*s_g))*irad
        self._p_ibeta = numpy.arccos((c_g*c_a-c_b)/(s_g*s_a))*irad
        self._p_igamma = numpy.arccos((c_a*c_b-c_g)/(s_a*s_b))*irad

        self._p_ia = b*c*s_a/vol
        self._p_ib = c*a*s_b/vol
        self._p_ic = a*b*s_g/vol


    def _calc_m_b(self):
        """
        calculate matrix B 
        """
        c = self._p_c

        ia = self._p_ia 
        ib = self._p_ib 
        ic = self._p_ic 
        
        c_a = self._p_cos_a
        
        #ic_a = self._p_cos_ia 
        ic_b = self._p_cos_ib 
        ic_g = self._p_cos_ig 
        #is_a = self._p_sin_ia 
        is_b = self._p_sin_ib 
        is_g = self._p_sin_ig 
        
        self._p_m_b = numpy.array([[ia,  ib*ic_g,  ic*ic_b],
            [0.,  ib*is_g, -ic*is_b*c_a],
            [0.,       0.,  1./c]], dtype = float)

    def _calc_m_ib(self):
        """
        calculate inverse B matrix 
        """
        x1 = self._p_m_b[0,0]
        x2 = self._p_m_b[1,1]
        x3 = self._p_m_b[2,2]
        x4 = self._p_m_b[0,1]
        x5 = self._p_m_b[0,2]
        x6 = self._p_m_b[1,2]
        #B=[[x1,x4,x5],
        #   [0.,x2,x6],
        #   [0.,0.,x3]]
        #it shuld be checked
        #iB=numpy.linalg.inv(B)
        y1 = 1./x1
        y2 = 1./x2
        y3 = 1./x3
        y4 = -1*x4*1./(x1*x2)
        y6 = -1*x6*1./(x2*x3)
        y5 = (x4*x6-x2*x5)*1./(x1*x2*x3)
        
        self._p_m_ib = numpy.array([[y1,y4,y5],[0.,y2,y6],[0.,0.,y3]], 
                                   dtype = float)
            
                
        
    
    def calc_sthovl(self, h, k, l):
        """
        calculate sin(theta)/lambda for list of hkl reflections
        """
            
        a = self._p_a
        b = self._p_b
        c = self._p_c
        c_a = self._p_cos_a
        c_b = self._p_cos_b
        c_g = self._p_cos_g
        c_a_sq = self._p_cos_a_sq
        c_b_sq = self._p_cos_b_sq
        c_g_sq = self._p_cos_g_sq
        s_a_sq = self._p_sin_a_sq
        s_b_sq = self._p_sin_b_sq
        s_g_sq = self._p_sin_g_sq

        A=( 1. - c_a_sq - c_b_sq - c_g_sq + 2.*c_a*c_b*c_g)
        B1 = (s_a_sq*(h*1./a)**2+s_b_sq*(k*1./b)**2+s_g_sq*(l*1./c)**2)
        B2 = 2.*(k*l*c_a)/(b*c)+2.*(h*l*c_b)/(a*c)+2.*(h*k*c_g)/(a*b)
        #it should be checked, I am not sure
        B = B1-B2
        inv_d = (B*1./A)**0.5
        return 0.5*inv_d

    def calc_k_loc(self, h, k, l):
        """
        calculate unity scattering vector
        """
        m_b = self.get_val("m_b")
        k_x = m_b[0, 0]*h + m_b[0, 1]*k +m_b[0, 2]*l
        k_y = m_b[1, 0]*h + m_b[1, 1]*k +m_b[1, 2]*l
        k_z = m_b[2, 0]*h + m_b[2, 1]*k +m_b[2, 2]*l
        
        k_norm = (k_x**2 + k_y**2 + k_z**2)**0.5
        k_norm[k_norm == 0.] = 1.
        
        k_x = k_x/k_norm
        k_y = k_y/k_norm
        k_z = k_z/k_norm
        
        return k_x, k_y, k_z
        
    def calc_m_t(self, h, k, l):
        """define rotation matrix to have new z axis along kloc
        Rotation matrix is defined by Euler angles
        """
        m_b = self.get_val("m_b")
        k_x = m_b[0, 0]*h + m_b[0, 1]*k +m_b[0, 2]*l
        k_y = m_b[1, 0]*h + m_b[1, 1]*k +m_b[1, 2]*l
        k_z = m_b[2, 0]*h + m_b[2, 1]*k +m_b[2, 2]*l
        
        k_norm = (k_x**2 + k_y**2 + k_z**2)**0.5
        k_norm[k_norm == 0.] = 1.
        
        k_x = k_x/k_norm
        k_y = k_y/k_norm
        k_z = k_z/k_norm
        

        al = numpy.zeros(k_x.shape, dtype=float)
        
        be = numpy.arccos(k_z)
        sb = numpy.sin(be)
        flag = (sb != 0.)
        
        sa1 = k_x[flag]*1./sb[flag]
        ca2 = -1*k_y[flag]*1./sb[flag]
        sa1[sa1>1] = 1.
        sa1[sa1<-1] = -1.
            
        ca2[ca2>1] = 1.
        ca2[ca2<-1] = -1.

        al1 = numpy.arcsin(sa1)
        al2 = numpy.arccos(ca2)
        
        al_sh = numpy.copy(al1)
        al_sh[sa1 > 0.] = al2[sa1 > 0.]
        al_sh[sa1 <= 0.] = 2.*numpy.pi-al2[sa1 <= 0.]
        al_sh[numpy.abs(al2-al1)<0.00001] = al1[numpy.abs(al2-al1)<0.00001]

        al[flag] = al_sh
            
        ga=0.
        ca, cb, cg = numpy.cos(al), numpy.cos(be), numpy.cos(ga)
        sa, sb, sg = numpy.sin(al), numpy.sin(be), numpy.sin(ga)
        t_11, t_12, t_13 = ca*cg-sa*cb*sg, -ca*sg-sa*cb*cg,  sa*sb
        t_21, t_22, t_23 = sa*cg+ca*cb*sg, -sa*sg+ca*cb*cg, -ca*sb
        t_31, t_32, t_33 =          sb*sg,           sb*cg,     cb
        
        flag = (((sa*sb-k_x)**2+(-ca*sb-k_y)**2+(cb-k_z)**2)>0.0001)
        if any(flag):
            print("Mistake with k_loc")
            print("Program is stopped")
            quit()
        return t_11, t_12, t_13, t_21, t_22, t_23, t_31, t_32, t_33 
        

class SpaceGroupe(dict):
    """
    Space Groupe
    """
    def __init__(self, spgr_given_name = "P1", spgr_choice = "1",
                 f_dir_prog = os.getcwd()):
        super(SpaceGroupe, self).__init__()
        
        if isinstance(spgr_choice, float):
            spgr_choice = "{:}".format(int(spgr_choice))
        
        self._p_spgr_given_name = None
        self._p_spgr_choice = None
        self._p_f_dir_prog = None
        self._p_spgr_table = None

        self._p_centr = None
        self._p_el_symm = None
        self._p_orig = None
        self._p_p_centr = None
        self._p_spgr_name = None
        self._p_spgr_number = None

        self._p_r_11 = None
        self._p_r_12 = None
        self._p_r_13 = None
        self._p_r_21 = None
        self._p_r_22 = None
        self._p_r_23 = None
        self._p_r_31 = None
        self._p_r_32 = None
        self._p_r_33 = None

        self._p_b_1 = None
        self._p_b_2 = None
        self._p_b_3 = None

        self._refresh(spgr_given_name, spgr_choice, f_dir_prog)
        self.set_val()
        
    def __repr__(self):
        lsout = """Space group: \n name: {:}\n choiсe: {:}
 directory: '{:}'""".format(self._p_spgr_given_name, self._p_spgr_choice, 
                            self._p_f_dir_prog)
        return lsout

    def _refresh(self, spgr_given_name, spgr_choice, f_dir_prog):
        
        if not(isinstance(f_dir_prog, type(None))):
            f_itables = os.path.join(f_dir_prog,"itables.txt")
            self._read_el_cards(f_itables)        
            self._p_f_dir_prog = f_dir_prog
        if not(isinstance(spgr_given_name, type(None))):
            self._p_spgr_given_name = spgr_given_name
        if not(isinstance(spgr_choice, type(None))):
            self._p_spgr_choice = spgr_choice
            

    def set_val(self, spgr_given_name = None, spgr_choice = None,
                   f_dir_prog = None):
        self._refresh(spgr_given_name, spgr_choice, f_dir_prog)
        
        self._get_symm()
        self._calc_rotation_matrix_anb_b()
        
    def get_val(self, label):
        lab = "_p_"+label
        
        if lab in self.__dict__.keys():
            val = self.__dict__[lab]
            if isinstance(val, type(None)):
                self.set_val()
                val = self.__dict__[lab]
        else:
            print("The value '{:}' is not found".format(lab))
            val = None
        return val

    def list_vals(self):
        """
        give a list of parameters with small descripition
        """
        lsout = """
Parameters:
spgr_given_name is number or name of the space groupe
spgr_choice is choise of origin, 1, 2, "abc", "bac"
f_dir_prog is directory where the file "itables.txt" it is 

centr is inversion center
p_centr is position of inversin center
el_symm is element of symmetry
orig is packing
spgr_name is name of space groupe
spgr_number is number of space groupe

r_11, r_12, r_13  
r_21, r_22, r_23    element of symmetry in form of element of rotation matrix
r_31, r_32, r_33 

b_1, b_2,  b_3 is translation vecto for symmetry elements
        """
        print(lsout)
        
    def _read_el_cards(self, f_itables):
        """
        reading information about space grooupe from file fitables to list of cards ldcard
        Info in file fitables:
        
        1 P1               Triclinic
        choice: 1
        centr: false
        pcentr: 0, 0, 0
        symmetry: X,Y,Z
        
        2 P-1              Triclinic
        ...
        """
        fid = open(f_itables, "r")
        lcontent = fid.readlines()
        fid.close()
    
        lcontent = [hh.strip() for hh in lcontent if hh.strip() != ""]
        ldcard = []
        dcard = None
        for hh in lcontent:
            lhelp = hh.split()
            if lhelp[0].isdigit():
                if dcard != None:
                    ldcard.append(dcard)
                dcard = {"number":lhelp[0], "name": lhelp[1], "syngony": lhelp[2]}
            else:
                lhelp = hh.split(":")
                if (lhelp[0].strip() in dcard.keys()):
                    dcard[lhelp[0].strip()].append(lhelp[1].strip())
                else:
                    dcard[lhelp[0].strip()] = [lhelp[1].strip()]
        self._p_spgr_table = ldcard
        

    def _get_symm(self):
        """
        get symmetry from space group
        """
        
        spgr_choice = self._p_spgr_choice
        
        spgr_given_name = self._p_spgr_given_name
        

        if spgr_given_name.isdigit():
            spgr_n = spgr_given_name
            spgr_name = ""
        else:
            spgr_n = ""
            spgr_name = spgr_given_name
        
        spgr_table = self._p_spgr_table

        for dcard in spgr_table:
            if (((dcard["number"] == spgr_n)|(dcard["name"] == spgr_name))&(dcard["choice"][0] == spgr_choice)):
                flag = True
                break
        if (not flag):
            print("Space groupe is not found")
            return
        
        flag = False
            
        lelsymm = []
        for ssymm in dcard["symmetry"]:
            lelsymm.append(self._trans_str_to_el_symm(ssymm))
        centr = dcard["centr"][0]=="true"
        pcentr = [float(hh) for hh in dcard["pcentr"][0].split(",")]
        fletter = dcard["name"][0]
        spgr = dcard["name"]
        number = int(dcard["number"])
        if (fletter == "P"):
            lorig = [(0, 0, 0)]
        elif fletter == "C":
            lorig = [(0, 0, 0), (0.5, 0.5, 0)]
        elif fletter == "I":
            lorig = [(0, 0, 0), (0.5, 0.5, 0.5)]
        elif fletter == "F":
            lorig = [(0, 0, 0), (0.5, 0.5, 0), (0.5, 0, 0.5), (0, 0.5, 0.5)]
        elif (fletter == "R"):
            if spgr_choice == "1":
                lorig = [(0, 0, 0), (0.66667, 0.33333, 0.33333), (0.33334, 0.66666, 0.66666)]
            else:
                lorig = [(0, 0, 0)]
        else:
            print("Undefined syngony")

            
        self._p_centr = centr
        self._p_el_symm = lelsymm
        self._p_orig = lorig
        self._p_p_centr = pcentr
        self._p_spgr_name = spgr
        self._p_spgr_number = number
        
    def _calc_rotation_matrix_anb_b(self):
        """
        give representation for rotation matrix: r_11, r_22, r_33, r_12, r_13, r_23 and vector b_1, b_2, b_3
        """
        lel_symm = self._p_el_symm
        b_1 = numpy.array([hh[0] for hh in lel_symm], dtype = float)
        r_11 = numpy.array([hh[1] for hh in lel_symm], dtype = int)
        r_12 = numpy.array([hh[2] for hh in lel_symm], dtype = int)
        r_13 = numpy.array([hh[3] for hh in lel_symm], dtype = int)

        b_2 = numpy.array([hh[4] for hh in lel_symm], dtype = float)
        r_21 = numpy.array([hh[5] for hh in lel_symm], dtype = int)
        r_22 = numpy.array([hh[6] for hh in lel_symm], dtype = int)
        r_23 = numpy.array([hh[7] for hh in lel_symm], dtype = int)

        b_3 = numpy.array([hh[8] for hh in lel_symm], dtype = float)
        r_31 = numpy.array([hh[9] for hh in lel_symm], dtype = int)
        r_32 = numpy.array([hh[10] for hh in lel_symm], dtype = int)
        r_33 = numpy.array([hh[11] for hh in lel_symm], dtype = int)
        
        self._p_r_11 = r_11
        self._p_r_12 = r_12
        self._p_r_13 = r_13

        self._p_r_21 = r_21
        self._p_r_22 = r_22
        self._p_r_23 = r_23

        self._p_r_31 = r_31
        self._p_r_32 = r_32
        self._p_r_33 = r_33

        self._p_b_1 = b_1
        self._p_b_2 = b_2
        self._p_b_3 = b_3

        
        

    def calc_hkl_equiv(self, h, k, l):
        """
        give equivalent reflections of hkl and its multiplicity
        """
        
        r_11 = self._p_r_11
        r_12 = self._p_r_12
        r_13 = self._p_r_13
        r_21 = self._p_r_21
        r_22 = self._p_r_22
        r_23 = self._p_r_23
        r_31 = self._p_r_31
        r_32 = self._p_r_32
        r_33 = self._p_r_33

        h_s = r_11*h + r_21*k + r_31*l 
        k_s = r_12*h + r_22*k + r_32*l 
        l_s = r_13*h + r_23*k + r_33*l 
        
        hkl_s = numpy.vstack([h_s, k_s, l_s])
        hkl_s = numpy.hstack([hkl_s,-1*hkl_s])
        hkl_s_un = numpy.unique(hkl_s, axis=1)
        multiplicity = int(round(hkl_s.shape[1]*1./hkl_s_un.shape[1]))
        h_s, k_s, l_s = hkl_s_un[0, :], hkl_s_un[1, :], hkl_s_un[2, :]
        return h_s, k_s, l_s, multiplicity

    def calc_xyz_mult(self, x, y, z):
        """
        give unique x,y,z elements and calculate multiplicit for given x,y,z fract
        """
        r_11 = self._p_r_11
        r_12 = self._p_r_12
        r_13 = self._p_r_13
        r_21 = self._p_r_21
        r_22 = self._p_r_22
        r_23 = self._p_r_23
        r_31 = self._p_r_31
        r_32 = self._p_r_32
        r_33 = self._p_r_33
        b_1 = self._p_b_1
        b_2 = self._p_b_2
        b_3 = self._p_b_3
        
        lorig = self._p_orig
        centr = self._p_centr
        p_centr = self._p_p_centr

        x_s = numpy.round(numpy.mod(r_11*x + r_12*y + r_13*z + b_1, 1), 5)
        y_s = numpy.round(numpy.mod(r_21*x + r_22*y + r_23*z + b_2, 1), 5)
        z_s = numpy.round(numpy.mod(r_31*x + r_32*y + r_33*z + b_3, 1), 5)

        x_o = [orig[0] for orig in lorig]
        y_o = [orig[1] for orig in lorig]
        z_o = [orig[2] for orig in lorig]
        
        x_s_2d, x_o_2d = numpy.meshgrid(x_s, x_o)
        y_s_2d, y_o_2d = numpy.meshgrid(y_s, y_o)
        z_s_2d, z_o_2d = numpy.meshgrid(z_s, z_o)
        
        x_s_2d = numpy.round(numpy.mod(x_s_2d+x_o_2d, 1), 5)
        y_s_2d = numpy.round(numpy.mod(y_s_2d+y_o_2d, 1), 5)
        z_s_2d = numpy.round(numpy.mod(z_s_2d+z_o_2d, 1), 5)

        x_s = x_s_2d.flatten()
        y_s = y_s_2d.flatten()
        z_s = z_s_2d.flatten()

        if centr:
            x_s_h = numpy.round(numpy.mod(2.*p_centr[0]-1.*x_s, 1), 5)
            y_s_h = numpy.round(numpy.mod(2.*p_centr[1]-1.*y_s, 1), 5)
            z_s_h = numpy.round(numpy.mod(2.*p_centr[2]-1.*z_s, 1), 5)
            x_s =numpy.hstack([x_s, x_s_h])
            y_s =numpy.hstack([y_s, y_s_h])
            z_s =numpy.hstack([z_s, z_s_h])
                        
        xyz_s = numpy.vstack([x_s, y_s, z_s])
        
        xyz_s_un = numpy.unique(xyz_s, axis=1)
        n_atom = int(round(xyz_s.shape[1]*1./xyz_s_un.shape[1]))
        x_s, y_s, z_s = xyz_s_un[0, :], xyz_s_un[1, :], xyz_s_un[2, :]
        return x_s, y_s, z_s, n_atom
    
    
    def calc_atom_mult(self, np_x, np_y, np_z):
        """
        calculate atom multiplicity
        """
        lmult=[]
        for x, y, z in zip(np_x, np_y, np_z):
            np_x_s = self.calc_xyz_mult(x, y, z)[0]
            lmult.append(np_x_s.shape[0])
        np_multiplicity = numpy.array(lmult, dtype=int)
        
        return np_multiplicity
    
    def _trans_str_to_el_symm(self, str1):
        """
        transform string to element of symmetry: (x,y,-z) -> 0.0 1 0 0  0.0 0 1 0  0.0 0 0 -1
        """
        str2="".join(str1.split(" "))
        lhelp1,lhelp2,lhelp3=[],[],[]
        lhelp1=[hh for hh in str2.split('(') if hh!=""]
        [lhelp2.extend(hh.split(')')) for hh in lhelp1 if hh!=""]
        [lhelp3.extend(hh.split(',')) for hh in lhelp2 if hh!=""]
        lAx=['x','y','z']
        lelsymm=[]
        for hh in lhelp3:
            elsymmh=[0.0,0,0,0]
            strh=hh
            for inum,Ax in enumerate(lAx):
                if (strh.find(Ax)!=-1):
                    if (strh.find("+"+Ax)!=-1):
                        elsymmh[inum+1]=1
                        strh="".join(strh.split("+"+Ax))
                    elif (strh.find("-"+Ax)!=-1):
                        elsymmh[inum+1]=-1
                        strh="".join(strh.split("-"+Ax))
                    else:
                        elsymmh[inum+1]=1
                        strh="".join(strh.split(Ax))
            if (strh==""):
                pass
            elif (strh.find("/")!=-1):
                lhelp1=strh.split("/")
                elsymmh[0]=float(lhelp1[0])/float(lhelp1[1])
            else:
                elsymmh[0]=float(strh)
            lelsymm.append(elsymmh)
        elsymm=[]
        [elsymm.extend(hh) for hh in lelsymm]
        return elsymm



class AtomType(dict):
    """
    Description of atom
    """    
    def __init__(self, type_n="H", type_m="Fe3", flag_m=False, x=0., y=0., z=0., 
                 b_iso=0., beta_11=0., beta_22=0., beta_33=0., beta_12=0., 
                 beta_13=0., beta_23=0., chi_11=0., chi_22=0., chi_33=0., 
                 chi_12=0., chi_13=0., chi_23=0., kappa=1., factor_lande=2.,
                 occupation = 1., f_dir_prog = os.getcwd()):
        super(AtomType, self).__init__()
        
        self._p_type_n = None
        self._p_type_m = None
        self._p_flag_m = None
        self._p_x = None
        self._p_y = None
        self._p_z = None

        self._p_b_scat = None
        self._p_b_occupation = None

        self._p_b_iso = None
        self._p_beta_11 = None 
        self._p_beta_22 = None 
        self._p_beta_33 = None 
        self._p_beta_12 = None 
        self._p_beta_13 = None 
        self._p_beta_23 = None 
        self._p_chi_11 = None 
        self._p_chi_22 = None 
        self._p_chi_33 = None 
        self._p_chi_12 = None 
        self._p_chi_13 = None 
        self._p_chi_23 = None 
        self._p_kappa = None 
        self._p_factor_lande = None 

        self._p_j0_A = None 
        self._p_j0_a = None 
        self._p_j0_B = None 
        self._p_j0_b = None 
        self._p_j0_C = None 
        self._p_j0_c = None 
        self._p_j0_D = None 

        self._p_j2_A = None 
        self._p_j2_a = None 
        self._p_j2_B = None 
        self._p_j2_b = None 
        self._p_j2_C = None 
        self._p_j2_c = None 
        self._p_j2_D = None 
        self._p_f_dir_prog = None
        self._handbook_nucl = []
        self._handbook_mag = []
        
        self._refresh(type_n, type_m, flag_m, x, y, z, b_iso, beta_11, beta_22, 
                      beta_33, beta_12, beta_13, beta_23, chi_11, chi_22, 
                      chi_33, chi_12, chi_13, chi_23, kappa, factor_lande, 
                      occupation, f_dir_prog)

    def __repr__(self):
        lsout = """AtomType:
            
Type nuclear: {:} and magentic {:}({:})
b_scat: {:}
occupation: {:}
Fract  x: {:}  y: {:}  z: {:}\n b_iso: {:}, kappa: {:}, lande factor: {:}
beta_11: {:}, beta_22: {:}, beta_33: {:}, 
beta_12: {:}, beta_13: {:}, beta_23: {:}, 

chi_11: {:}, chi_22: {:}, chi_33: {:}, 
chi_12: {:}, chi_13: {:}, chi_23: {:}, 

j0 -- A: {:}, a: {:}, B: {:}, b: {:}, C: {:},  c: {:}, D: {:}
j2 -- A: {:}, a: {:}, B: {:}, b: {:}, C: {:},  c: {:}, D: {:}

f_dir_prog: {:}
""".format(self._p_type_n, self._p_type_m, self._p_flag_m, self._p_b_scat, 
self._p_occupation, self._p_x, 
self._p_y, self._p_z, self._p_b_iso, self._p_kappa, self._p_factor_lande,
self._p_beta_11, self._p_beta_22, self._p_beta_33, self._p_beta_12, 
self._p_beta_13, self._p_beta_23, self._p_chi_11, self._p_chi_22, 
self._p_chi_33, self._p_chi_12, self._p_chi_13, self._p_chi_23, self._p_j0_A,
self._p_j0_a, self._p_j0_B, self._p_j0_b, self._p_j0_C, self._p_j0_c, 
self._p_j0_D, self._p_j2_A, self._p_j2_a, self._p_j2_B, self._p_j2_b, 
self._p_j2_C, self._p_j2_c, self._p_j2_D, self._p_f_dir_prog)
        return lsout
    
    def _refresh(self, type_n, type_m, flag_m, x, y, z, b_iso, beta_11, 
                 beta_22, beta_33, beta_12, beta_13, beta_23, chi_11, chi_22, 
                 chi_33, chi_12, chi_13, chi_23, kappa, factor_lande, 
                 occupation, f_dir_prog):
        
        if not(isinstance(f_dir_prog, type(None))):
            self._p_f_dir_prog = f_dir_prog
            self._load_handbook_n()
            self._load_handbook_m()

        if not(isinstance(type_n, type(None))):
            self._p_type_n = type_n
            self._get_b_scat(type_n)
        if not(isinstance(type_m, type(None))):
            self._p_type_m = type_m
            self._get_j0j2(type_m)
        if not(isinstance(flag_m, type(None))):
            self._p_flag_m = flag_m

        if not(isinstance(x, type(None))):
            self._p_x = numpy.mod(x, 1.)
        if not(isinstance(y, type(None))):
            self._p_y = numpy.mod(y, 1.)
        if not(isinstance(z, type(None))):
            self._p_z = numpy.mod(z, 1.)
    
        if not(isinstance(b_iso, type(None))):
            self._p_b_iso = b_iso
        if not(isinstance(occupation, type(None))):
            self._p_occupation = occupation
            
        if not(isinstance(beta_11, type(None))):
            self._p_beta_11 = beta_11 
        if not(isinstance(beta_22, type(None))):
            self._p_beta_22 = beta_22 
        if not(isinstance(beta_33, type(None))):
            self._p_beta_33 = beta_33 
        if not(isinstance(beta_12, type(None))):
            self._p_beta_12 = beta_12 
        if not(isinstance(beta_13, type(None))):
            self._p_beta_13 = beta_13 
        if not(isinstance(beta_23, type(None))):
            self._p_beta_23 = beta_23 
    
            
        if not(isinstance(chi_11, type(None))):
            self._p_chi_11 = chi_11 
        if not(isinstance(chi_22, type(None))):
            self._p_chi_22 = chi_22 
        if not(isinstance(chi_33, type(None))):
            self._p_chi_33 = chi_33 
        if not(isinstance(chi_12, type(None))):
            self._p_chi_12 = chi_12 
        if not(isinstance(chi_13, type(None))):
            self._p_chi_13 = chi_13 
        if not(isinstance(chi_23, type(None))):
            self._p_chi_23 = chi_23 
            
        if not(isinstance(kappa, type(None))):
            self._p_kappa = kappa 
        if not(isinstance(factor_lande, type(None))):
            self._p_factor_lande = factor_lande 

            
    def set_val(self, type_n=None, type_m=None, flag_m=None, x=None, y=None, 
                z=None, b_iso=None, beta_11=None, beta_22=None, beta_33=None, 
                beta_12=None, beta_13=None, beta_23=None, chi_11=None, 
                chi_22=None, chi_33=None, chi_12=None, chi_13=None, 
                chi_23=None, kappa=None, factor_lande=None, occupation=None,
                f_dir_prog=None):
        self._refresh(type_n, type_m, flag_m, x, y, z, b_iso, beta_11, beta_22, 
                      beta_33, beta_12, beta_13, beta_23, chi_11, chi_22, 
                      chi_33, chi_12, chi_13, chi_23, kappa, factor_lande, 
                      occupation, f_dir_prog)
        
    def get_val(self, label):
        lab = "_p_"+label
        
        if lab in self.__dict__.keys():
            val = self.__dict__[lab]
            if isinstance(val, type(None)):
                self.set_val()
                val = self.__dict__[lab]
        else:
            print("The value '{:}' is not found".format(lab))
            val = None
        return val
            

    def list_vals(self):
        """
        give a list of parameters with small descripition
        """
        lsout = """
Parameters of AtomType:
type_n is nuclear type of atom to defince b_scat
type_m is magnetic type of atom to define magetic atom
flag_m is True if atom magnetic and False if not.

x, y, z is fraction of atom in the crystal
b_scat is scattering amplitude
occupation is occupation factor
b_iso is isotropical atomic vibrations

beta_11, beta_22, beta_33 
beta_12, beta_13, beta_23       is anisotropical atomic vibrations

chi_11, chi_22, chi_33
chi_12, chi_13, chi_23          is susceptibility

kappa is expansion/contraction coefficient (by default 1.)
factor_lande is factor landé (by default 2.)

j0_A, j0_a, j0_B, j0_b, j0_C, j0_c, j0_D is coefficient to calculate <j0>

j2_A, j2_a, j2_B, j2_b, j2_C, j2_c, j2_D is coefficient to calculate <j2>

f_dir_prog is directory with file 'bscat.tab', 'formmag.tab'
        """
        print(lsout)
        
    def _load_handbook_n(self):
        f_name = os.path.join(self._p_f_dir_prog, "bscat.tab")
        fid = open(f_name, 'r')
        lcont = fid.readlines()
        fid.close()
        lcont = [line for line in lcont if not(line.startswith("#"))]
        ldcard = []
        for line in lcont:
            lhelp = line.strip().split()
            
            sline = lhelp[2].replace("i","j")
            sline = sline.split("(")[0]
            try:
                if sline.rfind("j") != -1:
                    b_scat = 0.1*complex(sline)
                else:
                    b_scat = 0.1*float(sline)
            except:
                b_scat = 0.
            dcard = {"type_n": lhelp[0], "b_scat": b_scat}
            ldcard.append(dcard)
        self._handbook_nucl = ldcard
    
    def _load_handbook_m(self):
        f_name = os.path.join(self._p_f_dir_prog, "formmag.tab")
        fid = open(f_name, 'r')
        lcont = fid.readlines()
        fid.close()
        lcont = [line for line in lcont if line.startswith("F")]
        ldcard = []
        for line in lcont:
            lhelp = line.strip().split()
            dcard = {"type_m": lhelp[1], "order": int(lhelp[2]),
                     "A": float(lhelp[3]),"a": float(lhelp[4]),
                     "B": float(lhelp[5]),"b": float(lhelp[6]),
                     "C": float(lhelp[7]),"c": float(lhelp[8]),
                     "D": float(lhelp[9])}
            ldcard.append(dcard)
        self._handbook_mag = ldcard

    def _get_b_scat(self, type_n):
        """
        Take b_scat
        """

        ldcard = self._handbook_nucl 
        flag = False
        for dcard in ldcard:
            if (dcard["type_n"] == type_n):
                self._p_b_scat = dcard["b_scat"]
                flag = True
            elif flag:
                break
        if not(flag):
            print("Can not find b_scat for '{:}'".format(type_n))
            
    def _get_j0j2(self, type_m):
        """
        Take coefficients for <j0> and <j2>
        """
        ldcard = self._handbook_mag 
        flag_0, flag_2 = False, False
        for dcard in ldcard:
            if ((dcard["type_m"] == type_m)&(dcard["order"] == 0)):
                self._p_j0_A = dcard["A"]
                self._p_j0_a = dcard["a"]
                self._p_j0_B = dcard["B"]
                self._p_j0_b = dcard["b"]
                self._p_j0_C = dcard["C"]
                self._p_j0_c = dcard["c"]
                self._p_j0_D = dcard["D"]
                flag_0 = True
            elif ((dcard["type_m"] == type_m)&(dcard["order"] == 2)):
                self._p_j2_A = dcard["A"]
                self._p_j2_a = dcard["a"]
                self._p_j2_B = dcard["B"]
                self._p_j2_b = dcard["b"]
                self._p_j2_C = dcard["C"]
                self._p_j2_c = dcard["c"]
                self._p_j2_D = dcard["D"]
                flag_2 = True
            elif (flag_0 & flag_2):
                break
        if not(flag_0):
            print("Can not find coefficients <j0> for '{:}'".format(type_m))
        if not(flag_2):
            print("Can not find coefficients <j2> for '{:}'".format(type_m))


class Fract(dict):
    """
    Fract of atom_site(s) in unit cell.
    """
    def __init__(self, x = 0., y = 0., z = 0.):
        super(Fract, self).__init__()
        self._p_x = None
        self._p_y = None
        self._p_z = None
        
        self._refresh(x, y, z)
        self.set_val()


    def __repr__(self):
        lsout = """Fract: \n xyz: {:} {:} {:}""".format(self._p_x, self._p_y, 
                                  self._p_z)
        return lsout


    def _refresh(self, x, y, z):
        if not(isinstance(x, type(None))):
            self._p_x = numpy.mod(x, 1.)
        if not(isinstance(y, type(None))):
            self._p_y = numpy.mod(y, 1.)
        if not(isinstance(z, type(None))):
            self._p_z = numpy.mod(z, 1.)

            
    def set_val(self, x = None, y = None, z = None):
        self._refresh(x, y, z)
        
    def get_val(self, label):
        lab = "_p_"+label
        
        if lab in self.__dict__.keys():
            val = self.__dict__[lab]
            if isinstance(val, type(None)):
                self.set_val()
                val = self.__dict__[lab]
        else:
            print("The value '{:}' is not found".format(lab))
            val = None
        return val

    def list_vals(self):
        """
        give a list of parameters with small descripition
        """
        lsout = """
Parameters:
x, y, z is atoms coordinate
        """
        print(lsout)
    
    def calc_phase(self, space_groupe, h, k, l):
        """
        calculate phase: exp(-2 pi i * (h*x+k*y+l*z))
        r_11, r_22, r_33, r_12, r_13, r_23 are element of symmetry 
        """
        
        x, y, z = self._p_x, self._p_y, self._p_z

        r_11, r_12 = space_groupe.get_val("r_11"), space_groupe.get_val("r_12")
        r_13, r_21 = space_groupe.get_val("r_13"), space_groupe.get_val("r_21")
        r_22, r_23 = space_groupe.get_val("r_22"), space_groupe.get_val("r_23")
        r_31, r_32 = space_groupe.get_val("r_31"), space_groupe.get_val("r_32")
        r_33 = space_groupe.get_val("r_33")
        b_1, b_2 = space_groupe.get_val("b_1"), space_groupe.get_val("b_2")
        b_3 = space_groupe.get_val("b_3")
        
        np_h, np_x, np_r_11 = numpy.meshgrid(h, x, r_11, indexing="ij")
        np_k, np_y, np_r_22 = numpy.meshgrid(k, y, r_22, indexing="ij")
        np_l, np_z, np_r_33 = numpy.meshgrid(l, z, r_33, indexing="ij")
        
        np_r_12 = numpy.meshgrid(h, x, r_12, indexing="ij")[2]
        np_r_13 = numpy.meshgrid(k, y, r_13, indexing="ij")[2]
        np_r_23 = numpy.meshgrid(l, z, r_23, indexing="ij")[2]
        np_r_21 = numpy.meshgrid(h, x, r_21, indexing="ij")[2]
        np_r_31 = numpy.meshgrid(k, y, r_31, indexing="ij")[2]
        np_r_32 = numpy.meshgrid(l, z, r_32, indexing="ij")[2]

        np_b_1 = numpy.meshgrid(l, z, b_1, indexing="ij")[2]
        np_b_2 = numpy.meshgrid(l, z, b_2, indexing="ij")[2]
        np_b_3 = numpy.meshgrid(l, z, b_3, indexing="ij")[2]
        
        
        np_x_s = np_x*np_r_11 + np_y*np_r_12 + np_z*np_r_13 + np_b_1
        np_y_s = np_x*np_r_21 + np_y*np_r_22 + np_z*np_r_23 + np_b_2
        np_z_s = np_x*np_r_31 + np_y*np_r_32 + np_z*np_r_33 + np_b_3
        
        phase = numpy.exp(2*numpy.pi*1j*(np_h*np_x_s + np_k*np_y_s+ np_l*np_z_s))
        
        return phase
        
        
    def els4pos(self, space_groupe):
        """
        give the lelements of symmetry which transfer atom to the same atom
        """
        
        lelsymm = space_groupe.get_val("el_symm")
        lorig = space_groupe.get_val("orig")
        centr = space_groupe.get_val("centr")
        pcentr = space_groupe.get_val("pcentr")
    
        lelsat = []
        lelsuniqat, lcoorduniqat = [], []
        [x, y, z] = xyz
        x, y, z = x%1, y%1, z%1
        for els in lelsymm:
            for orig in lorig:
                xat = (els[0] + els[1]*x + els[ 2]*y + els[ 3]*z+orig[0])%1
                yat = (els[4] + els[5]*x + els[ 6]*y + els[ 7]*z+orig[1])%1
                zat = (els[8] + els[9]*x + els[10]*y + els[11]*z+orig[2])%1
                elsn = [els[0]+orig[0],els[1],els[2],els[3],els[4]+orig[1],els[5],els[6],els[7],
                els[8]+orig[2],els[9],els[10],els[11]]
                if ((abs(xat-x)<10**-5)&(abs(yat-y)<10**-5)&(abs(zat-z)<10**-5)): lelsat.append(elsn)
                xyzatu = (round(xat,4),round(yat,4),round(zat,4))
                if (not(xyzatu in lcoorduniqat)):
                    lcoorduniqat.append(xyzatu)
                    lelsuniqat.append(elsn)
                if (centr):
                    elsn=[2*pcentr[0]-els[0]-orig[0],-1*els[1],-1*els[2],-1*els[3],
                        2*pcentr[1]-els[4]-orig[1],-1*els[5],-1*els[6],-1*els[7],
                        2*pcentr[2]-els[8]-orig[2],-1*els[9],-1*els[10],-1*els[11]]
                    xat,yat,zat=(2*pcentr[0]-xat)%1,(2*pcentr[1]-yat)%1,(2*pcentr[2]-zat)%1
                    if ((abs(xat-x)<10**-5)&(abs(yat-y)<10**-5)&(abs(zat-z)<10**-5)): lelsat.append(elsn)
                    xyzatu=(round(xat,4),round(yat,4),round(zat,4))
                    if (not(xyzatu in lcoorduniqat)):
                        lcoorduniqat.append(xyzatu)
                        lelsuniqat.append(elsn)
        return lelsat,lelsuniqat



class ADP(dict):
    """
    ADP
    """
    def __init__(self, beta_11 = 0., beta_22 = 0., beta_33 = 0., 
                 beta_12 = 0., beta_13 = 0., beta_23 = 0., b_iso = 0.):
        super(ADP, self).__init__()
        self._p_beta_11 = None
        self._p_beta_22 = None
        self._p_beta_33 = None
        self._p_beta_12 = None
        self._p_beta_13 = None
        self._p_beta_23 = None
        self._p_b_iso = None
        self._refresh(beta_11, beta_22, beta_33, beta_12, beta_13, beta_23, 
                      b_iso)

    def __repr__(self):
        lsout = """Debye Waller: \n beta_11: {:}, beta_22: {:}, beta_33: {:}
 beta_12: {:}, beta_13: {:}, beta_23: {:}\n b_iso: {:}""".format(
 self._p_beta_11, self._p_beta_22, self._p_beta_33, self._p_beta_12, 
 self._p_beta_13, self._p_beta_23, self._p_b_iso)
        return lsout


    def _refresh(self, beta_11, beta_22, beta_33, beta_12, beta_13, beta_23, 
                 b_iso):
        
        if not(isinstance(beta_11, type(None))):
            self._p_beta_11 = beta_11
        if not(isinstance(beta_22, type(None))):
            self._p_beta_22 = beta_22
        if not(isinstance(beta_33, type(None))):
            self._p_beta_33 = beta_33
        if not(isinstance(beta_12, type(None))):
            self._p_beta_12 = beta_12
        if not(isinstance(beta_13, type(None))):
            self._p_beta_13 = beta_13
        if not(isinstance(beta_23, type(None))):
            self._p_beta_23 = beta_23
        if not(isinstance(b_iso, type(None))):
            self._p_b_iso = b_iso

    def set_val(self, beta_11=None, beta_22=None, beta_33=None, beta_12=None, 
                beta_13=None, beta_23=None, b_iso=None):
        self._refresh(beta_11, beta_22, beta_33, beta_12, beta_13, beta_23, 
                      b_iso)
        
    def get_val(self, label):
        lab = "_p_"+label
        
        if lab in self.__dict__.keys():
            val = self.__dict__[lab]
            if isinstance(val, type(None)):
                self.set_val()
                val = self.__dict__[lab]
        else:
            print("The value '{:}' is not found".format(lab))
            val = None
        return val

    def list_vals(self):
        """
        give a list of parameters with small descripition
        """
        lsout = """
Parameters:
beta_ij are Debye-Waller factor
b_iso is the isotropical Debye-Waller factor
        """
        print(lsout)
        
    def _calc_dwf_iso(self, sthovl):
        """
        isotropic harmonic Debye-Waller factor
        """
        b_iso = self._p_b_iso
        sthovl_sq = sthovl**2
        np_biso, np_sthovl_sq = numpy.meshgrid(sthovl_sq, b_iso, indexing="ij")
        
        dwf_iso = numpy.exp(-np_biso*np_sthovl_sq)
        return dwf_iso

    def calc_dwf_aniso(self, space_groupe, h, k, l):
        """
        anisotropic harmonic Debye-Waller factor
        
        h,k,l is 1D (temporary solution)
        """
        r_11, r_12 = space_groupe.get_val("r_11"), space_groupe.get_val("r_12")
        r_13, r_21 = space_groupe.get_val("r_13"), space_groupe.get_val("r_21")
        r_22, r_23 = space_groupe.get_val("r_22"), space_groupe.get_val("r_23")
        r_31, r_32 = space_groupe.get_val("r_31"), space_groupe.get_val("r_32")
        r_33 = space_groupe.get_val("r_33")
  

        b_11, b_22 = self._p_beta_11, self._p_beta_22 
        b_33, b_12 = self._p_beta_33, self._p_beta_12
        b_13, b_23 = self._p_beta_13, self._p_beta_23
        

        np_h, np_b_11, np_r_11 = numpy.meshgrid(h, b_11, r_11, indexing="ij")
        np_k, np_b_22, np_r_22 = numpy.meshgrid(k, b_22, r_22, indexing="ij")
        np_l, np_b_33, np_r_33 = numpy.meshgrid(l, b_33, r_33, indexing="ij")
        np_h, np_b_12, np_r_12 = numpy.meshgrid(h, b_12, r_12, indexing="ij")
        np_h, np_b_13, np_r_13 = numpy.meshgrid(h, b_13, r_13, indexing="ij")
        np_h, np_b_23, np_r_23 = numpy.meshgrid(h, b_23, r_23, indexing="ij")
        np_r_21 = numpy.meshgrid(h, b_23, r_21, indexing="ij")[2]
        np_r_31 = numpy.meshgrid(h, b_23, r_31, indexing="ij")[2]
        np_r_32 = numpy.meshgrid(h, b_23, r_32, indexing="ij")[2]
        
        np_h_s = np_h*np_r_11 + np_k*np_r_21 + np_l*np_r_31
        np_k_s = np_h*np_r_12 + np_k*np_r_22 + np_l*np_r_32
        np_l_s = np_h*np_r_13 + np_k*np_r_23 + np_l*np_r_33
        
        dwf_aniso = numpy.exp(-1.*(np_b_11*np_h_s**2 + np_b_22*np_k_s**2 + 
                           np_b_33*np_l_s**2 + 2.*np_b_12*np_h_s*np_k_s + 
                    2.*np_b_13*np_h_s*np_l_s + 2.*np_b_23*np_k_s*np_l_s))
        
        return dwf_aniso 
        
    def calc_dwf(self, space_groupe, h, k, l):
        """
        calculate Debye-Waller factor
        """
        #self._calc_dwf_iso(sthovl)
        dwf_3d = self.calc_dwf_aniso(space_groupe, h, k, l)
        return dwf_3d
        



class Magnetism(dict):
    """
    Magnetism
    """
    def __init__(self, kappa=1.0, factor_lande=2.0, chi_11=0., chi_22=0., 
                 chi_33=0., chi_12=0., chi_13=0., chi_23=0., j0_A=0., j0_a=0., 
                 j0_B=0., j0_b=0., j0_C=0., j0_c=0., j0_D=0., j2_A=0., j2_a=0., 
                 j2_B=0., j2_b=0., j2_C=0., j2_c=0., j2_D=0.):
        super(Magnetism, self).__init__()
        self._p_chi_11 = None
        self._p_chi_22 = None
        self._p_chi_33 = None
        self._p_chi_12 = None
        self._p_chi_13 = None
        self._p_chi_23 = None
        self._p_kappa = None
        self._p_factor_lande = None
        self._p_j0_A = None
        self._p_j0_a = None
        self._p_j0_B = None
        self._p_j0_b = None
        self._p_j0_C = None
        self._p_j0_c = None
        self._p_j0_D = None
        self._p_j2_A = None
        self._p_j2_a = None
        self._p_j2_B = None
        self._p_j2_b = None
        self._p_j2_C = None
        self._p_j2_c = None
        self._p_j2_D = None
        self._refresh(chi_11, chi_22, chi_33, chi_12, chi_13, chi_23,kappa, 
                      factor_lande, j0_A, j0_a, j0_B, j0_b, j0_C, j0_c, j0_D, 
                      j2_A, j2_a, j2_B, j2_b, j2_C, j2_c, j2_D)
        
    def __repr__(self):
        lsout = """Magnetism: \n chi_11: {:}\n chi_22: {:}\n chi_33: {:}
 chi_12: {:}\n chi_13: {:}\n chi_23: {:}\n kappa: {:}
 factor_lande: {:}""".format(
 self._p_chi_11, self._p_chi_22, self._p_chi_33, self._p_chi_12, 
 self._p_chi_13, self._p_chi_23, self._p_kappa, self._p_factor_lande)
        return lsout


    def _refresh(self, chi_11, chi_22, chi_33, chi_12, chi_13, chi_23, kappa, 
                      factor_lande, j0_A, j0_a, j0_B, j0_b, j0_C, j0_c, j0_D, 
                      j2_A, j2_a, j2_B, j2_b, j2_C, j2_c, j2_D):
        
        if not(isinstance(chi_11, type(None))):
            self._p_chi_11 = chi_11
        if not(isinstance(chi_22, type(None))):
            self._p_chi_22 = chi_22
        if not(isinstance(chi_33, type(None))):
            self._p_chi_33 = chi_33
        if not(isinstance(chi_12, type(None))):
            self._p_chi_12 = chi_12
        if not(isinstance(chi_13, type(None))):
            self._p_chi_13 = chi_13
        if not(isinstance(chi_23, type(None))):
            self._p_chi_23 = chi_23
        if not(isinstance(kappa, type(None))):
            self._p_kappa = kappa 
        if not(isinstance(factor_lande, type(None))):
            self._p_factor_lande = factor_lande 
        if not(isinstance(j0_A, type(None))):
            self._p_j0_A = j0_A 
        if not(isinstance(j0_a, type(None))):
            self._p_j0_a = j0_a 
        if not(isinstance(j0_B, type(None))):
            self._p_j0_B = j0_B 
        if not(isinstance(j0_b, type(None))):
            self._p_j0_b = j0_b 
        if not(isinstance(j0_C, type(None))):
            self._p_j0_C = j0_C 
        if not(isinstance(j0_c, type(None))):
            self._p_j0_c = j0_c 
        if not(isinstance(j0_D, type(None))):
            self._p_j0_D = j0_D 
        if not(isinstance(j2_A, type(None))):
            self._p_j2_A = j2_A 
        if not(isinstance(j2_a, type(None))):
            self._p_j2_a = j2_a 
        if not(isinstance(j2_B, type(None))):
            self._p_j2_B = j2_B 
        if not(isinstance(j2_b, type(None))):
            self._p_j2_b = j2_b 
        if not(isinstance(j2_C, type(None))):
            self._p_j2_C = j2_C 
        if not(isinstance(j2_c, type(None))):
            self._p_j2_c = j2_c 
        if not(isinstance(j2_D, type(None))):
            self._p_j2_D = j2_D 
            

    def set_val(self, chi_11=None, chi_22=None, chi_33=None, chi_12=None, 
                chi_13=None, chi_23=None, kappa=None, factor_lande=None, 
                j0_A=None, j0_a=None, j0_B=None, j0_b=None, j0_C=None, 
                j0_c=None, j0_D=None, j2_A=None, j2_a=None, j2_B=None, 
                j2_b=None, j2_C=None, j2_c=None, j2_D=None):
        self._refresh(chi_11, chi_22, chi_33, chi_12, chi_13, chi_23, kappa, 
                      factor_lande, j0_A, j0_a, j0_B, j0_b, j0_C, j0_c, j0_D, 
                      j2_A, j2_a, j2_B, j2_b, j2_C, j2_c, j2_D)
        
        
    def get_val(self, label):
        lab = "_p_"+label
        
        if lab in self.__dict__.keys():
            val = self.__dict__[lab]
            if isinstance(val, type(None)):
                self.set_val()
                val = self.__dict__[lab]
        else:
            print("The value '{:}' is not found".format(lab))
            val = None
        return val

    def list_vals(self):
        """
        give a list of parameters with small descripition
        """
        lsout = """
Parameters:

chi_ij are the susceptibility vector
kappa define the size of the radial function (equals 1. by default)
factor_lande is the factor Lande (equals 2. by default)
        """
        print(lsout)
    
    def _calc_chi_loc(ia, ib, ic, matrix_ib):
        """
        representation of chi in crystallographic coordinate system defined as x||a*, z||c, y= [z x] (right handed)
        expressions are taken from international tables
        matrix_ib is inversed matrix B
        ia, ib, ic is inversed unit cell parameters (it can be estimated from matrix matrix_ib)

        X = B x, x = iB X
        xT*CHI*x = XT iBT CHI iB X
    
        output chiLOC = iBT CHI iB
        """
        matrix_chi = numpy.array(
                [[self["chi_11"], self["chi_12"], self["chi_13"]],
                 [self["chi_12"], self["chi_22"], self["chi_23"]],
                 [self["chi_13"], self["chi_23"], self["chi_33"]]], 
                 dtype = float)
        #mchi=[[chi[0],chi[3],chi[4]],[chi[3],chi[1],chi[5]],[chi[4],chi[5],chi[2]]]
        #[a,b,c,alpha,beta,gamma]=ucp
        y1 = matrix_ib[0,0]
        y2 = matrix_ib[1,1]
        y3 = matrix_ib[2,2]
        y4 = matrix_ib[0,1]
        y5 = matrix_ib[0,2]
        y6 = matrix_ib[1,2]
        #B=[[x1,x4,x5],
        #   [0.,x2,x6],
        #   [0.,0.,x3]]
        #it shuld be checked
        #iB=numpy.linalg.inv(B)
        y1 = 1./x1
        y2 = 1./x2
        y3 = 1./x3
        y4 = -1*x4*1./(x1*x2)
        y6 = -1*x6*1./(x2*x3)
        y5 = (x4*x6-x2*x5)*1./(x1*x2*x3)
        matrix_ib_norm = matrix_ib
        matrix_ib_norm[:,0] *= ia
        matrix_ib_norm[:,1] *= ib
        matrix_ib_norm[:,2] *= ic
        
        matrix_ibt_norm = matrix_ib_norm.transpose()
        #it is not compatible with case, vhen chi_ij is 1D array 
        ibt_chi = numpy.matmul(matrix_ibt_norm, matrix_chi)
        matrix_chi_loc = numpy.matmul(ibt_chi, matrix_ib_norm)
        d_out = dict(matrix_chi_loc = matrix_chi_loc)
        self.update(d_out)
    
    def calc_form_factor_tensor(self,space_groupe, cell, h, k, l):
        """
        give components of form factor tensor:
            fft_11, fft_12, fft_13
            fft_21, fft_22, fft_23
            fft_31, fft_32, fft_33
            
        in 3 dimension (hkl, atoms, symmetry elements)            
        """
        sthovl = cell.calc_sthovl(h, k, l)
        #dimension (hkl, atoms)
        form_factor_2d = self._calc_form_factor(sthovl)
        
        r_11, r_12 = space_groupe.get_val("r_11"), space_groupe.get_val("r_12")
        r_13, r_21 = space_groupe.get_val("r_13"), space_groupe.get_val("r_21")
        r_22, r_23 = space_groupe.get_val("r_22"), space_groupe.get_val("r_23")
        r_31, r_32 = space_groupe.get_val("r_31"), space_groupe.get_val("r_32")
        r_33 = space_groupe.get_val("r_33")

        chi_11, chi_22 = self._p_chi_11, self._p_chi_22 
        chi_33, chi_12 = self._p_chi_33, self._p_chi_12
        chi_13, chi_23 = self._p_chi_13, self._p_chi_23
        chi_21, chi_31, chi_32 = chi_12, chi_13, chi_23 
        
        c11, r11 = numpy.meshgrid(chi_11, r_11, indexing="ij")
        c22, r22 = numpy.meshgrid(chi_22, r_22, indexing="ij")
        c33, r33 = numpy.meshgrid(chi_33, r_33, indexing="ij")
        c12, r12 = numpy.meshgrid(chi_12, r_12, indexing="ij")
        c13, r13 = numpy.meshgrid(chi_13, r_13, indexing="ij")
        c23, r23 = numpy.meshgrid(chi_23, r_23, indexing="ij")
        c21, r21 = numpy.meshgrid(chi_21, r_21, indexing="ij")
        c31, r31 = numpy.meshgrid(chi_31, r_31, indexing="ij")
        c32, r32 = numpy.meshgrid(chi_32, r_32, indexing="ij")
        
        
        rcrt_11, rcrt_12, rcrt_13, rcrt_21, rcrt_22, rcrt_23, rcrt_31, rcrt_32, rcrt_33 = calc_mRmCmRT(
                r11, r12, r13, r21, r22, r23, r31, r32, r33,
                c11, c12, c13, c21, c22, c23, c31, c32, c33)        
        
        #dimension (hkl, atoms, symmetry)
        fft_11 = form_factor_2d[:,:,numpy.newaxis]*rcrt_11[numpy.newaxis, :,:]
        fft_12 = form_factor_2d[:,:,numpy.newaxis]*rcrt_12[numpy.newaxis, :,:]
        fft_13 = form_factor_2d[:,:,numpy.newaxis]*rcrt_13[numpy.newaxis, :,:]
        fft_21 = form_factor_2d[:,:,numpy.newaxis]*rcrt_21[numpy.newaxis, :,:]
        fft_22 = form_factor_2d[:,:,numpy.newaxis]*rcrt_22[numpy.newaxis, :,:]
        fft_23 = form_factor_2d[:,:,numpy.newaxis]*rcrt_23[numpy.newaxis, :,:]
        fft_31 = form_factor_2d[:,:,numpy.newaxis]*rcrt_31[numpy.newaxis, :,:]
        fft_32 = form_factor_2d[:,:,numpy.newaxis]*rcrt_32[numpy.newaxis, :,:]
        fft_33 = form_factor_2d[:,:,numpy.newaxis]*rcrt_33[numpy.newaxis, :,:]
        
        #ortogonalization should be done
        
        return fft_11, fft_12, fft_13, fft_21, fft_22, fft_23, fft_31, fft_32, fft_33
    
    def calc_chi_rot(matrix_chi, elsymm):
        """
        calculate R*chi*RT
        rotation of chi by element of symmetry
        """
        [b1,r11,r12,r13,b2,r21,r22,r23,b3,r31,r32,r33]=elsymm
        matrix_r = numpy.array([[r11, r12, r13], [r21, r22, r23], 
                               [r31, r32, r33]], dtype=float)
        matrix_rt = matrix_r.transpose()
        r_chi = numpy.matmul(matrix_r, matrix_chi)
        
        matrix_chi_rot = numpy.matmul(r_chi, matrix_rt)
        return matrix_chi_rot 
    
    def _calc_form_factor(self, sthovl):
        """Calculate magnetic form factor in frame of Spherical model (Int.Tabl.C.p.592)\n
        LFactor is Lande factor\n
        coeff0 is a list [A,a,B,b,C,c,D] at n=0\n
        coeff2 is a list [A,a,B,b,C,c,D] at n=2\n
        lsthovl is list sin(theta)/lambda in Angstrems**-1

        Calculation of magnetic form factor <j0>,<j2>,<j4>,<j6>\n
        coeff is a list [A,a,B,b,C,c,D] at n=0,2,4,6
        For help see International Table Vol.C p.460
        """
        #not sure about kappa, it is here just for test, by default it is 1.0
        kappa = self._p_kappa
        factor_lande = self._p_factor_lande
        j0_A = self._p_j0_A
        j0_a = self._p_j0_a
        j0_B = self._p_j0_B
        j0_b = self._p_j0_b
        j0_C = self._p_j0_C
        j0_c = self._p_j0_c
        j0_D = self._p_j0_D
        j2_A = self._p_j2_A
        j2_a = self._p_j2_a
        j2_B = self._p_j2_B
        j2_b = self._p_j2_b
        j2_C = self._p_j2_C
        j2_c = self._p_j2_c
        j2_D = self._p_j2_D     
        
        np_sthovl, np_kappa = numpy.meshgrid(sthovl, kappa, indexing ="ij")
        np_factor_lande = numpy.meshgrid(sthovl, factor_lande, indexing ="ij")[1]
        np_j0_A = numpy.meshgrid(sthovl, j0_A, indexing ="ij")[1]
        np_j0_a = numpy.meshgrid(sthovl, j0_a, indexing ="ij")[1]
        np_j0_B = numpy.meshgrid(sthovl, j0_B, indexing ="ij")[1]
        np_j0_b = numpy.meshgrid(sthovl, j0_b, indexing ="ij")[1]
        np_j0_C = numpy.meshgrid(sthovl, j0_C, indexing ="ij")[1]
        np_j0_c = numpy.meshgrid(sthovl, j0_c, indexing ="ij")[1]
        np_j0_D = numpy.meshgrid(sthovl, j0_D, indexing ="ij")[1]
        np_j2_A = numpy.meshgrid(sthovl, j2_A, indexing ="ij")[1]
        np_j2_a = numpy.meshgrid(sthovl, j2_a, indexing ="ij")[1]
        np_j2_B = numpy.meshgrid(sthovl, j2_B, indexing ="ij")[1]
        np_j2_b = numpy.meshgrid(sthovl, j2_b, indexing ="ij")[1]
        np_j2_C = numpy.meshgrid(sthovl, j2_C, indexing ="ij")[1]
        np_j2_c = numpy.meshgrid(sthovl, j2_c, indexing ="ij")[1]
        np_j2_D = numpy.meshgrid(sthovl, j2_D, indexing ="ij")[1]

        np_h = (np_sthovl*1./np_kappa)**2
        j0_av = (np_j0_A*numpy.exp(-np_j0_a*np_h)+
                 np_j0_B*numpy.exp(-np_j0_b*np_h)+
                 np_j0_C*numpy.exp(-np_j0_c*np_h)+np_j0_D)
        j2_av = (np_j2_A*numpy.exp(-np_j2_a*np_h)+
                 np_j2_B*numpy.exp(-np_j2_b*np_h)+
                 np_j2_C*numpy.exp(-np_j2_c*np_h)+np_j2_D)*np_h
        form_factor = j0_av+(1.0-2.0/np_factor_lande)*j2_av
        return form_factor




class AtomSite(dict):
    """
    AtomSite
    """
    def __init__(self):
        super(AtomSite, self).__init__()
        self._p_fract = None
        self._p_adp = None
        self._p_magnetism = None
        self._p_b_scat = None
        self._p_occupation = None
        self._list_atoms = []
    
    def __repr__(self):
        lsout = """AtomSite:\n number of atoms: {:}.\n""".format(len(self._list_atoms))
        for iatom, atom_type in enumerate(self._list_atoms):
            lsout += "\n"+70*"*"+"\n {:}. ".format(iatom+1)+atom_type.__repr__()
        return lsout
    
    
    def _refresh(self):
        print("The option '_refresh' is not valiable")
        pass
    
    
    def set_val(self):
        print("The option 'set_val' is not valiable")
        pass
    
    
    def get_val(self, label):
        lab = "_p_"+label
        
        if lab in self.__dict__.keys():
            val = self.__dict__[lab]
            if isinstance(val, type(None)):
                self.set_val()
                val = self.__dict__[lab]
        else:
            print("The value '{:}' is not found".format(lab))
            val = None
        return val
    
    
    def list_vals(self):
        """
        give a list of parameters with small descripition
        """
        lsout = """
Parameters:

b_scat is amplitude scattering  
occupation is occupation factor  
fract  is fraction of atoms

        """
        print(lsout)
        
    def add_atom(self, atom):
        self._list_atoms.append(atom)
        self._form_arrays()
    
    def del_atom(self, ind):
        self._list_atoms.pop(ind)        
        self._form_arrays()

    def replace_atom(self, ind, atom):
        self._list_atoms.pop(ind)
        self._list_atoms.insert(ind, atom)
        self._form_arrays()

    def _form_arrays(self):
        lb_scat, locc = [], []
        lx, ly, lz = [], [], []
        lbeta_11, lbeta_22, lbeta_33 = [], [], []
        lbeta_12, lbeta_13, lbeta_23 = [], [], []
        lb_iso = []
        lchi_11, lchi_22, lchi_33 = [], [], []
        lchi_12, lchi_13, lchi_23 = [], [], []
        lkappa, lfactor_lande = [], []
        lj0_A, lj0_a, lj0_B, lj0_b, lj0_C, lj0_c = [], [], [], [], [], []
        lj0_D = []
        lj2_A, lj2_a, lj2_B, lj2_b, lj2_C, lj2_c = [], [], [], [], [], []
        lj2_D = []
        for atom in self._list_atoms:
            lb_scat.append(atom.get_val("b_scat"))
            locc.append(atom.get_val("occupation"))
            lx.append(atom.get_val("x"))
            ly.append(atom.get_val("y"))
            lz.append(atom.get_val("z"))
            lbeta_11.append(atom.get_val("beta_11"))
            lbeta_22.append(atom.get_val("beta_22"))
            lbeta_33.append(atom.get_val("beta_33"))
            lbeta_12.append(atom.get_val("beta_12"))
            lbeta_13.append(atom.get_val("beta_13"))
            lbeta_23.append(atom.get_val("beta_23"))
            lb_iso.append(atom.get_val("b_iso"))
            lchi_11.append(atom.get_val("chi_11"))
            lchi_22.append(atom.get_val("chi_22"))
            lchi_33.append(atom.get_val("chi_33"))
            lchi_12.append(atom.get_val("chi_12"))
            lchi_13.append(atom.get_val("chi_13"))
            lchi_23.append(atom.get_val("chi_23"))
            lkappa.append(atom.get_val("kappa"))
            lfactor_lande.append(atom.get_val("factor_lande"))
            lj0_A.append(atom.get_val("j0_A"))
            lj0_a.append(atom.get_val("j0_a")) 
            lj0_B.append(atom.get_val("j0_B")) 
            lj0_b.append(atom.get_val("j0_b")) 
            lj0_C.append(atom.get_val("j0_C")) 
            lj0_c.append(atom.get_val("j0_c"))
            lj0_D.append(atom.get_val("j0_D"))
            lj2_A.append(atom.get_val("j2_A"))
            lj2_a.append(atom.get_val("j2_a")) 
            lj2_B.append(atom.get_val("j2_B")) 
            lj2_b.append(atom.get_val("j2_b")) 
            lj2_C.append(atom.get_val("j2_C")) 
            lj2_c.append(atom.get_val("j2_c"))
            lj2_D.append(atom.get_val("j2_D"))
            
        np_b_scat = numpy.array(lb_scat, dtype=float)
        np_occ = numpy.array(locc, dtype=float)
        np_x = numpy.array(lx, dtype=float)
        np_y = numpy.array(ly, dtype=float)
        np_z = numpy.array(lz, dtype=float)
        fract = Fract(x=np_x, y=np_y, z=np_z)

        np_beta_11 = numpy.array(lbeta_11, dtype=float)
        np_beta_22 = numpy.array(lbeta_22, dtype=float)
        np_beta_33 = numpy.array(lbeta_33, dtype=float)
        np_beta_12 = numpy.array(lbeta_12, dtype=float)
        np_beta_13 = numpy.array(lbeta_13, dtype=float)
        np_beta_23 = numpy.array(lbeta_23, dtype=float)
        np_b_iso = numpy.array(lb_iso, dtype=float)
        adp = ADP(beta_11=np_beta_11, beta_22=np_beta_22, beta_33=np_beta_33,
                  beta_12=np_beta_12, beta_13=np_beta_13, beta_23=np_beta_23,
                  b_iso = np_b_iso)

        np_chi_11 = numpy.array(lchi_11, dtype=float)
        np_chi_22 = numpy.array(lchi_22, dtype=float)
        np_chi_33 = numpy.array(lchi_33, dtype=float)
        np_chi_12 = numpy.array(lchi_12, dtype=float)
        np_chi_13 = numpy.array(lchi_13, dtype=float)
        np_chi_23 = numpy.array(lchi_23, dtype=float)
        np_kappa = numpy.array(lkappa, dtype=float)
        np_factor_lande = numpy.array(lfactor_lande, dtype=float)
        np_j0_A = numpy.array(lj0_A, dtype=float)
        np_j0_a = numpy.array(lj0_a, dtype=float)
        np_j0_B = numpy.array(lj0_B, dtype=float)
        np_j0_b = numpy.array(lj0_b, dtype=float)
        np_j0_C = numpy.array(lj0_C, dtype=float)
        np_j0_c = numpy.array(lj0_c, dtype=float)
        np_j0_D = numpy.array(lj0_D, dtype=float)
        np_j2_A = numpy.array(lj2_A, dtype=float)
        np_j2_a = numpy.array(lj2_a, dtype=float)
        np_j2_B = numpy.array(lj2_B, dtype=float)
        np_j2_b = numpy.array(lj2_b, dtype=float)
        np_j2_C = numpy.array(lj2_C, dtype=float)
        np_j2_c = numpy.array(lj2_c, dtype=float)
        np_j2_D = numpy.array(lj2_D, dtype=float)
        

        magnetism = Magnetism(chi_11=np_chi_11, chi_22=np_chi_22, 
            chi_33=np_chi_33, chi_12=np_chi_12, chi_13=np_chi_13, 
            chi_23=np_chi_23, kappa = np_kappa, factor_lande = np_factor_lande,
            j0_A=np_j0_A, j0_a=np_j0_a, j0_B=np_j0_B, j0_b=np_j0_b, 
            j0_C=np_j0_C, j0_c=np_j0_c, j0_D=np_j0_D, j2_A=np_j2_A, 
            j2_a=np_j2_a, j2_B=np_j2_B, j2_b=np_j2_b, j2_C=np_j2_C, 
            j2_c=np_j2_c, j2_D=np_j2_D)
        
        self._p_b_scat = np_b_scat
        self._p_occupation = np_occ
        self._p_fract = fract
        self._p_adp = adp 
        self._p_magnetism = magnetism
    
    def calc_sf(self, space_groupe, cell, h, k, l):
        """
        calculate nuclear structure factor
        """
        #sthovl = cell.calc_sthovl(h, k, l)
        
        fract = self._p_fract
        adp = self._p_adp
        magnetism = self._p_magnetism
        b_scat = self._p_b_scat
        occupation = self._p_occupation
        x, y, z = fract.get_val("x"), fract.get_val("y"), fract.get_val("z")
        atom_multiplicity = space_groupe.calc_atom_mult(x, y, z)
        occ_mult = occupation*atom_multiplicity 
        
        phase_3d = fract.calc_phase(space_groupe, h, k, l)#3d object
        dwf_3d = adp.calc_dwf(space_groupe, h, k, l)
        ff_11, ff_12, ff_13, ff_21, ff_22, ff_23, ff_31, ff_32, ff_33 =  magnetism.calc_form_factor_tensor(space_groupe, cell, h, k, l)
        
        hh = phase_3d*dwf_3d
        
        phase_2d = hh.sum(axis=2)

        ft_11 = (ff_11*hh).sum(axis=2)
        ft_12 = (ff_12*hh).sum(axis=2)
        ft_13 = (ff_13*hh).sum(axis=2)
        ft_21 = (ff_21*hh).sum(axis=2)
        ft_22 = (ff_22*hh).sum(axis=2)
        ft_23 = (ff_23*hh).sum(axis=2)
        ft_31 = (ff_31*hh).sum(axis=2)
        ft_32 = (ff_32*hh).sum(axis=2)
        ft_33 = (ff_33*hh).sum(axis=2)
        
        b_scat_2d = numpy.meshgrid(h, b_scat, indexing="ij")[1]
        occ_mult_2d = numpy.meshgrid(h, occ_mult, indexing="ij")[1]
        
        lel_symm = space_groupe.get_val("el_symm")
        lorig = space_groupe.get_val("orig")
        centr = space_groupe.get_val("centr")

        #calculation of nuclear structure factor        
        hh = phase_2d * b_scat_2d * occ_mult_2d
        f_hkl_as = hh.sum(axis=1)*1./len(lel_symm)
        
        
        orig_x = [hh[0] for hh in lorig]
        orig_y = [hh[1] for hh in lorig]
        orig_z = [hh[2] for hh in lorig]
        
        np_h, np_orig_x = numpy.meshgrid(h, orig_x, indexing = "ij")
        np_k, np_orig_y = numpy.meshgrid(k, orig_y, indexing = "ij")
        np_l, np_orig_z = numpy.meshgrid(l, orig_z, indexing = "ij")
        
        np_orig_as = numpy.exp(2*numpy.pi*1j*(np_h*np_orig_x+np_k*np_orig_y+np_l*np_orig_z))
        f_hkl_as = f_hkl_as*np_orig_as.sum(axis=1)*1./len(lorig)

        if (centr):
            orig = space_groupe.get_val("p_centr")
            f_nucl = 0.5*(f_hkl_as+f_hkl_as.conjugate()*numpy.exp(2.*2.*numpy.pi*1j* (h*orig[0]+k*orig[1]+l*orig[2])))
        else:
            f_nucl = f_hkl_as

        #calculation of structure factor tensor
        sft_as_11 = (ft_11 * occ_mult_2d).sum(axis=1)*1./len(lel_symm)
        sft_as_12 = (ft_12 * occ_mult_2d).sum(axis=1)*1./len(lel_symm)
        sft_as_13 = (ft_13 * occ_mult_2d).sum(axis=1)*1./len(lel_symm)
        sft_as_21 = (ft_21 * occ_mult_2d).sum(axis=1)*1./len(lel_symm)
        sft_as_22 = (ft_22 * occ_mult_2d).sum(axis=1)*1./len(lel_symm)
        sft_as_23 = (ft_23 * occ_mult_2d).sum(axis=1)*1./len(lel_symm)
        sft_as_31 = (ft_31 * occ_mult_2d).sum(axis=1)*1./len(lel_symm)
        sft_as_32 = (ft_32 * occ_mult_2d).sum(axis=1)*1./len(lel_symm)
        sft_as_33 = (ft_33 * occ_mult_2d).sum(axis=1)*1./len(lel_symm)

        sft_as_11 = sft_as_11 * np_orig_as.sum(axis=1)*1./len(lorig)
        sft_as_12 = sft_as_12 * np_orig_as.sum(axis=1)*1./len(lorig)
        sft_as_13 = sft_as_13 * np_orig_as.sum(axis=1)*1./len(lorig)
        sft_as_21 = sft_as_21 * np_orig_as.sum(axis=1)*1./len(lorig)
        sft_as_22 = sft_as_22 * np_orig_as.sum(axis=1)*1./len(lorig)
        sft_as_23 = sft_as_23 * np_orig_as.sum(axis=1)*1./len(lorig)
        sft_as_31 = sft_as_31 * np_orig_as.sum(axis=1)*1./len(lorig)
        sft_as_32 = sft_as_32 * np_orig_as.sum(axis=1)*1./len(lorig)
        sft_as_33 = sft_as_33 * np_orig_as.sum(axis=1)*1./len(lorig)
    
        if (centr):
            orig = space_groupe.get_val("p_centr")
            hh = numpy.exp(2.*2.*numpy.pi*1j* (h*orig[0]+k*orig[1]+l*orig[2]))
            sft_11 = 0.5*(sft_as_11+sft_as_11.conjugate()*hh)
            sft_12 = 0.5*(sft_as_12+sft_as_12.conjugate()*hh)
            sft_13 = 0.5*(sft_as_13+sft_as_13.conjugate()*hh)
            sft_21 = 0.5*(sft_as_21+sft_as_21.conjugate()*hh)
            sft_22 = 0.5*(sft_as_22+sft_as_22.conjugate()*hh)
            sft_23 = 0.5*(sft_as_23+sft_as_23.conjugate()*hh)
            sft_31 = 0.5*(sft_as_31+sft_as_31.conjugate()*hh)
            sft_32 = 0.5*(sft_as_32+sft_as_32.conjugate()*hh)
            sft_33 = 0.5*(sft_as_33+sft_as_33.conjugate()*hh)
        else:
            sft_11, sft_12, sft_13 = sft_as_11, sft_as_12, sft_as_13
            sft_21, sft_22, sft_23 = sft_as_21, sft_as_22, sft_as_23
            sft_31, sft_32, sft_33 = sft_as_31, sft_as_32, sft_as_33            
            
        return f_nucl, sft_11, sft_12, sft_13, sft_21, sft_22, sft_23, sft_31, sft_32, sft_33


class Extinction(dict):
    """
    Extinction
    """
    def __init__(self, domain_radius=0., mosaicity=0., model="gauss"):
        super(Extinction, self).__init__()
        self._p_domain_radius = None
        self._p_mosaicity = None
        self._p_model = None
        self._refresh(domain_radius, mosaicity, model)

    def __repr__(self):
        lsout = """Extinction: \n model: {:},\n domain_radius: {:}
 mosaicity: {:}""".format(self._p_model, self._p_domain_radius, 
 self._p_mosaicity)
        return lsout


    def _refresh(self, domain_radius, mosaicity, model):
        
        if domain_radius is not None:
            self._p_domain_radius = domain_radius
        if mosaicity is not None:
            self._p_mosaicity = mosaicity
        if model is not None:
            self._p_model = model

    def set_val(self, domain_radius=None, mosaicity=None, model=None):
        self._refresh(domain_radius, mosaicity, model)
        
    def get_val(self, label):
        lab = "_p_"+label
        
        if lab in self.__dict__.keys():
            val = self.__dict__[lab]
            if isinstance(val, type(None)):
                self.set_val()
                val = self.__dict__[lab]
        else:
            print("The value '{:}' is not found".format(lab))
            val = None
        return val

    def list_vals(self):
        """
        give a list of parameters with small descripition
        """
        lsout = """
Parameters:
model can be "gauss" of "lorentz" model
domain_radius is the averaged radius of domains in Angstrems (???)
mosaicity is the mosaicity of domains in Minutes (???)
        """
        print(lsout)
        
    def calc_extinction(self, cell, h, k, l, f_sq, wave_length):
        """
        f_sq in 10-12cm
        extinction for spherical model
        """
        r = 1*self._p_domain_radius
        g = 1*self._p_mosaicity
        model = self._p_model
        kk = 1.
        vol = cell.get_val("vol")
        sthovl = cell.calc_sthovl(h, k, l)
        stheta = sthovl * wave_length
        s2theta = 2. * stheta * (1. - stheta**2)**0.5
        c2theta = 1. - 2. * stheta**2
    
        q = (f_sq*kk/vol**2)*(wave_length**3)*1./s2theta
    
        t = 1.5*r
        alpha = 1.5*r*s2theta*1./wave_length
        x = 2./3*q*alpha*t
    
        A = 0.20 + 0.45 * c2theta
        B = 0.22 - 0.12 * (0.5-c2theta)**2
        yp = (1+2*x+(A*x**2)*1./(1.+B*x))**(-0.5)
        
        ag = numpy.zeros(h.shape, dtype=float)
        al = numpy.zeros(h.shape, dtype=float)
        
        flag = alpha != 0.
        ag[flag] = alpha[flag]*g*(g**2+0.5*alpha[flag]**2)**(-0.5)
        al[flag] = alpha[flag]*g*1./(g+alpha[flag]*2./3.)
        
        if model == "gauss":
            xs = 2./3.*q*ag*t
            A = 0.58 + 0.48 * c2theta + 0.24 * c2theta**2
            B = 0.02 - 0.025 * c2theta
            #print("A, B", A, B)
            ys = (1+2.12*xs+(A*xs**2)*1./(1+B*xs))**(-0.5)
        elif model == "lorentz":
            xs = 2./3.*q*al*t
            A = 0.025 + 0.285 * c2theta
            B = -0.45 * c2theta
            flag = c2theta>0
            B[flag] = 0.15 - 0.2 * (0.75-c2theta[flag])**2
            ys = (1+2*xs+(A*xs**2)*1./(1+B*xs))**(-0.5)
        else:
            ys = 1.
        #print("ys", ys)
        yext = yp * ys
        return yext
            

    
class Crystal(dict):
    """
    Crystal
    """
    def __init__(self, space_groupe = SpaceGroupe(), cell = Cell(), 
                 atom_site = AtomSite(), extinction=Extinction(), i_g = 0.):
        super(Crystal, self).__init__()
        
        self._p_space_groupe = None
        self._p_cell = None
        self._p_atom_site = None
        self._p_extinction = None
        self._p_i_g = None
        self._refresh(space_groupe, cell, atom_site, extinction, i_g)
        
    def __repr__(self):
        lsout = """Phase: \n i_g: {:}\n{:}\n{:}\n{:}
{:}""".format(self._p_i_g, self._p_space_groupe, self._p_cell, 
                         self._p_atom_site, self._p_extinction)
        return lsout

    def _refresh(self, space_groupe, cell, atom_site, extinction, i_g):
        if space_groupe is not None:
            self._p_space_groupe = space_groupe
        if cell is not None:
            self._p_cell = cell
        if atom_site is not None:
            self._p_atom_site = atom_site
        if extinction is not None:
            self._p_extinction = extinction
        if i_g is not None:
            self._p_i_g = i_g

    def set_val(self, space_groupe=None, cell=None, atom_site=None, 
                extinction=None, i_g=None):
        self._refresh(space_groupe, cell, atom_site, extinction, i_g)
        
    def get_val(self, label):
        lab = "_p_"+label
        
        if lab in self.__dict__.keys():
            val = self.__dict__[lab]
            if isinstance(val, type(None)):
                self.set_val()
                val = self.__dict__[lab]
        else:
            print("The value '{:}' is not found".format(lab))
            val = None
        return val

        
    def calc_sf(self, h, k, l, mode="FN"):
        """
        calculate nuclear structure factor
        """
        cell = self._p_cell
        space_groupe = self._p_space_groupe
        atom_site = self._p_atom_site
        f_nucl, sft_11, sft_12, sft_13, sft_21, sft_22, sft_23, sft_31, sft_32, sft_33 = atom_site.calc_sf(space_groupe, cell, h, k, l)
        #sft_ij form the structure factor tensor in local coordinate system (ia, ib, ic)
        #chi in 10-12 cm; chim in muB (it is why here 0.2695)
        s_11, s_12, s_13, s_21, s_22, s_23, s_31, s_32, s_33 = self._orto_matrix(
                cell,
                sft_11*0.2695, sft_12*0.2695, sft_13*0.2695, 
                sft_21*0.2695, sft_22*0.2695, sft_23*0.2695, 
                sft_31*0.2695, sft_32*0.2695, sft_33*0.2695)

        return f_nucl, s_11, s_12, s_13, s_21, s_22, s_23, s_31, s_32, s_33


    def _orto_matrix(self, cell, l_11, l_12, l_13, l_21, l_22, l_23, l_31, 
                     l_32, l_33):
        """
        rewrite matrix l_ij defined in coordinate (ia, ib, ic) to matrix s_ij, 
        which is denined in Chartesian coordinate system, such as:
        x||ia, y in blane (ia, ib), z perpendicular to that plane.
        ...
        
        ...
        representation of chi in crystallographic coordinate system defined as x||a*, z||c, y= [z x] (right handed)
        expressions are taken from international tables
        matrix_ib is inversed matrix B
        ia, ib, ic is inversed unit cell parameters (it can be estimated from matrix matrix_ib)

        X = B x, x = iB X
        xT*CHI*x = XT iBT CHI iB X
    
        output chiLOC = iBT CHI iB
        """
        m_ib = cell.get_val("m_ib")
        ia, ib, ic = cell.get_val("ia"), cell.get_val("ib"), cell.get_val("ic")
        """
        matrix_chi = numpy.array(
                [[self["chi_11"], self["chi_12"], self["chi_13"]],
                 [self["chi_12"], self["chi_22"], self["chi_23"]],
                 [self["chi_13"], self["chi_23"], self["chi_33"]]], 
                 dtype = float)
        #mchi=[[chi[0],chi[3],chi[4]],[chi[3],chi[1],chi[5]],[chi[4],chi[5],chi[2]]]
        #[a,b,c,alpha,beta,gamma]=ucp
        y1 = m_ib[0,0]
        y2 = m_ib[1,1]
        y3 = m_ib[2,2]
        y4 = m_ib[0,1]
        y5 = m_ib[0,2]
        y6 = m_ib[1,2]
        #B=[[x1,x4,x5],
        #   [0.,x2,x6],
        #   [0.,0.,x3]]
        #it shuld be checked
        #iB=numpy.linalg.inv(B)
        y1 = 1./x1
        y2 = 1./x2
        y3 = 1./x3
        y4 = -1*x4*1./(x1*x2)
        y6 = -1*x6*1./(x2*x3)
        y5 = (x4*x6-x2*x5)*1./(x1*x2*x3)
        """
        m_ib_norm = numpy.copy(m_ib)
        m_ib_norm[:,0] *= ia
        m_ib_norm[:,1] *= ib
        m_ib_norm[:,2] *= ic
        
        m_ibt_norm = m_ib_norm.transpose()
        
        r11, r12, r13 = m_ibt_norm[0, 0], m_ibt_norm[0, 1], m_ibt_norm[0, 2]
        r21, r22, r23 = m_ibt_norm[1, 0], m_ibt_norm[1, 1], m_ibt_norm[1, 2]
        r31, r32, r33 = m_ibt_norm[2, 0], m_ibt_norm[2, 1], m_ibt_norm[2, 2]
        
        s_11, s_12, s_13, s_21, s_22, s_23, s_31, s_32, s_33 = calc_mRmCmRT(
                r11, r12, r13, r21, r22, r23, r31, r32, r33,
                l_11, l_12, l_13, l_21, l_22, l_23, l_31, l_32, l_33)        
        """
        ibt_chi = numpy.matmul(m_ibt_norm, matrix_chi)
        matrix_chi_loc = numpy.matmul(ibt_chi, m_ib_norm)
        d_out = dict(matrix_chi_loc = matrix_chi_loc)
        self.update(d_out)
        """
        return s_11, s_12, s_13, s_21, s_22, s_23, s_31, s_32, s_33
    
    def calc_extinction(self, h, k, l, fp_sq, fm_sq, fpm_sq, wave_length):
        cell = self._p_cell
        extinction = self._p_extinction
        yp = extinction.calc_extinction(cell, h, k, l, fp_sq, wave_length)
        ym = extinction.calc_extinction(cell, h, k, l, fm_sq, wave_length)
        ypm = extinction.calc_extinction(cell, h, k, l, fpm_sq, wave_length)
        return yp, ym, ypm
        
    
if (__name__ == "__main__"):
  pass

