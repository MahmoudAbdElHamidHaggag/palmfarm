# # Copyright (c) 2025, MahmoudAbdElHamidHaggag and contributors
# # For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _
from erpnext.accounts.general_ledger import  make_gl_entries
from frappe.utils import flt
from frappe import _dict


class OpeningPalmBalance(Document):
    def validate(self):
        self.validate_data()
        
    def on_submit(self):
        self.create_gl()
        self.create_l()



    def validate_data(self):
        self.total_cost_of_palms = flt(self.number_of_palm) * flt(self.cost_of_palm)


    def create_gl(self):
        h = frappe.get_single("Palm Farm Setting")
        com = h.company
        tem = h.temporary_account
        acc_t = h.bio_assets_account
        acc_s = h.capitalization_bio_assets_account
        c = frappe.db.get_value ("Types Of Palm Trees", self.types_of_palm_trees, "cost_center")

        debit_account = acc_t if self.type_of_implant == "Tree" else acc_s

        gl = [
            _dict({
                "posting_date": self.posting_date,
                "account": debit_account,
                "against": tem,
                "company": com,
                "cost_center": c,
                 "voucher_subtype":self.types_of_palm_trees,
                "debit": flt(self.total_cost_of_palms),
                "credit": 0,
                "debit_in_account_currency": flt(self.total_cost_of_palms),
                "credit_in_account_currency": 0,
                "is_opening": "Yes",
                "voucher_type": self.doctype,
                "voucher_no": self.name,
                "remarks": f"{self.type_of_implant} - {self.number_of_palm} palms @ {self.cost_of_palm}",
            }),
            _dict({
                "posting_date": self.posting_date,
                "account": tem,
                "against": debit_account,
                "company": com,
                "cost_center": c,
                "voucher_subtype":self.types_of_palm_trees,
                "debit": 0,
                "credit": flt(self.total_cost_of_palms),
                "debit_in_account_currency": 0,
                "credit_in_account_currency": flt(self.total_cost_of_palms),
                "is_opening": "Yes",
                "voucher_type": self.doctype,
                "voucher_no": self.name,
                "remarks": f"{self.type_of_implant} - {self.number_of_palm} palms @ {self.cost_of_palm}",
            })
        ]


        make_gl_entries(gl)


    def create_l(self):
        c = frappe.db.get_value("Types Of Palm Trees", self.types_of_palm_trees, "cost_center")
        h = frappe.get_single("Palm Farm Setting")
        acc_s = h.capitalization_bio_assets_account

        doc_t = frappe.get_doc({
            "doctype": "Palm Tree Leadger",
            "posting_date": self.posting_date,
            "cost_center": c,
            "types_of_palm_trees": self.types_of_palm_trees,
            "qty_after_transaction": self.number_of_palm,
            "valuation_rate": self.cost_of_palm,
            "voucher_type": self.doctype,
            "voucher_no": self.name,
        })

        parent_name = frappe.db.get_value(
            "Seed Cost Aggregation",
            {"types_of_palm_trees": self.types_of_palm_trees, "status":"Open"},
            "name"
        )

        if self.type_of_implant == "Tree":
            doc_t.insert()
            doc_t.submit()
        else:
            if parent_name:
                parent = frappe.get_doc("Seed Cost Aggregation", parent_name)
            else:
                parent = frappe.get_doc({
                    "doctype": "Seed Cost Aggregation",
                    "types_of_palm_trees": self.types_of_palm_trees,
                    "posting_date": self.posting_date,
                    "status": "Open",
                })
                parent.insert(ignore_permissions=True)

            parent.append("aggregation", {
                "voucher_type": self.doctype,
                "voucher_no": self.name,
                "qty_seeding": self.number_of_palm,
                "share": self.cost_of_palm,
                "account": acc_s,
                "total_share": flt(self.number_of_palm) * flt(self.cost_of_palm),
            })

            parent.save(ignore_permissions=True)
