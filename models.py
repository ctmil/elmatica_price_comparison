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
