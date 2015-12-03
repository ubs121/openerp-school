# -*- encoding: utf-8 -*-
'''
Created on Dec 8, 2009

@author: ubs121
'''

from osv import osv, fields

class school_teacher(osv.osv):
    ''' Энэ модуль нь hr.employee моделийг өргөтгөсөн учраас багшийн хүний нөөцтэй холбоотой асуудлууд  автоматаар шийдэгдэнэ.
    '''
    _name = "hr.employee"
    _inherit = 'hr.employee'
    _description = u'Багш'
    
    _columns = {
        'profession': fields.char(u'Мэргэжлийн чиглэл'),
        'degree' : fields.selection([('dip', u'Диплом'), ('B.A', u'Бакалавр'), ('M.A', u'Магистр'), ('PhD', u'Доктор')], u'Эрдмийн зэрэг'),
        'rank' : fields.selection([('lead', u'Тэргүүлэх'), ('ass', u'Зөвлөх'), ('cert', u'Мэргэшсэн'), ('senior', u'Ахлах'), ('prf', u'Профессор')], u'Зэрэглэл'),
        'joined' : fields.date(u"Ажилд орсон огноо"),
        'worked':fields.integer(u'Ажилласан жил'),
        # 'offerings':
    }
school_teacher()

class school_teacher_consummation(osv.osv):
    _name = "school.teacher.consummation"
    _description = u'Багшийн заасан цагийн бүртгэл'
    
    _columns = {
        'name':fields.char(u'Сэдэв', size=20, required=True),
        'subject':fields.many2one('school.curr.line', u'Хичээл', required=True),
        'sub_type' : fields.selection([('lec', u'Лекц'), ('sem', u'Семинар'), ('lab', u'Лабораторийн ажил')], u'Хичээлийн хэлбэр'),
        'teacher':fields.many2one('hr.employee', u'Заасан багш'),
        'date': fields.date(u'Огноо', required=True),
        'time':fields.integer(u'Цагийн тоо'),
        
    }
school_teacher_consummation()
