from django.contrib import admin
from .models import WikiScrape
from .models import Quiz

# Register your models here.
class WikiAdmin(admin.ModelAdmin):
    list_display=['user','url','title','summary','sections','key_entities','related_topics','created_at']

class QuizAdmin(admin.ModelAdmin):
    list_display=['scrape','question','options','answer','difficulty','explanation']


admin.site.register(WikiScrape,WikiAdmin)
admin.site.register(Quiz,QuizAdmin)