from PIL import Image

from django.contrib import admin
from django.forms import ModelChoiceField, ModelForm, ValidationError
from django.utils.safestring import mark_safe

from .models import *

# class for Validations with resolutions and size


class TShirtAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['main_image'].help_text = mark_safe(
            '<span style="color:red; font-size:13px;">Завантажуйте зображення з розширенням не менш ніж 500 x 450, якщо більше то само відріже</span>'
            )


class BagAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['main_image'].help_text = mark_safe(
            '<span style="color:red; font-size:13px;">Завантажуйте зображення з розширенням не менш ніж 400 x 600, якщо більше то само відріже</span>'
            )


class HoodAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['main_image'].help_text = mark_safe(
            '<span style="color:red; font-size:13px;">Завантажуйте зображення з розширенням не менш ніж 400 x 600, якщо більше то само відріже</span>'
        )


class ShoperAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['main_image'].help_text = mark_safe(
            '<span style="color:red; font-size:13px;">Завантажуйте зображення з розширенням не менш ніж 400 x 600, якщо більше то само відріже</span>'
        )


class SockAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['main_image'].help_text = mark_safe(
            '<span style="color:red; font-size:13px;">Завантажуйте зображення з розширенням не менш ніж 400 x 600, якщо більше то само відріже</span>'
        )


class SweetshotAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['main_image'].help_text = mark_safe(
            '<span style="color:red; font-size:13px;">Завантажуйте зображення з розширенням не менш ніж 400 x 600, якщо більше то само відріже</span>'
        )


class PantAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['main_image'].help_text = mark_safe(
            '<span style="color:red; font-size:13px;">Завантажуйте зображення з розширенням не менш ніж 400 x 600, якщо більше то само відріже</span>'
        )


class ScarfAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['main_image'].help_text = mark_safe(
            '<span style="color:red; font-size:13px;">Завантажуйте зображення з розширенням не менш ніж 400 x 600, якщо більше то само відріже</span>'
        )


class JacketAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['main_image'].help_text = mark_safe(
            '<span style="color:red; font-size:13px;">Завантажуйте зображення з розширенням не менш ніж 400 x 600, якщо більше то само відріже</span>'
        )


class PatchAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['main_image'].help_text = mark_safe(
            '<span style="color:red; font-size:13px;">Завантажуйте зображення з розширенням не менш ніж 400 x 600, якщо більше то само відріже</span>'
        )


    # def clean_image(self):
    #     image = self.cleaned_data['image']
    #     img = Image.open(image)
    #     min_height, min_width = Product.MIN_RESOLUTION
    #     max_height, max_width = Product.MAX_RESOLUTION
    #     if image.size > Product.MAX_IMAGE_SIZE:
    #         raise ValidationError('Розмір зображення не повинен перевищувати 3 мб')
    #     if img.height < min_height or img.width < min_width:
    #         raise ValidationError('Розширення зображення меньше мінімального')
    #     if img.height > max_height or img.width > max_width:
    #         raise ValidationError('Розшірення зображення більше максимального')
    #     return image


class TShirtAdmin(admin.ModelAdmin):

    form = TShirtAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='tshirts'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class BagAdmin(admin.ModelAdmin):

    form = BagAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='bags'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class HoodAdmin(admin.ModelAdmin):

    form = HoodAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='hoods'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ShoperAdmin(admin.ModelAdmin):

    form = ShoperAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='shopers'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SockAdmin(admin.ModelAdmin):

    form = SockAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='socks'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SweetshotAdmin(admin.ModelAdmin):

    form = SweetshotAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='sweetshots'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class PantAdmin(admin.ModelAdmin):

    form = PantAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='pants'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ScarfAdmin(admin.ModelAdmin):

    form = ScarfAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='scarfs'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class JacketAdmin(admin.ModelAdmin):

    form = JacketAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='jackets'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class PatchAdmin(admin.ModelAdmin):

    form = PatchAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='patchs'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Category)
admin.site.register(TShirt, TShirtAdmin)
admin.site.register(Bag, BagAdmin)
admin.site.register(Hood, HoodAdmin)
admin.site.register(Shoper, ShoperAdmin)
admin.site.register(Sock, SockAdmin)
admin.site.register(Sweetshot, SweetshotAdmin)
admin.site.register(Pant, PantAdmin)
admin.site.register(Scarf, ScarfAdmin)
admin.site.register(Jacket, JacketAdmin)
admin.site.register(Patch, PatchAdmin)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(Order)

