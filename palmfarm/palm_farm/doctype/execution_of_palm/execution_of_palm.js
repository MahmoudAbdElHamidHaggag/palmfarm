// Copyright (c) 2026, MahmoudAbdElHamidHaggag and contributors
// For license information, please see license.txt

frappe.ui.form.on('Execution of Palm', {
    type_of_implant: function(frm) {
        frm.set_value('cost_of_palm', 0);
        frm.set_value('total_of_cost', 0);
    },
    types_of_palm_trees: function(frm) {
        frm.set_value('cost_of_palm', 0);
        frm.set_value('total_of_cost', 0);
    }
});