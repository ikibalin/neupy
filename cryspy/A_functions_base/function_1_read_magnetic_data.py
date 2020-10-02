# ORIGINAL FORTRAN PROGRAM
#       program read_magnetic_data
# * read data about magnetic space groups
# * input data from magnetic_table.dat
#       implicit none
#       integer i,j,k,m,n

# * for the ith nonhexagonal point operator:
# * point_op_label(i): point operator symbol (from Litvin)
#       character point_op_label(48)*8
# * point_op_xyz(i): point operator in x,y,z notation
#       character point_op_xyz(48)*10
# * point_op_matrix(i): point operator matrix
#       integer point_op_matrix(3,3,48)

# * for the ith hexagonal point operator:
# * point_op_hex_label(i): point operator symbol (from Litvin)
#       character point_op_hex_label(24)*8
# * point_op_hex_xyz(i): point operator in x,y,z notation
#       character point_op_hex_xyz(24)*10
# * point_op_hex_matrix(i): point operator matrix
#       integer point_op_hex_matrix(3,3,24)

# * number of magnetic space groups
#       integer magcount
#       parameter(magcount=1651)

# * for the ith magnetic space group
# * nlabel_bns(i): numerical label in BNS setting
#       character nlabel_bns(magcount)*12
# * nlabel_parts_bns(j,i): jth part of nlabel_bns
#       integer nlabelparts_bns(2,magcount)
# * label_bns(i): group symbol
#       character spacegroup_label_bns(magcount)*14
# * nlabel_og(i): numerical label in OG setting
#       character nlabel_og(magcount)*12
# * nlabel_parts_og(j,i): jth part of nlabel_og
#       integer nlabelparts_og(3,magcount)
# * label_og(i): group symbol
#       character spacegroup_label_og(magcount)*14
# * magtype(i): type of magnetic space group (1-4)
#       integer magtype(magcount)

# * BNS-OG transformation (if type-4)
# * bnsog_point_op(j,k,i): 3x3 point operator part of transformation
#       integer bnsog_point_op(3,3,magcount)
# * bnsog_origin(j,i): translation part of transformation
# * bnsog_point_origin(i): common denominator
#       integer bnsog_origin(3,magcount)
#       integer bnsog_origin_denom(magcount)

# * iops_count(i): number of point operators
#       integer ops_count(magcount)
# * wyckoff_count(i): number of wyckoff sites
#       integer wyckoff_site_count(magcount)
# * wyckoff_pos_count(j,i): number of positions in jth wyckoff site
#       integer wyckoff_pos_count(27,magcount)
# * wyckoff_mult(j,i): multiplicity for jth wyckoff site
#       integer wyckoff_mult(27,magcount)
# * wyckoff_label(j,i): symbol (a,b,c,...,z,alpha) for jth wyckoff site
#       character wyckoff_label(27,magcount)

# * for BNS setting
# * lattice_bns_vectors_count(i): number of lattice vectors defining the lattice
#       integer lattice_bns_vectors_count(magcount)
# * lattice_bns_vectors(k,j,i): kth component of the jth lattice vector
# * lattice_bns_vectors_denom(j,i): common denominator
#       integer lattice_bns_vectors(3,6,magcount)
#       integer lattice_bns_vectors_denom(6,magcount)
# * for jth operator
# * ops_bns_point_op(j,i): point operator part
#       integer ops_bns_point_op(96,magcount)
# * ops_bns_trans(k,j,i): kth component of translation part
# * ops_bns_trans_denom(j,i): common denominator
#       integer ops_bns_trans(3,96,magcount)
#       integer ops_bns_trans_denom(96,magcount)
# * ops_bns_timeinv(j,i): 1=no time inversion, -1=time inversion
#       integer ops_bns_timeinv(96,magcount)
# * for jth wyckoff site
# * wyckoff_bns_fract(k,j,i): kth component of fractional part of wyckoff position
# * wyckoff_bns_fract_denom(j,i): common denominator
#       integer wyckoff_bns_fract(3,96,27,magcount)
#       integer wyckoff_bns_fract_denom(96,27,magcount)
# * wyckoff_bns_xyz(m,k,j,i): mth component to coeffcient of kth paramater (x,y,z)
#       integer wyckoff_bns_xyz(3,3,96,27,magcount)
# * wyckoff_bns_mag(m,k,j,i): mth component to coeffcient of kth magnetic
# * paramater (mx,my,mz)
#       integer wyckoff_bns_mag(3,3,96,27,magcount)

# * for OG setting (for type-4 groups)
# * lattice_og_vectors_count(i): number of lattice vectors defining the lattice
#       integer lattice_og_vectors_count(magcount)
# * lattice_og_vectors(k,j,i): kth component of the jth lattice vector
# * lattice_og_vectors_denom(j,i): common denominator
#       integer lattice_og_vectors(3,6,magcount)
#       integer lattice_og_vectors_denom(6,magcount)
# * for jth operator
# * ops_og_point_op(j,i): point operator part
#       integer ops_og_point_op(96,magcount)
# * ops_og_trans(k,j,i): kth component of translation part
# * ops_og_trans_denom(j,i): common denominator
#       integer ops_og_trans(3,96,magcount)
#       integer ops_og_trans_denom(96,magcount)
# * ops_og_timeinv(j,i): 1=no time inversion, -1=time inversion
#       integer ops_og_timeinv(96,magcount)
# * for jth wyckoff site
# * wyckoff_og_fract(k,j,i): kth component of fractional part of wyckoff position
# * wyckoff_og_fract_denom(j,i): common denominator
#       integer wyckoff_og_fract(3,96,27,magcount)
#       integer wyckoff_og_fract_denom(96,27,magcount)
# * wyckoff_og_xyz(m,k,j,i): mth component to coeffcient of kth paramater (x,y,z)
#       integer wyckoff_og_xyz(3,3,96,27,magcount)
# * wyckoff_og_mag(m,k,j,i): mth component to coeffcient of kth magnetic
# * paramater (mx,my,mz)
#       integer wyckoff_og_mag(3,3,96,27,magcount)

