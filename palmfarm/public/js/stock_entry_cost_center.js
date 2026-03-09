frappe.ui.form.on('Stock Entry', {
    stock_entry_type: function(frm) { apply_cc(frm); },
    company: function(frm) { apply_cc(frm); },
    custom_cost_center: function(frm) { apply_cc(frm); },
    items_add: function(frm) { apply_cc(frm); },
    refresh: function(frm) { apply_cc(frm); },
    custom_number_tree: function(frm) { calculate_total(frm); },
    custom_number_seeding: function(frm) { calculate_total(frm); }
});

function apply_cc(frm) {
    if (frm.doc.docstatus === 0) {
        const cost_center = frm.doc.custom_cost_center;
        if (cost_center) {
            (frm.doc.items || []).forEach(row => {
                if (row.cost_center !== cost_center) {
                    frappe.model.set_value(row.doctype, row.name, 'cost_center', cost_center);
                }
            });
        }
    }
}

function calculate_total(frm) {
    if (frm.doc.docstatus === 0) {
        let total = flt(frm.doc.custom_number_tree) + flt(frm.doc.custom_number_seeding);
        if (frm.doc.custom_total_trees !== total) {
            frm.set_value('custom_total_trees', total);
        }
    }
}