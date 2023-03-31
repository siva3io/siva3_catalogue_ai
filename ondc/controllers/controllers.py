# -*- coding: utf-8 -*-
from odoo import http


class Ondc(http.Controller):
    @http.route('/ondc/insert', auth='public')
    def object(self, obj, **kw):
        return http.request.render('ondc.object', {
            'object': obj
        })