# ******************************************************************************
# * open data file
#       open(30,file='magnetic_data.txt')
# * read nonhexangonal point operators
#       do i=1,48
#         read(30,*)n,point_op_label(i),point_op_xyz(i),
#      $       ((point_op_matrix(k,j,i),j=1,3),k=1,3)
#         if(n.ne.i)stop
#      $       'error in numbering of nonhexagonal point operators'
#       enddo
# * read hexangonal point operators
#       do i=1,24
#         read(30,*)n,point_op_hex_label(i),
#      $       point_op_hex_xyz(i),
#      $       ((point_op_hex_matrix(k,j,i),j=1,3),k=1,3)
#         if(n.ne.i)stop
#      $       'error in numbering of hexagonal point operators'
#       enddo
# * read data for each magnetic space group
#       do i=1,1651
#         read(30,*)(nlabelparts_bns(j,i),j=1,2),nlabel_bns(i),
#      $       spacegroup_label_bns(i),(nlabelparts_og(j,i),j=1,3),
#      $       nlabel_og(i),spacegroup_label_og(i)
#         read(30,*)magtype(i)
#         if(magtype(i).eq.4)then
#           read(30,*)((bnsog_point_op(j,k,i),j=1,3),k=1,3),
#      $         (bnsog_origin(j,i),j=1,3),bnsog_origin_denom(i)
#         endif
#         read(30,*)ops_count(i)
#         read(30,*)(ops_bns_point_op(j,i),(ops_bns_trans(k,j,i),k=1,3),
#      $       ops_bns_trans_denom(j,i),ops_bns_timeinv(j,i),
#      $       j=1,ops_count(i))
#         read(30,*)lattice_bns_vectors_count(i)
#         read(30,*)((lattice_bns_vectors(k,j,i),k=1,3),
#      $       lattice_bns_vectors_denom(j,i),
#      $       j=1,lattice_bns_vectors_count(i))
#         read(30,*)wyckoff_site_count(i)
#         do j=1,wyckoff_site_count(i)
#           read(30,*)wyckoff_pos_count(j,i),wyckoff_mult(j,i),
#      $         wyckoff_label(j,i)
#           do k=1,wyckoff_pos_count(j,i)
#             read(30,*)(wyckoff_bns_fract(m,k,j,i),m=1,3),
#      $           wyckoff_bns_fract_denom(k,j,i),
#      $           ((wyckoff_bns_xyz(m,n,k,j,i),m=1,3),n=1,3),
#      $           ((wyckoff_bns_mag(m,n,k,j,i),m=1,3),n=1,3)
#           enddo
#         enddo
#         if(magtype(i).eq.4)then
#         read(30,*)ops_count(i)
#         read(30,*)(ops_og_point_op(j,i),(ops_og_trans(k,j,i),k=1,3),
#      $       ops_og_trans_denom(j,i),ops_og_timeinv(j,i),
#      $       j=1,ops_count(i))
#         read(30,*)lattice_og_vectors_count(i)
#         read(30,*)((lattice_og_vectors(k,j,i),k=1,3),
#      $       lattice_og_vectors_denom(j,i),
#      $       j=1,lattice_og_vectors_count(i))
#         read(30,*)wyckoff_site_count(i)
#         do j=1,wyckoff_site_count(i)
#           read(30,*)wyckoff_pos_count(j,i),wyckoff_mult(j,i),
#      $         wyckoff_label(j,i)
#           do k=1,wyckoff_pos_count(j,i)
#             read(30,*)(wyckoff_og_fract(m,k,j,i),m=1,3),
#      $           wyckoff_og_fract_denom(k,j,i),
#      $           ((wyckoff_og_xyz(m,n,k,j,i),m=1,3),n=1,3),
#      $           ((wyckoff_og_mag(m,n,k,j,i),m=1,3),n=1,3)
#           enddo
#         enddo
#         endif
#       enddo
# * close data file
#       close(30)
#       end

import os
import numpy

# for the ith nonhexagonal point operator:
# point_op_label(i): point operator symbol (from Litvin)
point_op_label = numpy.zeros(shape=(48, ), dtype='<8U')

# point_op_xyz(i): point operator in x,y,z notation
point_op_xyz = numpy.zeros(shape=(48, ), dtype='<10U')

# point_op_matrix(i): point operator matrix
point_op_matrix = numpy.zeros(shape=(3, 3, 48, ), dtype=int)

# for the ith hexagonal point operator:
# point_op_hex_label(i): point operator symbol (from Litvin)
point_op_hex_label = numpy.zeros(shape=(24, ), dtype='<8U')

# point_op_hex_xyz(i): point operator in x,y,z notation
point_op_hex_xyz = numpy.zeros(shape=(24, ), dtype='<10U')

# point_op_hex_matrix(i): point operator matrix
point_op_hex_matrix = numpy.zeros(shape=(3, 3, 24, ), dtype=int)


# number of magnetic space groups
magcount = 1651

# for the ith magnetic space group
# nlabel_bns(i): numerical label in BNS setting
nlabel_bns = numpy.zeros(shape=(magcount, ), dtype='<12U')

