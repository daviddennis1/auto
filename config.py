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


class Command(BaseCommand):
    args = ""
    help = ""

    def add_arguments(s, parser):
        pass
        #parser.add_argument('--url', nargs='+', type=str)

    def process_args(s, options):
        pass
        # return url

    def handle(s, *args, **options):
        print('Hello World!')""",

    #
    'models': """class FauxModel(models.Model):

    num_legs = models.IntegerField(null=True)
    good_bad = models.BooleanField()

    # def __str__(s):
    #     return 
    """
}
