#!/usr/bin/python3

#install redis and run redis and stop redis and take backup redis
import sys
import subprocess
import shutil
import tarfile
import os

# backup directory path
backup_dir = '/home/vagrant/db_backup'

def install_redis():
    try:
        # Update package lists
        print("Updating package lists...")
        subprocess.run(['sudo', 'apt-get', 'update'], check=True)
        
        # Install Redis server
        print("Installing Redis server...")
        subprocess.run(['sudo', 'apt-get', 'install', '-y', 'redis-server'], check=True)
        
        # Enable Redis to start on system boot
        print("Enabling Redis to start on system boot...")
        subprocess.run(['sudo', 'systemctl', 'enable', 'redis-server'], check=True)
        
        # Start Redis server
        print("Starting Redis server...")
        subprocess.run(['sudo', 'systemctl', 'start', 'redis-server'], check=True)
        
        # Check Redis server status
        print("Checking Redis server status...")
        subprocess.run(['sudo', 'systemctl', 'status', 'redis-server'], check=True)
        
        print("Redis installation and setup completed successfully.")
        
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during the installation process: {e}")
        exit(1)

def start_redis():
    try:
        print("Starting Redis server...")
        subprocess.run(['sudo', 'systemctl', 'start', 'redis-server'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during the installation process: {e}")
        exit(1)
def stop_redis():
    try:
        print("Stopping Redis server...")
        subprocess.run(['sudo', 'systemctl', 'stop', 'redis-server'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during the installation process: {e}")
        exit(1)
def check_redis_status():
    try:
        print("Stopping Redis server...")
        subprocess.run(['sudo', 'systemctl', 'status', 'redis-server'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred Checking Redis server status: {e}")
        exit(1)

def backup_redis_db(backup_dir):
    try:
        print("Backing up Redis database...")

        # Path to Redis dump file
        redis_dump_path = '/var/lib/redis/dump.rdb'
        temp_dump_path = '/tmp/dump.rdb'

        # Ensure the backup directory exists
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        # Copy the Redis dump file to a temporary location with sudo
        subprocess.run(['sudo', 'cp', redis_dump_path, temp_dump_path], check=True)
        print(f"Copied dump.rdb to {temp_dump_path}")

        # Change ownership of the copied dump file to the current user
        subprocess.run(['sudo', 'chown', f'{os.geteuid()}:{os.getegid()}', temp_dump_path], check=True)
        
        # Define the backup file path
        backup_file_path = os.path.join(backup_dir, 'dump.rdb')

        # Move the temporary dump file to the backup directory
        shutil.move(temp_dump_path, backup_file_path)
        print(f"Moved dump.rdb to {backup_file_path}")

        # Define the tar archive file path
        tar_file_path = os.path.join(backup_dir, 'redis_backup.tar.gz')

        # Create a tar archive of the dump file
        with tarfile.open(tar_file_path, 'w:gz') as tar:
            tar.add(backup_file_path, arcname='dump.rdb')
        print(f"Created tar archive at {tar_file_path}")

        # Optionally, remove the copied dump.rdb file after archiving
        os.remove(backup_file_path)
        print(f"Removed temporary backup file {backup_file_path}")

        print("Backup completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during the backup process: {e}")
        exit(1)




# Calling functions based on CLI arguments.
if sys.argv[1]=='install':
  install_redis()
elif sys.argv[1]=='start':
  start_redis()
elif sys.argv[1]=='stop':
  stop_redis()
elif sys.argv[1]=='status':
  check_redis_status()
elif sys.argv[1]=='backup':
  backup_redis_db(backup_dir)
else:
  print('Help: ./system-metric.py {install|start|stop|status|backup}')