# nlabel_parts_bns(j,i): jth part of nlabel_bns
nlabelparts_bns = numpy.zeros(shape=(2, magcount, ), dtype=int)

# label_bns(i): group symbol
spacegroup_label_bns = numpy.zeros(shape=(magcount, ), dtype='<14U')

# nlabel_og(i): numerical label in OG setting
nlabel_og = numpy.zeros(shape=(magcount, ), dtype='<12U')

# nlabel_parts_og(j,i): jth part of nlabel_og
nlabelparts_og = numpy.zeros(shape=(3, magcount, ), dtype=int)

# label_og(i): group symbol
spacegroup_label_og = numpy.zeros(shape=(magcount, ), dtype='<14U')

# magtype(i): type of magnetic space group (1-4)
magtype = numpy.zeros(shape=(magcount, ), dtype=int)

# BNS-OG transformation (if type-4)
# bnsog_point_op(j,k,i): 3x3 point operator part of transformation
bnsog_point_op = numpy.zeros(shape=(3, 3, magcount, ), dtype=int)

# bnsog_origin(j,i): translation part of transformation
# bnsog_point_origin(i): common denominator
bnsog_origin = numpy.zeros(shape=(3, magcount, ), dtype=int)
bnsog_origin_denom = numpy.zeros(shape=(magcount, ), dtype=int)

# iops_count(i): number of point operators
ops_count = numpy.zeros(shape=(magcount, ), dtype=int)

# wyckoff_count(i): number of wyckoff sites
wyckoff_site_count = numpy.zeros(shape=(magcount, ), dtype=int)

# wyckoff_pos_count(j,i): number of positions in jth wyckoff site
wyckoff_pos_count = numpy.zeros(shape=(27, magcount, ), dtype=int)

# wyckoff_mult(j,i): multiplicity for jth wyckoff site
wyckoff_mult = numpy.zeros(shape=(27, magcount, ), dtype=int)

# wyckoff_label(j,i): symbol (a,b,c,...,z,alpha) for jth wyckoff site
wyckoff_label = numpy.zeros(shape=(27, magcount, ), dtype="<5U")

# for BNS setting
# lattice_bns_vectors_count(i): number of lattice vectors defining the lattice
lattice_bns_vectors_count = numpy.zeros(shape=(magcount, ), dtype=int)

# lattice_bns_vectors(k,j,i): kth component of the jth lattice vector
# lattice_bns_vectors_denom(j,i): common denominator
lattice_bns_vectors = numpy.zeros(shape=(3, 6, magcount, ), dtype=int)
lattice_bns_vectors_denom = numpy.zeros(shape=(6, magcount, ), dtype=int)

# for jth operator
# ops_bns_point_op(j,i): point operator part
ops_bns_point_op = numpy.zeros(shape=(96, magcount, ), dtype=int)

# ops_bns_trans(k,j,i): kth component of translation part
# ops_bns_trans_denom(j,i): common denominator
ops_bns_trans = numpy.zeros(shape=(3, 96, magcount, ), dtype=int)
ops_bns_trans_denom = numpy.zeros(shape=(96, magcount, ), dtype=int)

# ops_bns_timeinv(j,i): 1=no time inversion, -1=time inversion
ops_bns_timeinv = numpy.zeros(shape=(96, magcount, ), dtype=int)

# for jth wyckoff site
# wyckoff_bns_fract(k,j,i): kth component of fractional part of wyckoff
# position
# wyckoff_bns_fract_denom(j,i): common denominator
wyckoff_bns_fract = numpy.zeros(shape=(3, 96, 27, magcount, ), dtype=int)
wyckoff_bns_fract_denom = numpy.zeros(shape=(96, 27, magcount, ), dtype=int)

# wyckoff_bns_xyz(m,k,j,i): mth component to coeffcient of kth paramater
# (x,y,z)
wyckoff_bns_xyz = numpy.zeros(shape=(3, 3, 96, 27, magcount, ), dtype=int)

# wyckoff_bns_mag(m,k,j,i): mth component to coeffcient of kth magnetic
# paramater (mx,my,mz)
wyckoff_bns_mag = numpy.zeros(shape=(3, 3, 96, 27, magcount, ), dtype=int)


# for OG setting (for type-4 groups)
# lattice_og_vectors_count(i): number of lattice vectors defining the lattice
lattice_og_vectors_count = numpy.zeros(shape=(magcount, ), dtype=int)

# lattice_og_vectors(k,j,i): kth component of the jth lattice vector
# lattice_og_vectors_denom(j,i): common denominator
lattice_og_vectors = numpy.zeros(shape=(3, 6, magcount, ), dtype=int)
lattice_og_vectors_denom = numpy.zeros(shape=(6, magcount, ), dtype=int)

# for jth operator
# ops_og_point_op(j,i): point operator part
ops_og_point_op = numpy.zeros(shape=(96, magcount, ), dtype=int)

# ops_og_trans(k,j,i): kth component of translation part
# ops_og_trans_denom(j,i): common denominator
ops_og_trans = numpy.zeros(shape=(3, 96, magcount, ), dtype=int)
ops_og_trans_denom = numpy.zeros(shape=(96, magcount, ), dtype=int)

# ops_og_timeinv(j,i): 1=no time inversion, -1=time inversion
ops_og_timeinv = numpy.zeros(shape=(96, magcount, ), dtype=int)

