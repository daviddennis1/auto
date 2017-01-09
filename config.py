SETTINGS = {
    "database": "postgres",
    "models": [
        {
            "Dog": {
                "num_legs": "int",
                "s": 's',
            },
        }
    ],
}


TEXT = {
    #
    'mngcmd_txt': """from django.core.management.base import BaseCommand, CommandError
from app_demo.models import StubModel


class Command(BaseCommand):
    args = ""
    help = ""

    def add_arguments(s, parser):
        pass
        # parser.add_argument('--url', nargs='+', type=str)
        # parser.add_argument('--name', nargs='+', type=str)

    def process_args(s, options):
        pass
        # url = options['url'] if options.get('url') else None
        # name = options['name'] if options.get('name') else None
        # return url, name

    def handle(s, *args, **options):
        # url, name = s.process_args(options)
        print('Hello World!')
        if StubModel.objects.count() == 0:
            for i in range(5):
                stub = StubModel(num_legs=i, is_valid=True)
                stub.save()
            print("Created 5 %s's" % StubModel)
    """,

    #
    'models': """class %s(models.Model):

    num_legs = models.IntegerField(null=True)
    is_valid = models.BooleanField()

    # def __str__(s):
    #     return
    """,

    #
    "example_models": ('StubModel',),

    #
    "postgres_db_settings": """    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '%s',
        'USER': '%s',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
    },
    """,

    #
    "view_txt": """from django.http import HttpResponse
def index(request):

    context = {}

    stub_list = %s.objects.all()
    context['stub_list'] = stub_list

    return render(request, '%s/index.html', context)
    """,

    #
    "proj_url_txt": "    url(r'^%s/', include('%s.urls')),",

    #
    "app_url_txt": """from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]""",

    #
    "index_file_txt": """<html>
    <head>
        <title></title>
    </head>
    <body>

        <h1>Hello World!</h1>

        <ul>
            {% for stub in stub_list %}

            <li>
                {{ stub.num_legs }}
            </li>

            {% endfor %}
        </ul>

    </body>
</html>"""
}
