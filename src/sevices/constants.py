import re
import string

TEMPLATE_CONSTANT = re.compile(r"{{[\w, \d]*}}")
TEMPLATE_TITLE = re.compile(r"<<.*>>")
SPLIT_LITERAL = "}} -"
REPLACE_LITERAL = "{{"
TEMPLATE_KEY = string.Template("{{$key}}")
