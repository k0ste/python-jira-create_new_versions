#!/usr/bin/python2

'''
GPL
2015, Konstantin Shalygin (k0ste[at]cn.ru)
version: 0.1
'''

import json
import os
from optparse import OptionParser
from jira import JIRA, JIRAError

def get_jira_projects():
    jira_all_projects = jira.projects()
    '''Return all project as list'''
    jira_all_projects = [project.key for project in jira_all_projects]
    try:
        return jira_all_projects
    except JIRAError:
        raise SystemExit('Can\'t get all JIRA projects')

def version_generator(jira_all_projects, version_scope):
    for element in jira_all_projects:
        print 'Working on project:', element
        project_last_versions = get_last_versions(element, version_scope)
        json_versions(json_full, project_last_versions, element)

def get_last_versions(jira_project_key, version_scope):
    jira_all_versions = jira.project_versions(jira_project_key)
    '''Return last project versions as list'''
    jira_versions = ([version.name for version in reversed(jira_all_versions)][0:version_scope])
    try:
        return jira_versions
    except JIRAError:
        raise SystemExit('Can\'t get JIRA versions for project: \'%s\'' % jira_project_key)

def json_versions(json_full, jira_versions, jira_project_key):
    for version_index in range(len(json_full['versions'])):
        json_version = json_full['versions'][version_index]['ver']
        json_desc = json_full['versions'][version_index]['desc']
        json_start_date = json_full['versions'][version_index]['start_date']
        json_release_date = json_full['versions'][version_index]['release_date']
        version_comparator = compare_versions(jira_versions, json_version)
        if version_comparator == True:
            '''If returned value is True - version is present, skip it'''
            print 'For project', jira_project_key, 'version:', json_version, 'is preset, I pass'
            pass
        elif version_comparator == None:
            '''Version is not present, try create it'''
            print 'For project', jira_project_key, 'version:', json_version, 'is not present\n', 'I generate it with start date', json_start_date, 'and release date', json_release_date
            try:
                jira.create_version(name=json_version, project=jira_project_key, description=json_desc, releaseDate=json_release_date, startDate=json_start_date)
            except JIRAError:
                print 'Can\'t generate version: \'%s\' for project \'%s\', with start date: \'%s\', release date: \'%s\', desc: \'%s\'' % (json_version, jira_project_key, json_start_date, json_release_date, json_desc)
                raise SystemExit

def compare_versions(jira_versions, json_version):
    for element in jira_versions:
        if element in json_version:
            return True

def main():
    '''Check jira module installed or not'''
    try:
        from jira import JIRA
    except ImportError:
        print 'python-jira not found, please install it'
        raise SystemExit

    parser = OptionParser(usage='%prog -s http://localhost/jira -j JSONFILE -u admin -p admin', version='%prog 0.1')
    parser.add_option('-s', '--server', type='string', dest='jira_server', help='JIRA instance')
    parser.add_option('-j', '--json-file', type='string', dest='json_file', default='versions.json', help='The json versions definition')
    parser.add_option('-u', '--username', type='string', dest='jira_username', default='admin', help='Username of JIRA account for auth basic [default: %default]')
    parser.add_option('-p', '--password', type='string', dest='jira_password', default='admin', help='Password of JIRA account for auth basic [default: %default]')
    parser.add_option('--scope', type='int', dest='version_scope', default='12', help='How many versions for parse [default: %default]')
    (options, args) = parser.parse_args()

    '''If server/user/pwd is not defined or json file not found'''
    if not (options.jira_server or options.jira_username or options.jira_password):
        parser.print_help()
        raise SystemExit
    if not os.path.isfile(options.json_file):
        raise SystemExit('Unable to open \'%s\'' % options.json_file)

    global jira
    try:
        jira = JIRA(server=options.jira_server, basic_auth=(options.jira_username, options.jira_password))
    except JIRAError:
        print 'Can\'t connet to JIRA on: \'%s\' with username \'%s\' and password \'%s\'' % (options.jira_server, options.jira_username, options.jira_password)
        raise SystemExit

    '''If all checks ok, load json data'''
    with open(options.json_file) as json_data:
        global json_full
        json_full = json.loads(json_data.read())

    version_scope = options.version_scope
    jira_all_projects = get_jira_projects()
    version_generator(jira_all_projects, version_scope)

if __name__ == "__main__":
  main()
