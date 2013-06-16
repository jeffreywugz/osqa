import cgi

import browserid
from urllib import urlopen,  urlencode
from forum.authentication.base import AuthenticationConsumer, ConsumerTemplateContext, InvalidAuthentication

from django.conf import settings as django_settings

from django.core.urlresolvers import reverse

# from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext as _

class BrowserIdAuthConsumer(AuthenticationConsumer):

    def prepare_authentication_request(self, request, redirect_to):
        raise InvalidAuthentication(_("Invalid authentication request."))
    def process_authentication_request(self, request):
        

        assertion =  request.POST.get("assertion",None)
        if assertion == None:
            raise InvalidAuthentication(_("No assertion provided in Persona form post."))

        else:
            data = browserid.verify(assertion,django_settings.APP_URL)
            
            if data["status"] == "okay":
                request.session["browserid_email"] =  data["email"]
                uniq_id = "browserid://%s/%s" % (data["issuer"], data["email"])
                return uniq_id
            else:
                raise InvalidAuthentication(_("Invalid authentication."))

        

class BrowserIdAuthContext(ConsumerTemplateContext):
    mode = 'BIGICON'
    type = 'CUSTOM'
    weight = 450
    human_name = 'Persona'
    code_template = 'modules/browserid/button.html'
    extra_css = []
