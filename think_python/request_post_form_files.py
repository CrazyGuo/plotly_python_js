
import requests

form_data = {'name': 'Matthew', 'sex': 'M', 'age': 25}

excle_file_path = "C:\\Users\\wuzhuguo\\Downloads\\365.xls"
image_file_path = "C:\\Users\\wuzhuguo\\Downloads\\android.png"

multiple_files = [ ('myfile',   ('report.xls', open(excle_file_path, 'rb'), 'application/vnd.ms-excel') ),
                    ('myimages', ('bar.png', open(image_file_path, 'rb'), 'image/png'))
                 ]

r = requests.post("http://127.0.0.1:5000/process_form_file", data=form_data, files=multiple_files)

print(r.text)