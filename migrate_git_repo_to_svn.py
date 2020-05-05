# coding:utf-8
# author: CGWang
# git_repo: https://github.com/CGWang/migrate_git_repo_to_svn

import os
import shutil
from datetime import datetime 


# your local git local path
git_repo_path = "replace with your local git repo path"
svn_repo_path = "replace with local svn folder path" # better to be an empty svn folder

# if you want to keep author info, config the following info
commiter_mapping_info = [
	# {
	# 	'git_user_name' : '# replace: git commiter name 1',
	# 	'svn_user_name' : '# replace: svn name of git commiter 1',
	# 	'svn_password' : '# replace: svn password of svn name',
	# },
	{
		'git_user_name' : " xx's git username",
		'svn_user_name' : " xx's svn username",
		'svn_password' : " xx's svn password",
	},
]

# set to 'None' to start migrating from beginning. 
migrate_from_git_sha = None


def run_command_with_path(cmd_str, cmd_path):
	os.chdir(cmd_path)
	ret = os.system(cmd_str)
	if ret != 0:
		os._exit(0)


# update git and svn
def update_files_to_local():
	run_command_with_path("git pull", git_repo_path)
	run_command_with_path("svn update", svn_repo_path)


# get all git commit info
def fetch_git_commit_info_list():
	os.chdir(git_repo_path)

	result = os.popen("git log --pretty=format:'%H` %an` %s' | grep '`'")
	res = result.read()
	git_message_list = []
	for line in res.splitlines():
		git_message_list.append(line)

	return git_message_list


def make_folder_empty(folder_path):
	os.chdir(folder_path)
	
	dir_list = os.listdir(folder_path)
	for cont in dir_list:
		path = os.path.join(folder_path, cont)
		if os.path.isfile(path):
			os.remove(path)
		else:
			if '.git' not in path and '.svn' not in path:
				shutil.rmtree(path)


def commit_all_svn_changes(author, message):
	os.chdir(svn_repo_path)

	# svn add files 
	run_command_with_path('svn add --force .', svn_repo_path)

	# svn remove files
	# run_command_with_path("svn status | grep '^!' | awk '{print $2}' | xargs svn delete", svn_repo_path)
	# result = os.popen("svn status | grep '^!' | awk '{print $2, $3}'") # $3 for white space in file name or folder name
	result = os.popen("svn status | grep '^!'")
	res = result.read()
	for line in res.splitlines():
		line = line[1:]

		# handle filename with multi space
		while line.startswith(' '):
			line = line[1:]
		while line.endswith(' '):
			line = line[:-1]

		if '@' in line:
			line = line + '@' # handle filename with '@'
		# line = line.replace('(', "'('")
		# line = line.replace(')', "')'")
		line = line.replace('"', "'")

		delete_cmd = 'svn delete --force "' + line + '"'
		run_command_with_path(delete_cmd, svn_repo_path)

	# replace illegal char
	message = message.replace('"', ' ')
	message = message.replace("'", ' ')

	# svn commit files
	cmd = "svn commit -m '  " + author + " : " + message + "'"
	for commiter_info in commiter_mapping_info:
		if author in commiter_info['git_user_name']:
			cmd = "svn commit -m '" + message + "'" + ' --username ' + commiter_info['svn_user_name'] + ' --password ' + commiter_info['svn_password']
			break

	run_command_with_path(cmd, svn_repo_path)


# copy every git commit to svn 
def sync_git_commits_to_svn():
	git_message_list = fetch_git_commit_info_list()

	has_start_migrate = True
	if migrate_from_git_sha:
		has_start_migrate = False

	total_msg_count = len(git_message_list)
	for i in range(total_msg_count - 1, -1, -1):
		if migrate_from_git_sha and migrate_from_git_sha in git_message_list[i]:
			has_start_migrate = True

		if has_start_migrate == False:
			print('skip git commit: ' + git_message_list[i])
			continue

		print('start migrating git commit :  ' + git_message_list[i])
		commit_info_list = git_message_list[i].split('` ')
		
		run_command_with_path("git reset --hard " + commit_info_list[0], git_repo_path)
		run_command_with_path("git clean -f -d", git_repo_path)

		# clear svn folder
		run_command_with_path("svn update", svn_repo_path)
		make_folder_empty(svn_repo_path)

		# copy git files to svn folder
		copy_cmd = "cp -r " + git_repo_path + "/* " + svn_repo_path
		run_command_with_path(copy_cmd, svn_repo_path)

		commit_all_svn_changes(commit_info_list[1], commit_info_list[2])
		print(' =========== finish migrating : %d / %d  =========== ' % (total_msg_count - i, total_msg_count))


if __name__ == '__main__':
	start_time = datetime.now()

	update_files_to_local()
	sync_git_commits_to_svn()
	
	total_seconds = (datetime.now() - start_time).total_seconds()
	print(" Minutes used: %d minutes, %d seconds" % ((total_seconds / 60), (total_seconds % 60)))
