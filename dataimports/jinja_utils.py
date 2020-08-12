from jinja2 import (FileSystemLoader,
                    Environment)
from typing import Dict
from pathlib import Path


def load_template(template: str):
    f_loader = FileSystemLoader(Path(__file__).parent / 'templates')
    env = Environment(loader=f_loader)
    template_obj = env.get_template(template)
    return template_obj


def render_template(mw_template: str, item: Dict, subobjs=False) -> str:
    if subobjs:
        template_obj = load_template(template='wiki_subobjects.jinja')
        wiki_item = template_obj.render(wikitemplate=mw_template,
                                        subobjs_dict=item)
    else:
        template_obj = load_template(
            template='wiki_genericTemplate.jinja')
        wiki_item = template_obj.render(wikitemplate=mw_template,
                                        item_dict=item)
        # TODO remove wikitemplate
    return wiki_item
