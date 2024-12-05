from odoo import http
from odoo.http import request


class ProductList(http.Controller):
    @http.route('/three_product_list', type='json', auth='public')
    def product_list(self):
        products = request.env['product.product'].search([], order='create_date desc', limit=3)
        product_data_list = []
        for product in products:
            image_url = '/web/image/product.product/%s/image_128' % product.id
            product_data = {
                'name': product.name,
                'image_url': image_url
            }
            product_data_list.append(product_data)
        print(product_data_list)
        data_list = {
            'data': product_data_list
        }
        res = http.Response(template='dynamic_snippet.product_list_template',
                            qcontext=data_list)
        return res.render()

