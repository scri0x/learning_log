from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Topic, Entry
from .forms import TopicForm, EntryForm

def index(request):
    context = {
        'title': 'Learning Log'
    }
    return render(request, 'index.html', context)

 # закрыть доступ к топикам если пользователь не зареган
@login_required
def topics(request):
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {
        'title': 'Темы',
        'topics': topics,
    }
    return render(request, 'topics.html', context)

@login_required
def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)

    check_topic_owner(topic.owner, request.user)
    entries = topic.entry_set.order_by('-date_added')
    context = {
        'title': topic,
        'topic': topic,
        'entries': entries,
    }
    return render(request, 'topic.html', context)


@login_required
def new_topic(request):
    if request.method != 'POST': #если данные не были отправлены, то создать пустую форму
        form = TopicForm()
    else: # иначе обработать данные введенные пользователем
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('topics'))
    context = {
        'form': form
    }
    return render(request, 'new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    topic = Topic.objects.get(id = topic_id)
    
    check_topic_owner(topic.owner, request.user)
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid:
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('topic', args=[topic_id]))
    context = {
        'topic': topic,
        'form': form,
    }
    return render(request, 'new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('topic', args=[topic.id])) # возвращяем пользователя на отредактированную запись
    context = {
        'title': 'Редактирование записи',
        'entry': entry,
        'topic': topic,
        'form': form,
    }
    return render(request, 'edit_entry.html', context)


def check_topic_owner(topic_owner, request_user):
    if topic_owner != request_user:
        raise Http404


