class Node:
    def __init__(self, name, link, preconditions, triggers, description, postconditions,
    references):
        self.name = name
        self.link = link
        self.preconditions = list(preconditions)
        self.triggers = list(triggers)
        self.description = list(description)
        self.postconditions = list(postconditions)
        self.references = list(references)

    def __str__(self):
        return "Name: %s\nLink: %s\nPreconditions: %s\nTriggers: %s\n"  \
            "Description: %s\nPostconditions: %s\nReferences: %s" % (self.name, self.link,
            ", ".join(self.preconditions), ", ".join(self.triggers),
            ", ".join(self.description), ", ".join(self.postconditions), ", ".join(self.references))

    def get_name(self):
        return self.name

    def get_preconditions(self):
        return self.preconditions

    def get_triggers(self):
        return self.triggers

    def get_description(self):
        return self.description

    def get_postconditions(self):
        return self.postconditions

    def get_references(self):
                     return self.references

    def remove_preconditions(self, node):
        self.preconditions.remove(node)

    def remove_triggers(self, node):
        self.triggers.remove(node)

    def remove_description(self, node):
        self.description.remove(node)

    def remove_postconditions(self, node):
        self.postconditions.remove(node)

    def remove_references(self, node):
        self.references.remove(node)

    def set_preconditions(self, preconditions):
        self.preconditions = list(preconditions)

    def set_triggers(self, triggers):
        self.triggers = list(triggers)

    def set_description(self, description):
        self.description = list(description)

    def set_postconditions(self, postconditions):
        self.postconditions = list(postconditions)

    def set_references(self, references):
        self.references = list(references)