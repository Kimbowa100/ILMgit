from django.contrib import admin
from .models import Post, OrderP,Artist, OrderPost,Genre, Freestuff,UgandanMusic, InternationalMusic, ShareCategory,Share, AboutAuthor, Comment
# CommentReply, Document, UserImage, UserInfo, Hashtag


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)
        
         
admin.site.register(Post)
admin.site.register(AboutAuthor)
admin.site.register(Share)
admin.site.register(ShareCategory)


admin.site.register(OrderPost)
admin.site.register(OrderP)
admin.site.register(Freestuff)
admin.site.register(UgandanMusic)
admin.site.register(InternationalMusic)


admin.site.register(Artist)
admin.site.register(Genre)

#admin.site.register(Document)
#admin.site.register(CommentReply)
#admin.site.register(UserImage)
#admin.site.register(UserInfo)
#admin.site.register(Hashtag)




