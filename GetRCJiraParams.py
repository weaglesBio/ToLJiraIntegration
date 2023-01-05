#!/usr/bin/env python

from ToLJiraAuth import ToLJiraAuth
import JiraMethods as jm

def main():

    sample = "eePsaMili3"

    tja = ToLJiraAuth()
    jql_request = f"project = RC AND 'Sample ID' ~ {sample} ORDER BY updated DESC"
    results = tja.auth_jira.search_issues(jql_request)

    # Return most recently created entry if there are multiple with same name.
    issue = tja.auth_jira.issue(results[0])

    print(jm.get_contamination_files_path(issue))
    print(jm.get_alternative_hic(issue))


if __name__ == "__main__":
    main()