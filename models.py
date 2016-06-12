from openerp import models, fields, exceptions, api, _
from openerp.osv import osv
from openerp.exceptions import except_orm
from StringIO import StringIO
import urllib2, httplib, urlparse, gzip, requests, json
import openerp.addons.decimal_precision as dp
import logging
import datetime
from datetime import date
from openerp.fields import Date as newdate

#Get the logger
_logger = logging.getLogger(__name__)

class product_pricelist(models.Model):
	_inherit = 'product.pricelist'

	allow_price_comparison = fields.Boolean('Allow Price Comparison')


class partnerinfo_comparison(models.Model):
	_name = 'partnerinfo.comparison'

	name = fields.Char('Name')
	product_tmpl_id = fields.Many2one('product.template',string='Product')
	pricelist_id = fields.Many2one('product.pricelist',string='Pricelist')
	supplier_id = fields.Many2one('res.partner',string='Supplier')
	currency_id = fields.Many2one('res.currency',related='pricelist_id.currency_id')
	qty = fields.Integer(string='Qty')
	price = fields.Float(string='Price')

	@api.model
	def _update_price_comparison(self):
		pricelists = self.env['product.pricelist'].search(['allow_price_comparison','=',True)
		if not pricelists:
			return None
		self.search([]).unlink()
		partnerinfo_ids = self.env['pricelist.partnerinfo'].search([],order='suppinfo_id asc, min_quantity asc')
		min_value = 0
		for partnerinfo in partnerinfo_ids:
			# Creates records here
			product = self.env['product.product'].search([('product_tmpl_id','=',partnerinfo.product_tmpl_id.id)])
			if not product:
		                raise exceptions.ValidationError(_('No product set for product_tmpl %s' % partnerinfo.product_tmpl_id.name))
			else:
				product = product[0]
			min_qty = int(partnerinfo.min_quantity)
			max_qty = int(partnerinfo.breakpoint + 1)
			for index in range(min_qty,max_qty):
				vals = {
					'name': 'Product cost in USD',
					'product_tmpl_id': partnerinfo.suppinfo_id.product_tmpl_id.id,
					'supplier_id': partnerinfo.suppinfo_id.name.id,
					'qty': index,
					'price': partnerinfo.price
					#'pricelist_id': 
					}
				self.create(vals)
				for pricelist in pricelists:
                                        return_pricelist = pricelist.price_get(product, index or 1.0, False,\
                                                 context = {'uom': 1, 'date': str(date.today())})
                                        calculated_price = return_pricelist[pricelist.id]
					vals = {
						'name': pricelist.name,
						'product_tmpl_id': partnerinfo.suppinfo_id.product_tmpl_id.id,
						'supplier_id': partnerinfo.suppinfo_id.name.id,
						'pricelist_id': partnerinfo.suppinfo_id.pricelist_id.id,
						'qty': index,
						'price': calculated_price
						}
					self.create(vals)
		return None
