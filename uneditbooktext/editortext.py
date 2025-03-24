import os
import re
import difflib
import stanza

# Download the Persian model for Stanza if not already downloaded.
stanza.download('fa', verbose=False)

# Initialize the Persian NLP pipeline (using only the tokenize processor)
nlp = stanza.Pipeline(lang='fa', processors='tokenize', use_gpu=False, verbose=False)

def clean_persian_text(text):
    """
    Function to clean Persian text:
    1. Tokenize text using Stanza.
    2. Remove punctuation (except letters, numbers, whitespace, period, Persian comma, and colon).
    3. Remove tatweel (ـ), hyphens (-), and underscores (_).
    4. Remove extra whitespace.
    """
    # Tokenize the text using Stanza
    doc = nlp(text)
    tokens = []
    for sentence in doc.sentences:
        for token in sentence.tokens:
            tokens.append(token.text)
    tokenized_text = ' '.join(tokens)
    
    # Remove tatweel, hyphens, and underscores
    text_no_special = re.sub(r'[ـ\-_]+', '', tokenized_text)
    
    # Remove punctuation except ., ،, and :
    cleaned_text = re.sub(r'[^\w\s\.\،:]', '', text_no_special)
    
    # Remove extra spaces
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    return cleaned_text

def show_differences(original_text, cleaned_text):
    """
    Print line-by-line differences between original and cleaned text using difflib.ndiff.
    """
    original_lines = original_text.splitlines()
    cleaned_lines = cleaned_text.splitlines()
    
    if not cleaned_lines:
        cleaned_lines = [cleaned_text]
    
    diff = list(difflib.ndiff(original_lines, cleaned_lines))
    
    print("Differences between original and cleaned text:")
    for i, line in enumerate(diff, 1):
        if line.startswith("- ") or line.startswith("+ "):
            print(f"Line {i}: {line}")

def process_file(input_path, output_path):
    # Read the original text from the file
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            original_text = f.read()
    except Exception as e:
        print(f"Error reading file {input_path}: {e}")
        return False
    
    # Clean the text
    cleaned_text = clean_persian_text(original_text)
    
    # Save the cleaned text to a new file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(cleaned_text)
    
    print(f"File '{os.path.basename(input_path)}' processed and saved as '{output_path}'")
    show_differences(original_text, cleaned_text)
    print("\n" + "-"*50 + "\n")
    return True

def main():
    # Use the directory where this script is located as the input folder.
    # Assuming this script is in a subfolder (e.g., uneditbooktext), the project root is its parent.
    project_root = os.path.dirname(os.path.abspath(__file__))
    input_folder = project_root  # Folder containing input .txt files
    # Output folder: in the project root, named "edit book text"
    output_folder = os.path.join(project_root, "editedbooktext")
    
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # File to store the list of processed file names
    processed_list_file = os.path.join(project_root, "editedbook_list.txt")
    processed_files = []
    
    # Process all .txt files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            input_path = os.path.join(input_folder, filename)
            output_filename = "edited_" + filename
            output_path = os.path.join(output_folder, output_filename)
            success = process_file(input_path, output_path)
            if success:
                processed_files.append(filename)
                # Delete the original file after processing
                try:
                    os.remove(input_path)
                    print(f"Original file '{filename}' deleted.")
                except Exception as e:
                    print(f"Error deleting file {filename}: {e}")
    
    # Save the list of processed files to a text file
    if processed_files:
        with open(processed_list_file, "w", encoding="utf-8") as f:
            for fname in processed_files:
                f.write(fname + "\n")
        print(f"List of processed files saved in '{processed_list_file}'.")
    else:
        print("No files were processed.")

if __name__ == "__main__":
    main()
