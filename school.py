# -*- encoding: utf-8 -*-
'''
Created on May 1, 2009

@author: ubs121
'''

from osv import osv, fields
import time

class school_partner(osv.osv):
    _name = "res.partner"
    _inherit = 'res.partner'
    _description = u'res.partner'
    
    _columns = {
        'register_no' : fields.char(u'Улсын бүртгэлийн дугаар', size=11, help=u'Хэрэв энэ харилцагч улсын бүртгэлийн дугаартай бол дугаарыг бөглөнө.'),
    }
school_partner()

class district(osv.osv):
    _description = u"Сум/Дүүрэг"
    _name = 'res.country.district'
    _columns = {
        'state_id': fields.many2one('res.country.state', u'Аймаг/Муж', required=True),
        'name': fields.char(u'Сум/Дүүргийн нэр', size=64, required=True),
        'code': fields.char(u'Сум/Дүүргийн код', size=5, help=u'Сум/Дүүргийн код дээд тал нь 5 үсэгтэй байна.\n'),
    }
district()




class school_year(osv.osv):
    _name = 'school.year'
    _description = u'Хичээлийн жил'
    
    _columns = {
        'name': fields.char(u'Нэр', size=10, required=True, select=True),
        'date_start': fields.date(u'Эхлэл', required=True),
        'date_stop': fields.date(u'Төгсгөл', required=True),
        'term_ids' : fields.one2many('school.term', 'year_id', u'Семестер'),
        'school_id':fields.many2one('res.company', u'Сургууль'),
    }
    
    _order = "date_start"   
    
    def _default_school(self, cr, uid, context={}):
        user = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        if user.company_id:
            return user.company_id.id
        return self.pool.get('res.company').search(cr, uid, [('parent_id', '=', False)])[0]
    
    _defaults = {
        'school_id': _default_school,
    }

    def find(self, cr, uid, dt=None, context={}):
        ''' Өгсөн огноогоор хичээлийн жил хайх
        '''
        if not dt:
            dt = time.strftime('%Y-%m-%d')
            
        ids = self.search(cr, uid, [('date_start', '<=', dt), ('date_stop', '>=', dt)])
        if not ids:
            raise osv.except_osv(_(u'Алдаа !'), _(u'Хичээлийн жил үүсгэх хэрэгтэй !'))
        
        return ids[0]

school_year()
           
class school_term(osv.osv):
    _name = 'school.term'
    _description = u'Семестер'
    
    _columns = {
        'name': fields.char(u'Нэр', size=10, required=True, select=True),
        'date_start': fields.date(u'Эхлэл', required=True),
        'date_stop': fields.date(u'Төгсгөл', required=True),
        'year_id' : fields.many2one('school.year', u'Жил', required=True, select=True),
    }
    
    _order = "date_start"   
    
    def _check_duration(self, cr, uid, ids, context={}):
        obj_period = self.browse(cr, uid, ids[0])
        if obj_period.date_stop < obj_period.date_start:
            return False
        return True

    def _check_year_limit(self, cr, uid, ids, context={}):
        for obj_term in self.browse(cr, uid, ids):
            if obj_term.year_id.date_stop < obj_term.date_stop or \
               obj_term.year_id.date_stop < obj_term.date_start or \
               obj_term.year_id.date_start > obj_term.date_start or \
               obj_term.year_id.date_start > obj_term.date_stop:
                return False

            pids = self.search(cr, uid, [('date_stop', '>=', obj_term.date_start), ('date_start', '<=', obj_term.date_stop), ('id', '<>', obj_term.id)])
            for term in self.browse(cr, uid, pids):
                if term.year_id.school_id.id == obj_term.year_id.school_id.id:
                    return False
        return True
    
    _constraints = [
        (_check_duration, u'Алдаа ! Семестерийн үргэлжлэх хугацаа буруу байна.', ['date_stop']),
        (_check_year_limit, u'Алдаатай семестер ! Зарим семестер давхардсан эсвэл семестерийн эхлэл, төгсгөл хичээлийн жилдээ багтахгүй байна. ', ['date_stop'])
    ]
    
    def find(self, cr, uid, dt=None, context={}):
        ''' Өгсөн огноогоор семестер хайх
        '''
        if not dt:
            dt = time.strftime('%Y-%m-%d')

        ids = self.search(cr, uid, [('date_start', '<=', dt), ('date_stop', '>=', dt)])
        if not ids:
            raise osv.except_osv(_(u'Алдаа !'), _(u'Энэ огноонд тохирох семестер олдсонгүй.'))
        return ids
     
    def close_term(self, cr, uid, ids, context=None):
        print "close_term" 
        return False
    
