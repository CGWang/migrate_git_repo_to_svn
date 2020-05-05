# migrate_git_repo_to_svn


# Reason:
I am working on a project using gitlab. For some reason, I had to migrate the whole repo to svn, without losing any commit info.

After googling a long time, I decided to write a script to do the job. And also, I had already used it, it works Great.


# Env Requirements:
# Mac shell. (Tested on macos Catalina, but it should run on windows powershell or linux shell)
# Python3


# Usage:
1. Clone git folder to local disk, also checkout an empty svn folder to local.
2. Config `migrate_git_repo_to_svn.py`:
  2.1: fill `git_repo_path` and `svn_repo_path` with your local path.
  2.2: if you want every svn commit with the right author, config `commiter_mapping_info` with all users's name and password. Ofcourse, if you do not care, leave it as it is.
3. Run command in shell: `python3 migrate_git_repo_to_svn.py`
4. Get yourself a cup of coffee, and waiting. It may take several hours, depending on how large your git repo is.(It took me 3 hours to migrate about 2k git commits...)


# How it works：
1. Get all git log, in descending order.
2. Looping the git log, get every commit sha:
  2.1. Reset local git repo to that commit.
  2.2. Clear svn folder, and copy everything except `.git` to local svn folder.
  2.3. In svn folder, use `svn add` and `svn delete` to record all file changes, and then `svn commit` them, using the same git log.
  (also using the same git user, if you provide svn username and password)
3. The step 2 will loop every git commit, and migrate them to svn, until all git commit is migrated.


# Note（important）：
1. Submodule folder is not supported default. submodule is such a terrble design, which is the main reason I abandon git. But, you can also use `migrate_git_repo_to_svn.py` to migrate submodule folder:
  For example, my git repo `git_repo` has a submodule in `git_repo\stupid_submodule_folder`, then
  Config `migrate_git_repo_to_svn.py`, fill `git_repo_path` with `git_repo\stupid_submodule_folder`, and fill `svn_repo_path` with `svn_repo\stupid_submodule_folder`
2. While migrating, it may went wrong sometimes, due to some stange filenames which `svn commit` do not support. I had fixed most of them. In case of some conditions I missed, and after the bug fixed, you can use `migrate_from_git_sha`, to tell the script to continue the migrating from specified git commit, other than starting over again.
