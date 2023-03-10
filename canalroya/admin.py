from django.contrib import admin, messages
from django.utils.translation import ngettext

from canalroya.models import Testimonial


class TestimonialAdmin(admin.ModelAdmin):
    actions = ['mark_as_approved', 'mark_as_pending', 'mark_as_spam', 'send_to_trash']
    list_display = ("get_full_name", "priority", "status", "created_at", "city", "province", "comment")
    list_filter = ("status", "province")

    def mark_as_approved(self, request, queryset):
        self.update_status_to(request, queryset, Testimonial.Status.APPROVED)

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
