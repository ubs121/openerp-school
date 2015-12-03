# -*- encoding: utf-8 -*-
'''
Created on Dec 8, 2009

@author: ubs121
'''
from osv import osv, fields

class school_timetable(osv.osv):
    _name="school.timetable"
    _description=u'Хичээлийн хуваарь'
    
    _columns = {
        'name':fields.char(u'Нэр', size=20, required=True),
        'term_id':fields.many2one('school.term', u'Семестр'),
        'lines' : fields.one2many('school.timetable.line', 'table_id', u'Хуваарь'),
        'current' : fields.boolean(u'Идэвхитэй', help=u'Хичээлийн хуваарийг ашиглаж байгаа бол энэ нүдийг чагтлана. \
			Сургуулийн хувьд нэг семестерт олон хичээлийн хуваарь үүсгэж болох боловч зөвхөн нэг нь тухайн мөчлөгт ашиглагдана.'),
    }
school_timetable()

class school_timetable_line(osv.osv):
    _name="school.timetable.line"
    _description=u'Хичээлийн хуваариуд'
    
    _columns = {
		'table_id':fields.many2one('school.timetable', u'Хуваарь'),
		'week':fields.selection([('mon', u'Даваа'), ('tue', u'Мягмар'), ('wed', u'Лхагва'), ('thu', u'Пүрэв'), ('fri', u'Баасан'), ('sat', u'Бямба'), ('sun', u'Ням')], u'Долоо хоног'),
		'time_period': fields.many2one('school.timeperiod', u'Орох цаг'),
        'sub_id':fields.many2one('school.curr.line', u'Хичээл', required=True),
        'sub_type' : fields.selection([('lec', u'Лекц'), ('sem',u'Семинар'), ('lab', u'Лабораторийн ажил')], u'Хичээлийн хэлбэр'),
        'teacher_id':fields.many2one('hr.employee', u'Багш'),
        'grp_id':fields.many2one('school.student.group', u'Анги/Бүлэг'),        
        'classroom_id':fields.many2one('school.classroom', u'Өрөө'),        
    }
school_timetable_line()
