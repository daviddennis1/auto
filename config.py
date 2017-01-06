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
        stub = StubModel(num_legs=2, good_bad=True)
        stub.save()
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
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
    },
    """
}
