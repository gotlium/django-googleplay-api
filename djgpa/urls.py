from django.conf.urls import patterns, url


urlpatterns = patterns(
    'djgpa.views',
    url(r'^get_new_android_id/$', 'generate_aid', name='gpa-generate-aid'),
)
