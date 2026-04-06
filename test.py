import sys
import docx

doc = docx.Document()
doc.add_paragraph('El Sr. Juan Perez, que trabaja en Empresa Ficticia SA, visitó las oficinas de Buenos Aires.')
doc.save('test_doc.docx')
print("Created test_doc.docx")
