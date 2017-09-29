from django.conf.urls import *
from views import *
from django.contrib import admin
import settings
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^site_medias/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
    url(r'^help/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.HELP_ROOT }),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', index),
    url(r'^eindex', eindex),
    url(r'^probedesign', probedesign),
    url(r'^subseq', subseq),
    url(r'^intro', intro),
    url(r'^entrez', entrez),
    url(r'^fromfile', fromfile),
    url(r'^english', english),
    url(r'^downloadentrez', downloadentrez),
    url(r'^xmltoentrez', entreztoxml),
    url(r'^convertdata', convertdata),
    url(r'^test', test),
    url(r'^x4merCalc', x4merCalc),
    url(r'^startdesign', startdesign),
    url(r'^bingodesign', bingodesign),
    url(r'^NonNshFilter', NonNshFilter),
    url(r'^Probelist', Probelist),
    url(r'^PostCalcXmer', PostCalcXmer),
    url(r'^Universalvalue', Universalvalue),
    url(r'^ProbeSetsXmer',ProbeSetsXmer),
    url(r'^Probegroupsvalues',Probegroupsvalues),
    url(r'^GenerateProbesets',GenerateProbesets),
    url(r'^Probesetsgenerate',Probesetsgenerate),
    url(r'^bigdata',BigData),
    url(r'^tfdeal',tfdeal),
    url(r'^datatfshow',tfdealdata),
)
