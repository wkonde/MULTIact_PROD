# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from itertools import groupby

class pos_config(models.Model):
	_inherit = 'pos.config'

	bundle_print = fields.Selection([('only_bundle', "Print only Bundle Product on Receipt"), ('with_products', "Print bundle and bundle item both on receipt")], string='Bundle Print Type', default='with_products')


class RelatedPosStock(models.Model):
	_inherit = 'stock.picking'
	
	def _prepare_stock_move_vals_for_sub_product(self,first_line,item,order_lines):
		return {
			'name': first_line.name,
			'product_uom': item.product_id.uom_id.id,
			'picking_id': self.id,
			'picking_type_id': self.picking_type_id.id,
			'product_id': item.product_id.id,
			'product_uom_qty': item.qty_uom * abs(sum(order_lines.mapped('qty'))),
			'state': 'draft',
			'location_id': self.location_id.id,
			'location_dest_id': self.location_dest_id.id,
			'company_id': self.company_id.id,
		}

	def _create_move_from_pos_order_lines(self, lines):
		self.ensure_one()
		lines_by_product = groupby(sorted(lines, key=lambda l: l.product_id.id), key=lambda l: l.product_id.id)
		for product, lines in lines_by_product:
			order_lines = self.env['pos.order.line'].concat(*lines)
			first_line = order_lines[0]
			move_record = []

			if first_line.product_id.pack_ids:
				for item in first_line.product_id.pack_ids:
					current_move = self.env['stock.move'].create(
						self._prepare_stock_move_vals_for_sub_product(first_line,item, order_lines)
					)
					move_record.append(current_move)
			else:
				current_move = self.env['stock.move'].create(
					self._prepare_stock_move_vals(first_line, order_lines)
				)
				move_record.append(current_move)

			for move in move_record:
				move._action_confirm()
				if first_line.product_id == move.product_id and first_line.product_id.tracking != 'none':
					if self.picking_type_id.use_existing_lots or self.picking_type_id.use_create_lots:
						for line in order_lines:
							sum_of_lots = 0
							for lot in line.pack_lot_ids.filtered(lambda l: l.lot_name):
								if line.product_id.tracking == 'serial':
									qty = 1
								else:
									qty = abs(line.qty)
								ml_vals = move._prepare_move_line_vals()
								ml_vals.update({'qty_done':qty})
								if self.picking_type_id.use_existing_lots:
									existing_lot = self.env['stock.production.lot'].search([
										('company_id', '=', self.company_id.id),
										('product_id', '=', line.product_id.id),
										('name', '=', lot.lot_name)
									])
									if not existing_lot and self.picking_type_id.use_create_lots:
										existing_lot = self.env['stock.production.lot'].create({
											'company_id': self.company_id.id,
											'product_id': line.product_id.id,
											'name': lot.lot_name,
										})
									quant = existing_lot.quant_ids.filtered(lambda q: q.quantity > 0.0 and q.location_id.parent_path.startswith(move.location_id.parent_path))[-1:]
									ml_vals.update({
										'lot_id': existing_lot.id,
										'location_id': quant.location_id.id or move.location_id.id
									})
								else:
									ml_vals.update({
										'lot_name': lot.lot_name,
									})
								self.env['stock.move.line'].create(ml_vals)
								sum_of_lots += qty
							if abs(line.qty) != sum_of_lots:
								difference_qty = abs(line.qty) - sum_of_lots
								ml_vals = current_move._prepare_move_line_vals()
								if line.product_id.tracking == 'serial':
									ml_vals.update({'qty_done': 1})
									for i in range(int(difference_qty)):
										self.env['stock.move.line'].create(ml_vals)
								else:
									ml_vals.update({'qty_done': difference_qty})
									self.env['stock.move.line'].create(ml_vals)
					else:
						move._action_assign()
						for move_line in move.move_line_ids:
							move_line.qty_done = move_line.product_uom_qty
						if float_compare(move.product_uom_qty, move.quantity_done, precision_rounding=move.product_uom.rounding) > 0:
							remaining_qty = move.product_uom_qty - move.quantity_done
							ml_vals = move._prepare_move_line_vals()
							ml_vals.update({'qty_done':remaining_qty})
							self.env['stock.move.line'].create(ml_vals)

				else:
					if self.user_has_groups('stock.group_tracking_owner'):
						move._action_assign()
						for move_line in move.move_line_ids:
							move_line.qty_done = move_line.product_uom_qty
						if float_compare(move.product_uom_qty, move.quantity_done, precision_rounding=move.product_uom.rounding) > 0:
							remaining_qty = move.product_uom_qty - move.quantity_done
							ml_vals = move._prepare_move_line_vals()
							ml_vals.update({'qty_done':remaining_qty})
							self.env['stock.move.line'].create(ml_vals)
					move.quantity_done = move.product_uom_qty

	
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
