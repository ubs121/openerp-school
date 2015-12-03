# -*- encoding: utf-8 -*-
'''
Created on May 1, 2009

@author: ubs121
'''
from osv import osv, fields

class school_gbook(osv.osv):
    _name = 'school.gbook'
    _description = u'Дүнгийн хавтгай'
    
    #TODO: Хичээл сонгогдсон үед eval_by буюу Үнэлгээ өгсөн багшийг автоматаар тохируулах
    
    _columns = {
        'name': fields.char(u'Дүнгийн хавтгай', size=50),
        'term_id':fields.many2one('school.term', u'Семестер', required=True),
        'type':fields.selection([('subject', u'Хичээлийн'), ('exam', u'Шалгалтын'), ('other', u'Бусад')], u'Төрөл'),
        'std_grp':fields.many2one('school.student.group', u'Анги/Бүлэг'),
        # TODO: oferring-д заагдсан хичээл байх ёстой. Гэнэтийн хичээл гэж байхгүй?!
        #'curr_sub_id' : fields.many2one('school.curr.line', u'Сургалт/Хичээл'),        
        'sub_id':fields.many2one('school.subject', u'Хичээл'), # , required=True if type='normal'
        'lines':fields.one2many('school.gbook.line', 'gbook_id', u'Дүнгийн жагсаалт'),
        'eval_formula': fields.char(u'Дүн бодох томъёо', size=100,
			help=u'Энд томъёо оруулахгүй бол сургуулийн үндсэн дүн бодох аргачлалыг ашиглан дүн бодогдоно.'),
        'state': fields.selection([('open', u'Нээлттэй'), ('closed', u'Хаагдсан')], u'Төлөв', readonly=True),
        # TODO: Хичээл заасан багш нь байж болох уу? Дараа нь энэ хүнд журнал засах эрх байх ёстой
        'user_id': fields.many2one('res.users', u'Засах эрх',
			help=u"Дүнгийн хавтгайг засах хоёрдогч этгээд (ихэнхидээ хичээл заасан багш)", readonly=True),
        'notes':fields.text(u'Тэмдэглэл'),
        
        'eval_date':fields.datetime(u'Огноо'),
        'eval_by':fields.many2one('hr.employee', u'Дүгнэсэн багш', readonly=True),
    }
    
    _defaults = {
        'state' : lambda * a : 'draft',
        'term_id':1,
        'type' : lambda * a : 'normal',
        'user_id':lambda self, cr, uid, ctx : uid,
        'eval_formula' : lambda self, cr, uid, context: \
                self.pool.get('res.users').browse(cr, uid, uid,
                    context=context).company_id.eval_formula,
    }

    def close(self, cr, uid, ids, context=None):
        for gb in self.browse(cr, uid, ids):
            cr.execute("UPDATE school_gbook_line SET state = 'valid' WHERE gbook_id = %s" % (gb.id))
            cr.execute("UPDATE school_gbook SET state = 'valid' WHERE id = %s" % (gb.id))
        return True
    
    def open(self, cr, uid, ids, context=None):
        for gb in self.browse(cr, uid, ids):
            cr.execute("UPDATE school_gbook SET state = 'draft' WHERE id = %s" % (gb.id))
        return True
        
#    def write(self, cr, uid, ids, vals, context=None):
#        if not context:
#            context = {}
#            
#        for gb in self.browse(cr, uid, ids):
#            cr.execute("""
#                UPDATE school_gbook 
#                SET state = 
#                    case 
#                    when (select count(*) from school_gbook_line where gbook_id=%s and state='draft')>0 then 'draft'
#                    else 'valid'
#                    end
#                WHERE id = %s
#                """ % (gb.id, gb.id))
#
#        return super(school_gbook, self).write(cr, uid, ids, vals, context=context)
    
school_gbook()

