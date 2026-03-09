# Copyright (c) 2026, MahmoudAbdElHamidHaggag and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Addingadateharvest(Document):
	def on_submit(self):

		p_name = frappe.db.get_value(
			"Cost And Production Aggregation",
			{"types_of_palm_trees": self.types_of_palm_trees, "status": "Open"},
			"name"
		)
		if p_name:
			p_doc = frappe.get_doc("Cost And Production Aggregation", p_name)
		else:
			p_doc = frappe.get_doc({
				"doctype": "Cost And Production Aggregation",
				"types_of_palm_trees": self.types_of_palm_trees,
				"posting_date": self.posting_date,
				"status": "Open"
			})
			p_doc.insert(ignore_permissions=True)

		p_doc.append("date_harvest_collection", {
			"voucher_type": self.doctype,
			"voucher_no": self.name,
			"voucher_date":self.posting_date,
			"date_harvest_item":self.date_harvest_item,
			"qty_by_kg": self.qty_by_kg,
		})
		p_doc.save(ignore_permissions=True)
