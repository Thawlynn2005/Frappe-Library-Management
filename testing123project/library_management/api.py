
import frappe
from frappe.utils import today


@frappe.whitelist(allow_guest=True)
def available_articles(search: str | None = None):
    """Public catalogue of available articles."""

    filters = {"status": "Available"}

    if search:
        filters["article_name"] = ["like", f"%{search}%"]

    return frappe.get_all(
        "Article",
        filters=filters,
        fields=["name", "article_name", "author", "image"],
        order_by="article_name asc",
    )


@frappe.whitelist(methods=["POST"])
def issue_article(article: str, member: str):
    """Create and submit an article issue transaction."""

    doc = frappe.get_doc({
        "doctype": "Library Transcation",
        "article": article,
        "library_member": member,
        "type": "Issue",
        "date": today(),
    })

    doc.insert()
    doc.submit()

    return doc.name

@frappe.whitelist()
def start_inventory_report():
    frappe.enqueue(
        "testing123project.library_management.tasks.build_inventory_report",
        queue="long",
        job_id="inventory_report",
        deduplicate=True,
        user=frappe.session.user,
    )