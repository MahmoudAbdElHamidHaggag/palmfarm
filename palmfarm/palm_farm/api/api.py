# Copyright (c) 2026, MahmoudAbdElHamidHaggag and contributors
# For license information, please see license.txt


import frappe
from frappe import _
from frappe.utils import flt

def create_cost(document, method=None):
    h = frappe.get_single("Palm Farm Setting")
    acc_a = h.stock_adjustment_account
    if not acc_a and flt(document.custom_has_seeding) == 1:
        frappe.throw(_("Please set Stock Adjustment Account in Palm Farm Setting."))
    p_name = frappe.db.get_value(
        "Cost And Production Aggregation",
        {"types_of_palm_trees": document.custom_types_of_palm_trees, "status": "Open"},
        "name"
    )
    
    s_name = frappe.db.get_value(
        "Seed Cost Aggregation",
        {"types_of_palm_trees": document.custom_types_of_palm_trees, "status": "Open"},
        "name"
    )

    if p_name:
        p_doc = frappe.get_doc("Cost And Production Aggregation", p_name)
    else:
        p_doc = frappe.get_doc({
            "doctype": "Cost And Production Aggregation",
            "types_of_palm_trees": document.custom_types_of_palm_trees,
            "posting_date": document.posting_date,
            "status": "Open"
        })
        p_doc.insert(ignore_permissions=True)

    if s_name:
        s_doc = frappe.get_doc("Seed Cost Aggregation", s_name)
    else:
        s_doc = frappe.get_doc({
            "doctype": "Seed Cost Aggregation",
            "types_of_palm_trees": document.custom_types_of_palm_trees,
            "posting_date": document.posting_date,
            "status": "Open"
        })
        s_doc.insert(ignore_permissions=True)

    total_outgoing = flt(document.total_outgoing_value)
    qty_t = flt(document.custom_number_tree)
    qty_s = flt(document.custom_number_seeding)
    
    if flt(document.custom_has_seeding) == 0:
        qty = 1
        share = total_outgoing
        share_production = total_outgoing
        share_seeds = 0
    else:
        qty = flt(document.custom_total_trees) or 1
        share = total_outgoing / qty
        share_production = share * qty_t
        share_seeds = share * qty_s

    p_doc.append("production_cost_aggregation", {
        "voucher_type": document.doctype,
        "voucher_no": document.name,
        "voucher_date":document.posting_date,
        "qty_trees": qty,
        "total_cost": total_outgoing,
        "qty_tree": qty_t,
        "share": share,
        "total_share": share_production,
    })
    p_doc.save(ignore_permissions=True)

    s_doc.append("aggregation", {
        "voucher_type": document.doctype,
        "voucher_no": document.name,
        "voucher_date":document.posting_date,
        "qty_trees": qty,
        "total_cost": total_outgoing,
        "qty_seeding": qty_s,
        "share": share,
        "total_share": share_seeds,
        "account": acc_a,
    })
    s_doc.save(ignore_permissions=True)

    frappe.db.commit()