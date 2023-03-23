from django.conf import settings
from django.contrib import admin, messages
from django.core.mail import send_mass_mail
from django.template import Context, Template
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import ngettext

from canalroya.models import Testimonial, annotate_ephemeral_slug
from canalroya import utils


class TestimonialAdmin(admin.ModelAdmin):
    actions = ['mark_as_approved', 'mark_as_incomplete', 'mark_as_pending', 'mark_as_spam', 'send_to_trash']
    list_display = ("get_full_name", "priority", "status", "email", "get_created_at",
                    "get_updated_at", "city", "province", "comment", "get_update_link")
    list_filter = ("status", "province")
    search_fields = ['first_name', 'last_name', 'email']
    readonly_fields = ["generate_slug"]

    def get_created_at(self, obj):
        c = Context({"created_at": obj.created_at})
        return Template("{{ created_at|date:'SHORT_DATETIME_FORMAT' }}").render(c)
    get_created_at.admin_order_field = "created_at"
    get_created_at.short_description = "Created at"

    def get_updated_at(self, obj):
        c = Context({"updated_at": obj.updated_at})
        return Template("{{ updated_at|date:'SHORT_DATETIME_FORMAT' }}").render(c)
    get_updated_at.admin_order_field = "updated_at"
    get_updated_at.short_description = "Updated at"

    def get_update_link(self, obj):
        if obj.status in [Testimonial.Status.INCOMPLETE, Testimonial.Status.PENDING]:
            path = reverse("canalroya:testimonial-preview", kwargs={"slug": obj.slug})
            url = self.request.build_absolute_uri(path)
            return format_html("<p style='text-align:center;'><a href='{}' target='blank'><img alt='public update link'"
                               "src='/static/admin/img/icon-viewlink.svg'></a></p>", url)
        return format_html("<p style='text-align:center;'>-</p>")
    get_update_link.short_description = format_html("<span title='Comparte este link con el autor para que pueda hacer"
                                                    " correcciones.' style='cursor:help;'>link <img "
                                                    "src='/static/admin/img/icon-unknown.svg'></span>")

    def get_queryset(self, request):
        self.request = request
        qs = super().get_queryset(request)
        return annotate_ephemeral_slug(qs)

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

    def save_model(self, request, obj, form, change):
        """Submit emails after moderating"""
        super().save_model(request, obj, form, change)

        if "status" in form.changed_data:
            if obj.status == Testimonial.Status.APPROVED:
                utils.notify_testimonial_approved(obj)
            elif obj.status == Testimonial.Status.INCOMPLETE:
                utils.notify_testimonial_incomplete(obj)


admin.site.register(Testimonial, TestimonialAdmin)
