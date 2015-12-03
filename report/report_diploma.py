# -*- encoding: utf-8 -*-
'''
Created on May 12, 2009

@author: ubs121
'''

from report import report_sxw
import netsvc
import pooler
import time


logger = netsvc.Logger()

mn2lat = {
 u'А':'A',
 u'Б':'B',
 u'В':'V',
 u'Г':'G',
 u'Д':'D',
 u'Е':'E',
 u'Ё':'Yo',
 u'Ж':'J',
 u'З':'Z',
 u'И':'I',
 u'К':'K',
 u'Л':'L',
 u'М':'M',
 u'Н':'N',
 u'О':'O',
 u'Ө':'U',
 u'П':'P',
 u'Р':'R',
 u'С':'S',
 u'Т':'T',
 u'У':'U',
 u'Ү':'U',
 u'Ф':'F',
 u'Х':'H',
 u'Ц':'Ts',
 u'Ш':'Sh',
 u'Ч':'Ch',
 u'Й':'I',
 u'Ь':'I',
 u'Ъ':'I',
 u'Э':'E',
 u'Ю':'Yu',
 u'Я':'Ya',
 u'Ы':'I',
 
 u'а':'a',
 u'б':'b',
 u'в':'v',
 u'г':'g',
 u'д':'d',
 u'е':'e',
 u'ё':'yo',
 u'ж':'j',
 u'з':'z',
 u'и':'i',
 u'К':'k',
 u'л':'l',
 u'м':'m',
 u'н':'n',
 u'о':'o',
 u'ө':'u',
 u'п':'p',
 u'р':'r',
 u'с':'s',
 u'т':'t',
 u'у':'u',
 u'ү':'u',
 u'ф':'f',
 u'х':'h',
 u'ц':'ts',
 u'ш':'sh',
 u'ч':'ch',
 u'й':'i',
 u'ь':'i',
 u'ъ':'i',
 u'э':'e',
 u'ю':'yu',
 u'я':'ya',
 u'ы':'i',
}

