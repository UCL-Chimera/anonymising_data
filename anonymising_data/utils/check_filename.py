import re


def extract_and_check_format(xml_filename):
    match = re.match(r"^CPET\d{2,4}", xml_filename)

    if match:
        extracted_value = match.group()
        return extracted_value
    else:
        return xml_filename
