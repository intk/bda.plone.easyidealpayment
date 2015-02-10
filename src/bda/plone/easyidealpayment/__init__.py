from bda.plone.shop import message_factory as _

from zope import schema
from plone.supermodel import model
from zope.interface import Interface
from zope.interface import provider

from bda.plone.shop.interfaces import IShopSettingsProvider

#from zope.interface import Attribute


@provider(IShopSettingsProvider)
class IeasyidealPaymentSettings(model.Schema):
    
    model.fieldset( 'easyideal',label=_(u'easyideal', default=u'easyideal'),
        fields=[
        'easyideal_server_url',
        'easyideal_sha_in_password',
        'easyideal_sha_out_password',
        ],
    )
                   
    easyideal_server_url = schema.ASCIILine(title=_(u'easyideal_server_url', default=u'Server url'),
                 required=True
    )

    easyideal_sha_in_password = schema.ASCIILine(title=_(u'easyideal_sha_in_password', default=u'SHA in password'),
               required=True
    )
    
    easyideal_sha_out_password = schema.ASCIILine(title=_(u'easyideal_sha_out_password', default=u'SHA out password'),
               required=True
    )
    