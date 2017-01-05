SETTINGS = {
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
    'models': """from django.db import models

from app_ddb.models import BaseModel


class DBUpdate(BaseModel):

    agg1_tbl_forum_max_id = models.IntegerField(null=True)
    agg1_tbl_forum_room_max_id = models.IntegerField(null=True)
    agg1_tbl_forum_thread_max_id = models.IntegerField(null=True)
    """
}
