# Copyright (c) 2026, MahmoudAbdElHamidHaggag and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt
from erpnext.accounts.general_ledger import make_gl_entries

class ExecutionofPalm(Document):
    def validate(self):
        self.validate_data()
        self.total_of_cost = self.number * self.cost_of_palm

    def on_submit(self):
        self.create_gl()
        self.create_l()


    def validate_data(self):
        self.cost_of_palm = 0
        c = frappe.db.get_value("Types Of Palm Trees", self.types_of_palm_trees, "cost_center")
        
        data = frappe.db.get_value(
            "Seed Cost Aggregation",
            {"types_of_palm_trees": self.types_of_palm_trees, "status": "Open"},
            ["total_cost", "total_qty"],
            as_dict=True
        )

        previous_record = frappe.db.sql("""
            SELECT valuation_rate 
            FROM `tabPalm Tree Leadger`
            WHERE types_of_palm_trees = %s
            AND cost_center = %s
            AND posting_datetime < %s
            ORDER BY posting_datetime DESC
            LIMIT 1
        """, (self.types_of_palm_trees, c, self.posting_datetime))

        if not previous_record:
            frappe.throw(_("No trees of this type are available in the ledger. Please add the quantity/value first."))

        previous_valuation = flt(previous_record[0][0])

        if self.type_of_implant == "seedling":
            if not data:
                frappe.throw(_("There is no Open Seed Cost Aggregation for this type"))

            total_cost = flt(data.total_cost)
            total_qty = flt(data.total_qty)

            if total_qty == 0:
                frappe.throw(_(f"Open Seed Cost Aggregation has zero quantity for {self.types_of_palm_trees}"))

            if flt(self.number) > total_qty:
                frappe.throw(_("The quantity exceeds the available seedlings in Seed Cost Aggregation"))

            self.cost_of_palm = total_cost / total_qty
        elif self.type_of_implant == "Tree":
            self.cost_of_palm = previous_valuation
        else:
            frappe.throw(_("Please select type of implant"))

        self.total_of_cost = flt(self.number) * flt(self.cost_of_palm)

    def create_gl(self):
        h = frappe.get_single("Palm Farm Setting")
        com = h.company
        acc_t = h.bio_assets_account
        acc_s = h.capitalization_bio_assets_account
        acc_e = h.execution_of_palm_account

        if not acc_e:
            frappe.throw(_("Please set Execution of Palm Account in Palm Farm Setting."))

        credit_account = acc_t if self.type_of_implant == "Tree" else acc_s


        c = frappe.db.get_value("Types Of Palm Trees", self.types_of_palm_trees, "cost_center")
        amount = flt(self.total_of_cost)

        base_args = {
            "posting_date": self.posting_date,
            "company": com,
            "cost_center": c,
            "voucher_subtype": self.types_of_palm_trees,
            "is_opening": "No",
            "voucher_type": self.doctype,
            "voucher_no": self.name,
            "remarks": f"{self.type_of_implant} - {self.number} palms @ {self.cost_of_palm}",
        }

        gl = []

        gl.append(self.get_gl_dict(
            base_args,
            account=acc_e,
            debit=amount,
            credit=0,
            against=credit_account
        ))

        gl.append(self.get_gl_dict(
            base_args,
            account=credit_account,
            debit=0,
            credit=amount,
            against=acc_e
        ))

        if gl:
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
        acc_e = h.execution_of_palm_account

        doc_t = frappe.get_doc({
            "doctype": "Palm Tree Leadger",
            "posting_date": self.posting_date,
            "cost_center": c,
            "types_of_palm_trees": self.types_of_palm_trees,
            "qty_change": -self.number,
            "incoming_rate": -self.cost_of_palm,
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
                "voucher_date":self.posting_date,
                "qty_seeding": -self.number,
                "share": -self.cost_of_palm,
                "total_share": -(flt(self.number) * flt(self.cost_of_palm)),
                "account": acc_e,
            })

            parent.save(ignore_permissions=True)


