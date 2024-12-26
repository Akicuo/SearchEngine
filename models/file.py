def read_content(file_path):
    try:
        with open(file_path, "r") as file:
            content = file.read()
            return content
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(0)