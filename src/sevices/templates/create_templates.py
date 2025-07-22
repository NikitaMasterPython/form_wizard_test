import re

import docx
from docx.document import Document as DocumentObject

from src.sevices.constants import (
    TEMPLATE_CONSTANT,
    TEMPLATE_KEY,
    TEMPLATE_TITLE,
)


class CreateDocuments:
    """Формирование документа по шаблону"""

    def __init__(self, template_path: str, **kwargs):
        self.template_path = template_path
        self.template_vars = {TEMPLATE_KEY.substitute(key=key): value for key, value in kwargs.items()}




    def create_doc(self) -> DocumentObject:
        """Формирование документа"""
        document = docx.Document(self.template_path)
        all_next_clean = False
        for num, i in enumerate(document.paragraphs):
            if re.match(TEMPLATE_TITLE, i.text) or all_next_clean:
                i.text = ""
                all_next_clean = True
            for var in re.findall(TEMPLATE_CONSTANT, i.text):
                value = self.template_vars.get(var, var)
                i.text = i.text.replace(var, value)

        return document
# для коммита