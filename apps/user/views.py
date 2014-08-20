from django.views.generic import DetailView

from braces.views import LoginRequiredMixin

from .models import User


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'user/user_detail.jhtml'

    def get_object(self, queryset=None):
        return self.model.objects.get(id=self.request.user.id)


user_detail = UserDetailView.as_view()
