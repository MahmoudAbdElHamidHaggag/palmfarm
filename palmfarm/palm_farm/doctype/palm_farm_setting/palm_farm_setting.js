// Copyright (c) 2026, MahmoudAbdElHamidHaggag and contributors
// For license information, please see license.txt

frappe.ui.form.on("Palm Farm Setting", {
	refresh(frm) {
        frm.set_query("biological_assets_category", () => {
            return {
                filters: {
                    is_group: 1,
                    root_type: "Asset",
                    disabled: 0,
                    freeze_account: "No"
                }
            };
        });
        frm.set_query("bio_assets_account", () => {
            let bo = frm.doc.biological_assets_category;
            let filters = {
                is_group: 0,
                disabled: 0,
                freeze_account: "No",
                account_type: "Fixed Asset"
            };

            if (bo) {
                filters.parent_account = bo;
            }
            return { filters: filters };
        });
        frm.set_query("capitalization_bio_assets_account", () => {
            let bo = frm.doc.biological_assets_category;
            let filters = [
                ["Account", "is_group", "=", 0],
                ["Account", "disabled", "=", 0],
                ["Account", "freeze_account", "=", "No"],
                ["Account", "account_type", "in", ["Fixed Capital Work in Progress", "Expenses Included In Asset Valuation"]]
            ];

            if (bo) {
                filters.push(["Account", "parent_account", "=", bo]);
            }
            return { filters: filters };
        });
        frm.fields_dict["biological_assets_category"].df.onchange = function() {
            frm.refresh_field("bio_assets_account");
        }
        frm.set_query("temporary_account", () => {
            return{
                filters:{
                    is_group: 0,
                    disabled: 0,
                    freeze_account: "No",
                    account_type: "Temporary"
                }
            }
        })
         frm.set_query("execution_of_palm_account", () => {
            return {
                filters: [
                    ["is_group", "=", 0],
                    ["disabled", "=", 0],
                    ["freeze_account", "=", "No"],
                    ["account_type", "like", "%Expense%"]
                ]
            }
        })
        frm.set_query("stock_adjustment_account", () => {
            return {
                filters: [
                    ["is_group", "=", 0],
                    ["disabled", "=", 0],
                    ["freeze_account", "=", "No"],
                    ["account_type", "=", "Stock Adjustment"]
                ]
            }
        })
        frm.set_query("parent_item_group", () => {
            return{
                filters:{
                    is_group: 1,
                }
            }
        })
        frm.set_query("parent_cost_center", () => {
            return{
                filters:{
                    is_group: 1,
                    disabled: 0,
                }
            }
        })
    }
});
