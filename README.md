These files are located in ~/AutomatedBackup/ on the PARVI computer.

### rsync_raw.py
This Python script first calls an rsync dry run, returning all the raw data files with differences between Palomar and NYC. It then splits those files (if there are any) among 6 parallel threads, which call simultaneous rsyncs.
**DryRun.log** tracks the files returned in the daily dry run. **RawBackup.log** tracks the status of the actual rsync backup. **crontab_rawbackup.log** tracks the status of the cronjob for the raw data backup, and **crontab_backup.log** tracks the status of the cronjob for the slope/log file backup, which is not parallelized.

### rsync_raw.sh
This shell script calls the Python script. It is in the computer's crontab (edit using "crontab -e"), scheduled to run daily at 7pm PDT or 6pm PST. 

The slope file backup is scheduled to run daily at 9pm PDT or 8pm PST.