class school_gbook_line(osv.osv):
    _name = 'school.gbook.line'
    _description = u'Дүн'
    
    def _mark(self, cr, uid, ids, name, args, context):
        res = {}
        for line in self.browse(cr, uid, ids):
            res[line.id] = (line.total * 2 >= line.std_id.curr_id.duration)
            
        return res
    
    def _get_term(self, cr, uid, ids, args, context):
        res = {}
        for line in self.browse(cr, uid, ids):
            res[line.id] = line.gbook_id.term_id
            
        return res
    
    def _get_general_gbook(self, cr, uid, context):
        self.pool.get('school.gbook').find(cr, uid)
        
    def _calc_point(self, cr, uid, ids, name, args, context={}):
        res = {}
        #FIXME: Дүн бодолтыг засах
        #for gb_line in self.browse(cr, uid, ids):
#            formula = gb_line.gbook_id.eval_formula
#            p1 = gb_line.p1
#            p2 = gb_line.p2
#            p3 = gb_line.p3
#            p4 = gb_line.p4
#            p5 = gb_line.p5
            
            #TODO: Ерөнхий оноог заасан томъёогоор бодох!!!
            #res[gb_line.id] = float(eval(formula))
        return res
        
    _columns = {
		'gbook_id': fields.many2one('school.gbook', u'Дүнгийн хавтгай', required=True,
			help=u'Дүнгийн хавтгай заавал заах хэрэгтэй, \
				Хэрэв боломжгүй бол "Ерөнхий журнал" гэсэн дүнгийн хавтгай үүсгэж хэрэглэж болно'),
        'std_id':fields.many2one('school.student', u'Оюутан', required=True),
        # TODO: Сургалтын төлөвлөгөөнд заагдсан хичээл байх ёстой!
        # Сургалтын төлөвлөгөөнөөс гадуур хичээл судалж болохгүй!
        #'curr_sub_id':fields.many2one('school.curr.line', u'Сургалтын төлөвлөгөөнд заасан хичээл', required=True),
        'sub_id':fields.many2one('school.subject', u'Хичээл'),
        'term_id':fields.function(_get_term, type='many2one', string=u'Семестер', method=True),
        
        # Онооны задаргаа
        'p1':fields.float(u'Шалгалт'),
        'p2':fields.float(u'Явц'),
        'p3':fields.float(u'Бие даалт'),
        'p4':fields.float(u'Ирц'),
        'p5':fields.float(u'Идэвхи'),
        
        # Ерөнхий оноо
        'point':fields.function(_calc_point, type='float', string=u'Ерөнхий оноо', method=True, store=True),
        'mark':fields.char(u'Үнэлгээ', size=3),
        
        'state':fields.selection([('draft', u'Ноорог'), ('valid', u'Баталсан')], u'Төлөв'),
        'notes':fields.text(u'Тэмдэглэл'),
        
        'edited_date':fields.datetime(u'Зассан Огноо', readonly=True),
        'edited_by':fields.many2one('res.users', u'Засварласан', readonly=True, help=u"Зассан хэрэглэгч"),
    }
    
   # _order = "term_id desc"
    
    _defaults = {
        'point' : lambda * a : 0,
        'state' : lambda * a : 'draft',
        'edited_by': lambda obj, cr, uid, context: uid,
    }
    
    def _check_std_id(self, cr, uid, ids):
        for gbl in self.browse(cr, uid, ids):
            cr.execute("SELECT gbook_id FROM school_gbook_line WHERE id = %s" % (gbl.id))
            gb_id = cr.dictfetchall()[0]
            print gb_id 
            cr.execute("SELECT count(std_id) FROM school_gbook_line WHERE gbook_id = %s GROUP BY std_id" % (gb_id['gbook_id'])) 
            res = cr.dictfetchall()
            for r in res:
                print r['count']
                if r['count'] > 1:
                    return False
        return True
        
    _constraints = [
        (_check_std_id, u'Алдаа ! Оюутан давхардаж орсон байна. Устгана уу ', ['std_id'])
    ]
   
#    def write(self, cr, uid, ids, vals, context=None):
#        if not context:
#            context = {}
#        print "*********************"    
#        for gb_line in self.browse(cr, uid, ids):
#            print gb_line 
#            if gb_line.state == 'draft':
#                print "draft"
#                cr.execute("""
#                    UPDATE school_gbook 
#                    SET state = 'draft'
#                    WHERE id = %s
#                    """ % (gb_line.gbook_id.id))
#
#        return super(school_gbook_line, self).write(cr, uid, ids, vals, context=context)
    
school_gbook_line()
