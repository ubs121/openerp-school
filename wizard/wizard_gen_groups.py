# -*- encoding: utf-8 -*-
'''
Created on May 4, 2009

@author: ubs121
'''

import wizard
import pooler

dates_form = u'''<?xml version="1.0"?>
                <form string="Select period">
                    <field name="company_id"/>
                    <newline/>
                    <field name="based_on"/>
                    <field name="periods" colspan="4"/>
                </form>'''

dates_fields = {
    'company_id': {'string': 'Company', 'type': 'many2one',
        'relation': 'res.company', 'required': True},
    'based_on':{'string':'Base on', 'type':'selection', 'selection':[
            ('invoices','Invoices'),
            ('payments','Payments'),
            ], 'required':True, 'default': lambda *a: 'invoices'},
    'periods': {'string': 'Periods', 'type': 'many2many', 'relation': 'account.period', 'help': 'All periods if empty'},

}


class wizard_report(wizard.interface):

    def _get_defaults(self, cr, uid, data, context):
        pool = pooler.get_pool(cr.dbname)
        #period_obj = pool.get('account.period')

        user = pool.get('res.users').browse(cr, uid, uid, context=context)
        if user.company_id:
            company_id = user.company_id.id
        else:
            company_id = pool.get('res.company').search(cr, uid,
                    [('parent_id', '=', False)])[0]
        data['form']['company_id'] = company_id

        return data['form']

    states = {
        'init': {
            'actions': [_get_defaults],
            'result': {
                'type': 'form',
                'arch': dates_form,
                'fields': dates_fields,
                'state': [
                    ('end', 'Cancel'),
                    ('report', 'Print VAT Decl.')
                ]
            }
        },
        'report': {
            'actions': [],
            'result': {
                'type': 'print',
                'report': 'account.vat.declaration',
                'state':'end'
            }
        }
    }

wizard_report('school.student.def')