# for jth wyckoff site
# wyckoff_og_fract(k,j,i): kth component of fractional part of wyckoff position
# wyckoff_og_fract_denom(j,i): common denominator
wyckoff_og_fract = numpy.zeros(shape=(3, 96, 27, magcount, ), dtype=int)
wyckoff_og_fract_denom = numpy.zeros(shape=(96, 27, magcount, ), dtype=int)

# wyckoff_og_xyz(m,k,j,i): mth component to coeffcient of kth paramater (x,y,z)
wyckoff_og_xyz = numpy.zeros(shape=(3, 3, 96, 27, magcount, ), dtype=int)

# wyckoff_og_mag(m,k,j,i): mth component to coeffcient of kth magnetic
# paramater (mx,my,mz)
wyckoff_og_mag = numpy.zeros(shape=(3, 3, 96, 27, magcount, ), dtype=int)


F_MAG_DATA = os.path.join(os.path.dirname(__file__), "magnetic_data.txt")


def read_magnetic_data():
    """Read magnetic data."""
    with open(F_MAG_DATA, "r") as fid:
        l_cont = fid.readlines()
    # read nonhexangonal point operators
    i_line = 0
    for i in range(48):
        l_h = l_cont[i_line].split(); i_line += 1
        n = int(l_h[0])
        point_op_label[i] = l_h[1]
        point_op_xyz[i] = l_h[2]
        point_op_matrix[:, :, i] = numpy.array(l_h[3:3+9], dtype=int).reshape(
            3, 3)
        if n != (i+1):
            break
    # read hexangonal point operators
    for i in range(24):
        l_h = l_cont[i_line].split(); i_line += 1
        n = int(l_h[0])
        point_op_hex_label[i] = l_h[1]
        point_op_hex_xyz[i] = l_h[2]
        point_op_hex_matrix[:, :, i] = numpy.array(l_h[3:3+9], dtype=int
                                                   ).reshape(3, 3)
        if n != (i+1):
            break

    for i in range(magcount):
        l_h = l_cont[i_line].split(); i_line += 1
        nlabelparts_bns[:, i] = numpy.array(l_h[0:2], dtype=int)
        nlabel_bns[i] = l_h[2].strip("\"")
        spacegroup_label_bns[i] = l_h[3].strip("\"")
        nlabelparts_og[:, i] = numpy.array(l_h[4:7], dtype=int)
        nlabel_og[i] = l_h[7]
        spacegroup_label_og[i] = l_h[8].strip("\"")

        l_h = l_cont[i_line].split(); i_line += 1
        magtype[i] = l_h[0]

        if magtype[i] == 4:
            l_h = l_cont[i_line].split(); i_line += 1
            bnsog_point_op[:, :, i] = numpy.transpose(
                numpy.array(l_h[0:9], dtype=int).reshape(3, 3))
            bnsog_origin[:, i] = numpy.array(l_h[9:9+3], dtype=int)
            bnsog_origin_denom[i] = l_h[12]

        l_h = l_cont[i_line].split(); i_line += 1
        ops_count[i] = l_h[0]

        for j in range(ops_count[i]):
            if j % 4 == 0:
                l_h = l_cont[i_line].split(); i_line += 1
            ops_bns_point_op[j, i], ops_bns_trans[0, j, i], \
                ops_bns_trans[1, j, i], ops_bns_trans[2, j, i], \
                ops_bns_trans_denom[j, i], ops_bns_timeinv[j, i] = \
                l_h[0+6*(j % 4)], l_h[1+6*(j % 4)], l_h[2+6*(j % 4)],\
                l_h[3+6*(j % 4)], l_h[4+6*(j % 4)], l_h[5+6*(j % 4)]

        l_h = l_cont[i_line].split(); i_line += 1
        lattice_bns_vectors_count[i] = l_h[0]

        l_h = l_cont[i_line].split(); i_line += 1
        for j in range(lattice_bns_vectors_count[i]):
            lattice_bns_vectors[0, j, i], lattice_bns_vectors[1, j, i], \
                lattice_bns_vectors[2, j, i], \
                lattice_bns_vectors_denom[j, i] = \
                l_h[0+4*j], l_h[1+4*j], l_h[2+4*j], l_h[3+4*j]

        l_h = l_cont[i_line].split(); i_line += 1
        wyckoff_site_count[i] = l_h[0]

        for j in range(wyckoff_site_count[i]):
            l_h = l_cont[i_line].split(); i_line += 1
            wyckoff_pos_count[j, i],  wyckoff_mult[j, i], \
                wyckoff_label[j, i] = l_h[0], l_h[1], l_h[2][1:]

            for k in range(wyckoff_pos_count[j, i]):
                l_h = l_cont[i_line].split(); i_line += 1
                wyckoff_bns_fract[:, k, j, i] = numpy.array(l_h[0:3],
                                                            dtype=int)
                wyckoff_bns_fract_denom[k, j, i] = l_h[3]
                wyckoff_bns_xyz[:, :, k, j, i] = numpy.transpose(
                    numpy.array(l_h[4:13], dtype=int).reshape(3, 3))
                wyckoff_bns_mag[:, :, k, j, i] = numpy.transpose(
                    numpy.array(l_h[13:22], dtype=int).reshape(3, 3))

        if magtype[i] == 4:
            l_h = l_cont[i_line].split(); i_line += 1
            ops_count[i] = l_h[0]

            for j in range(ops_count[i]):
                if j % 4 == 0:
                    l_h = l_cont[i_line].split(); i_line += 1
                ops_og_point_op[j, i], ops_og_trans[0, j, i], \
                    ops_og_trans[1, j, i], ops_og_trans[2, j, i], \
                    ops_og_trans_denom[j, i], ops_og_timeinv[j, i] = \
                    l_h[0+6*(j % 4)], l_h[1+6*(j % 4)], l_h[2+6*(j % 4)], \
                    l_h[3+6*(j % 4)], l_h[4+6*(j % 4)], l_h[5+6*(j % 4)]

            l_h = l_cont[i_line].split(); i_line += 1
            lattice_og_vectors_count[i] = l_h[0]

            l_h = l_cont[i_line].split(); i_line += 1
            for j in range(lattice_og_vectors_count[i]):
                lattice_og_vectors[:, j, i] = numpy.array(l_h[0+4*j:3+4*j],
                                                          dtype=int)
                lattice_og_vectors_denom[j, i] = l_h[3+4*j]

            l_h = l_cont[i_line].split(); i_line += 1
            wyckoff_site_count[i] = l_h[0]

            for j in range(wyckoff_site_count[i]):
                l_h = l_cont[i_line].split(); i_line += 1
                wyckoff_pos_count[j, i], wyckoff_mult[j, i] = l_h[0], l_h[1]
                wyckoff_label[j, i] = l_h[2][1:]

                for k in range(wyckoff_pos_count[j, i]):
                    l_h = l_cont[i_line].split(); i_line += 1
                    wyckoff_og_fract[:, k, j, i] = numpy.array(l_h[0:3],
                                                               dtype=int)
                    wyckoff_og_fract_denom[k, j, i] = l_h[3]
                    wyckoff_og_xyz[:, :, k, j, i] = numpy.transpose(
                        numpy.array(l_h[4:4+9], dtype=int).reshape(3, 3))
                    wyckoff_og_mag[:, :, k, j, i] = numpy.transpose(
                        numpy.array(l_h[13:13+9], dtype=int).reshape(3, 3))


