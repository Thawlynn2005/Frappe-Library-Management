// Copyright (c) 2026, Frappe Technologies and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Library Transcation", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on("Library Transcation", {
	refresh(frm) {
		// Only show available articles when issuing
		frm.set_query("article", () => {
			if (frm.doc.type === "Issue") {
				return {
					filters: {
						status: "Available",
					},
				};
			}
		});

		if (frm.doc.docstatus === 1 && frm.doc.type === "Issue") {
			frm.add_custom_button(__("Return Article"), () => {
				frappe.new_doc("Library Transcation", {
					article: frm.doc.article,
					library_member: frm.doc.library_member,
					type: "Return",
				});
			});
		}
	},
});
