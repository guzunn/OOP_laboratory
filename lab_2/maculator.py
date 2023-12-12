import os
from datetime import datetime
import time
import threading
import sched
class File:
    class File:
        def __init__(self, filename, extension, created_time, updated_time):
            self.filename = filename
            self.extension = extension
            self.created_time = created_time
            self.updated_time = updated_time

        def get_info(self):
            return f"File: {self.filename}, Extension: {self.extension}, Created: {datetime.fromtimestamp(self.created_time)}, Updated: {datetime.fromtimestamp(self.updated_time)}"
class ImageFile(File):
    def __init__(self, filename, extension, created_time, updated_time, image_size):
        super().__init__(filename, extension, created_time, updated_time)
        self.image_size = image_size

    def get_info(self):
        return super().get_info() + f", Image Size: {self.image_size}"

class TextFile(File):
    def __init__(self, filename, extension, created_time, updated_time, line_count, word_count, char_count):
        super().__init__(filename, extension, created_time, updated_time)
        self.line_count = line_count
        self.word_count = word_count
        self.char_count = char_count

    def get_info(self):
        return super().get_info() + f", Lines: {self.line_count}, Words: {self.word_count}, Characters: {self.char_count}"

class ProgramFile(File):
    def __init__(self, filename, extension, created_time, updated_time, line_count, class_count, method_count):
        super().__init__(filename, extension, created_time, updated_time)
        self.line_count = line_count
        self.class_count = class_count
        self.method_count = method_count

    def get_info(self):
        return super().get_info() + f", Lines: {self.line_count}, Classes: {self.class_count}, Methods: {self.method_count}"

class FolderMonitor:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.files = {}
        self.previous_files = set()
        self.snapshot_time = 0
        self.lock = threading.Lock()
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.scheduled_event = None

    def commit(self):
        with self.lock:
            self.scan_folder()
            self.previous_files = set(self.files.keys())
            self.snapshot_time = datetime.now()
            print(f"Created Snapshot at: {self.snapshot_time}")

    def scan_folder(self):
        with self.lock:
            self.files = {}
            for filename in os.listdir(self.folder_path):
                file_path = os.path.join(self.folder_path, filename)
                if os.path.isfile(file_path):
                    file_obj = self.get_file_info(file_path)
                    self.files[file_obj.filename] = file_obj

    def status(self):
        with self.lock:
            self.scan_folder()
            print(f"Created Snapshot at: {self.snapshot_time}")

            for filename, file_obj in self.files.items():
                if filename in self.previous_files:
                    changed = file_obj.updated_time > self.snapshot_time.timestamp()
                    if changed:
                        print(f"{filename} - {'No change' if not changed else 'Changed'}")
                else:
                    print(f"{filename} - New File")

            for filename in set(self.previous_files) - set(self.files.keys()):
                print(f"{filename} - Deleted")

    def scheduled_detection(self):
        self.scheduler.enter(5, 1, self.scheduled_detection)
        self.status()
        self.scheduled_event = threading.Timer(5, self.scheduler.run)
        self.scheduled_event.start()

    def get_file_info(self, file_path):
        filename, file_extension = os.path.splitext(os.path.basename(file_path))
        created_time = os.path.getctime(file_path)
        updated_time = os.path.getmtime(file_path)

        if file_extension.lower() in ['.png', '.jpg']:
            image_size = self.get_image_size(file_path)
            return ImageFile(filename, file_extension, created_time, updated_time, image_size)

        elif file_extension.lower() == '.txt':
            line_count, word_count, char_count = self.get_text_file_stats(file_path)
            return TextFile(filename, file_extension, created_time, updated_time, line_count, word_count, char_count)

        elif file_extension.lower() in ['.py', '.java']:
            line_count, class_count, method_count = self.get_program_file_stats(file_path)
            return ProgramFile(filename, file_extension, created_time, updated_time, line_count, class_count,
                               method_count)

        else:
            return File(filename, file_extension, created_time, updated_time)

    def get_image_size(self, file_path):
        return "1024x860"

    def get_text_file_stats(self, file_path):
        with open(file_path, 'r') as file:
            content = file.read()
            lines = content.split('\n')
            words = content.split()
            return len(lines), len(words), len(content)

    def get_program_file_stats(self, file_path):
        return 100, 5, 20

    def info(self, filename):
        if filename.lower() == "all files":
            for file_obj in self.files.values():
                print(file_obj.get_info())
        elif filename in self.files:
            print(self.files[filename].get_info())
        else:
            print(f"File '{filename}' not found in the monitored folder.")

if __name__ == "__main__":
    monitored_folder = r"C:\Users\guzun\PycharmProjects\OOP_laboratory\lab_1"
    folder_monitor = FolderMonitor(monitored_folder)

    detection_thread = threading.Thread(target=folder_monitor.scheduled_detection, daemon=True)
    detection_thread.start()

    while True:
        action = input("Enter action (commit, info <filename>, status): ").split()

        if action[0] == "commit":
            folder_monitor.commit()

        elif action[0] == "info":
            if len(action) == 2:
                folder_monitor.info(action[1])
            else:
                print("Invalid 'info' command. Please provide a filename.")

        elif action[0] == "status":
            folder_monitor.status()

        else:
            print("Invalid command. Please enter a valid action.")