# -*- coding: utf-8 -*-
import base64
import hashlib
import json
import os
import shutil
import tempfile
from datetime import timedelta


from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import redirect, render, reverse
from django.template import loader
from django.utils import timezone




from STLViewer.models import Items, Taggins
from .forms import AddItemsForm, ItemSearchForm, TagEditor, TagFilter
from .models import Taggins



@login_required
def recentAdditions(request):
    template = loader.get_template("STLViewer/recentAdditions.html")

    # Get the number of days from query parameter (default: 7)
    num_days = int(request.GET.get('num_days', 7))

    # Get the number of items from query parameter (default: 10)
    num_items = int(request.GET.get('num_items', 10))

    # Calculate the start date based on the number of days
    start_date = timezone.now() - timedelta(days=num_days)

    # Retrieve the latest items based on the date field and number of items
    latest_items = Items.objects.filter(date_added__gte=start_date).order_by('-date_added')[:num_items]

    tag_editor_forms = []


    context = {
        'latest_items': latest_items,
        'num_days': num_days,
        'num_items': num_items,
    }

    return HttpResponse(template.render(context, request))

@login_required
def editThumbView(request):
    if request.method == "POST":
        pass
    else:
        id = request.GET.get("id", None)
        item = Items.objects.get(itemid=id)
        template = loader.get_template("STLViewer/editThumbView.html") 
        src_path = 'STLViewer/static/stl/'+ item.path    
        dst_dir = 'STLViewer/static/temp/'

        # Generate a random file name for the temporary file
        with tempfile.NamedTemporaryFile(dir=dst_dir, delete=False) as tmp:
            dst_path = tmp.name
            # Copy the file from src_path to dst_path
            shutil.copyfile(src_path, dst_path)
        context = {
            "item":item,
            'temp_stl':tmp.name.split("/")[-1],
        } 
        return HttpResponse(template.render(context,request))
    
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

        dublicates =  Items.objects.filter(hash = item.hash).exclude(itemid=id)
        dublicates = dublicates.values_list("itemid",flat=True)

        tagEditor_form  = TagEditor(initial={'tagEditor': list(tags.values_list("tag", flat=True))})
        
        context = {
            "item":item,
            "tags":tags,
            "dublicates":dublicates,
            "tagEditor_form":tagEditor_form,
        }    
        return HttpResponse(template.render(context,request))

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
    file_name = str(item.name) + ".stl"
    # Let NGINX handle it
    response['X-Accel-Redirect'] = '/download/' + item.path
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(file_name)
   
    print(response['X-Accel-Redirect'])
    return response

def save_uploaded_file(uploaded_file):
    file_name = uploaded_file.name

    # Choose a directory to store the uploaded files
    upload_directory = 'STLViewer/static/stl/upload/'
    if not os.path.exists(upload_directory):
        os.makedirs(upload_directory)

    file_path = os.path.join(upload_directory, file_name)
    relative_path = file_path.split('/stl/')[1]

     

    with open(file_path, 'wb') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
    
    #create file hash, and check for duplicates
    with open(file_path, "rb") as f:
        file_hash = hashlib.blake2b()
        while chunk := f.read(8192):
            file_hash.update(chunk)

    return relative_path, file_name.split('.')[0],file_hash.hexdigest()

@login_required   
def create_item(request):
    if request.method == 'POST':
        form = AddItemsForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['file']
            relative_path, file_name,file_hash = save_uploaded_file(uploaded_file)

            current_time = timezone.now()
            instance = Items(
                name=file_name,
                path=relative_path,
                found=0,
                hash=file_hash,
                thumbnail="Thumbnails/error.jpg",
                date_added=current_time
            )
            instance.save()
            item_id = instance.itemid
            redirect_url = "../item/?id="+str(item_id)
            return redirect(redirect_url)        
    else:
        form = AddItemsForm()
    
    context = {'form': form}
    return render(request, 'STLViewer/create_item.html', context)

@login_required   
def updateThumb(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        #delte the temp file
        temp_file_name = json_data['tempfile'].split('/')[-1]
       
        try:
            os.remove('STLViewer/static/temp/'+temp_file_name)
        except FileNotFoundError:
            pass

        id = json_data['id']
        base64_data = json_data['imageData'].split(',')[1]  # Extract base64 data after the comma
        image_data = base64.b64decode(base64_data)
        # Process the decoded image data
        # Example: Save the image to a file
        upload_directory = 'STLViewer/static/Thumbnails/'
        file_path = os.path.join(upload_directory, str(id)+'.jpg')
        with open(file_path, 'wb') as file:
            file.write(image_data)
        #update database entry
        item = Items.objects.get(itemid=id)
        item.thumbnail = 'Thumbnails/'+ str(id)+'.jpg'
        # Save the changes
        item.save()
        redirect_url = "../STLViewer/item/?id="+str(id)
        return redirect(redirect_url)
    else:
        return  HttpResponse()
        

