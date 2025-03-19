from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404

from django.urls import reverse
from django.shortcuts import redirect

from django.contrib.auth.decorators import login_required


from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Create your views here.
def foo(request):
    return HttpResponse("Hola django")

def index(request):
    return render(request, 'learning_logs/index.html')
    
@login_required    
def topics(request):
    
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    
    return render(request, 'learning_logs/topics.html', context)

def check_topic_owner(request, topic):
    if topic.owner != request.user:
        raise Http404
    
@login_required    
def topic(request, topic_id):
    
    topic = get_object_or_404(Topic, id=topic_id)
    check_topic_owner(request, topic)
    
    
    entries = topic.entry_set.order_by('-date_added')
    
    contexto = {'topic': topic, 'entries': entries }
    
    return render(request, 'learning_logs/topic.html', contexto)

def public_topics(request):
    
    topics = Topic.objects.filter(public=True).order_by('date_added')
    context = {'topics': topics}
    
    return render(request, 'learning_logs/public_topics.html', context)

def public_topic(request, topic_id):
    
    topic = get_object_or_404(Topic, id=topic_id)
        
    entries = topic.entry_set.order_by('-date_added')
    
    contexto = {'topic': topic, 'entries': entries }
    
    return render(request, 'learning_logs/topic.html', contexto)


@login_required
def new_topic(request):
    
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('topics')
    
    
    context = {'form': form}    
    return render(request, 'learning_logs/new_topic.html', context)
    
@login_required
def new_entry(request, topic_id):
    
    topic = get_object_or_404(Topic, id=topic_id)
    check_topic_owner(request, topic)
    
    if request.method != 'POST':
        form = EntryForm()
        
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            
            url = reverse('topic', args=[topic_id] )
            return redirect(url)
            

    context = {'topic': topic, 'form': form}
    
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    
    entry = get_object_or_404(Entry, id=entry_id)
    
    topic = entry.topic
    check_topic_owner(request, topic)
    
    
    if request.method == 'GET':
        form = EntryForm(instance=entry)
    
    else:
        form = EntryForm(instance=entry, data=request.POST)
        
        if form.is_valid():
            form.save()
    
            url = reverse('topic', args=[topic.id])
            return redirect(url)
    
    context = {
        'entry': entry,
        'topic': topic,
        'form': form
    }
    
    
    
    return render(request, 'learning_logs/edit_entry.html', context)
    
