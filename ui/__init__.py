a = (('animatic', None, 'NYS', None, None, 'CLOSED', None, None, None), ('sh001', 'durgesh.n', 'TWIP', 1, 77, 'CLOSED', None, None, None), ('sh002', 'amol.r', 'NYS', 1, 100, 'CLOSED', None, None, None), ('sh003', 'amol.r', 'NYS', 1, 100, 'CLOSED', None, None, None), ('sh004', 'prafull.s', 'NYS', 11, 56, 'CLOSED', None, None, None), ('sh005', 'prafull.s', 'NYS', 1, 39, 'CLOSED', None, None, None), ('sh006', 'prafull.s', 'NYS', 9, 46, 'CLOSED', None, None, None))



for e in a:
    if 'sh001' in e:
        print e[2], e[1]



