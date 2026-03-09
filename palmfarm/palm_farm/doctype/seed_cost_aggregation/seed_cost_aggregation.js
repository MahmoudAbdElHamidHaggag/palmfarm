// Copyright (c) 2026, MahmoudAbdElHamidHaggag and contributors
// For license information, please see license.txt

frappe.ui.form.on("Seed Cost Aggregation", {
	refresh: function (frm) {
		frm.page.btn_secondary.hide();
		frm.page.btn_primary.hide();
		if(!frm.doc.add_of_palm && frm.doc.total_qty > 0){
			frm.add_custom_button("Create Add Asset", function() {
				frappe.call({
					method: "palmfarm.palm_farm.doctype.seed_cost_aggregation.seed_cost_aggregation.create_add",
					args: {
						docname: frm.doc.name
					},
					callback: function(r) {
						if(!r.exc) {
							frm.set_value("add_of_palm", r.message);
							frm.save().then(() => {
								frappe.msgprint("Add of Palm created: " + r.message);
								frm.refresh_field("add_of_palm");
							});
						}
					}
				});
			});
		}
    }
});
