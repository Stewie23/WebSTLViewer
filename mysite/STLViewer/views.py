# -*- coding: utf-8 -*-
from django.http import HttpResponse
from STLViewer.models import Items,Taggins
from django.template import loader
from django.core.paginator import Paginator
from .forms import TagFilter, ItemSearchForm, TagEditor
from .models import Taggins
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def detailView(request):
    if request.method == "POST":
        form = TagEditor(request.POST)
        if form.is_valid():
            id = request.POST.get("id")
            #do something with the tags 
            #delete all the old taggins for this id
            Taggins.objects.filter(item=id).delete()
            #write new ids 
            item = Items.objects.get(itemid=id)
            tags = form.cleaned_data['tagEditor']
            for tag in tags:
                tag_obj = Taggins(item=item, tag=tag)
                tag_obj.save()
                
            #redirect to the same page, id is supplied by a hidden field
            return redirect('/STLViewer/item/?id='+id)        
        else:
            errors = form.errors.as_data()
            print(errors)
    else:
        # Obtain the context from the HTTP request.
        id = request.GET.get("id", None)
        template = loader.get_template("STLViewer/detailView.html")
        item = Items.objects.get(itemid=id)
        tags = Taggins.objects.filter(item=item)
        tagEditor_form  = TagEditor(initial={'tagEditor': list(tags.values_list("tag", flat=True))})
        context = {
            "item":item,
            "tags":tags,
            "tagEditor_form":tagEditor_form,
        }    
        return HttpResponse(template.render(context,request))
        #return HttpResponse(tags)

@login_required
def basicView(request):
    #post data, generated from forms
    if request.method == "POST":
        print(request.POST)


    #template
    template = loader.get_template("STLViewer/basicView.html")
    #GET Data (for sharebile links)
    page_number = request.GET.get('page')
    filter_tag = request.GET.getlist("tagFilter")
    search_string = request.GET.get('search',"")

  
    #get items, by filter tag or all
    if (len(filter_tag) == 0 or filter_tag[0] ==''):
        #get all the items
        item_list = Items.objects.order_by("name").filter(name__contains=search_string)
    else:
        taggedResults = set()
        for tag in filter_tag:
            if (tag == "noTag"):#special tag for items that currently dont have a tag
                #list of items with no tags
                itemsWithTag_list = Taggins.objects.all().values_list("item_id",flat=True).distinct()
                taggedResults = Items.objects.all().exclude(itemid__in = itemsWithTag_list)
                break
            if len(taggedResults) == 0:
                taggedResults = set(Items.objects.filter(itemid__in=Taggins.objects.filter(tag = tag).values('item_id')).values_list("itemid",flat=True))
            else:
                taggedResults = set(taggedResults.intersection (Items.objects.filter(itemid__in=Taggins.objects.filter(tag = tag).values('item_id')).values_list("itemid",flat=True)))
        
        item_list = Items.objects.filter(itemid__in=taggedResults).filter(name__contains=search_string).order_by("name")
    #tag list
    tag_list = Taggins.objects.values_list("tag",flat=True).distinct()

    
    
    

    #form content
    filter_form  = TagFilter(initial={'tagFilter': filter_tag})
    search_form = ItemSearchForm(initial={'search': search_string})

    
    #
    reformated_filter_tag = "tagFilter="
    for i, tag in enumerate(filter_tag):
        if i == len(filter_tag) - 1:
            reformated_filter_tag += tag 
        else:
            reformated_filter_tag += tag + "&tagFilter="


    paginator = Paginator(item_list, 12)   
    page_obj = paginator.get_page(page_number)

    

    context = {
        'page_obj': page_obj,
        'filter_tag':reformated_filter_tag ,
        'tag_list':tag_list,
        'filter_form':filter_form,
        'search_form':search_form,
        'search_string':search_string,
    }  

    return HttpResponse(template.render(context,request))
 
@login_required
def download(request):
    response = HttpResponse()
    id = request.GET.get("id", None)
    item = Items.objects.get(itemid=id)
    file_name = item.name
    file_path = f'/stl/{item.path}' 
    # Let NGINX handle it
    response['X-Accel-Redirect'] = file_path
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(
        file_name
    )

    return response
    
