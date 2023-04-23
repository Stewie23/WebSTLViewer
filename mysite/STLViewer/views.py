# -*- coding: utf-8 -*-
from django.http import HttpResponse
from STLViewer.models import Items,Taggins
from django.template import loader
from django.core.paginator import Paginator
from django.utils.text import slugify
from .forms import TagFilter, ItemSearchForm, TagEditor



def detailView(request):
    # Obtain the context from the HTTP request.
    id = request.GET.get("id", None)
    template = loader.get_template("STLViewer/detailView.html")

    item = Items.objects.get(itemid=id)
    tags = Taggins.objects.filter(item=item)

    tagEditor_form  = TagEditor(initial={'tagEditor': tags.values_list("tag", flat=True)})
 
 

    context = {
        "item":item,
        "tags":tags,
        "tagEditor_form":tagEditor_form,
    }    
    return HttpResponse(template.render(context,request))
    #return HttpResponse(tags)

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
            if len(taggedResults) == 0:
                taggedResults = set(Items.objects.filter(itemid__in=Taggins.objects.filter(tag = tag)).values_list("itemid",flat=True))
            else:
                taggedResults = set(taggedResults.intersection (Items.objects.filter(itemid__in=Taggins.objects.filter(tag = tag)).values_list("itemid",flat=True)))
        
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


    paginator = Paginator(item_list, 8)   
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
 