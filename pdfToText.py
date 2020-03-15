from tika import parser

with open('test3.txt','w') as outfile:
    file = 'spring2020class_schedule.pdf'
    file_data=parser.from_file(file)
    text=file_data['content']
    outfile.write(text)
