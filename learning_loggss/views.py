from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

# Create your views here.
from .models import Topic, Entry
from .forms import TopicForm, EntryForm

def index(request):
    """Learning Logg Home page."""
    return render(request, 'learning_loggss/index.html')

@login_required
def topics(request):
    """Show all topics."""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_loggss/topics.html', context)

@login_required
def topic(request, topic_id):
    """Show all entries for a specific topic."""
    topic = Topic.objects.get(id=topic_id)
    # Make sure the topic belongs to the current user.
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic':topic, 'entries':entries}
    return render(request, 'learning_loggss/topic.html', context)

@login_required
def new_topic(request):
    """Add a new topic."""
    if request.method != 'POST':
        #No data submitted; create a blank form
        form = TopicForm()

    else:
        #POST data submitted; process the data
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_loggss:topics')

    #Display a blank or invalid form
    context = {'form': form}
    return render(request, 'learning_loggss/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """Adding new entries."""
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        #No POST data submitted; create a blank form.
        form = EntryForm()
    else:
        #POST data submitted; process data.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_loggss:topic', topic.id)

    #Display a blank or invalid form.
    context = {'topic':topic, 'form':form}
    return render(request, 'learning_loggss/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edit an entry that you added."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        #Initial request; pre-fill form wih current entry.
        form = EntryForm(instance=entry)
    else:
        #POST data submitted; process data.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_loggss:topic', topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_loggss/edit_entry.html', context)