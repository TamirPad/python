import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from watchdog.events import FileSystemEvent


def on_moved(event):
    print("file moved")


def on_created(event):
    print("file created")


def on_deleted(event):
    print("file deleted")


def on_modified(event):
    print("file modified")


def on_closed(event):
    print("file closed")


path = "C:\\Users\\Admin\\Desktop\\tempo"

# Initialize logging event handler
event_handler = FileSystemEventHandler()

# calling the functions
event_handler.on_created = on_created
event_handler.on_closed = on_closed
event_handler.on_moved = on_moved
event_handler.on_modified = on_modified
event_handler.on_deleted = on_deleted
print(FileSystemEvent.event_type)

# Initialize Observer
observer = Observer()
observer.schedule(event_handler, path, recursive=True)

# Start the observer
observer.start()
try:
    print("Monitoring")
    while True:
        # Set the thread sleep time
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
    print("Done")
observer.join()
