"""
Template module; Can be handy when using different template types such as from starlette
Cf. https://github.com/pierrz/brif/tree/main/app/templates
"""

from fastapi.templating import Jinja2Templates as jinja

templates = jinja(directory="templates")