def calc_fract_by_sym_elem(sym_elems, fract):
    """Calculate fraction of atom for given atom and symmetry element."""
    fract_np = numpy.array(fract, dtype=float)

    if len(fract_np.shape) == 1:
        fract_np.resize((3,1))

    f_x, f_y, f_z = fract_np[0], fract_np[1], fract_np[2]
    b_x, b_y, b_z = sym_elems[0], sym_elems[1], sym_elems[2]
    denom = sym_elems[3]
    r_11, r_12, r_13 = sym_elems[4], sym_elems[5], sym_elems[6]
    r_21, r_22, r_23 = sym_elems[7], sym_elems[8], sym_elems[9]
    r_31, r_32, r_33 = sym_elems[10], sym_elems[11], sym_elems[12]

    n_a = numpy.newaxis
    at_x_new = numpy.mod(r_11[:, n_a] * f_x[n_a, :] + r_12[:, n_a] * \
                         f_y[n_a, :] + r_13[:, n_a] * f_z[n_a, :] + \
                             (b_x/denom)[:, n_a], 1.)
    at_y_new = numpy.mod(r_21[:, n_a] * f_x[n_a, :] + r_22[:, n_a] * \
                         f_y[n_a, :] + r_23[:, n_a] * f_z[n_a, :] + \
                             (b_y/denom)[:, n_a], 1.)
    at_z_new = numpy.mod(r_31[:, n_a] * f_x[n_a, :] + r_32[:, n_a] * \
                         f_y[n_a, :] + r_33[:, n_a] * f_z[n_a, :] + \
                             (b_z/denom)[:, n_a], 1.)
    at_new = numpy.array([at_x_new, at_y_new, at_z_new], dtype=float)
    return at_new


def calc_moment_by_sym_elem(sym_elems, moment):
    """Calculate fraction of atom for given atom and symmetry element."""
    moment_np = numpy.array(moment, dtype=float)

    if len(moment_np.shape) == 1:
        moment_np.resize((3,1))

    m_x, m_y, m_z = moment_np[0], moment_np[1], moment_np[2]

    r_11, r_12, r_13 = sym_elems[13], sym_elems[14], sym_elems[15]
    r_21, r_22, r_23 = sym_elems[16], sym_elems[17], sym_elems[18]
    r_31, r_32, r_33 = sym_elems[19], sym_elems[20], sym_elems[21]

    n_a = numpy.newaxis
    # FIXME: multiplication on det(R) is missed.
    m_x_new = r_11[:, n_a] * m_x[n_a, :] + r_12[:, n_a] * m_y[n_a, :] + \
        r_13[:, n_a] * m_z[n_a, :]
    m_y_new = r_21[:, n_a] * m_x[n_a, :] + r_22[:, n_a] * m_y[n_a, :] + \
        r_23[:, n_a] * m_z[n_a, :]
    m_z_new = r_31[:, n_a] * m_x[n_a, :] + r_32[:, n_a] * m_y[n_a, :] + \
        r_33[:, n_a] * m_z[n_a, :]
    m_new = numpy.array([m_x_new, m_y_new, m_z_new], dtype=float)
    return m_new


def get_sym_elem_by_ops(ops, flag_non_hexagonal: bool = True):
    """Get symmetry element by operator.

    oops = [point_group_number, f_x, f_y, f_z, denom, time_inversion]

    flag_non_hexagonal is True for nonhexagonal point group number.
    """
    try:
        size_ops = len(ops[0])  # if ops is list of numpy arrays
    except TypeError:
        size_ops = 1  # if ops is list of numbers

    t_i = ops[5]  # time inversion

    if flag_non_hexagonal:
        val = numpy.reshape(point_op_matrix[:, :, ops[0]-1], (9, size_ops))
    else:
        val = numpy.reshape(point_op_hex_matrix[:, :, ops[0]-1], (9, size_ops))
    res = numpy.array([
        ops[1], ops[2], ops[3], ops[4], val[0], val[1], val[2], val[3], val[4],
        val[5], val[6], val[7], val[8], t_i*val[0], t_i*val[1], t_i*val[2],
        t_i*val[3], t_i*val[4], t_i*val[5], t_i*val[6], t_i*val[7],
        t_i*val[8]], dtype=int)
    return res

