import PyPDF2
import re

# converts given pdf file into text that is wrote to given text file
def pdf_to_text(pdf_path, output_txt):
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        if pdf_reader.is_encrypted:
            try:
                pdf_reader.decrypt("") 
            except Exception as e:
                print(f"Failed to decrypt PDF: {e}")
                return

        text = ''

        for page_num in range(len(pdf_reader.pages)):
            try:
                page = pdf_reader.pages[page_num]
                extracted = page.extract_text()
                if extracted:
                    text += extracted
            except Exception as e:
                print(f"Error extracting text from page {page_num + 1}: {e}")
                continue

    with open(output_txt, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)

# gets all course codes of classes taken including those currently being taken
def get_classes(txt_file, start_phrase, end_phrase): 
    with open(txt_file, 'r', encoding='utf-8') as f:
        text = f.read()
    start_index = text.find(start_phrase)
    if start_index == -1:
        print(f"Start phrase not found: '{start_phrase}'")
        return None

    start_index += len(start_phrase) 
    end_index = text.find(end_phrase, start_index)
    if end_index == -1:
        print(f"End phrase not found: '{end_phrase}'")
        return None

    block = text[start_index:end_index]
    block = block.strip()
    return extract_course_codes(block)

# extracts course codes from the list of all
def extract_course_codes(text):
    lines = text.splitlines()
    course_codes = []
    for line in lines:
        if not line.strip():
            continue
        match = re.search(r'\b[A-Z]{2,4}-[A-Z]{0,2}\s*\d{3}\b', line)
        if match:
            course_code = re.sub(r'\s+', ' ', match.group()).strip()
            course_codes.append(course_code)

    return course_codes

# currently only understand how to do this for basic degree, at some point have to apply this to minor and major
def get_requirements(output_txt):

    # key is requirement, value is number of credits needed
    requirements = {}

    with open(output_txt, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line == "Not Satisfied:":
            # Look one line up for the requirement name
            if i > 0:
                requirement_name = lines[i - 1].strip()
            else:
                i += 1
                continue

            # Start looking forward for the "needed" phrase
            j = i + 1
            needed_value = None

            while j < len(lines):
                needed_match = re.search(r'(\d+\.\d+)\s+needed', lines[j])
                if needed_match:
                    needed_value = float(needed_match.group(1))
                    break
                j += 1

            if needed_value is not None:
                requirements[requirement_name] = needed_value
                # Skip to after the "needed" so we don’t capture inner Not Satisfieds
                i = j + 1
                continue

        i += 1
    
    return requirements

def get_requirements_helper(text, start, end):
    start_index = text.find(start)
    start_index += len("start") 
    end_index = text.find(end, start_index)
    block = text[start_index:end_index].strip()
    match = re.search(r'(\d+\.\d+)\s+needed', block)
    return match
