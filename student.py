# -*- encoding: utf-8 -*-
'''
Created on May 3, 2009

@author: ubs121
'''

from osv import osv, fields
import time
import name_util

class school_student_adm(osv.osv):
    _name = "school.student.adm"
    _description = u"Оюутны Элсэлт"
    _columns = {
        'admitted_date':fields.date(u'Бүртгэсэн огноо'),
        'pre_enroll':fields.selection([('k8', u'8 жилийн сургууль'),
                                       ('k12', u'12 жилийн сургууль'),
                                       ('tech', u'МСҮТ'),
                                       ('college', u'Коллеж'),
                                       ('university', u'Их сургууль'),
                                       ('non-worker', u'Ажилгүй'),
                                       ('worker', u'Ажил эрхэлж байсан'),
                                       ('other', u'Бусад')],
                                       u'Өмнөх ажил/сургууль'),
        'k12_school': fields.char(u'Төгссөн дунд сургууль', size=128),
        'k12_score':fields.float(u'Дунд сургууль төгссөн үнэлгээ'),
        'k12_date':fields.date(u'Дунд сургууль төгссөн огноо'),
        'k12_diploma':fields.date(u'Дунд сургуулийн гэрчилгээ'),
        'notes':fields.text(u'Тэмдэглэл'),
    }
    _defaults = {
        'admitted_date' : lambda * a : time.strftime("%Y-%m-%d"),
    }
school_student_adm()



class school_student_group(osv.osv):
    _name = "school.student.group"
    _description = u'Оюутны бүлэг'
    
    def _is_graduate(self, cr, uid, ids, name, args, context):
        res = {}
        for grp in self.browse(cr, uid, ids):
            res[grp.id] = (grp.cls * 2 >= grp.curr_id.duration)
            
        return res
    _columns = {
        'code' : fields.char(u'Код', size=10),
        'name' : fields.char(u'Нэр', size=60, required=True),
        # 'leader':fields.many2one('school.student', u'Ангийн ахлагч'),
        'ass_teacher':fields.many2one('hr.employee', u'Зөвлөх багш'),
        'curr_id':fields.many2one('school.curriculum', u'Хөтөлбөр', required=True),
        'cls':fields.integer(u'Анги'),
        'is_graduate': fields.function(_is_graduate, method=True, type='boolean', string=u'Төгсөх анги'),
        'year_id':fields.many2one('school.year', u'Хичээлийн жил'),
        'pre_group':fields.many2one('school.student.group', u'Өмнөх бүлэг'),
        'tuition_amount':fields.float(u'Сургалтын төлбөрийн хэмжээ'),
        'notes':fields.text(u'Тэмдэглэл'),
        'members':fields.one2many('school.student', 'grp_id', u'Ангийн гишүүд'),
    }
    _defaults = {
        'cls' : lambda * a: 0,
        'tuition_amount': lambda * a: 0.0,
    }
school_student_group()

class res_partner(osv.osv):
    _name = "res.partner"
    _inherit = 'res.partner'
    _description = u'Контакт'
    
    _columns = {
        'reg_id':fields.char(u'Регистр', size=20),
        'gender': fields.selection([('', ''), ('male', u'Эр'), ('female', u'Эм')], u'Хүйс'),
        'rel_contacts':fields.one2many('res.partner', 'partner_id', u'Холбоотой контактууд'),
        'partner_id': fields.many2one('res.partner', u'Контакт', ondelete='cascade'),
        'std_relation' : fields.selection([('father', u'Аав'),
                                           ('mother', u'Ээж'),
                                           ('brother', u'Ах'),
                                           ('sister', u'Эгч'),
                                           ('husband', u'Нөхөр'),
                                           ('wife', u'Эхнэр'),
                                           ('relative', u'Хамаатан')], u'Хэн болох'),
    }
res_partner()

