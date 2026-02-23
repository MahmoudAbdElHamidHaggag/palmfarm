// Copyright (c) 2025, MahmoudAbdElHamidHaggag and contributors
// For license information, please see license.txt

frappe.ui.form.on("Opening Palm Balance", {
	refresh(frm) {


        if (frm.doc.docstatus === 0 && !frm.doc.__islocal) {
            frm.add_custom_button("Preview GL", function() {


                let total = flt(frm.doc.number_of_palm) * flt(frm.doc.cost_of_palm);


                let debit_account = frm.doc.type_of_implant === "Tree" 
                    ? "Bio Assets" 
                    : "Capitalization Account";

                let gl_entries = [
                    {
                        account: debit_account,
                        debit: total,
                        credit: 0,
                        remarks: `Debit for ${frm.doc.type_of_implant} - ${frm.doc.number_of_palm} palms`
                    },
                    {
                        account: "Temporary Account",
                        debit: 0,
                        credit: total,
                        remarks: `Credit for ${frm.doc.type_of_implant} - ${frm.doc.number_of_palm} palms`
                    }
                ];

                let dialog = new frappe.ui.Dialog({
                    title: "Preview GL Entries",
                    fields: [{fieldname: "html_field", fieldtype: "HTML", options: ""}]
                });

                let html = "<table class='table table-bordered'><thead><tr><th>Account</th><th>Debit</th><th>Credit</th><th>Remarks</th></tr></thead><tbody>";
                gl_entries.forEach(function(gl) {
                    html += `<tr>
                        <td>${gl.account}</td>
                        <td>${gl.debit}</td>
                        <td>${gl.credit}</td>
                        <td>${gl.remarks}</td>
                    </tr>`;
                });
                html += "</tbody></table>";

                dialog.fields_dict.html_field.$wrapper.html(html);
                dialog.show();
            });
        }

        if (frm.doc.docstatus === 1) {
            frm.add_custom_button("View GL Entry", function() {
                frappe.set_route("query-report", "General Ledger", {
                    voucher_no: frm.doc.name
                });
            });
        }
    
	},
});