def find_i_for_nlabel_bns(part_1: int, part_2: int):
    flag_1 = nlabelparts_bns[0, :] == part_1
    flag_2 = nlabelparts_bns[1, :] == part_2
    flag_3 = flag_1*flag_2
    return int(numpy.argwhere(flag_3))

D_CENTRING_TYPE_SHIFT = {
    "P": numpy.array([[0, 0, 0, 1], ], dtype=int).transpose(),
    "A": numpy.array([[0, 0, 0, 1], [0, 1, 1, 2]], dtype=int).transpose(),    
    "B": numpy.array([[0, 0, 0, 1], [1, 0, 1, 2]], dtype=int).transpose(),    
    "C": numpy.array([[0, 0, 0, 1], [1, 1, 0, 2]], dtype=int).transpose(),    
    "F": numpy.array([[0, 0, 0, 1], [0, 1, 1, 2], [1, 0, 1, 2], [1, 1, 0, 2]],
                     dtype=int).transpose(),    
    "I": numpy.array([[0, 0, 0, 1], [1, 1, 1, 2]], dtype=int).transpose(),    
    "R": numpy.array([[0, 0, 0, 1], [2, 1, 1, 3], [1, 2, 2, 3]],
                     dtype=int).transpose(),    
    "Rrev": numpy.array([[0, 0, 0, 1], [1, 2, 1, 3], [2, 1, 2, 3]],
                        dtype=int).transpose(),    
    "H": numpy.array([[0, 0, 0, 1], [2, 1, 0, 3], [1, 2, 0, 3]],
                     dtype=int).transpose(),    
        }


def get_sym_elems_magn_centering_for_bns(part_1: int, part_2: int):
    """Get symmetry elements for bns space group."""
    i = find_i_for_nlabel_bns(part_1, part_2)
    j = ops_count[i]
    ops = [ops_bns_point_op[:j, i], ops_bns_trans[0, :j, i],
           ops_bns_trans[1, :j, i], ops_bns_trans[2, :j, i],
           ops_bns_trans_denom[:j, i], ops_bns_timeinv[:j, i]]

    flag_non_hexagonal = True  # FIXME
    sym_elems = get_sym_elem_by_ops(ops, flag_non_hexagonal=flag_non_hexagonal)
    
    label = spacegroup_label_bns[i]
    n_shift = D_CENTRING_TYPE_SHIFT[label[0]]
    new_shape = (18, )+n_shift.shape[1:]
    xyz_sym = numpy.zeros(shape=new_shape, dtype=int)
    xyz_sym[0], xyz_sym[4], xyz_sym[8] = 1, 1, 1
    xyz_sym[9], xyz_sym[13], xyz_sym[17] = 1, 1, 1
    magn_centering = numpy.vstack([n_shift, xyz_sym])
    return sym_elems, magn_centering


