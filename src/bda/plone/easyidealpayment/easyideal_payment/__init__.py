import urllib
import urllib2
import urlparse
import logging
from lxml import etree
from zExceptions import Redirect
from zope.i18nmessageid import MessageFactory
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from bda.plone.payment.interfaces import IPaymentData

from bda.plone.shop.interfaces import IShopSettings
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from zope.i18n.interfaces import IUserPreferredLanguages
from status_codes import get_status_category, SUCCESS_STATUS
from bda.plone.orders import interfaces as ifaces
from bda.plone.orders.common import OrderData
from bda.plone.orders.common import get_order

from bda.plone.payment import (
    Payment,
    Payments,
)

from ZTUtils import make_query
from bda.plone.orders.common import get_order
from security import easyidealSignature
from easyideal import EasyIdeal
from decimal import Decimal as D


logger = logging.getLogger('bda.plone.payment')
_ = MessageFactory('bda.plone.payment')

#
# Easy-iDEAL Data
#

API_URL = "https://www.qantanipayments.com/api/"
MERCHANT_ID = ""
MERCHANT_KEY = ""
MERCHANT_SECRET = ""

#
# Util functions
#
def shopmaster_mail(context):
    props = getToolByName(context, 'portal_properties')
    return props.site_properties.email_from_address

class easyidealPayment(Payment):
    pid = 'easyideal_payment'
    label = _('easyideal_payment', 'Easy-iDeal Payment')

    def init_url(self, uid):
        return '%s/@@easyideal_payment?uid=%s' % (self.context.absolute_url(), uid)

# 
# Easy-iDEAL implementation
#
class easyidealPay(BrowserView):
    def __call__(self):
        base_url = self.context.absolute_url()
        order_uid = self.request['uid']
        
        easy_ideal = EasyIdeal(MERCHANT_ID, MERCHANT_KEY, MERCHANT_SECRET)
        banks_response = easy_ideal.request_banks()

        print banks_response

        transaction_response = easy_ideal.request_transaction(
        D(100), 'RABOBANK', 'Order number 10', 'http://127.0.0.1:8000/@@easyideal_success')

        print transaction_response
        
        transaction_status_response = easy_ideal.request_transaction_status(
            transaction_id=transaction_response.transaction_id,
            transaction_code=transaction_response.transaction_code
        )
        
        print transaction_status_response

#
# Payment success
#
class easyidealPaySuccess(BrowserView):
    def verify(self):
        return True

    @property
    def shopmaster_mail(self):
        return shopmaster_mail(self.context)
    
#
# Payment failed
#
class easyidealPayFailed(BrowserView):
    def finalize(self):
        return True

class easyidealError(Exception):
    """Raised if Easy-iDeal Payment return an error.
    """


    

        
