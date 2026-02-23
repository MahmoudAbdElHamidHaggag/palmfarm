# Copyright (c) 2026, MahmoudAbdElHamidHaggag and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt
from erpnext.accounts.party import get_party_account
from frappe import _
from erpnext.accounts.general_ledger import  make_gl_entries


class AddofPalm(Document):
    def validate(self):
        self.total_cost = flt(self.number) * flt(self.purchase_cost)
    def on_submit(self):
        self.create_l()
        self.create_gl()



    def create_gl(self):
        h = frappe.get_single("Palm Farm Setting")
        com = h.company
        acc_t = h.bio_assets_account
        acc_s = h.capitalization_bio_assets_account
        plant_doc = frappe.get_doc("Seed Cost Aggregation")

        debit_account = acc_t if self.type_of_implant == "Tree" else acc_s

        c = frappe.db.get_value("Types Of Palm Trees", self.types_of_palm_trees, "cost_center")
        credit_account =  get_party_account("Supplier", self.supplier, com )

        if not credit_account:
            frappe.throw("No payable account found for this Supplier.")

        gl = []

        base_args = {
            "posting_date": self.posting_date,
            "company": com,
            "cost_center": c,
            "voucher_subtype": self.types_of_palm_trees,
            "is_opening": "No",
            "voucher_type": self.doctype,
            "voucher_no": self.name,
            "remarks": f"{self.type_of_implant} - {self.number} palms @ {self.purchase_cost}",
        }

        gl.append(self.get_gl_dict(base_args, debit_account, flt(self.total_cost), 0, credit_account))

        gl.append(self.get_gl_dict(base_args, credit_account, 0, flt(self.total_cost), debit_account, "Supplier", self.supplier))

        if self.purchases_type == "Cash":
            if not self.payment_account:
                frappe.throw("Please select a Payment Account for Cash purchase.")

            gl.append(self.get_gl_dict(base_args, credit_account, flt(self.total_cost), 0, self.payment_account, "Supplier", self.supplier))

            gl.append(self.get_gl_dict(base_args, self.payment_account, 0, flt(self.total_cost), credit_account))

        if self.source == "Purchases" and gl:
            make_gl_entries(gl)

    def get_gl_dict(self, base, account, debit, credit, against, party_type=None, party=None):
        d = frappe._dict(base.copy())
        d.update({
            "account": account,
            "against": against,
            "debit": debit,
            "credit": credit,
            "debit_in_account_currency": debit,
            "credit_in_account_currency": credit,
            "party_type": party_type,
            "party": party
        })
        return d


    def create_l(self):
        c = frappe.db.get_value("Types Of Palm Trees", self.types_of_palm_trees, "cost_center")
        h = frappe.get_single("Palm Farm Setting")
        acc_s = h.capitalization_bio_assets_account
        if not acc_s and self.type_of_implant != "Tree":
            frappe.throw(_("Please set Capitalization BIO Assets Account in Palm Farm Setting."))
        doc_t = frappe.get_doc({
            "doctype": "Palm Tree Leadger",
            "posting_date": self.posting_date,
            "cost_center": c,
            "types_of_palm_trees": self.types_of_palm_trees,
            "qty_change": self.number,
            "incoming_rate": self.purchase_cost,
            "voucher_type": self.doctype,
            "voucher_no": self.name,
        })
        parent_name = frappe.db.get_value(
            "Seed Cost Aggregation",
            {"types_of_palm_trees": self.types_of_palm_trees, "status":"Open"},
            "name"
        )

        if self.type_of_implant == "Tree" :
            doc_t.insert()
            doc_t.submit()
        else:
            if parent_name:
                parent = frappe.get_doc("Seed Cost Aggregation", parent_name)
            else:
                parent = frappe.get_doc({
                    "doctype": "Seed Cost Aggregation",
                    "types_of_palm_trees": self.types_of_palm_trees,
                    "posting_date": self.posting_date
                })
                parent.insert(ignore_permissions=True)

            parent.append("aggregation", {
                "voucher_type": self.doctype,
                "voucher_no": self.name,
                "qty_seeding": self.number,
                "share": self.purchase_cost,
                "total_share": flt(self.number) * flt(self.purchase_cost),
                "account": acc_s,
            })

            parent.save(ignore_permissions=True)
