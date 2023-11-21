import os

def check_disk_space(path):
    total, used, free = os.statvfs(path)[:3]
    disk_space = {
        'total': total * 4 / 1024 / 1024,  # in GB
        'used': used * 4 / 1024 / 1024,  # in GB
        'free': free * 4 / 1024 / 1024,  # in GB
        'usage': used / total * 100  # in percentage
    }
    return disk_space

if __name__ == '__main__':
    path = '/'
    disk_space = check_disk_space(path)
    print(f"Total disk space: {disk_space['total']} GB")
    print(f"Used disk space: {disk_space['used']} GB")
    print(f"Free disk space: {disk_space['free']} GB")
    print(f"Disk space usage: {disk_space['usage']}%")