# -*- encoding: utf-8 -*-
import wizard

t_form = u'''<?xml version="1.0"?>
            <form string="Багшийн цагийн тооцооны тайлан">
                <field name="term_id" colspan="4"/>
            </form>'''

t_fields = {
    'term_id': {'string':u'Семестр', 'type':'many2one', 'relation':'school.term'},
}

class wizard_teacher_time(wizard.interface):
    def _get_defaults(self, cr, uid, data, context):
        cr.execute('SELECT id FROM school_term WHERE now() BETWEEN date_start AND date_stop')
        term = cr.dictfetchall()
        if term:
            data['form']['term_id'] = term[0]['id']
        return data['form']
    states = {
        'init': {
            'actions': [_get_defaults],
            'result': {'type':'form', 'arch':t_form, 'fields':t_fields, 'state':[('end',u'Болих','gtk-cancel'),('report',u'Хэвлэх','gtk-print')]}
        },
        'report': {
            'actions': [],
            'result': {'type':'print', 'report':'teacher_time', 'state':'end'}
        },
    }
wizard_teacher_time('teacher_time.report')

