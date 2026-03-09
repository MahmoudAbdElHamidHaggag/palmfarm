// Copyright (c) 2026, MahmoudAbdElHamidHaggag and contributors
// For license information, please see license.txt

frappe.ui.form.on("Adding a date harvest", {
    types_of_palm_trees: function(frm) {
        if (frm.doc.types_of_palm_trees) {

            frappe.db.get_single_value("Palm Farm Setting", "date_harvest_item")
                .then(val => {
                    if (val) {

                        frm.set_value("date_harvest_item", val);
                    } else {

                        frm.set_value("date_harvest_item", "");
                        

                        frappe.msgprint({
                            title: __('Configuration Missing'),
                            message: __("Please set 'Date Harvest Item' in 'Palm Farm Setting' before proceeding."),
                            indicator: 'red'
                        });
                    }
                });
        }
    },
    

    before_save: function(frm) {
        if (frm.doc.types_of_palm_trees && !frm.doc.date_harvest_item) {
            frappe.throw(__("Action cancelled: 'Date Harvest Item' is not configured in Palm Farm Settings."));
        }
    }
});