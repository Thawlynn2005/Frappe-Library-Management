from frappe.model.document import Document


class LibraryMember(Document):
    def before_save(self):
        self.full_name = " ".join(filter(None, [self.first_name, self.last_name]))