// Copyright (c) 2026, MahmoudAbdElHamidHaggag and contributors
// For license information, please see license.txt

frappe.ui.form.on('Add of Palm', {

    number: function(frm) {
        calculate_total(frm);
    },

    purchase_cost: function(frm) {
        calculate_total(frm);
    },
    refresh(frm){
        frm.set_query("payment_account", () => {
            return {
                filters: {
                    is_group: 0,
                    account_type: ["in", ["Cash", "Bank"]],
                    disabled: 0,
                    freeze_account: "No"
                }
            };
        });
        if(frm.doc.source ===  "Added from the collection" && frm.doc.auto_generated !== 1){
            frappe.msgprint(__("This Choose For Auto Genrated Only"));
            frm.set_value("source", "");
        }
    }

});

function calculate_total(frm) {
    if (frm.doc.number && frm.doc.purchase_cost) {
        frm.set_value(
            "total_cost",
            frm.doc.number * frm.doc.purchase_cost
        );
    } else {
        frm.set_value("total_cost", 0);
    }
}

