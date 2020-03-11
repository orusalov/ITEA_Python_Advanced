from threading_decorator import my_own_decorator
import requests as req
import threading
import os

threads_preffix = 'file_downloader'

def create_folder(directory):

    if not os.path.exists(directory):
        os.makedirs(directory)

    print(f'Directory "{directory}" created')

@my_own_decorator(threads_preffix)
def download_file_by_link(link):

    url_obj = req.get(url=link)
    head = url_obj.headers

    content_type = head.get('Content-Type')

    file_name = (link.rsplit('/')[-1] if link.rsplit('/')[-1] else link.rsplit('/')[-2])
    file_ends = content_type.rsplit('/')[-1].split(';')[0]

    file_name = f'{file_name}.{file_ends}' if '.' not in file_name else file_name

    charset = None
    if 'charset=' in content_type:
        charset = content_type.rsplit('/')[-1].split('charset=')[-1].strip()

    if 'text' in content_type:
        with open(file_name, 'w', encoding=('UTF-8' if not charset else charset)) as f:
            f.write(url_obj.text)
    else:
        with open(file_name, 'wb') as f:
            f.write(url_obj.content)


link_list = [
    'https://upload.wikimedia.org/wikipedia/commons/f/f5/Sun_Studio.jpg',
    'https://en.wikipedia.org/wiki/Kevin_Spacey',
    'https://docs.python.org/3/library/threading.html',
    'https://www.g-loaded.eu/2016/11/24/how-to-terminate-running-python-threads-using-signals/',
    'https://docs.python.org/3/tutorial/datastructures.html',
    'https://www.python.org/dev/peps/pep-0008/',
    'https://m.media-amazon.com/images/G/01/6pm/promos/200301/Sub5._CB421832937_.jpg',
    'https://i.forfun.com/k7i0tgqd.mp4',
    'https://i.forfun.com/k69l2q9i.mp4',
    'https://dump.video/i/OdaSZy.mp4'
]

# change directory
download_directory = 'downloads'
create_folder(download_directory)
os.chdir(download_directory)

# Start the cycle
for link in link_list:
    download_file_by_link(link)

# thread list
my_thread_list = [thread for thread in threading.enumerate() if thread.name.startswith(threads_preffix)]

###### Below is the code which takes information from ended threads from thread_list. It is commented, cause the same
# information has been thrown from custom Thread class

# while my_thread_list:
#     for thread in my_thread_list:
#         if not thread.is_alive():
#             print(f'{thread.getName()} finished {thread.target.__name__}{thread.args}')
#             my_thread_list.remove(thread)
#     sleep(0.1)
