from django import forms
from hc.api.models import Channel


class NameTagsForm(forms.Form):
    name = forms.CharField(max_length=100, required=False)
    tags = forms.CharField(max_length=500, required=False)

    def clean_tags(self):
        l = []

        for part in self.cleaned_data["tags"].split(" "):
            part = part.strip()
            if part != "":
                l.append(part)

        return " ".join(l)


class TimeoutForm(forms.Form):
    timeout = forms.IntegerField(min_value=60, max_value=5184000)
    grace = forms.IntegerField(min_value=60, max_value=5184000)
    nag_time = forms.IntegerField(min_value=60, max_value=5184000)


class AddChannelForm(forms.ModelForm):
    
    class Meta:
        model = Channel
        fields = ['kind', 'value']

    def clean_value(self):
        value = self.cleaned_data["value"]
        return value.strip()


class AddWebhookForm(forms.Form):
    error_css_class = "has-error"

    value_down = forms.URLField(max_length=1000, required=False)
    value_up = forms.URLField(max_length=1000, required=False)

    def get_value(self):
        return "{value_down}\n{value_up}".format(**self.cleaned_data)


class AddShopifyForm(forms.Form):
    error_css_class = "has-error"

    ping_url = forms.URLField(max_length=1000, required=True)
    CHOICES = (
        ('carts/create','Cart creation'),
        ('carts/update','Cart update'),
        ('checkouts/create','Checkout creation'),
        ('checkouts/delete','Checkout deletion'),
        ('checkouts/update','Checkout update'),
        ('collection_listings/add','Collecttion listing creation'),
        ('collection_listings/remove','Collection listing deletion'),
        ('collection_listings/update','Collection listing update'),
        ('collections/create','Collection creation'),
        ('collections/delete','Collection deletion'),
        ('collections/update','Collection update'),
        ('customer_groups/create','Customer group creation'),
        ('customer_groups/delete','Customer group deletion'),
        ('customer_groups/update','Customer group update'),
        ('customers/create','Customer creation'),
        ('customers/delete','Customer deletion'),
        ('customers/disable','Customer disable'),
        ('customers/enable','Customer enable'),
        ('customers/update','Customer update'),
        ('draft_orders/create','Draft order creation'),
        ('draft_orders/delete','Draft order deletion'),
        ('draft_orders/update','Draft order update'),
        ('fulfillments/create','Fulfillment creation'),
        ('fulfillments/update','Fulfillment update'),
        ('orders/cancelled','Order cancellation'),
        ('orders/create','Order creation'),
        ('orders/delete','Order deletion'),
        ('orders/fulfilled','Order fulfillment'),
        ('orders/paid','Order payment'),
        ('orders/updated','Order update'),
        ('product_listings/add','Product listing creation'),
        ('product_listings/remove','Product listing deletion'),
        ('product_listings/update','Product listing update'),
        ('products/create','Product creation'),
        ('products/delete','Product deletion'),
        ('products/update','Product update'),
        ('refunds/create','Refund creation'),
        ('shop/update','Shop update'),
        ('themes/create','Theme creation'),
        ('themes/delete','Theme deletion'),
        ('themes/publish','Theme publish'),
        ('themes/update','Theme update'),
    )
    event = forms.ChoiceField(widget=forms.Select, choices=CHOICES)
    shop = forms.URLField(max_length=1000, required=True)
    api_key = forms.CharField(max_length=500, required=True)
    password = forms.CharField(max_length=500, required=True)

    def clean_ping_url(self):
        ping_url = self.cleaned_data["ping_url"]
        return ping_url.strip()

    def clean_shop(self):
        shop = self.cleaned_data["shop"]
        return shop.strip()

    def clean_api_key(self):
        api_key = self.cleaned_data["api_key"]
        return api_key.strip()

    def clean_password(self):
        password = self.cleaned_data["password"]
        return password.strip()

    def get_event(self):
        return '{event}'.format(**self.cleaned_data)

    def get_displayed_option(self):
        event = self.cleaned_data['event']
        event_text = dict(self.fields['event'].choices)[event]
        return event_text
