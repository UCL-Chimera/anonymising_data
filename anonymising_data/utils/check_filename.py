import re


def extract_and_check_format(xml_filename):
    """
    Function to check the filename and remove the person name from the filename.
    :param xml_filename: XML filename.
    :return: the new XML filename without the person name.
    """
    match = re.search(r"([^_]*CPET\d{2,4})", xml_filename)

    if match:
        extracted_value = match.group(1)
        return extracted_value
    else:
        return xml_filename
