import os
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

src = "/proj/parvi/data/raw/"
dest = "tron@dnah.amnh.org:/export/parvi/data/data/raw/"
dest_dir = "/export/parvi/data/data/raw/"
log_file = "/home/parvi/AutomatedBackup/DryRun.log"
rsync_log_file = "/home/parvi/AutomatedBackup/RawBackup.log"
num_processes = 6

def rsync_dryrun(depth):
    rsync_output = subprocess.check_output('rsync -vrt --dry-run --log-file="{}" {} {}'.format(log_file, src, dest), shell=True).decode('utf-8')
    output_lines = rsync_output.split('\n')[2:-3]
    dryrun_dirs = [line.split()[-1] for line in output_lines if len(line.split()) >= 1]
    dirs = [dirpath for dirpath in dryrun_dirs if (dirpath.count(os.path.sep) == depth) and ('.' not in dirpath)]
    days = [dirpath for dirpath in dryrun_dirs if (dirpath.count(os.path.sep) == 3)]
    return dirs, days

def sync_files(src_dest):
    src_folder, dest_folder = src_dest
    subprocess.call(["rsync", "-vrt", "{}".format(src_folder), "{}".format(dest_folder), "--log-file={}".format(rsync_log_file)])
    current_date = subprocess.check_output(['date', '+%Y-%m-%d %H:%M:%S']).decode().strip()
    size = subprocess.check_output(["du", "-sh", src_folder]).decode().strip()
    subprocess.run('echo "{}: Finished with {}, Size: {}" >> "{}"'.format(current_date, src_folder, size, log_file),shell=True)

if __name__ == "__main__":
    subprocess.call('echo "$(date "+%Y-%m-%d %H:%M:%S"): Starting dry run" >> "{}"'.format(log_file),shell=True)
    directories, days = rsync_dryrun(depth=4)
    for day in days:
        subprocess.call(["ssh", "-t", "tron@dnah.amnh.org", "mkdir -p {}/{}".format(dest_dir, day)])

    subprocess.call('echo "$(date "+%Y-%m-%d %H:%M:%S"): Finished dry run" >> "{}"'.format(log_file),shell=True)

    paths = [(os.path.join(src, directory), os.path.join(dest, directory)) for directory in directories]

    with ThreadPoolExecutor(max_workers=num_processes) as executor:
        print("Paths: ",paths)
        print("Number of paths: ",len(paths))
        futures = {executor.submit(sync_files, path): path for path in paths}
        for future in as_completed(futures):
            path = futures[future]
            try:
                future.result()
            except Exception as e:
                print("Error occurred while processing {path}: {}".format(e))

