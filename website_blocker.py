# Run this script as administrator

import time
from datetime import datetime as dt

# change hosts path according to your OS
hosts_path = "C:\\Windows\\System32\\drivers\\etc\\hosts"

# localhost's IP
redirect = "127.0.0.1"

################################################
# Blocking Method 1
################################################
# Uncomment to use a static list of websites you want to block
# website_list = ["pornhub.com", "www.pornhub.com"]

################################################
# Blocking Method 2
################################################
# Uncomment to use a dynamic list, read from a file
with open("sites", 'r') as file:
    website_list = file.readlines()


def sanitizeData(website_list):
    print("Removing comments and unwanted data...")

    # Remove all elements that are comments (that begin with "#")
    removeCommentsOnly(website_list)

    for idx, website in enumerate(website_list):
        # Cut out any later comments in entry
        website = website.split('#', 1)[0]

        # Remove beginning & end whitespace, tabs, and newlines
        website = website.strip(' \n\t')
        
        # Update the list
        website_list[idx] = website


# Add ".com" to all entries not containing a top-level domain
def addTopLevelDomain(website_list):
    print("Adding top-level domains...")

    for idx, website in enumerate(website_list):
        # Remove beginning & end whitespace, tabs, and newlines
        website = website.strip(' \n\t')
        
        if not '.' in website:
            website += ".com"
            website_list[idx] = website # Update the list


def updateHostsFile():
    print("Updating hosts file...")

    while True:
        # Uncomment to use at all times
        print("Reading hostname map...")
        with open(hosts_path, 'r+') as file:
            content = file.read()
            for website in website_list:
                if website in content:
                    print("[{}] Website already in map. Everything looks good".format(dt.now()))
                    pass
                else:
                    # Mapping hostnames to your localhost IP address
                    print("[{}] Website not in map. Writing to hostname map...".format(dt.now()))
                    file.write("\n" + redirect + " " + website)

        # Uncomment to use during specific work hours
        """
        # time of your work
        if dt(dt.now().year, dt.now().month, dt.now().day, 8) 
        < dt.now() < dt(dt.now().year, dt.now().month, dt.now().day, 16):
            print("Working hours...")
            with open(hosts_path, 'r+') as file:
                content = file.read()
                for website in website_list:
                    if website in content:
                        pass
                    else:
                        # mapping hostnames to your localhost IP address
                        file.write(redirect + " " + website + "\n")
        else:
            with open(hosts_path, 'r+') as file:
                content=file.readlines()
                file.seek(0)
                for line in content:
                    if not any(website in line for website in website_list):
                        file.write(line)
    
                # removing hostnames from host file
                file.truncate()
    
            print("Fun hours...")
        """

        time.sleep(5)


# Remove all elements that are comments (that begin with "#")
def removeCommentsOnly(str_list):
    for idx, string in enumerate(str_list):
        # Remove beginning & end whitespace, tabs, and newlines
        string = string.strip(' \n\t')

        # Replace these entries with empty strings
        if string[0] == '#':
            str_list[idx] = ""

    # Remove all empty elements from str_list
    str_list.remove("")


################################################
# Run
################################################
# print("Initial sites list: \n\t{}".format(website_list))

# Sanitize website list for unwanted data
sanitizeData(website_list)
addTopLevelDomain(website_list)
# print("Sanitized sites list: \n\t{}".format(website_list))

# Update the hosts file
updateHostsFile()
