def byteFace(face):
    '''Creates 16 segment typeface, stored as byte arrays, from arbitrary lists of numbers x where 0<=x<=255'''
    compressed = {}
    for key,value in face.items():
        compressed[key]=bytes(value)