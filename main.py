# Steps
# Get the token from gitlab and the username

import requests
import os
import json

cache_enabled = False
cache_file = 'data.json'
token = 'GSAgpoqMW5sSCEGaMXtB'
url = 'https://gitlab.avantiplc.net/api/v4'
users_url = url + '/users'
user_projects_url = url + '/users/rdias/projects'
projects_url = url + '/projects'
project_merge_requests = url + '/projects/:id/merge_requests'
merge_request_url = url + '/projects/:id/merge_requests/:merge_request_iid/approvals'

def save_to_file(d, file_name=None):
    if file_name == None:
        file_name = cache_file
    with open('./cache/' + file_name, 'w') as f:
        f.write(d)

def get_merge_requests_for_project(item):
    pr_url = project_merge_requests.replace(':id', str(item['id']), -1)
    pr_resp = requests.get(pr_url, params={'private_token':token}).text
    if cache_enabled == True:
        save_to_file(pr_resp, str(item['name'])+'.pr.json')
    pr_obj = json.loads(pr_resp)
    return pr_obj

def get_merge_request(item, iid):
    mr_url = merge_request_url.replace(':id', str(item['id']), -1).replace(':merge_request_iid', str(iid), -1)
    mr_resp = requests.get(mr_url, params={'private_token':token}).text
    if cache_enabled == True:
        save_to_file(mr_resp, str(item['name'])+'.mr.json')
    return json.loads(mr_resp)

def debug(o):
    print(o)
    quit()


# Program start

if cache_enabled == False:
    data = requests.get(projects_url, params={'private_token':token})

if os.path.isfile(cache_file) == False or cache_enabled == True:
    if os.path.isfile(cache_file) == True:
        os.unlink(cache_file)
    data = requests.get(projects_url, params={'private_token':token})
    save_to_file(data.text)
    with open('./cache/' + cache_file, 'r') as f:
        data = f.read()

obj = json.loads(data)

for item in obj:
    name = item['name']
    print ("#" * 10 +' '+ name + ' ' +"#" * 10)
    pr_obj = get_merge_requests_for_project(item)
    if len(pr_obj) > 0:

        num_requests = 0
        for pr in pr_obj:
            if pr['state'] == 'open' or pr['state'] == 'opened':
                num_requests += 1

        mr = get_merge_request(item, pr_obj[0]['iid'])
        print ('Name:', name)
        print('link:', item['web_url'])
        print('Merge requests:', num_requests)
        # print('Approvals Required:', mr['approvals_required'])
        # print('Approvals Left:', mr['approvals_left'])
        print('Merge Status:', pr_obj[0]['merge_status'])
    else:
        print (name, item['web_url'], 0)
    print ("#" * 11 + "#" * len(name) + "#" * 11 + "\n\n")
    
        


