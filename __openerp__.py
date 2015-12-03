# -*- encoding: utf-8 -*-

{
    'name': u'School Management',
    'version': '1.0',
    'category': 'Generic Modules/School',
    'description': """
        Сургуулиудад зориулагдсан модуль:
            Хичээлийн жил, семестер
            Сургалт, Хичээл төлөвлөлт, Хичээл, Сургалтын хөтөлбөр
            Багш нарын бүртгэл
            Оюутны бүртгэл, мэдээлэл
            Анги төлөвлөлт
            Дүн, Сурлага, Сурлагын амжилт, чанар
            Хичээлийн хуваарь
            Тайлан (ДБ1-ДБ12)
            Дипломын хавсралт
    """,
    'author': 'ubs121',
    'website': '',
    'depends': ['base', 'contacts', 'hr'],
    'init_xml': [],
    'update_xml': ['school_view.xml',
                   'school_sequence.xml',
                   'employee_view.xml',
                   'student_view.xml',
                   'gradebook_view.xml',
                   'timetable_view.xml',
                   'security/school_security.xml',
                   'data/tchr_prof.xml',
                   'data/teacher.xml'
                   ],
    'demo_xml': [
                 'data/school.xml',
                 'data/teacher.xml',
                 'data/classroom.xml',
                ],
    'installable': True,
    'active': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
