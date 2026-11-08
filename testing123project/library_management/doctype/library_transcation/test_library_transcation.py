import frappe
from frappe.tests import IntegrationTestCase


class TestLibraryTranscation(IntegrationTestCase):

    def test_cannot_issue_twice(self):
        # Create an article
        article = frappe.get_doc({
            "doctype": "Article",
            "article_name": "Test Book",
        }).insert()

        # Create a library member
        member = frappe.get_doc({
            "doctype": "Library Member",
            "first_name": "Test",
        }).insert()

        # Helper function to issue the article
        def issue():
            return frappe.get_doc({
                "doctype": "Library Transcation",
                "article": article.name,
                "library_member": member.name,
                "type": "Issue",
            }).insert()

        # First issue should succeed
        issue().submit()

        self.assertEqual(
            frappe.db.get_value("Article", article.name, "status"),
            "Issued",
        )

        # Second issue should fail
        self.assertRaises(frappe.ValidationError, issue)