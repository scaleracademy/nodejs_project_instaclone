from django.contrib import admin
from .models import UserPost, PostMedia, PostComments

# Register your models here.


class UserPostAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_on'
    list_display = ('id', 'caption_text', 'created_on', 'updated_on', )
    list_filter = ('created_on', 'location', )


admin.site.register(UserPost, UserPostAdmin)

admin.site.register(PostMedia)
admin.site.register(PostComments)