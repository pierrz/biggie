"""
Module handling the Jinja2 templates for the frontend.
"""

from fastapi.templating import Jinja2Templates as jinja

templates = jinja(directory="templates")
