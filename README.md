# migrate git repository to svn repository


# Background:
I am working on a project using gitlab. For some reason, I had to migrate the whole repo to svn, without losing any git log.

After googling a long time, I decided to write a script to do the job.  And also, I had already used it, and it worked Great.

**This script will do no harm to the git repo, all it needs is clone your git repo to local folder, and provide an empty svn folder. That's all.**

---

# Env Requirements:
1. Mac.     (I tested on macos Catalina, but it should work on windows powershell or linux shell).
2. Python3.



# Usage:
1. Clone git repo to disk, also checkout an EMPTY svn folder to disk.
2. Config `migrate_git_repo_to_svn.py`:
   - fill `git_repo_path` and `svn_repo_path` with local path.
   - if you want every svn commit with the right author, config `commiter_mapping_info` with all team member's username and password. Ofcourse, if you do not care, leave it as it is.
3. Run command in shell: `python3 migrate_git_repo_to_svn.py`
4. Get yourself a cup of coffee, and waiting. It may take several hours, depending on how large your git repo is.(It took me 3 hours to migrate about 2k git commits...)


---

# Note（!important!）：
1. Submodule folder is not supported default. Submodule is such a terrble design in git, which is the main reason I abandon git. But, you can also use `migrate_git_repo_to_svn.py` to migrate submodule folder:
   - For example, my git repo `git_repo` has a submodule called `git_repo\stupid_submodule_folder`, then
   - Config `migrate_git_repo_to_svn.py`, fill `git_repo_path` with `git_repo\stupid_submodule_folder`, and fill `svn_repo_path` with `svn_repo\stupid_submodule_folder`.
   - Make sure your local submodule folder is on the master branch! (Usually it's not)
2. While migrating, it may went wrong sometimes, due to some stange filenames which `svn commit` do not support, I have fixed most of them. If there are some conditions I missed, and when you fixed it, you can use `migrate_from_git_sha`  to tell the script to continue  migrating from the specified git commit, other than starting all over again.



# How it works：
1. Get all git log.
2. In descending order, looping the git logs, get every git commit sha:
   - Reset local git repo to that commit sha.
   - Clear svn folder, and copy everything from git folder except `.git` to local svn folder.
   - In svn folder, use `svn add` and `svn delete` to record all file changes, and then `svn commit` them, using the same git log.
  (also using the same git author, if you provide svn username and password)
3. The step 2 will loop every git commit, and migrate them to svn, until all git commits is migrated.
