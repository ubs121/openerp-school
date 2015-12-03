# -*- encoding: utf-8 -*-

'''
Created on Jun 9, 2010

@author: ubs121
'''

"""
@summary: Эцгийн нэрийг харъяалахын тийн ялгалд хувиргаж бүтэн нэрийг буцаана
@param first_name: Эцгийн нэр
@param last_name: Өөрийн нэр 
"""
def fullname(first_name, last_name):
    #FIXME: Зарим нэрс дээр хувиргалт хийхгүй байгааг засах 
    if first_name:
        name = first_name
        if name.endswith(u'й'):
            name = name + u'н'
        elif name.endswith(u'ж') or name.endswith(u'ч') or name.endswith(u'ш'):
            name = name + u'ийн'
        elif name.endswith(u'ь'):
            name = name[0:len(name) - 1] + u'ийн'
        elif name[len(name) - 1] in (u'а', u'о', u'э', u'ө', u'ү', u'у', u'я', u'о', u'е', u'ё'):
            name = name + u'гийн'
        
        name = name + ' ' + last_name
    else:
        name = last_name
        
    return name


def shortname(first_name, last_name):
    if first_name: 
        return first_name[0] + '.' + last_name
    else:
        return last_name 
