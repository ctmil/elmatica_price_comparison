from openerp import models, fields, api, _
from openerp.osv import osv
from openerp.exceptions import except_orm
from StringIO import StringIO
import urllib2, httplib, urlparse, gzip, requests, json
import openerp.addons.decimal_precision as dp
import logging
import datetime
from openerp.fields import Date as newdate

#Get the logger
_logger = logging.getLogger(__name__)


class partnerinfo_comparison(models.Model):
	_name = 'partnerinfo.comparison'

	product_tmpl_id = fields.Many2one('product.template',string='Product')
	pricelist_id = fields.Many2one('product.pricelist',string='Pricelist')
	supplier_id = fields.Many2one('res.partner',string='Supplier')
	currency_id = fields.Many2one('res.currency',related='pricelist_id.currency_id')
	qty = fields.Integer(string='Qty')
	price = fields.Float(string='Price')

	@api.model
	def _update_price_comparison(self):
		self.search([]).unlink()
		import pdb;pdb.set_trace()
		partnerinfo_ids = self.env['pricelist.partnerinfo'].search([],order='product_tmpl_id, name, min_quantity')
		min_value = 0
		for partnerinfo in partnerinfo_ids:
			# Creates records here
			for index in range(partnerinfo.min_quantity,partnerinfo.breakpoint+1):
				vals = {
					'product_tmpl_id': partnerinfo.suppinfo_id.product_tmpl_id,
					'supplier_id': partnerinfo.suppinfo_id.name,
					'qty': index,
					'price': partnerinfo.price
					#'pricelist_id': 
					}
				self.create(vals)
		return None
