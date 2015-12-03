# -*- encoding: utf-8 -*-
import wizard
import pooler

db_form = u'''<?xml version="1.0"?>
            <form string="'ДБ-9' маягт хэвлэх">
                <separator string="Ажиллагчид" colspan="4" />
                <field name="school_id" colspan="4" />
                <field name="year" colspan="4"/>
            </form>'''

db_fields = {
    'year': {'string': u'Хичээлийн жил', 'type': 'many2one', 'relation': 'school.year'},
    'school_id': {'string':u'Сургууль', 'type':'many2one', 'relation':'res.company', 'required': True},
}

class wizard_db_9(wizard.interface):
    def _get_defaults(self, cr, uid, data, context):
        user = pooler.get_pool(cr.dbname).get('res.users').browse(cr, uid, uid, context=context)
        
        if user.company_id:
            company_id = user.company_id.id
        else:
            company_id = pooler.get_pool(cr.dbname).get('res.company').search(cr, uid, [('parent_id', '=', False)])[0]
           
        current_year = pooler.get_pool(cr.dbname).get('school.year').find(cr, uid)
        data['form']['year'] = current_year
        data['form']['school_id'] = company_id
        return data['form']

    states = {
        'init': {
            'actions': [_get_defaults],
            'result': {'type':'form', 'arch':db_form, 'fields':db_fields, 'state':[('end', u'Болих', 'gtk-cancel'), ('report', u'Хэвлэх', 'gtk-print')]}
        },
        'report': {
            'actions': [],
            'result': {'type':'print', 'report':'db_9', 'state':'end'}
        },
    }
wizard_db_9('db_9.report')

