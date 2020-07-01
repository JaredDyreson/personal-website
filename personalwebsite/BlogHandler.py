#!/usr/bin/env python3.8

import jinja2
import markdown
import pdflatex
import sys
from array import *

class BlogHandler():
    def __init__(self, input_file: str):
        self.template = """<!DOCTYPE html>
          <html>
          <head>
              <link href="http://netdna.bootstrapcdn.com/twitter-bootstrap/2.3.0/css/bootstrap-combined.min.css" rel="stylesheet">
              <style>
                  body {
                      font-family: sans-serif;
                  }
                  code, pre {
                      font-family: monospace;
                  }
                  h1 code,
                  h2 code,
                  h3 code,
                  h4 code,
                  h5 code,
                  h6 code {
                      font-size: inherit;
                  }
              </style>
          </head>
          <body>
          <div class="container">
          {{content}}
          </div>
          </body>
          </html>
          """
        self.input_file = input_file
        self.output_file = self.input_file.split(".")[0]

    def generate_output(self) -> None:
        extension = self.input_file.split(".")[1]
        if(extension == "md"):
          self.markdown_converter()
        elif(extension == "tex"):
          self.tex_converter()
        else:
          raise Exception("Unsupported file extension of: {}".format(extension))
            
    def markdown_converter(self) -> None:
       """
       Convert markdown => HTML.
       Code was improvised from here:
       https://gist.githubusercontent.com/jiffyclub/5015986/raw/7423dbd53e716cbd8f844aa89fc626bb6438d828/markdown_doc
       """
       ext = ['extra', 'smarty'] 
       contents = ""
       with open(self.input_file) as f:
        for line in f.readlines():
          contents+=line
       html = markdown.markdown(contents, extensions=ext, output_format='html5')
       doc = jinja2.Template(self.template).render(content=html)
       with open("{}.html".format(self.output_file), 'w') as f:
        f.write(doc)

    def tex_converter(self) -> None:
        self.write_bytes(self.generate_pdf())

    def generate_pdf(self) -> bytes:
        """
        How to convert latex to pdf:
        https://pypi.org/project/pdflatex/
        """
        with open(self.input_file, 'rb') as f:
            pdfl = pdflatex.PDFLaTeX.from_binarystring(f.read(), self.output_file)
        pdf, log, cp = pdfl.create_pdf()
        return pdf

    def write_bytes(self, bits: bytes) -> None:
        """
        How to write bytes to a file:
        https://www.tutorialspoint.com/How-to-write-binary-data-to-a-file-using-Python
        """
        with open("{}.pdf".format(self.output_file), 'w+b') as f:
            f.write(bytearray(bits))