def get_str_for_sym_elem(sym_elem, labels=("x", "y", "z", "mx", "my", "mz")):
    """Get str for sym element."""
    flag_moment = sym_elem.shape[0] > 12
    sym_elem_zero = 0*sym_elem
    sym_elem_plus_one = sym_elem_zero + 1
    sym_elem_minus_one = sym_elem_zero - 1

    flag_plus_one = sym_elem_plus_one == sym_elem
    flag_minus_one = sym_elem_minus_one == sym_elem

    str_empty = numpy.zeros(shape=sym_elem_zero.shape, dtype='<3U')

    str_empty[4] = numpy.where(flag_plus_one[4], "+"+labels[0], numpy.where(
        flag_minus_one[4], "-"+labels[0], ""))
    str_empty[5] = numpy.where(flag_plus_one[5], "+"+labels[1], numpy.where(
        flag_minus_one[5], "-"+labels[1], ""))
    str_empty[6] = numpy.where(flag_plus_one[6], "+"+labels[2], numpy.where(
        flag_minus_one[6], "-"+labels[2], ""))

    str_empty[7] = numpy.where(flag_plus_one[7], "+"+labels[0], numpy.where(
        flag_minus_one[7], "-"+labels[0], ""))
    str_empty[8] = numpy.where(flag_plus_one[8], "+"+labels[1], numpy.where(
        flag_minus_one[8], "-"+labels[1], ""))
    str_empty[9] = numpy.where(flag_plus_one[9], "+"+labels[2], numpy.where(
        flag_minus_one[9], "-"+labels[2], ""))

    str_empty[10] = numpy.where(flag_plus_one[10], "+"+labels[0], numpy.where(
        flag_minus_one[10], "-"+labels[0], ""))
    str_empty[11] = numpy.where(flag_plus_one[11], "+"+labels[1], numpy.where(
        flag_minus_one[11], "-"+labels[1], ""))
    str_empty[12] = numpy.where(flag_plus_one[12], "+"+labels[2], numpy.where(
        flag_minus_one[12], "-"+labels[2], ""))

    if flag_moment:
        str_empty[13] = numpy.where((flag_plus_one[4]*flag_plus_one[13] | 
                                     flag_minus_one[4]*flag_minus_one[13]),
                                    "+1", "-1")

    char_add = numpy.char.add
    char_strip = numpy.char.strip

    t_x = sym_elem[0]
    t_y = sym_elem[1]
    t_z = sym_elem[2]
    denom = sym_elem[3]

    gcd_x = numpy.gcd(t_x, denom)
    gcd_y = numpy.gcd(t_y, denom)
    gcd_z = numpy.gcd(t_z, denom)

    denom_x, denom_y, denom_z = denom // gcd_x, denom // gcd_y, denom // gcd_z
    t_x_new, t_y_new, t_z_new = t_x // gcd_x, t_y // gcd_y, t_z // gcd_z

    s_t_x_new, s_t_y_new = t_x_new.astype(str), t_y_new.astype(str)
    s_t_z_new = t_z_new.astype(str)

    s_denom_x, s_denom_y = denom_x.astype(str), denom_y.astype(str)
    s_denom_z = denom_z.astype(str)

    s_fract_x = char_add(char_add(s_t_x_new, "/"), s_denom_x)
    s_fract_y = char_add(char_add(s_t_y_new, "/"), s_denom_y)
    s_fract_z = char_add(char_add(s_t_z_new, "/"), s_denom_z)
    
    s_fract_x[numpy.char.startswith(s_fract_x, "0")] = ""
    s_fract_y[numpy.char.startswith(s_fract_y, "0")] = ""
    s_fract_z[numpy.char.startswith(s_fract_z, "0")] = ""

    flag_x = numpy.char.startswith(s_fract_x, "-")
    s_fract_x = numpy.where(flag_x, s_fract_x, char_add("+", s_fract_x))
    flag_y = numpy.char.startswith(s_fract_y, "-")
    s_fract_y = numpy.where(flag_y, s_fract_y, char_add("+", s_fract_y))
    flag_z = numpy.char.startswith(s_fract_z, "-")
    s_fract_z = numpy.where(flag_z, s_fract_z, char_add("+", s_fract_z))

    s_out_f_1 = char_add(char_add(char_add(str_empty[4], str_empty[5]),
                                  str_empty[6]), s_fract_x)
    s_out_f_2 = char_add(char_add(char_add(str_empty[7], str_empty[8]),
                                  str_empty[9]), s_fract_y)
    s_out_f_3 = char_add(char_add(char_add(str_empty[10], str_empty[11]),
                                  str_empty[12]), s_fract_z)

    s_out_f_1 = char_strip(s_out_f_1, "+")
    s_out_f_2 = char_strip(s_out_f_2, "+")
    s_out_f_3 = char_strip(s_out_f_3, "+")

    s_out_fract = char_add(char_add(char_add(char_add(s_out_f_1, ","),
                                             s_out_f_2), ","), s_out_f_3) 
    if flag_moment:
        # s_out_moment = char_add(char_add(char_add(char_add(
        #     s_out_m_1, ","), s_out_m_2), ","), s_out_m_3) 
        # s_out = char_add(char_add(s_out_fract, ";"), s_out_moment)
        s_out = char_add(char_add(s_out_fract, ","), str_empty[13])
    else:
        s_out = s_out_fract
    return s_out