class report_diploma(report_sxw.rml_parse):
    ''' TODO: Сургууль бүрт тохируулж дипломын хавсралт хэвлэх шинэ модуль 
    хийгдэх учраас энэ тайланг (дипломын хавсралт) ерөнхий шинжтэй болгох 
    '''
    
    def __init__(self, cr, uid, name, context):
        super(report_diploma, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'get_grid': self.get_grid,
            'get_his_or_her': self.get_his_or_her,
            'name2eng': self.name2eng,
        })
        self.context = context
    
    def name2eng(self, name):
        name_en = u''
        for c in name:
            if c in mn2lat:
                name_en = name_en + mn2lat[c]
            else:
                name_en = name_en + c
                
        return name_en
    
    def get_his_or_her(self, std):
        return 'her' if std.gender == 'f' else 'his'
     
    def get_grid(self, std, lang='mn'):
        row_count = 50
        
        # init
        grid = []
            
        for i in range(0, row_count + 1):
            grid.append({'no':'', 'name':'', 'name_en':'', 'mark':'', 'credit':'',
                        'no1':'', 'name1':'', 'name1_en':'', 'mark1':'', 'credit1':''})
        
        if lang == 'mn':
            # Үндсэн хөтөлбөрийн хичээлүүд
            self.cr.execute("select s.name, s.credit, g.point, g.mark " \
                            "from school_gbook_line g, school_subject s " \
                            "where g.sub_id=s.id and g.std_id=%s and s.type=%s " \
                            "order by s.type, s.name" , (std.id, 'normal'))
            
            rs = self.cr.fetchall()
            grid[0] = {'no':'I.', 'name':u'Үндсэн хөтөлбөр', 'credit':u'Кр', 'mark':u'Үнэлгээ'}
            i = 1 # grid мөрийн дугаарлалт
            no = 1 # дотоод дугаарлалт
            r_i = 0
            while i <= row_count and r_i < len(rs):
                grid[i]['no'] = no
                grid[i]['name'] = rs[r_i][0]
                grid[i]['credit'] = rs[r_i][1]
                grid[i]['mark'] = '%s(%s)' % (rs[r_i][2], rs[r_i][3])
                    
                no = no + 1
                i = i + 1
                r_i = r_i + 1
            
            # next column
            if i > row_count:
                i = 0
                while r_i < len(rs):
                    grid[i]['no1'] = no
                    grid[i]['name1'] = rs[r_i][0]
                    grid[i]['credit1'] = rs[r_i][1]
                    grid[i]['mark1'] = '%s(%s)' % (rs[r_i][2], rs[r_i][3])
                    no = no + 1
                    i = i + 1
                    r_i = r_i + 1
            else:
                i = 0
                    
                    
            # Курсын төсөл
            self.cr.execute("select s.name, s.credit, g.point, g.mark " \
                            "from school_gbook_line g, school_subject s " \
                            "where g.sub_id=s.id and g.std_id=%s and s.type=%s " \
                            "order by s.type, s.name" , (std.id, 'project'))
            rs = self.cr.fetchall()
            
            i = i + 1
            grid[i]['no1'] = 'II.' 
            grid[i]['name1'] = u'Курсын Төсөл' 
            grid[i]['mark1'] = u'Үнэлгээ'
            no = 1
            r_i = 0
            i = i + 1
            while r_i < len(rs):
                grid[i]['no1'] = no
                grid[i]['name1'] = rs[r_i][0]
                grid[i]['mark1'] = '%s(%s)' % (rs[r_i][2], rs[r_i][3])
                no = no + 1
                i = i + 1
                r_i = r_i + 1
            
            # Дадлага
            self.cr.execute("select s.name, s.credit, g.point, g.mark " \
                            "from school_gbook_line g, school_subject s " \
                            "where g.sub_id=s.id and g.std_id=%s and s.type=%s " \
                            "order by s.type, s.name" , (std.id, 'practice'))
            rs = self.cr.fetchall()
            i = i + 1
            grid[i]['no1'] = 'III.' 
            grid[i]['name1'] = u'Дадлага' 
            grid[i]['mark1'] = u'Үнэлгээ'
            i = i + 1
            no = 1
            r_i = 0
            while r_i < len(rs):
                grid[i]['no1'] = no
                grid[i]['name1'] = rs[r_i][0]
                grid[i]['mark1'] = '%s(%s)' % (rs[r_i][2], rs[r_i][3])
                no = no + 1
                i = i + 1
                r_i = r_i + 1
            
            # Улсын Шалгалт
            self.cr.execute("select s.name, s.credit, g.point, g.mark " \
                            "from school_gbook_line g, school_subject s " \
                            "where g.sub_id=s.id and g.std_id=%s and s.type=%s " \
                            "order by s.type, s.name" , (std.id, 'exam'))
            rs = self.cr.fetchall()
            i = i + 1
            grid[i]['no1'] = 'IV.' 
            grid[i]['name1'] = u'Улсын шалгалт' 
            grid[i]['mark1'] = u'Үнэлгээ'
            i = i + 1
            no = 1
            r_i = 0
            while r_i < len(rs):
                grid[i]['no1'] = no
                grid[i]['name1'] = rs[r_i][0]
                grid[i]['mark1'] = '%s(%s)' % (rs[r_i][2], rs[r_i][3])
                no = no + 1
                i = i + 1
                r_i = r_i + 1
            
            grid[row_count - 12]['name1'] = u'Нийт кредит'
            grid[row_count - 12]['mark1'] = round(std.credit, 2)
            grid[row_count - 11]['name1'] = u'Үнэлгээний голч дүн'
            grid[row_count - 11]['mark1'] = round(std.gpa, 2)
            grid[row_count - 10]['name1'] = u'Онооны дундаж'
            grid[row_count - 10]['mark1'] = round(std.gsa, 2)
            
            if len(std.diploma) == 0:
                manager = 'XXX'
                head = 'XXX'
            else:
                manager = '%s.%s' % (std.diploma[0].manager_id.first_name[0], std.diploma[0].manager_id.name)
                head = '%s.%s' % (std.diploma[0].head_id.first_name[0], std.diploma[0].head_id.name)
                
            grid[row_count - 8]['name1'] = u'СУРГАЛТЫН АХЛАХ МЕНЕЖЕР'
            grid[row_count - 7]['name1'] = manager
            
            grid[row_count - 5]['name1'] = u'МЭРГЭЖЛИЙН БОЛОВСРОЛЫН'
            grid[row_count - 4]['name1'] = u'ТЭНХИМИЙН ЭРХЛЭГЧ'
            grid[row_count - 3]['name1'] = head
            
        elif lang == 'en':
            # Үндсэн хөтөлбөрийн хичээлүүд
            self.cr.execute("select s.name_en, s.credit, g.point, g.mark " \
                            "from school_gbook_line g, school_subject s " \
                            "where g.sub_id=s.id and g.std_id=%s and s.type=%s " \
                            "order by s.type, s.name" , (std.id, 'normal'))
            
            rs = self.cr.fetchall()
            grid[0] = {'no':'I.', 'name':u'Major programme', 'credit':u'Cr', 'mark':u'Grade'}
            i = 1 # grid мөрийн дугаарлалт
            no = 1 # дотоод дугаарлалт
            r_i = 0
            while i <= row_count and r_i < len(rs):
                grid[i]['no'] = no
                grid[i]['name'] = rs[r_i][0]
                grid[i]['credit'] = rs[r_i][1]
                grid[i]['mark'] = '%s(%s)' % (rs[r_i][2], rs[r_i][3])
                no = no + 1
                i = i + 1
                r_i = r_i + 1
            
            # next column
            if i > row_count:
                i = 0
                while r_i < len(rs):
                    grid[i]['no1'] = no
                    grid[i]['name1'] = rs[r_i][0]
                    grid[i]['credit1'] = rs[r_i][1]
                    grid[i]['mark1'] = '%s(%s)' % (rs[r_i][2], rs[r_i][3])
                    no = no + 1
                    i = i + 1
                    r_i = r_i + 1
            else:
                i = 0
                    
            # Курсын төсөл
            self.cr.execute("select s.name_en, s.credit, g.point, g.mark " \
                            "from school_gbook_line g, school_subject s " \
                            "where g.sub_id=s.id and g.std_id=%s and s.type=%s " \
                            "order by s.type, s.name" , (std.id, 'project'))
            rs = self.cr.fetchall()
            i = i + 1
            grid[i]['no1'] = 'II.' 
            grid[i]['name1'] = u"Course's project for thesis"
            grid[i]['mark1'] = u'Grade'
            no = 1
            r_i = 0
            i = i + 1
            while r_i < len(rs):
                grid[i]['no1'] = no
                grid[i]['name1'] = rs[r_i][0]
                grid[i]['mark1'] = '%s(%s)' % (rs[r_i][2], rs[r_i][3])
                no = no + 1
                i = i + 1
                r_i = r_i + 1
            
            # Дадлага
            self.cr.execute("select s.name_en, s.credit, g.point, g.mark " \
                            "from school_gbook_line g, school_subject s " \
                            "where g.sub_id=s.id and g.std_id=%s and s.type=%s " \
                            "order by s.type, s.name" , (std.id, 'practice'))
            rs = self.cr.fetchall()
            i = i + 1
            grid[i]['no1'] = 'III.' 
            grid[i]['name1'] = u'Practice' 
            grid[i]['mark1'] = u'Grade'
            no = 1
            r_i = 0
            i = i + 1
            while r_i < len(rs):
                grid[i]['no1'] = no
                grid[i]['name1'] = rs[r_i][0]
                grid[i]['mark1'] = '%s(%s)' % (rs[r_i][2], rs[r_i][3])
                no = no + 1
                i = i + 1
                r_i = r_i + 1
            
            # Улсын Шалгалт
            self.cr.execute("select s.name_en, s.credit, g.point, g.mark " \
                            "from school_gbook_line g, school_subject s " \
                            "where g.sub_id=s.id and g.std_id=%s and s.type=%s " \
                            "order by s.type, s.name" , (std.id, 'exam'))
            rs = self.cr.fetchall()
            i = i + 1
            grid[i]['no1'] = 'IV.' 
            grid[i]['name1'] = u'The state examination' 
            grid[i]['mark1'] = u'Grade'
            no = 1
            r_i = 0
            i = i + 1
            while r_i < len(rs):
                grid[i]['no1'] = no
                grid[i]['name1'] = rs[r_i][0]
                grid[i]['mark1'] = '%s(%s)' % (rs[r_i][2], rs[r_i][3])
                no = no + 1
                i = i + 1
                r_i = r_i + 1
            
            grid[row_count - 12]['name1'] = u'Total Credits'
            grid[row_count - 12]['mark1'] = round(std.credit, 2)
            grid[row_count - 11]['name1'] = u'Accumlative GPA'
            grid[row_count - 11]['mark1'] = round(std.gpa, 2)
            grid[row_count - 10]['name1'] = u'Average Rating'
            grid[row_count - 10]['mark1'] = round(std.gsa, 2)
            
            if std.diploma[0].signature1:
                grid[row_count - 8]['name1'] = std.diploma[0].signature1
                #grid[row_count - 7]['name1'] = self.name2eng(manager)
            
            if std.diploma[0].signature2:
                grid[row_count - 5]['name1'] = std.diploma[0].signature2
#                grid[row_count - 4]['name1'] = u'EDUCATION'
#                grid[row_count - 3]['name1'] = self.name2eng(head)
            
        return grid

report_sxw.report_sxw(
    'report.diploma',
    'school.student',
    'addons/school/report/report_diploma.rml',
    parser=report_diploma,
    header=False)