#    _defaults = {
#        'name': _default_school,
#    }
school_term()


class school_timeperiod(osv.osv):
    _name = 'school.timeperiod'
    _description = u'Цагийн хуваарь'
   
    
    _columns = {
        'name': fields.char(u'Цаг', size=10, required=True, select=True),
        'start_time': fields.datetime(u'Эхлэх цаг', required=True),
        'duration': fields.integer(u'Үргэлжлэх хугацаа', help=u"Хичээл үргэлжлэх хугацааг минутаар заана"),
    }
    
    def _default_duration(self, cr, uid, context={}):
        user = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        if user.company_id:
            return user.company_id.class_duration
        else:
            return 90 # 90 minutes
    
    def _start_time(self, cr, uid, context={}):
        user = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        duration = 90
        recess = 15
        
        if user.company_id:
            duration = user.company_id.class_duration
            recess = user.company_id.class_recess
        
        time_to_add = duration + recess
        
        cr.execute("select max(start_time) + '" + str(time_to_add) + " minutes'::INTERVAL from school_timeperiod")
        res = cr.fetchone()
        if res:
            (str_time,) = res
            return str_time
        else:
            return '08:00'
    
    
        
    
    def _check_intersect(self, cr, uid, ids, context={}):
        # TODO: хоёр цаг огтлолцоогүй болохыг шалгах
        return True
    
    _defaults = {
        'duration': _default_duration,
        'start_time' : _start_time,
    }
    
    _order = "start_time"
    
    _constraints = [
        (_check_intersect, u'Алдаа ! Цагийн хуваарь огтлолцож байна.', ['start_time']),
    ]
    
school_timeperiod()
    
class school_school(osv.osv):
    _name = "res.company"
    _inherit = "res.company"
    _description = u'Сургуулийн Мэдээлэл'
    
    _columns = {
        'name': fields.char(u'Нэр', size=50, required=True),
        'code': fields.char(u'Код', size=7),
        'type':fields.selection([('k12', u'Дунд сургууль'), ('tech', u'МСҮТ'), ('college', u'Коллеж'), ('university', u'Их сургууль')], u'Төрөл'),
        'class_duration': fields.integer(u'Хичээллэх хугацаа (минутаар)'),
        'class_recess': fields.integer(u'Завсарлага (минутаар)'),
        'eval_formula': fields.char(u'Томъёо', size=200, help=u"p1-Шалгалтын оноо, p2-Явцын оноо, p3-Бие даалт, p4-Ирц, p5-Идэвхи утгууд дээр үндэслэн эцсийн үнэлгээг тооцоолох томъёог энд бичнэ. Жишээ нь (p1+p2+p3+p4+p5)/5"),
    }
    
    _defaults = {
        'type': lambda * a: 'college',
        'class_duration': lambda * a: 90, # 90 минут буюу 1:30
        'eval_formula': lambda * a: 'p1*0.3+p2*0.5+p3*0.1+p4*0.1',
    }
school_school()

class school_mark(osv.osv):
    _name = "school.mark"
    _description = u'Үнэлгээ'
    
    _columns = {
        'letter': fields.char(u'Үнэлгээ', size=3, required=True, select=True),
        'gpa': fields.float(u'Оноо', required=True),
        'lo_percent': fields.integer(u'Доод %', required=True),
        'hi_percent': fields.integer(u'Дээд %', required=True),
        'description': fields.text(u'Үнэлгээний тайлбар'),
        'active': fields.boolean(u'Идэвхитэй'),
    }
    _defaults = {
        'active': lambda * a: True,
    }
school_mark()

