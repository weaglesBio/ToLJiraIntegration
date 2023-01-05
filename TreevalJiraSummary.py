#!/usr/bin/env python

from ToLJiraAuth import ToLJiraAuth
import JiraMethods as jm

jql_field_map = {"tolid": "'Sample ID'",
                "species_name": "'Species Name'",
                "jira_ticket": "key",
                "last_updated": "updated",
                "jbrowse_hyperlink": "'Datatype Available'" } # Last to be updated when correct field available in JIRA

def add_contains_str_filter(filter_dict, field_key):
    field_value = filter_dict.get(field_key,"")
    return f" AND {jql_field_map[field_key]} ~ '*{field_value}*'" if field_value else ""

def parse_filter_str_to_dict(filter_str):
    filter_dict = {}

    # Trim '[' and ']'
    filter_str = filter_str[1:-1]

    for filter_val in filter_str.split(","):
        filter_tuple = filter_val.split("==")

        if len(filter_tuple) >= 2:
            filter_dict[filter_tuple[0]] = filter_tuple[1]

    return filter_dict

def apply_filter_sort_to_jql(jql, filter, sort_by):
    # As JIRA field names do not match those within application, fields need mapping then adding to jql.

    # Convert filter string to dictionary
    filter_dict = parse_filter_str_to_dict(filter)
 
    # Add filters to fields, if filter set.
    jql += "".join([add_contains_str_filter(filter_dict, key) for key in jql_field_map])

    # Add sort to JQL
    (sort_field, sort_direction) = (sort_by[1:], "DESC") if sort_by[0] == "-" else (sort_by, "ASC")
    jql += f" ORDER BY {jql_field_map[sort_field]} {sort_direction}" if sort_field or jql_field_map[sort_field] else ""

    return jql

def get_all_from_jira(page_size, page_number, filter, sort_by):

    tja = ToLJiraAuth()
    jql_request = apply_filter_sort_to_jql("project in (GRIT,RC)", filter, sort_by)

    # Return all results for page until the number requested.
    results = tja.auth_jira.search_issues(jql_request, maxResults=page_size*page_number)

    # Filter down to selected page (last returned).
    num_entries_on_last_page = len(results) % page_size if not 0 else page_size
    filtered_jira_results = results[-num_entries_on_last_page:]

    entries = []
    for i in filtered_jira_results:
        issue = tja.auth_jira.issue(i)
        entry = {}
        entry["tolid"] = jm.get_species_id(issue)
        entry["species_name"] = jm.get_species_name(issue)
        entry["jira_ticket"] = issue.key
        entry["jira_ticket_hyperlink"] = f"{tja.jira_path}/browse/{issue.key}"
        entry["last_updated"] = issue.fields.updated
        entry["jbrowse_availability"] = False
        entry["jbrowse_hyperlink"] = f""
        entries.append(entry)

    print(entries)

    return entries

def get_record_from_jira(id):
    return get_all_from_jira(1, 1, f'[id={id}]', 'id')[0]

def main():
    get_all_from_jira(10, 1, f'[]', 'last_updated')

if __name__ == "__main__":
    main()