import os 
class Command: 
"""The abstract base class for all file operations.""" 
def execute(self): 
pass 
def undo(self): 
pass 
class EditCommand(Command): 
"""Command to modify the content of one or multiple files.""" 
def __init__(self, file_paths, new_text): 
self.file_paths = file_paths 
self.new_text = new_text 
        self.old_contents = {}   
 
    def execute(self): 
        for path in self.file_paths: 
            if os.path.exists(path): 
                with open(path, 'r', encoding='utf-8') as f: 
                    self.old_contents[path] = f.read() 
            else: 
                self.old_contents[path] = None  
             
            with open(path, 'w', encoding='utf-8') as f: 
                f.write(self.new_text) 
        print(f"Modified files: {', '.join(self.file_paths)}") 
 
    def undo(self): 
        for path, content in self.old_contents.items(): 
            if content is None: 
                if os.path.exists(path): 
                    os.remove(path) 
            else: 
                with open(path, 'w', encoding='utf-8') as f: 
                    f.write(content) 
        print(f"Rollback completed for: {', '.join(self.file_paths)}") 
 
 
class MacroCommand(Command): 
    """Groups multiple operations into a single complex action.""" 
    def __init__(self, commands): 
        self.commands = commands 
 
    def execute(self): 
        for cmd in self.commands: 
            cmd.execute() 
 
    def undo(self): 
        for cmd in reversed(self.commands): 
            cmd.undo() 
 
class FileEditor: 
    def __init__(self): 
        self._history = [] 
 
    def read_files(self, file_paths): 
        results = {} 
        for path in file_paths: 
            if os.path.exists(path): 
                with open(path, 'r', encoding='utf-8') as f: 
                    results[path] = f.read() 
            else: 
                results[path] = "Error: File not found" 
        return results 
 
    def execute_action(self, command): 
        command.execute() 
        self._history.append(command) 
 
    def undo_last(self): 
        if not self._history: 
            print("History is empty.") 
            return 
        command = self._history.pop() 
        command.undo() 
 
 
if __name__ == "__main__": 
    editor = FileEditor() 
    test_files = ["sample1.txt", "sample2.txt"] 
 
    print("--- Step 1: Single Operation ---") 
    edit_cmd = EditCommand(test_files, "Hello World!") 
    editor.execute_action(edit_cmd) 
 
    print("\n--- Step 2: Complex Operation (Macro) ---") 
    cmd1 = EditCommand(["sample1.txt"], "Data Chunk A") 
    cmd2 = EditCommand(["sample2.txt"], "Data Chunk B") 
    macro = MacroCommand([cmd1, cmd2]) 
    editor.execute_action(macro) 
 
    print("\n--- Current File States ---") 
    print(editor.read_files(test_files)) 
 
    print("\n--- Step 3: Undoing Macro ---") 
editor.undo_last() 
print("\n--- Step 4: Undoing First Operation ---") 
editor.undo_last() 