class school_subject(osv.osv):
    _name = "school.subject"
    _description = u'Хичээл'
    
    _columns = {
        'name':fields.char(u'Нэр', size=60, required=True),
        'code':fields.char(u'Код', size=10),
        'prereq':fields.many2one('school.subject', u'Өмнөх холбоо хичээл',
			help=u'Энэ хичээлийн өмнө заавал судалсан байх ёстой хичээл.'),
        'web_page':fields.char(u'Вэб хуудас', size=150, help=u'Хичээлийн танилцуулга вэб хуудас'),
        'type':fields.selection([('normal', u'Үндсэн хөтөлбөр'), ('practice', u'Дадлага'), ('project', u'Төсөл'), ('exam', u'Улсын Шалгалт')], u'Төрөл'),
        'credit':fields.float(u'Кредит'),
        'notes':fields.text(u'Тэмдэглэл'),
        'active':fields.boolean(u'Идэвхитэй', help=u'Одоо заагдаж байгаа хичээл мөн эсэх'),
    }
    _defaults = {
        'active' : lambda * a: True,
    }
    
    def _check_recursion(self, cr, uid, ids):
        obj_self = self.browse(cr, uid, ids[0])
        if obj_self == obj_self.prereq:
            return False
        while(ids):
            cr.execute('select distinct prereq from school_subject where id in (' + ','.join(map(str, ids)) + ')')
            prereq_ids = filter(None, map(lambda x: x[0], cr.fetchall()))
            if obj_self.id in prereq_ids:
                return False
            ids = prereq_ids
        return True

    constraints = [
        (_check_recursion, u'Алдаа ! Рекурсив өмнөх холбоо үүсгэж болохгүй.', ['id'])
    ]
school_subject()

#class SubjectType(db.Model):
#    ''' Хичээлийн төрөл: лекц, лаб, сем гэх мэт
#    '''
#    
#    type = db.StringProperty(u'Төрөл', choices=('lec', 'lab', 'sem', 'prac'))
#    credit = db.FloatProperty(u'Кредит')
#    subject = db.ReferenceProperty(Subject, collection_name='subject_types')
#    
#    def __unicode__(self):
#        return self.subject.code + '/' + self.type

class school_profession(osv.osv):
    _name = 'school.profession'
    _description = u'Мэргэжил'
    
    _columns = {
        'name':fields.char(u'Нэр', size=50, required=True),
        'code':fields.char(u'Код', size=10),
        'index':fields.char(u'Индекс', size=20, help=u'Боловсролын яамнаас баталсан албан ёсны индекс'),
        'web_page':fields.char(u'Вэб хуудас', size=150, help=u'Мэргэжлийн танилцуулга вэб хуудас'),
        'curr_ids': fields.one2many('school.curriculum', 'prof_id', u'Хөтөлбөрүүд',
			help=u'Энэ мэргэжлээр сургалт явуулах хөтөлбөрүүд'),
		'notes':fields.text(u'Тэмдэглэл'),
    }
school_profession() 
   
class school_curriculum(osv.osv):
    _name = 'school.curriculum'
    _description = u'Сургалтын Хөтөлбөр'
    
    def __total_credit(self, cr, uid, ids, name, args, context):
        res = {}
        for curr in self.browse(cr, uid, ids):
            total = 0.0
            for cl in curr.lines:
                total += cl.credit
            res[curr.id] = total
            
        return res
    
    _columns = {
        'name':fields.char(u'Нэр', size=60),
        'code':fields.char(u'Код', size=5),
        'prof_id' : fields.many2one('school.profession', u'Мэргэжил', required=True),
        'study_type':fields.selection([('normal', u'Өдөр'), ('ext', u'Орой'), ('echnee', u'Эчнээ')], u'Суралцах хэлбэр'),
        'duration':fields.integer(u'Суралцах хугацаа', help=u'Суралцах хугацааг семестерээр заана'),
        'credit': fields.function(__total_credit, method=True, type='float', string=u'Нийт кредит'),
        'lines': fields.one2many('school.curr.line', 'curr_id', u'Хичээлүүд'),
        'degree':fields.selection([('k12', u'Бүрэн Дунд'), ('wrkr', u'Ажилчин'),
                                   ('tech', u'Техникч'), ('dip', u'Дипломын'),
                                   ('B.A', u'Бакалавр'), ('M.A', u'Магистр'),
                                   ('PhD', u'Доктор')], u'Боловсролын Зэрэг'),
    }
    
    _defaults = {
        'duration': lambda * a: 0,
    }