class school_student(osv.osv):
    _name = "school.student"
    _inherits = {'res.partner' : 'partner_id'}
    _description = u'Оюутан'
    
    def _std_class(self, cr, uid, ids, name, args, context):
        res = {}
        for std in self.browse(cr, uid, ids):
            cr.execute('select max(cls) as cls from school_student_year where std_id=%s', (std.id,))
            res[std.id] = cr.fetchone()[0]
            
        return res
    
    def _calc_gpa(self, cr, uid, ids, name, args, context):
        # FIXME: алдаатай байгааг засах
        res = {}
        
        for std in self.browse(cr, uid, ids):
            cr.execute('select sum(g.point*coalesce(s.credit, 0.0))/sum(coalesce(s.credit, 0.0)) as gpa ' \
                            'from school_gbook_line g, school_subject s ' \
                            'where g.std_id=%s and g.sub_id=s.id', (std.id,))
            res[std.id] = cr.fetchone()[0]
            
        return res
    
    def _calc_gsa(self, cr, uid, ids, name, args, context):
        # FIXME: алдаатай байгааг засах
        res = {}
        for std in self.browse(cr, uid, ids):
            cr.execute('select avg(point) as gsa from school_gbook_line where std_id=%s', (std.id,))
            res[std.id] = cr.fetchone()[0]
            
        return res
    
    def _calc_credit(self, cr, uid, ids, name, args, context):
        # FIXME: алдаатай байгааг засах
        res = {}
        for std in self.browse(cr, uid, ids):
            cr.execute('select sum(coalesce(s.credit, 0.0)) as cr ' \
                        'from school_gbook_line g, school_subject s ' \
                        'where g.std_id=%s and g.sub_id=s.id', (std.id,))
            res[std.id] = cr.fetchone()[0]
            
        return res
    def _is_graduate(self, cr, uid, ids, name, args, context):
        res = {}
        for std in self.browse(cr, uid, ids):
            res[std.id] = (std.cls * 2 >= std.curr_id.duration)
        return res
    
    _columns = {
        'partner_id':fields.many2one('res.partner', u'Оюутан', required=True, ondelete="cascade"),
        'code':fields.char(u'Оюутны код', size=12, required=True, select=True, readonly=True),
        # 'name_en':fields.char(u'Оюутны нэр(Англи)', size=40),
        'curr_id':fields.many2one('school.curriculum', u'Мэргэжил'),
        'curr_name':fields.char(u'Мэргэшил', size=200),  # зарим үед өөгрөөр нэрлэж болно
#        'cls':fields.function(_std_class, method=True, string=u'Анги', type='integer', store=True),
        'cls':fields.integer(u'Анги', default=0),
        'is_graduate':fields.boolean(u'Төгсөх курс эсэх'),
        'gpa':fields.function(_calc_gpa, method=True, string=u'GPA', type='float', store=True),
        'gsa':fields.function(_calc_gsa, method=True, string=u'GSA', type='float', store=True),
        'credit':fields.function(_calc_credit, method=True, string=u'Кредит', type='float', store=True),
        'presense' : fields.selection([('present', u'Байгаа'), ('absent', u'Чөлөөтэй'), ('left', u'Гарсан')], u'Төлөв'),
        'status' : fields.selection([('end', u'Сургууль төгссөн'),
                                     ('travel', u'Өөр сургуульд шилжсэн'),
                                     ('outer', u'Гадаадад суралцахаар явсан'),
                                     ('baldly', u'Сургалтын төлбөрөө төлөөгүйгээс'),
                                     ('bad', u'Сурлагаар хасагдсан'),
                                     ('discipline', u'Сахилгаар хасагдсан'),
                                     ('l_other', u'Бусад шалтгаанаар')],
                                      u'Шалтгаан'),
        'admission':fields.many2one('school.student.adm', u'Элсэлт'),
        'history':fields.one2many('school.student.year', 'std_id', u'Түүх'),
        'gradebook':fields.one2many('school.gbook.line', 'std_id', u'Дүнгийн хүснэгт'),
        'grp_id':fields.many2one('school.student.group', u'Групп'),
         # Элсэлт
        'admitted_date':fields.date(u'Бүртгэсэн огноо', required=True),
        'pre_enroll':fields.selection([('other_school', u'Өөр сургуулиас шилжиж ирсэн'),
                                       ('foreign_std', u'Гадаад суралцагчидаас шилжиж ирсэн'),
                                       ('new_std', u'Шинээр шилжиж ирсэн'),
                                       ('worker', u'Ажил эрхэлж байсан'),
                                       ('k8', u'Суурь боловсрол'),
                                       ('k12', u'Бүрэн дунд боловсрол'),
                                       ('tech', u'МСҮТ'),
                                       ('college', u'Коллеж'),
                                       ('university', u'Их сургууль'),
                                       ('non-worker', u'Ажилгүй'),
                                       ('worker', u'Ажил эрхэлж байсан'),
                                       ('a_other', u'Бусад')],
                                       u'Өмнөх ажил/сургууль'),
        'k12_school': fields.char(u'Сургуулийн нэр', size=128),
        'k12_score':fields.float(u'Үнэлгээ'),
        'k12_date':fields.date(u'Төгссөн огноо'),
        'k12_diploma':fields.date(u'Гэрчилгээ'),
        'living_address':fields.selection([
                                           ('home', u'Өөрийн гэрт'),
                                        ('sc_dorm', u'Сургуулийн дотуур байранд'),
                                       ('other_dorm', u'Бусад сургуулийн дотуур байранд'),
                                       ('rel', u'Хамаатныд'),
                                       ('rent', u'Байр хөлсөлдөг'),
                                       ('other', u'Бусад'),
                                       ],
                                       u'Хаана амьдардаг'),
        
        # ар гэр
        'family_head':fields.boolean(u'Өрх толгойлдог'),
        'marital': fields.selection([('maried', u'Гэрлэсэн'), ('unmaried', u'Гэрлээгүй'), ('divorced', u'Салсан'), ('other', u'Бусад')], u'Гэрлэлт', size=32),
        'family_members':fields.integer(u'Ам бүлийн тоо'),
        'fatherless':fields.boolean(u'Эцэггүй'),
        'motherless':fields.boolean(u'Эхгүй'),
        'family_income':fields.float(u'Өрхийн орлого'),
        'herder_family':fields.boolean(u'Малчин өрх'),
        'poor_family':fields.boolean(u'Нэн ядуу өрх'),
    }
    
    _defaults = {
        'code': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'school.student'),
        'presense' : lambda * a: 'present',
        'is_company': False,
        'customer': True,
        'cls' : lambda * a: 0,
        'pre_enroll' : lambda * a: 'k12',
        'admitted_date':lambda * a: time.strftime('%Y-%m-%d')
    }
    
    def fullname(self, cr, user, ids, context={}):
        ''' Эцгийн нэрийг харъяалахын тийн ялгалд хувирган оюутны бүтэн нэрийг буцаана.
        Жнь: "Сүхбаатар Ууганбаяр" нэрийг "Сүхбаатарын Ууганбаяр"
        '''
        if not len(ids):
            return []
        
        res = []
        for r in self.read(cr, user, ids, ['name']):
            res.append((r['id'], name_util.fullname(r['name'], r['name'])))
        return res
    
    def grade_up(self, cr, uid, ids, context):
        ''' Оюутныг анги дэвшүүлэх
        '''
        # TODO: Student.grade_up()
        ''' Анги дэвшихийн тулд 
        - төлбөрийн тооцоогүй байх
        - сурлагаар тэнцэх
        - сахилга батаар тэнцэх
        '''
        pass
    
    def graduate(self, cr, uid, ids, context):
        ''' Оюутныг төгсгөх
        '''
        # TODO: Student.do_graduate()
        pass
    
    def onchange_grp(self, cr, uid, ids, grp_id, context={}) :
        res = {}
        if not grp_id :
            res['curr_id'] = False
            res['cls'] = 0
        else :
            grp = self.pool.get('school.student.group').browse(cr, uid, grp_id)
            res['curr_id'] = grp.curr_id.id
            res['cls'] = grp.cls
        return {'value':res}
    

    
