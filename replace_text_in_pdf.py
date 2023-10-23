## requirement install
## get this during the installion of llibrary
## 33 PyPDF2.errors.DeprecationError: PdfFileReader is deprecated and was removed in PyPDF2 3.0.0. Use PdfReader instead.
## PyPDF2.errors.DeprecationError: getData is deprecated and was removed in PyPDF2 3.0.0. Use get_data instead.
## referance link: https://stackoverflow.com/questions/41769120/search-and-replace-for-text-within-a-pdf-in-python
import os
import argparse
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import DecodedStreamObject, EncodedStreamObject, NameObject

def replace_text(content, replacements=dict()):
    lines = content.splitlines()
    result = ""
    in_text = False

    for line in lines:
        if line == "BT":
            in_text = True
        elif line == "ET":
            in_text = False
        elif in_text:
            cmd = line[-2:]
            if cmd.lower() == 'tj':
                replaced_line = line
                for k, v in replacements.items():
                    replaced_line = replaced_line.replace(k, v)
                result += replaced_line + "\n"
            else:
                result += line + "\n"
            continue

        result += line + "\n"

    return result

def process_data(obj, replacements):
    data = obj.get_data()
    decoded_data = data.decode('iso-8859-1', 'replace') 
    replaced_data = replace_text(decoded_data, replacements)
    encoded_data = replaced_data.encode('iso-8859-1','replace')

    if obj.decoded_self is not None:
        obj.decoded_self.set_data(encoded_data)
    else:
        obj.set_data(encoded_data)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required=True, help="path to input PDF document")
    ap.add_argument("-o", "--output", required=True, help="path to output PDF document")
    args = vars(ap.parse_args())

    in_file = args["input"]
    out_file = args["output"]

    # Provide replacements list that you need here
    replacements = {'PHR1B': 'PNEO4','PLEIADES':'PLEIADES-NEO','PHR 1B':'PNEO4'}

    pdf = PdfReader(in_file)
    writer = PdfWriter()

    for page_number in range(0, len(pdf.pages)):
        page = pdf.pages[page_number]
        contents = page['/Contents']

        if isinstance(contents, DecodedStreamObject) or isinstance(contents, EncodedStreamObject):
            process_data(contents, replacements)
        elif len(contents) > 0:
            for obj in contents:
                if isinstance(obj, DecodedStreamObject) or isinstance(obj, EncodedStreamObject):
                    stream_obj = obj.getObject()
                    process_data(stream_obj, replacements)

        # Force content replacement
        page[NameObject("/Contents")] = contents.decoded_self
        writer.add_page(page)

    with open(out_file, 'wb') as output_pdf:
        writer.write(output_pdf)



'''
to run the used this cmd line: python replace_text_in_pdf.py -i DELIVERY.pdf -o out.pdf
'''

## We can used diff. encodings and decoding method but the

'''

1) decoded_data = data.decode('utf-8', 'replace')
   replaced_data = replace_text(decoded_data, replacements)
   encoded_data = replaced_data.encode("utf-8", "replace")

2) decoded_data = data.decode('iso-8859-1', 'replace')
   replaced_data = replace_text(decoded_data, replacements)
   encoded_data = replaced_data.encode("iso-8859-1", "replace")
## (i used this due to its handel proprly the spacial charaters)

3) decoded_data = data.decode('ascii', 'replace')
   replaced_data = replace_text(decoded_data, replacements)
   encoded_data = replaced_data.encode("ascii", "replace")

4) decoded_data = data.decode('utf-8', 'ignore')
   replaced_data = replace_text(decoded_data, replacements)
   encoded_data = replaced_data.encode("utf-8", "ignore")

'''
