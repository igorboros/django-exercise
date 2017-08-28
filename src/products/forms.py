from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div


from crispy_forms.utils import render_field
from django.template.loader import render_to_string
from django.template import Context

from .models import Product, Location



class BaseTable(object):

    template = "forms/layout/table_elems.html"

    def __init__(self, *fields, **kwargs):
        self.fields = fields

        if hasattr(self, 'css_class') and 'css_class' in kwargs:
            self.css_class += ' %s' % kwargs.get('css_class')
        if not hasattr(self, 'css_class'):
            self.css_class = kwargs.get('css_class', None)

        self.css_id = kwargs.get('css_id', '')
        self.template = kwargs.get('template', self.template)

    def render(self, form, form_style, context):
        fields = ''
        for field in self.fields:
            fields += render_field(field, form, form_style, context)

        return render_to_string(self.template, Context({'tag': self.element,
                                                        'elem': self,
                                                        'fields': fields}))


class TD(BaseTable):
    element = 'td'


class TR(BaseTable):
    element = 'tr'


class LocationForm(ModelForm):

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.help_text_inline = True
        self.helper.form_class = 'form-horizontal'
        self.helper.form_tag = False

        self.helper.layout = Layout(
           TR(
              'id',
              TD(
                 Field('datetime', css_class='',
                                 template="forms/field.html"),),
              TD(
                 Field('longitude', css_class='',
                                 template="forms/field.html"),),
              TD(
                 Field('latitude', css_class='',
                                 template="forms/field.html"),),
              TD(
                 Field('elevation', css_class='',
                                 template="forms/field.html"),),
               TD(
                 Field('DELETE', template="forms/field.html")
               ),
               css_class='detail-form',
           )
        )

        super(LocationForm, self).__init__(*args, **kwargs)

    class Meta:
		model = Location
		fields = [
			'datetime',
			'longitude',
			'latitude',
			'elevation',
		]	


class ProductForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super(ProductForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_tag = False
		self.helper.layout = Layout(
			Div(
				Div('description', css_class='col'),
			css_class='row'),
		)
	class Meta:
		model = Product
		fields = [
			'description'
		]