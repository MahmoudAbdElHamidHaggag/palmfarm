// Copyright (c) 2026, MahmoudAbdElHamidHaggag and contributors
// For license information, please see license.txt

frappe.ui.form.on("Cost And Production Aggregation", {
    refresh(frm) {
        frm.disable_save();
        frm.page.btn_secondary.hide();
        frm.page.btn_primary.hide();
        
        fetch_harvest_item(frm);

        if (!frm.is_new() && frm.doc.status === "Open" && !frm.doc.add_havest_voucher) {
            frm.add_custom_button(__('إضافة التمر الخام'), function() {
                frappe.confirm(__('هل أنت متأكد من إنشاء سند إضافة مخزنية بالتكلفة المحسوبة؟'), function() {
                    frm.call({
                        doc: frm.doc,
                        method: "create_stock_entry",
                      
                        callback: function(r) {
                            if (!r.exc) {
                                frappe.msgprint({
                                    title: __('نجاح'),
                                    message: __('تم إنشاء سند الإضافة برقم: ') + r.message,
                                    indicator: 'green'
                                });
                                frm.reload_doc();
                            }
                        }
                    });
                });
            }, __("الإجراءات"));
        }
    },
    
    types_of_palm_trees: function(frm) {
        fetch_harvest_item(frm);
    }
});

function fetch_harvest_item(frm) {
    if (frm.doc.types_of_palm_trees) {
        frappe.db.get_single_value("Palm Farm Setting", "date_harvest_item")
            .then(val => {
                if (val) {
                    frm.set_value("date_harvest_item", val);
                    frm.page.btn_primary.show();
                } else {
                    frm.set_value("date_harvest_item", "");
                    frm.page.btn_primary.hide();
                    
                    if (frm.doc.types_of_palm_trees) {
                        frappe.msgprint({
                            title: __('إعدادات مفقودة'),
                            message: __("يرجى تحديد 'صنف حصاد التمور' في 'إعدادات مزرعة النخيل' للمتابعة."),
                            indicator: 'red'
                        });
                    }
                }
            });
    }
}