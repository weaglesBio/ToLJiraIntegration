#!/usr/bin/env python

from ToLJiraAuth import ToLJiraAuth
import JiraMethods as jm

jql_field_map = {"tolid": "'Sample ID'",
                "species_name": "'Species Name'",
                "jira_issue": "key",
                "jira_issue_last_updated": "updated",
                "jbrowse_link": "'Datatype Available'" } # Last to be updated when correct field available in JIRA

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

def get_all_from_jira(page_size, page_number, filter, sort_by, password_eagles):

    tja = ToLJiraAuth(password = password_eagles)
    jql_request = apply_filter_sort_to_jql("project in (GRIT,RC)", filter, sort_by)

    # Return all results for page until the number requested.
    results = tja.auth_jira.search_issues(jql_request, maxResults=page_size*page_number)

    entries_len = len(results)
    offset = page_size * (page_number - 1)

    page_first_row = offset + 1 
    page_last_row = offset + page_size

    if entries_len < page_last_row:
        filtered_jira_results = results[page_first_row-1:entries_len]
    else:
        filtered_jira_results = results[page_first_row-1:page_last_row]

    entries = []
    for i in filtered_jira_results:
        issue = tja.auth_jira.issue(i)
        entry = {}
        entry["tolid"] = jm.get_species_id(issue)
        entry["species_name"] = jm.get_species_name(issue)
        entry["jira_issue"] = issue.key
        entry["jira_issue_link"] = f"{tja.jira_path}/browse/{issue.key}"
        entry["jira_issue_last_updated"] = issue.fields.updated
        entry["jbrowse_link"] = f""
        entries.append(entry)

    return {'total': entries_len, 'data': entries}

def get_record_from_jira(id, password_eagles):
    return get_all_from_jira(1, 1, f'[id={id}]', 'id', password_eagles)[0]

def main():
    print(get_all_from_jira(5, 2, f'[]', 'jira_issue',""))
    


if __name__ == "__main__":
    main()