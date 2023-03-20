from django.conf import settings
from django.contrib import admin, messages
from django.core.mail import send_mass_mail
from django.template import Context, Template
from django.utils.translation import ngettext

from canalroya.models import Testimonial


class TestimonialAdmin(admin.ModelAdmin):
    actions = ['mark_as_approved', 'mark_as_incomplete', 'mark_as_pending', 'mark_as_spam', 'send_to_trash']
    list_display = ("get_full_name", "priority", "status", "email", "get_created_at", "city", "province", "comment")
    list_filter = ("status", "province")
    search_fields = ['first_name', 'last_name', 'email']

    def get_created_at(self, obj):
        c = Context({"created_at": obj.created_at})
        return Template("{{ created_at|date:'SHORT_DATETIME_FORMAT' }}").render(c)
    get_created_at.admin_order_field = "created_at"
    get_created_at.short_description = "Created at"

    def mark_as_approved(self, request, queryset):
        self.update_status_to(request, queryset, Testimonial.Status.APPROVED)
        # notify user that its testimonial has been approved
        datatuple = []
        for instance in queryset:
            message = (
                'Testimonio aprobado | El Pirineo no se vende',
                'Tu testimonio ha sido aprobado, gracias por unirte a la voz de la montaña.\n#SalvemosCanalRoya',
                settings.DEFAULT_FROM_EMAIL,
                [instance.email]
            )
            datatuple.append(message)
        send_mass_mail(datatuple, fail_silently=True)

    def mark_as_incomplete(self, request, queryset):
        self.update_status_to(request, queryset, Testimonial.Status.INCOMPLETE)

    def mark_as_pending(self, request, queryset):
        self.update_status_to(request, queryset, Testimonial.Status.PENDING)

    def mark_as_spam(self, request, queryset):
        self.update_status_to(request, queryset, Testimonial.Status.SPAM)

    def send_to_trash(self, request, queryset):
        self.update_status_to(request, queryset, Testimonial.Status.TRASH)

    def update_status_to(self, request, queryset, status):
        updated = queryset.update(status=status)
        self.message_user(request, ngettext(
            f'%d testimonial was successfully marked as {status.label}.',
            f'%d testimonials were successfully marked as {status.label}.',
            updated,
        ) % updated, messages.SUCCESS)


admin.site.register(Testimonial, TestimonialAdmin)
