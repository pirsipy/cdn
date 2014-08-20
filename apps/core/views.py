from django.views.generic import TemplateView


class MainView(TemplateView):
    template_name = 'main.jhtml'


main = MainView.as_view()
