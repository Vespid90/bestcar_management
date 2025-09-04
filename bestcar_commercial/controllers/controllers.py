# -*- coding: utf-8 -*-
# from odoo import http


# class BestcarCommercial(http.Controller):
#     @http.route('/bestcar_commercial/bestcar_commercial', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bestcar_commercial/bestcar_commercial/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('bestcar_commercial.listing', {
#             'root': '/bestcar_commercial/bestcar_commercial',
#             'objects': http.request.env['bestcar_commercial.bestcar_commercial'].search([]),
#         })

#     @http.route('/bestcar_commercial/bestcar_commercial/objects/<model("bestcar_commercial.bestcar_commercial"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bestcar_commercial.object', {
#             'object': obj
#         })

