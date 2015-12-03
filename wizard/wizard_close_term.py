# -*- encoding: utf-8 -*-
import wizard

t_form = u'''<?xml version="1.0"?>
                <form string="Хаах семестрээ сонгоно уу">
                    <field name="term_id" colspan="4"/>
                </form>'''
t_fields = {
    'term_id': {'string': u'Семестр', 'type': 'many2one', 'relation': 'school.term', 'required':'True',
                    'domain':[('date_stop','<=',None)]},
}

s_form = '''<?xml version="1.0"?>
            <form string="">
                <label string="Семестрийг хаалаа" colspan="2"/>
            </form>'''
s_fields = {
}

class wizard_close_term(wizard.interface):
    def _get_defaults(self, cr, uid, data, context):
        return data['form']
    
    def _close_term(self, cr, uid, data, context):
        cr.execute("SELECT id FROM school_gbook WHERE term_id = %s" % (data['form']['term_id']))
        gbook_ids = cr.dictfetchall()
        for i in gbook_ids:
            cr.execute("UPDATE school_gbook SET state = 'done' WHERE id = %s" % (i['id']))
            cr.execute("UPDATE school_gbook_line SET state = 'done' WHERE gbook_id = %s" % (i['id']))
        cr.execute("select year_id, date_stop from school_term where id = %s" % (data['form']['term_id']))
        term = cr.dictfetchall()[0]
        cr.execute("select max(date_stop) from school_term where year_id = %s" % (term['year_id']))
        max_date_stop = cr.dictfetchall()[0]
        if max_date_stop['max'] == term['date_stop']:
            cr.execute("UPDATE school_student SET cls = cls + 1 WHERE presense = 'present'")
        return {}
    
    states = {
        'init': {
            'actions': [_get_defaults],
            'result': {'type':'form', 'arch':t_form, 'fields':t_fields, 'state':[('end', u'Болих', 'gtk-cancel'), ('close_term', u'Хаах', 'gtk-ok')]}
        },
        'close_term': {
            'actions': [_close_term],
            'result' : {'type':'form', 'arch':s_form, 'fields':s_fields, 'state':[('end', 'OK')] }
        },
    }
wizard_close_term('school.term.close')

