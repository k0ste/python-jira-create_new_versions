# python-jira-create_new_versions

Create new versions from JSON for all JIRA projects

##Options:
* json-file: provide json file with versions definition
* scope: how far parse present versions for each project. For example you need generate 12 versions for the year ahead (one version as working plan for the month). Before generate version, you need to make sure is not preset, i.e not created by user (project administrator). 'scope' is a how deep enter for search versions.