school_curriculum()

class school_curr_line(osv.osv):
    _name = 'school.curr.line'
    _description = u'Хөтөлбөрийн хичээлүүд'
    
    _columns = {
		'sub_id':fields.many2one('school.subject', u'Хичээл', required=True),
        'curr_id':fields.many2one('school.curriculum', u'Хөтөлбөр', required=True),
        'category':fields.selection([('core', u'Үндсэн хөтөлбөр'),
                                     ('project', u'Курсын төсөл'),
                                     ('practice', u'Дадлага'),
                                     ('exam', u'Улсын шалгалт')], u'Ангилал',
			help=u'Ангилал нь дипломын хавсралт болон бусад тайлан дээр хичээлүүдийг эрэмбэлж харуулах, \
				бусад зорилгоор бүлэглэхэд ашиглагдана.'),
        'is_optional':fields.boolean(u'Сонгох хичээл',
			help=u'Заавал судлах бус оюутан сонгон суралцаж болох хичээл юм.'),
        'year':fields.integer(u'Жил', help=u'Хэд дэх жилд судлах'),
        'season':fields.selection([('fall', u'Намар'), ('spring', u'Хавар')], u'Улирал'),
        'credit':fields.float(u'Кредит', help=u'Нийт кредит'),
        'hour1':fields.integer(u'Лекц'),
        'hour2':fields.integer(u'Лаб'),
        'hour3':fields.integer(u'Сем'),
        'hour4':fields.integer(u'Дадлага'),
        'weeks':fields.integer(u'Хугацаа', help=u'Хичээлийн судлах хугацааг 7 хоногоор заана'),
    }
    
    _order = "year, season"
    
    _defaults = {
        'is_optional': lambda * a: False,
        'credit': lambda * a: 0.0,
        'weeks' : 16, # Ихэнхи сургууль нэг улиралд 16 долоо хоногоор нэг хичээлийг судалж байгаа
    }
school_curr_line()

class school_offering(osv.osv):
    _name = "school.offering"
    _description = u'Хичээл төлөвлөлт'
    
    _columns = {
        'name':fields.char(u'Сургалтын нэр', size=20, required=True),
        'term_id':fields.many2one('school.term', u'Семестер', required=True),
        'curr_sub_id':fields.many2one('school.curr.line', u'Хичээл', required=True),
        'curr_id':fields.many2one('school.curriculum', u'Хөтөлбөр'),
        'teacher_id':fields.many2one('hr.employee', u'Заах багш'),
        'date_start': fields.date(u'Эхлэл'),
        'date_stop': fields.date(u'Төгсгөл'),
        'student_limit':fields.integer(u'Оюутны хязгаар'),
    }
    
    _defaults = {
        'name': lambda * a: False,
        # TODO: term_id-д одоогийн семестерийг оноох
    }
school_offering()

class school_classroom_type(osv.osv):
    _name = 'school.classroom.type'
    _columns = {
        'name': fields.char(u'Нэр', required=True, size=46, translate=True),
        'shortcut': fields.char(u'Товчлол', required=True, size=16),
    }
    _order = 'name'
school_classroom_type()

def _classroom_type_get(self, cr, uid, context={}):
    cr.execute("SELECT * FROM school_classroom_type") 
    res = cr.dictfetchall()
    return [(r['shortcut'], r['name']) for r in res] + [('', '')]

class school_classroom(osv.osv):
    _name = "school.classroom"
    _description = u'Өрөө/Танхим'
    
    _columns = {
        'name':fields.char(u'Дугаар/нэр', size=20, required=True),
        'type': fields.selection(_classroom_type_get, u'Өрөөний төрөл', size=32),
        'capacity':fields.integer(u'Хүний багтаамж'),
    }
school_classroom()