school_student()

class school_student_year(osv.osv):
    _name = 'school.student.year'
    _description = u'Оюутны түүх (жил бүрээр)'
    
    def _calc_gpa(self, cr, uid, ids, name, args, context):
        res = {}
        for sy in self.browse(cr, uid, ids):
            # fn_gpa функцийг солих???
            rows = cr.execute('select sum(g.point*coalesce(s.credit, 0.0))/sum(coalesce(s.credit, 0.0)) as gpa ' \
                            'from school_gbook_line g, school_subject s ' \
                            'where g.std_id=%s and g.sub_id=s.id and ' \
                            'term_id in (select id from school_term where year_id=%s)',
                            (sy.id, sy.year_id))
            res[sy.id] = rows[0]['gpa']
            
        return res
    
    def _calc_gsa(self, cr, uid, ids, name, args, context):
        res = {}
        for sy in self.browse(cr, uid, ids):
            rows = cr.execute('select avg(point) as gsa ' \
                            'from school_gbook_line where std_id=%s and ' \
                            'term_id in (select id from school_term where year_id=%s)',
                            (sy.id, sy.year_id))
            res[sy.id] = rows[0]['gsa']
            
        return res
    
    def _calc_credit(self, cr, uid, ids, name, args, context):
        res = {}
        for sy in self.browse(cr, uid, ids):
            rows = cr.execute('select sum(coalesce(s.credit, 0.0)) as cr' \
                            'from school_gbook_line g, school_subject s ' \
                            'where g.std_id=%s and g.sub_id=s.id and ' \
                            'term_id in (select id from school_term where year_id=%s)',
                            (sy.id, sy.year_id))
            res[sy.id] = rows[0]['cr']
        
        return res
    
    _columns = {
        'std_id':fields.many2one('school.student', u'Оюутан'),
        'year_id':fields.many2one('school.year', u'Хичээлийн жил'),
        'curr_id':fields.many2one('school.curriculum', u'Мэргэжил'),
        'cls':fields.integer(u'Анги'),
        'gpa':fields.function(_calc_gpa, method=True, string=u'GPA', type='float', store=True),
        'gsa':fields.function(_calc_gsa, method=True, string=u'GSA', type='float', store=True),
        'credit':fields.function(_calc_credit, method=True, string=u'Кредит', type='float', store=True),
        'std_grp':fields.many2one('school.student.group', u'Групп'),
        'is_paid':fields.boolean(u'Төлбөр төлсөн'),
        'tuition_type':fields.selection([('self', u'Хувиараа'), ('gov_loan', u'Төрийн сангийн зээл'),
                        ('sc_disc', u'Сургуулийн хөнгөлөлтөөр'), ('gov_wrk', u'Төрийн албан хуулийн дагуу төрийн зардлаар'),
                        ('gov_help', u'Төрөөс үзүүлэх буцалтгүй тусламжаар'), ('poor', u'Нэн ядуу'),
                        ('herd', u'Малчны хүүхэд'), ('gov', 'Монгол улсын зардлаар'),
                        ('foreign', u'Гадаад улсын зардлаар'), ('other', u'Бусад')], u'Төлбөрийн Хэлбэр'),
    }
    _order = "cls desc"
