import json
import os
import tempfile
from pathlib import Path

import requests
from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from django.utils import timezone

from canalroya.models import Testimonial, testimonial_image_path


def download_from_url(url, file_path):
    r = requests.get(url, stream=True)
    if r.ok:
        with open(file_path, 'wb') as f:
            print("saving to", f.name)
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())

    else:  # HTTP status code 4XX/5XX
        print("Download failed: status code {}\n{}".format(r.status_code, r.text))


class Command(BaseCommand):
    help = "Load data from JSON"

    def add_arguments(self, parser) -> None:
        parser.add_argument('input_file', type=str)

    def handle(self, *args, **options):
        self.input_file = options['input_file']
        with open(self.input_file) as f:
            data = json.load(f)

        self.stdout.write(f"Importando {len(data)} elementos desde {self.input_file}")

        for d in data:
            try:
                first_name, last_name = d["full_name"].split(" ", 1)
            except ValueError:
                last_name = " "

            if "," in d["profession"]:
                prof_tuple = d["profession"].split(", ")
                profession = ", ".join(prof_tuple[:-1])
                city = prof_tuple[-1]
            else:
                profession = d["profession"]
                city = " "

            instance = Testimonial(
                first_name=first_name,
                last_name=last_name,
                profession=profession,
                city=city,
                province="Huesca",
                comment=d["comment"],
                created_at=timezone.now(),
                status=Testimonial.Status.APPROVED,
            )

            filename = d["image_url"].split("/")[-1]
            dst_rel_path = testimonial_image_path(instance, filename)
            dst_file = Path(settings.MEDIA_ROOT, dst_rel_path)

            download_from_url(d["image_url"], dst_file)
            instance.image.name = dst_rel_path
            instance.save()
