import os 

class Command: 
    def execute(self): 
        pass 
    def undo(self): 
        pass 

class EditCommand(Command): 
    def __init__(self, file_paths, new_text): 
        self.file_paths = file_paths 
        self.new_text = new_text 
        self.old_contents = {}   

    def execute(self): 
        for path in self.file_paths: 
            if os.path.exists(path): 
                with open(path, 'r', encoding='utf-8') as f: 
                    self.old_contents[path] = f.read() [cite: 217]
            else: 
                self.old_contents[path] = None [cite: 219]
             
            with open(path, 'w', encoding='utf-8') as f: 
                f.write(self.new_text) [cite: 220]
        print(f"Modified files: {', '.join(self.file_paths)}") 

    def undo(self): 
        for path, content in self.old_contents.items(): 
            if content is None: 
                if os.path.exists(path): 
                    os.remove(path) [cite: 225]
            else: 
                with open(path, 'w', encoding='utf-8') as f: 
                    f.write(content) [cite: 227]
        print(f"Rollback completed for: {', '.join(self.file_paths)}") 

class MacroCommand(Command): 
    def __init__(self, commands): 
        self.commands = commands 

    def execute(self): 
        for cmd in self.commands: 
            cmd.execute() [cite: 236]

    def undo(self): 
        for cmd in reversed(self.commands): 
            cmd.undo() [cite: 239]

class FileEditor: 
    def __init__(self): 
        self._history = [] 

    def read_files(self, file_paths): 
        results = {} 
        for path in file_paths: 
            if os.path.exists(path): 
                with open(path, 'r', encoding='utf-8') as f: 
                    results[path] = f.read() [cite: 249]
            else: 
                results[path] = "Error: File not found" [cite: 250]
        return results 

    def execute_action(self, command): 
        command.execute() [cite: 253]
        self._history.append(command) [cite: 254]

    def undo_last(self): 
        if not self._history: 
            print("History is empty.") [cite: 257]
            return 
        command = self._history.pop() [cite: 258]
        command.undo() [cite: 258]

if __name__ == "__main__": 
    editor = FileEditor() [cite: 260]
    test_files = ["sample1.txt", "sample2.txt"] 

    print("--- Step 1: Single Operation ---") 
    edit_cmd = EditCommand(test_files, "Hello World!") [cite: 263]
    editor.execute_action(edit_cmd) 

    print("\n--- Step 2: Complex Operation (Macro) ---") 
    cmd1 = EditCommand(["sample1.txt"], "Data Chunk A") [cite: 265]
    cmd2 = EditCommand(["sample2.txt"], "Data Chunk B") [cite: 266]
    macro = MacroCommand([cmd1, cmd2]) [cite: 266]
    editor.execute_action(macro) 

    print("\n--- Current File States ---") 
    print(editor.read_files(test_files)) [cite: 271]

    print("\n--- Step 3: Undoing Macro ---") 
    editor.undo_last() [cite: 273]
    print("\n--- Step 4: Undoing First Operation ---") 
    editor.undo_last() [cite: 274]
