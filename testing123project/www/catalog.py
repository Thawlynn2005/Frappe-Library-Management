import frappe

no_cache = 1


def get_context(context):
    # Block users who are not logged in
    if frappe.session.user == "Guest":
        raise frappe.PermissionError

    context.title = "Library Catalog"
    context.articles = frappe.get_all(
        "Article",
        fields=["name", "article_name", "author", "status"],
        order_by="article_name asc",
    )