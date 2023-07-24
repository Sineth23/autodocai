def is_text_file(file_path):
    text_extensions = ['.txt', '.md', '.py', '.java', '.cpp', '.h', '.html', '.css', '.js', 'jsx', 'ts']
    ext = os.path.splitext(file_path)[1]
    return ext.lower() in text_extensions
