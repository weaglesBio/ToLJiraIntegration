import yaml
from yaml.loader import SafeLoader

# Methods for reading from JIRA object.

def get_species_name(issue):
    species_name = issue.fields.customfield_11676

    if species_name:

        # Trim unused common name
        suffix = " ()"
        if species_name.endswith(suffix):
            species_name = species_name[:-len(suffix)]

        return species_name
    else:
        return ""

def get_species_id(issue):
    species_id = issue.fields.customfield_11627

    if species_id:
        return species_id
    else:
        return ""

def get_contamination_files_path(issue):
    con_file_path = issue.fields.customfield_11677

    if con_file_path:
        return con_file_path
    else:
        return ""

def get_yaml_attachment(issue):
    for attachment in issue.fields.attachment:
        if attachment.filename.endswith('.yaml'):
            yaml_data = yaml.load(attachment.get(), Loader=SafeLoader)
            return yaml_data

def get_alternative_hic(issue):
    yaml_data = get_yaml_attachment(issue)
    yaml_notes = yaml_data["notes"]

    for yaml_note in yaml_notes:
        # Trim unused common name
        prefix = "hic data was from "
        if yaml_note.startswith(prefix):
            return yaml_note[len(prefix):]