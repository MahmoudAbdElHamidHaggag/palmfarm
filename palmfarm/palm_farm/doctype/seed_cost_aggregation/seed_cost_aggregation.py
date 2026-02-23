# Copyright (c) 2026, MahmoudAbdElHamidHaggag and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt


class SeedCostAggregation(Document):
	pass
# 	def validate(self):

# 		total_v = 0
# 		total_q = 0

# 		for row in self.aggregation:
# 			share = flt(row.total_share)
# 			qty = flt(row.qty_seeding)
# 			if row.voucher_type in ["Opening Palm Balance", "Add of Palm"]:
# 				total_v += share
# 				total_q += qty
# 			elif row.voucher_type == "Execution of Palm":
# 				total_v -= share
# 				total_q -= qty
# 			else:
# 				total_v -= share


# 		self.total_cost = total_v
# 		self.total_qty = total_q

# 		if self.add_of_palm:
# 			self.status = "Transformed of Tree"
# 		else:
# 			self.status = "Open"


# @frappe.whitelist()
# def create_add(docname):
# 	parent = frappe.get_doc("Seed Cost Aggregation", docname)

# 	account_totals = {}
# 	for row in parent.aggregation:
# 		if row.account:
# 			account_totals[row.account] = account_totals.get(row.account, 0) + flt(row.total_share)

# 	doc = frappe.get_doc({
# 		"doctype": "Add of Palm",
# 		"auto_generated": 1,
# 		"voucher_type": parent.doctype,
# 		"voucher_no": parent.name,
# 		"posting_date": today(),
# 		"types_of_palm_trees": parent.types_of_palm_trees,
# 		"type_of_implant": "Tree",
# 		"number": parent.total_qty,
# 		"source": "Added from the collection",
# 		"purchase_cost": parent.total_cost / parent.total_qty,
# 		"aggregation_account": []
# 	})
# 	for acc, total_amount in account_totals.items():
# 		doc.append("aggregation_account", {
# 		"account": acc,
# 		"total": total_amount
# 		})
# 	doc.insert()
# 	doc.submit()

# 	return doc.name