def calc_full_sym_elems(sym_elems, magn_centering):
    """Calculate full list of symmetry elements.
         0      1      2        3     4     5     6     7     8     9
    [num_x, num_y, num_z, den_xyz, r_11, r_12, r_13, r_21, r_22, r_23,
        10   11    12    13    14    15    16    17    18    19    20    21
     r_31, r_32, r_33, m_11, m_12, m_13, m_21, m_22, m_23, m_31, m_32, m_33]
    """
    new_shape = (22, ) + sym_elems.shape[1:] + magn_centering.shape[1:]
    full_sym_elems = numpy.zeros(shape=new_shape, dtype=int)
    full_ones = numpy.ones(shape=(1, ) + sym_elems.shape[1:] + magn_centering.shape[1:], dtype=int)

    n_ax = numpy.newaxis
    for j in range(2):
        full_sym_elems[4+j*9] = \
            magn_centering[4, n_ax, :] * sym_elems[4+j*9, :, n_ax] + \
            magn_centering[5, n_ax, :] * sym_elems[7+j*9, :, n_ax] + \
            magn_centering[6, n_ax, :] * sym_elems[10+j*9, :, n_ax]
        full_sym_elems[5+j*9] = \
            magn_centering[4, n_ax, :] * sym_elems[5+j*9, :, n_ax] + \
            magn_centering[5, n_ax, :] * sym_elems[8+j*9, :, n_ax] + \
            magn_centering[6, n_ax, :] * sym_elems[11+j*9, :, n_ax]
        full_sym_elems[6+j*9] = \
            magn_centering[4, n_ax, :] * sym_elems[6+j*9, :, n_ax] + \
            magn_centering[5, n_ax, :] * sym_elems[9+j*9, :, n_ax] + \
            magn_centering[6, n_ax, :] * sym_elems[12+j*9, :, n_ax]
    
        full_sym_elems[7+j*9] = \
            magn_centering[7, n_ax, :] * sym_elems[4+j*9, :, n_ax] + \
            magn_centering[8, n_ax, :] * sym_elems[7+j*9, :, n_ax] + \
            magn_centering[9, n_ax, :] * sym_elems[10+j*9, :, n_ax]
        full_sym_elems[8+j*9] = \
            magn_centering[7, n_ax, :] * sym_elems[5+j*9, :, n_ax] + \
            magn_centering[8, n_ax, :] * sym_elems[8+j*9, :, n_ax] + \
            magn_centering[9, n_ax, :] * sym_elems[11+j*9, :, n_ax]
        full_sym_elems[9+j*9] = \
            magn_centering[7, n_ax, :] * sym_elems[6+j*9, :, n_ax] + \
            magn_centering[8, n_ax, :] * sym_elems[9+j*9, :, n_ax] + \
            magn_centering[9, n_ax, :] * sym_elems[12+j*9, :, n_ax]
    
        full_sym_elems[10+j*9] = \
            magn_centering[10, n_ax, :] * sym_elems[4+j*9, :, n_ax] + \
            magn_centering[11, n_ax, :] * sym_elems[7+j*9, :, n_ax] + \
            magn_centering[12, n_ax, :] * sym_elems[10+j*9, :, n_ax]
        full_sym_elems[11+j*9] = \
            magn_centering[10, n_ax, :] * sym_elems[5+j*9, :, n_ax] + \
            magn_centering[11, n_ax, :] * sym_elems[8+j*9, :, n_ax] + \
            magn_centering[12, n_ax, :] * sym_elems[11+j*9, :, n_ax]
        full_sym_elems[12+j*9] = \
            magn_centering[10, n_ax, :] * sym_elems[6+j*9, :, n_ax] + \
            magn_centering[11, n_ax, :] * sym_elems[9+j*9, :, n_ax] + \
            magn_centering[12, n_ax, :] * sym_elems[12+j*9, :, n_ax]


    num_x, den_x = rational_sum(
        magn_centering[4, n_ax, :]*sym_elems[0, :, n_ax] +
        magn_centering[5, n_ax, :]*sym_elems[1, :, n_ax] +
        magn_centering[6, n_ax, :]*sym_elems[2, :, n_ax],
        full_ones*sym_elems[3, :, n_ax],
        full_ones*magn_centering[0, n_ax, :], full_ones*magn_centering[3, n_ax, :])

    num_y, den_y = rational_sum(
        magn_centering[7, n_ax, :]*sym_elems[0, :, n_ax] +
        magn_centering[8, n_ax, :]*sym_elems[1, :, n_ax] +
        magn_centering[9, n_ax, :]*sym_elems[2, :, n_ax],
        full_ones*sym_elems[3, :, n_ax],
        full_ones*magn_centering[1, n_ax, :], full_ones*magn_centering[3, n_ax, :])

    num_z, den_z = rational_sum(
        magn_centering[10, n_ax, :]*sym_elems[0, :, n_ax] +
        magn_centering[11, n_ax, :]*sym_elems[1, :, n_ax] +
        magn_centering[12, n_ax, :]*sym_elems[2, :, n_ax],
        full_ones*sym_elems[3, :, n_ax],
        full_ones*magn_centering[2, n_ax, :], full_ones*magn_centering[3, n_ax, :])

    num_xx = num_x*den_y*den_z
    num_yy = num_y*den_x*den_z
    num_zz = num_z*den_x*den_y
    den = den_x*den_y*den_z
    num_xx, num_yy, num_zz = num_xx%den, num_yy%den, num_zz%den
    
    gcd = numpy.gcd.reduce([num_xx, num_yy, num_zz, den])

    full_sym_elems[0] = num_xx // gcd
    full_sym_elems[1] = num_yy // gcd
    full_sym_elems[2] = num_zz // gcd
    full_sym_elems[3] = den // gcd
    
    n_vol = 1
    for val in sym_elems.shape[1:] + magn_centering.shape[1:]:
        n_vol *= val
    
    full_sym_elems_reshape = full_sym_elems.reshape((22, n_vol), order="C")
    full_sym_elems_unique = numpy.unique(full_sym_elems_reshape, axis=1)
    return full_sym_elems_unique


def rational_sum(numerator, denominator, *argv):
    """Sum of rational numbers."""
    if len(argv) < 2:
        gcd = numpy.gcd(numerator, denominator)
        num_out, den_out = numerator//gcd, denominator//gcd, 
    else:
        num_2 = argv[0]
        den_2 = argv[1]
        num_3 = numerator*den_2 + num_2*denominator
        den_3 = denominator*den_2
        gcd = numpy.gcd(num_3, den_3)
        num_out, den_out = rational_sum(num_3//gcd, den_3//gcd, argv[2:])
    return num_out, den_out

def calc_multiplicity(sym_elems, fract_xyz):
    fract_xyz_new = calc_fract_by_sym_elem(sym_elems, fract_xyz)
    fract_xyz_round = numpy.round(fract_xyz_new, 6)
    n_xyz, n_symm, n_at = fract_xyz_round.shape
    multiplicity = numpy.array([numpy.unique(
        fract_xyz_round[:,:,i], axis=1).shape[1] for i in range(n_at)],
        dtype = int)
    return multiplicity
    
read_magnetic_data()

# sym_elems, magn_centering = get_sym_elems_magn_centering_for_bns(71, 536)
# print("sym_elems.shape: ", sym_elems.shape)
# print("magn_centering.shape: ", magn_centering.shape)
# full_sym_elems = calc_full_sym_elems(sym_elems, magn_centering)
# print(get_str_for_sym_elem(sym_elems), end=2*"\n")
# print(get_str_for_sym_elem(magn_centering), end=2*"\n")
# print(get_str_for_sym_elem(full_sym_elems), end=2*"\n")
# fract_xyz = numpy.array([[0.1,0.0,0.0,0.2],
#                          [0.2,0.0,0.5,0.2],
#                          [0.5,0.0,0.5,0.2]], dtype=float)
# print(calc_multiplicity(full_sym_elems, fract_xyz))
# print(calc_multiplicity(full_sym_elems, (0.1, 0.2, 0.5)))
