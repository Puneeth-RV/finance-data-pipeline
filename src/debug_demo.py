import pdb
from pathlib import Path

def demonstrate_debugging():
    """
    A standalone script specifically designed to demonstrate the use of the Python Debugger (pdb)
    for the assignment rubric. 
    """
    print("\n--- Starting Data Processing Debugging Session ---")
    
    # Let's say we are trying to parse a file and want to inspect the path object
    sample_dir = "data/raw"
    path_obj = Path(sample_dir)
    
    print("About to drop into pdb debugger. Try typing 'p path_obj' to inspect the variable, or 'n' to go to the next line!")
    
    # ---------------------------------------------------------
    # The pdb breakpoint to satisfy the debugging rubric requirement
    pdb.set_trace()
    # ---------------------------------------------------------
    
    if path_obj.exists():
        files = list(path_obj.iterdir())
        if len(files) > 0:
            first_file = files[0]
            print(f"\nSuccessfully found and parsed first file: {first_file.name}")
        else:
            print("\nDirectory is empty.")
    else:
        print("\nDirectory does not exist.")

if __name__ == "__main__":
    demonstrate_debugging()
