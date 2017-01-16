from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
from django.contrib import messages


from ..forms import CategoryFormSet
from ..models import KategorieZakupu


class CategoryListView(TemplateView):
    template_name = "categories.html"

    def get(self, request, *args, **kwargs):
        formset = CategoryFormSet()

        context = {
            'formset': formset
        }

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        formset = CategoryFormSet(
            data=request.POST,
            queryset=KategorieZakupu.objects.all()
        )

        context = {
            'formset': formset
        }

        for key, value in request.POST.items():
            print(key, ": ", value)
        for form in formset:
            print(form)
            print("Valid? ", form.is_valid())
        if formset.is_valid():
            try:
                formset.save()
            except IntegrityError as error:
                message = messages.error(
                    request,
                    'Jedna z kategorii posiada przypisane zakupy.'
                )
                return self.render_to_response(context)
            return HttpResponseRedirect(reverse('categories'))
        else:
            return self.render_to_response(context)
