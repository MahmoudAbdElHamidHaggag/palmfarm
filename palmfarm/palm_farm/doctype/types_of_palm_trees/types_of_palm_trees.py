# Copyright (c) 2026, MahmoudAbdElHamidHaggag and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _


class TypesOfPalmTrees(Document):

	def on_submit(self):
		self.create_links()

	def create_links(self):
		company = frappe.db.get_single_value("Palm Farm Setting", "company")
		parent_cost_center = frappe.db.get_single_value("Palm Farm Setting", "parent_cost_center")
		parent_item_group = frappe.db.get_single_value("Palm Farm Setting", "parent_item_group")

		if not company or not parent_cost_center or not parent_item_group:
			frappe.throw(_("Palm Farm Setting is not complete"))

		title = self.name

		if not frappe.db.exists(
			"Cost Center",
			{"cost_center_name": title, "company": company}
		):
			cc = frappe.get_doc({
				"doctype": "Cost Center",
				"cost_center_name": title,
				"parent_cost_center": parent_cost_center,
				"company": company,
				"is_group": 0
			})
			cc.insert(ignore_permissions=True)
			self.db_set("cost_center", cc.name)

		if not frappe.db.exists(
			"Item Group",
			{"item_group_name": title}
		):
			ig = frappe.get_doc({
				"doctype": "Item Group",
				"item_group_name": title,
				"parent_item_group": parent_item_group,
				"is_group": 0
			})
			ig.insert(ignore_permissions=True)
			self.db_set("item_group", ig.name)

	def before_rename(self, old, new, merge=False):
		frappe.throw("Cannot rename this document.")

	def before_cancel(self):
		frappe.throw("Cannot cancel this document.")

	def before_delete(self):
		frappe.throw("Cannot delete this document.")

