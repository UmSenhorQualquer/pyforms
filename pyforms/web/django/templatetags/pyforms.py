from django 				import template
from django.template.loader import render_to_string
from django.conf 			import settings
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def renderPyFormsAppHTML( app): return mark_safe( app.html )
	