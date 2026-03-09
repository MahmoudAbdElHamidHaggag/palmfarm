# Copyright (c) 2026, MahmoudAbdElHamidHaggag and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt, nowdate
from frappe import _


class CostAndProductionAggregation(Document):
	def validate(self):
		if not self.add_havest_voucher:
			self.status = "Open"
		else:
			self.status = "Added"
		total_v = 0
		total_h = 0
		for v in self.production_cost_aggregation:
			total_v += flt(v.total_share)
			
		for h in self.date_harvest_collection:
			total_h += flt(h.qty_by_kg)
			
		if total_h > 0:
			self.cost_per_kilogram_cpk = total_v / total_h
		else:
			self.cost_per_kilogram_cpk = 0

		self.total_cost = total_v
		self.total_harvest = total_h




	@frappe.whitelist()
	def create_stock_entry(self):
		if not self.date_harvest_item:
			frappe.throw(_("Error: The harvest variety must be selected first."))

		h = frappe.get_single("Palm Farm Setting")
		com = h.company
		warehouse = h.date_harvet_warehouse
		if not com:
			frappe.throw(_("Please select the company in Palm Farm Setting"))

		if not warehouse:
			frappe.throw(_("Please select the Date Harvet Warehouse in Palm Farm Setting"))

		stock_entry = frappe.new_doc("Stock Entry")
		stock_entry.purpose = "Material Receipt"
		stock_entry.stock_entry_type = "Material Receipt"
		stock_entry.company = com
		stock_entry.posting_date = nowdate()
		stock_entry.custom_types_of_palm_trees = self.types_of_palm_trees

		stock_entry.append("items", {
			"item_code": self.date_harvest_item,
			"t_warehouse": warehouse,
			"qty": flt(self.total_harvest),
			"basic_rate": flt(self.cost_per_kilogram_cpk),
			"uom": frappe.db.get_value("Item", self.date_harvest_item, "stock_uom")
		})

		stock_entry.insert(ignore_permissions=True)
		stock_entry.submit()
		self.db_set("add_havest_voucher", stock_entry.name)
		return stock_entry.name



		
