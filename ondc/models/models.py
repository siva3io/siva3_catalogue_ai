# -*- coding: utf-8 -*-
import requests
from odoo import models, fields, api


class CategoryDomain(models.Model):
    _name = "category.domain"
    _description = "Category Domain"

    name = fields.Char(string="Name")

    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'The code must be unique!'),
    ]


class ProductCategory(models.Model):
    _inherit = "product.category"

    code = fields.Char(string="Code")
    domain = fields.Many2one("category.domain", string="Domain")

    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'The code must be unique!'),
    ]

    def insert_subcategory(self, categories, domain_id=False, parent_id=False):
        prod_env = self.env['product.category']
        for sub_category in categories:
            if not prod_env.search([('code', '=', sub_category.get('Id'))]):
                category_id = prod_env.create({
                    'code': sub_category['Id'],
                    'name': sub_category['Category'],

                })
                if sub_category.get('subCategories'):
                    self.insert_subcategory(sub_category['subCategories'], domain_id, category_id.id)

    def sync_categories(self):
        host = 'https://datala.siva3.io/api/getbcats'
        response = requests.get(host)
        if response.status_code == 200:
            categories = response.json()
            domain_code = response.json()['Id']
            domain_id = self.env["category.domain"].search([('code', '=', domain_code)], limit=1)
            self.insert_subcategory(categories, domain_id=domain_id.id)
