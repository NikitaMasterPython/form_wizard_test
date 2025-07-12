import re

TEMPLATE_CONSTANT = re.compile(r"{{.*}}")
TEMPLATE_TITLE = re.compile(r"<<.*>>")
SPLIT_LITERAL = "}} -"
REPLACE_LITERAL = "{{"
