# canalroya

## Setup

NOTE: if you don't have superuser privileges installation of postgres extensions may fail. Run they manually:
**Important**: select proper database where you want to create extensions.
```sql
# psql -d canalroya
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS unaccent;
```

## How to embed testimonial counter in your site
Using an iframe:
```html
<iframe height="130" width="250" src="https://testimonios.elpirineonosevende.org/counter-iframe/"></iframe>
```



## Send email to users of INCOMPLETE testimonials
```python
from canalroya.utils import submit_incomplete_email

qs = Testimonial.objects.filter(status=Testimonial.Status.INCOMPLETE)
submit_incomplete_email(qs)
```

## i18n
```bash
cd canalroya
../manage.py makemessages --locale fr
```
