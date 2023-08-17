import os
import time
import zipfile
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from flask import Flask, render_template

app = Flask(__name__)
zip_files_info = []

def get_files_in_zip(zip_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        return zip_ref.namelist()

def check_for_zip_files(folder_path):
    global zip_files_info
    zip_files_info = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".zip"):
            zip_path = os.path.join(folder_path, filename)
            files_in_zip = get_files_in_zip(zip_path)
            zip_info = {
                "zip_file": filename,
                "files_inside": files_in_zip
            }
            zip_files_info.append(zip_info)

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            print(f"Detected new directory: {event.src_path}")
        else:
            print(f"Detected new file: {event.src_path}")
            if event.src_path.endswith(".zip"):
                check_for_zip_files("C:\\Users\\andox\\OneDrive\\Рабочий стол\\tn")  # dir path
                print("Files inside the zips:")
                for zip_info in zip_files_info:
                    print(f"Zip: {zip_info['zip_file']}")
                    for file_name in zip_info['files_inside']:
                        print(f"  - {file_name}")
            else:
                print("The new file is not a zip archive.")

@app.before_request
def startup_event():
    global observer
    check_for_zip_files("C:\\Users\\andox\\OneDrive\\Рабочий стол\\tn")  # dir path
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, "C:\\Users\\andox\\OneDrive\\Рабочий стол\\tn", recursive=True)  # dir path
    observer.start()

@app.teardown_request
def shutdown_event(exception=None):
    observer.stop()
    observer.join()

@app.route('/')
def index():
    return render_template('index.html', zip_files_info=zip_files_info)

if __name__ == "__main__":
    app.run()