school_student_year()

class school_student_behavior(osv.osv):
    _name = 'school.student.behavior'
    _description = u'Оюутны зан төрх'
    _columns = {
        'std_id':fields.many2one('school.student', u'Оюутан'),
        'behavior':fields.text(u'Илэрсэн зан төрх'),
        'occured_date':fields.date(u'Илэрсэн огноо'),
        'level':fields.selection([('high', u'Маш өндөр'), ('above normal', u'Хэвийнээс өндөр'), ('normal', u'Хэвийн')], u'Түвшин'),
    }
school_student_behavior()

class school_diploma(osv.osv):
    _name = 'school.diploma'
    _description = u'Диплом'
    _columns = {
        'partner_id':fields.many2one('res.partner', u'Төгсөгч', required=True),
        'no':fields.char(u'Дугаар', size=15),
        'reg':fields.char(u'Бүртгэлийн дугаар', size=15),
        'reg_date':fields.date(u'Бүртгэсэн огноо'),
        'thesis':fields.char(u'Төгсөлтийн ажлын сэдэв', size=250),
        'thesis_en':fields.char(u'Төгсөлтийн ажлын сэдэв(Англиар)', size=250),
        'point':fields.integer('Оноо'),
        'mark':fields.char('Үнэлгээ', size=3),
        'signature1':fields.char(u'Гарын үсэг1', size=250),
        'signature2':fields.char(u'Гарын үсэг2', size=250),
        'school_id':fields.many2one('res.company', u'Сургууль'),
    }
school_diploma()
