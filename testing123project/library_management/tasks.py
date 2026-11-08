import frappe
from frappe.utils import add_days, today


def build_inventory_report(user):
    rows = frappe.get_all("Article", fields=["status"])

    summary = {
        "total": len(rows),
        "issued": sum(1 for r in rows if r.status == "Issued"),
    }

    frappe.publish_realtime(
        "inventory_report_done",
        summary,
        user=user
    )


def send_overdue_reminders():
    loan_period = (
        frappe.db.get_single_value("Library Settings", "loan_period") or 14
    )

    cutoff = add_days(today(), -loan_period)

    overdue = frappe.get_all(
        "Library Transcation",
        filters={
            "type": "Issue",
            "docstatus": 1,
            "date": ["<", cutoff]
        },
        fields=["article", "article_name", "library_member"],
    )

    for txn in overdue:
        if frappe.db.get_value("Article", txn.article, "status") != "Issued":
            continue

        email = frappe.db.get_value(
            "Library Member",
            txn.library_member,
            "email"
        )

        if email:
            frappe.sendmail(
                recipients=[email],
                subject=f"Overdue: {txn.article_name}",
                message=f"Please return <b>{txn.article_name}</b>. "
                        f"It was due after {loan_period} days.",
            )