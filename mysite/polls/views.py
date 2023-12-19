from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .forms import AdvUserForm, QuestionForm, SignUpForm
from .models import Question, Choice, AdvUser, Vote
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_object(self, queryset=None):
        question = super(DetailView, self).get_object(queryset)
        if question.was_published_recently or self.request.user.is_staff:
            return question
        else:
            raise PermissionDenied()

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': 'Ошибка! Вы ничего не выбрали!'
        })
    else:
        if Vote.objects.filter(question=question, user=request.user).exists():
            return render(request, 'polls/results.html', {
                'question': question,
                'error_message': 'Ошибка! Вы не можете голосовать несколько раз!'
            })
        else:
            question.question_votes +=1
            question.save()
            selected_choice.votes += 1
            selected_choice.save()
            voted = Vote.objects.create(question=question, user=request.user)
            voted.save()

            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def profile(request):
    return render(request, 'polls/profile.html')


class ChangeUserView(UpdateView):
    model = AdvUser
    form_class = AdvUserForm
    template_name = 'polls/change_user.html'
    success_url = reverse_lazy('polls:profile')


class DeleteUserView(DeleteView):
    model = AdvUser
    template_name = 'polls/delete_user.html'
    success_url = reverse_lazy('polls:index')


class ChangeQuestionView(UpdateView):
    model = Question
    template_name = "polls/change_image.html"
    form_class = QuestionForm
    success_url = reverse_lazy('polls:index')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user is not None and user.is_active:
                login(request, user)
                return HttpResponseRedirect("/polls")
    else:
        form = SignUpForm()
    return render(request, 'polls/signup.html', {'form': form})


class LoginServerView(LoginView):
    template_name = 'registration/login.html'


class LogoutServerView(LoginRequiredMixin, LogoutView):
    template_name = 'registration/logged_out.html'

