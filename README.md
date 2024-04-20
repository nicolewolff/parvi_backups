### rsync_raw.py
This Python script first calls an rsync dry run, returning all the files with differences between Palomar and NYC. It then splits those files (if there are any) among 6 parallel threads, which call simultaneous rsyncs.

### rsync_raw.sh
This shell script calls the Python script. It is in the computer's crontab, scheduled to run daily at 19:00 UTC. 
