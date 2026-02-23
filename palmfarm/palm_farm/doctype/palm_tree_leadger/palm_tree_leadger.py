# Copyright (c) 2026, MahmoudAbdElHamidHaggag and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.meta import get_field_precision
from frappe.model.naming import set_name_from_naming_options
from frappe.utils import create_batch, flt, fmt_money, now



class PalmTreeLeadger(Document):
    def validate(self):
        self.balance_stock_value = flt(self.qty_after_transaction) * flt(self.valuation_rate)
        if self.voucher_type == "Opening Palm Balance":
            return

        previous_qty = frappe.db.sql("""
            SELECT qty_after_transaction
            FROM `tabPalm Tree Leadger`
            WHERE types_of_palm_trees = %s
            AND cost_center = %s
            AND posting_datetime < %s
            ORDER BY posting_datetime DESC
            LIMIT 1
        """, (
            self.types_of_palm_trees,
            self.cost_center,
            self.posting_datetime,
        ))
        if previous_qty:
            previous_qty_q = previous_qty[0][0] or 0
        else:
            previous_qty_q = 0
        self.qty_after_transaction = self.qty_change + previous_qty_q


        previous_value = frappe.db.sql("""
            SELECT valuation_rate
            FROM `tabPalm Tree Leadger`
            WHERE types_of_palm_trees = %s
            AND cost_center = %s
            AND posting_datetime < %s
            ORDER BY posting_datetime DESC
            LIMIT 1
        """, (
            self.types_of_palm_trees,
            self.cost_center,
            self.posting_datetime,
        ))

        if previous_value:
            previous_value_v = previous_value[0][0] or 0
        else:
            previous_value_v = 0
        if self.valuation_rate == 0:
            self.valuation_rate = self.incoming_rate
        else:
            self.valuation_rate = ((flt(self.qty_change)*flt(self.incoming_rate))  + (previous_qty_q * previous_value_v))/(self.qty_change + previous_qty_q)





	

	
