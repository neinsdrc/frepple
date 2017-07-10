# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 by frePPLe bvba
#
# This library is free software; you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero
# General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import odoo
import logging
from datetime import datetime, timedelta
from xml.etree.cElementTree import iterparse
from werkzeug.formparser import parse_form_data

logger = logging.getLogger(__name__)


class importer(object):

  def __init__(self, req, database=None, company=None, mode=1):
    self.env = req.env
    self.database = database
    self.company = company
    self.datafile = req.httprequest.files.get('frePPLe plan')

    # The mode argument defines different types of runs:
    #  - Mode 1:
    #    Export of the complete plan. This first erase all previous frePPLe
    #    proposals in draft state.
    #  - Mode 2:
    #    Incremental export of some proposed transactions from frePPLe.
    #    In this mode mode we are not erasing any previous proposals.
    self.mode = mode


  def run(self):
    msg = []

    proc_order = self.env['procurement.order']
    mfg_order = self.env['mrp.production']
    if self.mode == 1:
      # Cancel previous draft purchase quotations
      m = self.env['purchase.order']
      recs = m.search([('state', '=', 'draft'), ('origin', '=', 'frePPLe')])
      recs.unlink()
      msg.append("Removed %s old draft purchase quotations" % len(recs))

      # Cancel previous draft procurement orders
      recs = proc_order.search(
        ['|', ('state', '=', 'draft'), ('state', '=', 'cancel'), ('origin', '=', 'frePPLe')]
        )
      recs.unlink()
      msg.append("Removed %s old draft procurement orders" % len(recs))

      # Cancel previous draft manufacturing orders
      recs = mfg_order.search(
        ['|', ('state', '=', 'draft'), ('state', '=', 'cancel'), ('origin', '=', 'frePPLe')]
        )
      recs.unlink()
      msg.append("Removed %s old draft manufacturing orders" % len(recs))

    # Parsing the XML data file    
    countproc = 0
    countmfg = 0
    for event, elem in iterparse(self.datafile, events=('start', 'end')):
      if event == 'end' and elem.tag == 'operationplan':
        uom_id, item_id = elem.get('item_id').split(',')
        try:
          if elem.type == 'PO':  # TODO missing fields warehouse and preferred routes (with implications)
            # Create purchase quotation
            x = proc_order.create({
              'name': elem.get('operation'),
              'product_qty': elem.get("quantity"),
              'date_planned': elem.get("end"),
              'product_id': int(item_id),
              'company_id': self.company.id,
              'product_uom': int(uom_id),
              'location_id': int(elem.get('location')),
              #'procure_method': 'make_to_order', # this field is no longer there
              # : elem.get('criticality'),
              'origin': 'frePPLe'
              })
            # proc_order.action_confirm([x], context=self.req.session.context) # it is confirmed by default
            # proc_order.action_po_assign([x], context=self.req.session.context) # TODO no idea of what this is yet, other than not available :)
            countproc += 1
          # TODO Create a distribution order
          # elif ????:
          else:
            # Create manufacturing order
            x = mfg_order.create({
              'product_qty': elem.get("quantity"),
              'date_planned': elem.get("end"),
              'product_id': int(item_id),
              'company_id': self.company.id,
              'product_uom': int(uom_id),
              'location_src_id': int(elem.get('location_id')),
              'product_uos_qty': False,
              'product_uos': False,
              'bom_id': False,
              # : elem.get('criticality'),
              'origin': 'frePPLe'
              })
            mfg_order.action_compute([x], context=self.req.session.context)
            countmfg += 1
        except Exception as e:
          msg.append(str(e))
        # Remove the element now to keep the DOM tree small
        root.clear()
      elif event == 'start' and elem.tag == 'operationplans':
        # Remember the root element
        root = elem

    # Be polite, and reply to the post
    msg.append("Processed %s uploaded procurement orders" % countproc)
    msg.append("Processed %s uploaded manufacturing orders" % countmfg)
    return '\n'.join(msg)
