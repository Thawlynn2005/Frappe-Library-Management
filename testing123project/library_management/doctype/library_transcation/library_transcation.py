import frappe
from frappe import _
from frappe.model.document import Document


class LibraryTranscation(Document):

    def validate(self):
        status = frappe.db.get_value(
            "Article", self.article, "status"
        )

        if self.type == "Issue":
            if status == "Issued":
                frappe.throw(
                    _("Article {0} is already issued").format(self.article)
                )

            self.validate_max_limit()

        elif self.type == "Return" and status == "Available":
            frappe.throw(
                _("Article {0} is not issued, so it cannot be returned")
                .format(self.article)
            )

    def validate_max_limit(self):
        max_articles = (
            frappe.db.get_single_value(
                "Library Settings", "max_articles"
            ) or 3
        )

        filters = {
            "library_member": self.library_member,
            "docstatus": 1
        }

        issued = frappe.db.count(
            "Library Transcation",
            {**filters, "type": "Issue"}
        )

        returned = frappe.db.count(
            "Library Transcation",
            {**filters, "type": "Return"}
        )

        if issued - returned >= max_articles:
            frappe.throw(
                _("Member has reached the limit of {0} articles")
                .format(max_articles)
            )

    def on_submit(self):
        new_status = (
            "Issued" if self.type == "Issue" else "Available"
        )

        frappe.db.set_value(
            "Article", self.article, "status", new_status
        )

    def on_cancel(self):
        old_status = (
            "Available" if self.type == "Issue" else "Issued"
        )

        frappe.db.set_value(
            "Article", self.article, "status", old_status
        )