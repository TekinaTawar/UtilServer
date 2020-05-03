from os import system
from subprocess import check_call
from sys import executable

from svglib import svglib


from smtplib import SMTP_SSL
from email.message import EmailMessage

from jinja2 import Environment, FileSystemLoader, select_autoescape
from reportlab.graphics import renderPDF

from PyPDF2 import PdfFileMerger
import glob
import os

def sendEmail(data):
    msg = EmailMessage()
    msg['Subject'] = 'Your guide to answering: "आज खाने में क्या बनाऊं?"'
    msg['From'] = 'astroaniket1@gmail.com'
    # msg['To'] = 'astroaniket1@gmail.com'  # only for testing
    msg['To'] = data["email"]

    msg.set_content(
        f"""Dear {data['name']}
        
        Thank you for your response. Your response sheet is attached to this email. 
        Please refer it to help you answer the question. Hope it helps you.

        Note: The names mentioned in the sheet are not of individual dishes and represent the group of dishes that come under a similar category.
        """
    )
    print(generatePdf(data))
    files = ['ResponseSheet.pdf']

    for fl in files:
        with open(fl, 'rb') as f:
            file_data = f.read()
            file_name = f.name
        msg.add_attachment(file_data, maintype='application',
                       subtype='octet-stream', filename=f.name)

    with SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('survey.foodforu@gmail.com', r"a8u%m68*an?Ku3\ ")
        smtp.send_message(msg)

    return "email Sent"


def generatePdf(data):
    env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html', 'xml', 'svg']))

    template = env.get_template('Page1.svg')
    template.stream(
        BV=int(((len(data["beveragesL"])+len(data["beveragesXL"]))/16)*100),
        SV=int(((len(data["snacksL"])+len(data["snacksXL"]))/57)*100),
        MCV=int(((len(data["main_coursesL"])+len(data["main_coursesXL"]))/36)*100),
        OV=int(((len(data["othersL"])+len(data["othersXL"]))/12)*100),
        ).dump("test1.svg")

    template = env.get_template('Page2.svg')
    template.stream(
        beveragesL=data["beveragesL"] + data["beveragesXL"],
        snacksL=data["snacksL"]+data["snacksXL"],
        mainCoursesL=data["main_coursesL"]+data["main_coursesXL"],
        othersL=data["othersL"]+data["othersXL"], 
        height=find_height(data)
    ).dump("test2.svg")

    page1 = svglib.svg2rlg(r'test1.svg')
    renderPDF.drawToFile(page1, "page1.pdf")
    page2 = svglib.svg2rlg(r'test2.svg')
    renderPDF.drawToFile(page2, "page2.pdf")
    page3 = svglib.svg2rlg(r'Page3.svg')
    renderPDF.drawToFile(page3, "page3.pdf")

    paths = glob.glob('*.pdf')
    paths.sort()
    merger('ResponseSheet.pdf', paths)

    filesToDel = ['page1.pdf', 'page2.pdf', 'page3.pdf', 'test1.svg', 'test2.svg']
    for fileToDel in filesToDel:
        if os.path.exists(fileToDel):
            os.remove(fileToDel)
    return "pdf generated"

def merger(output_path, input_paths):
    pdf_merger = PdfFileMerger()

    for path in input_paths:
        pdf_merger.append(path)

    with open(output_path, 'wb') as fileobj:
        pdf_merger.write(fileobj)
    pdf_merger.close()

def find_height(data):
    max_r = max([
        (len(data["beveragesL"])+len(data["beveragesXL"])),
        (len(data["snacksL"])+len(data["snacksXL"])),
        (len(data["main_coursesL"])+len(data["main_coursesXL"])),
        (len(data["othersL"])+len(data["othersXL"]))
    ])
    height = 720
    if max_r <= 11:
        pass
    else:
        height = 720 + ((max_r - 11)*70)
    return height