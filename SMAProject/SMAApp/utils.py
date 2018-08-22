
import ast, base64, functools
import django.http
from io import BytesIO, StringIO
from tempfile import NamedTemporaryFile
from shutil import copyfileobj
from PIL import Image
from django.urls import reverse
# This removes a dot from keys
# because mongodb doesnt allow keys with dots or $
def remove_dots_on_key(dictionary):
    # if passed data is string, convert it into a dict first.
    if isinstance(dictionary,str):
        dictionary = ast.literal_eval(dictionary)

    # looks for keys in the dictionary with . and removes it.
    for key in dictionary:
        if key.find('.') != -1 :
            newkey = key.replace(".","")
            dictionary[newkey] = dictionary.pop(key)
    return dictionary

# This returns lda_data keys into their original names
def restore_lda_keynames(dictionary):
    for key in dictionary:
        if key == 'tokentable':
            dictionary['token.table'] = dictionary.pop(key)
        if key == 'lambdastep':
            dictionary['lambda.step'] = dictionary.pop(key)
        if key == 'plotopts':
            dictionary['plot.opts'] = dictionary.pop(key)
        if key == 'topicorder':
            dictionary['topic.order'] = dictionary.pop(key)
    return dictionary 

def clear_specific_sessionkeys(request):
    if request.session.get("lda_data",False):
        del request.session['lda_data']

def convert_to_base64(image):
    # If passed image is a PIL image type
    # used by get_keyword, after generating the wordcloud image
    if isinstance(image,Image.Image): 
        buffered = BytesIO()
        image.save(buffered,format="PNG")
        b64_img_str = base64.b64encode(buffered.getvalue())
    # If passed image has a bytes type, 
    # used by load snapshot since mongodb image proxy gives image as bytes
    elif isinstance(image,bytes): 
        b64_img_str = base64.b64encode(image)
    return b64_img_str

def create_temp_img_file(pil_image):
    tempImgObj = NamedTemporaryFile(mode='w+b',suffix='.png')
    # with tempImgObj as png:
    #     png.write(pil_image)
    # print("ongj", tempImgObj.name)
    pil_image.save(tempImgObj,"PNG")
    # copyfileobj(pil_image,tempImgObj)
    print("Temp image path", tempImgObj.name)
    return tempImgObj

# Prevents users from accessing a page when they are not logged in yet.
# To use: just put @login_required on top of a method you want to be restricted.
# Note: make sure you import this by placing: "from .utils import login_required" on the file that this will be used
def login_required(view_func):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):              
        # if request.session.get('isloggedin'):
        if 'isloggedin' in request.session and 'search_keyword' in request.session:
            return view_func(request, *args, **kwargs)  
            # return django.http.HttpResponseRedirect(reverse('diagnostics'))
        else:
            return django.http.HttpResponseRedirect(reverse('login_user'))
        # return django.http.JsonResponse('Unauthorized', status=401,safe=False)
    return wrapper

# Prevents users from accessing any pages when they have not conducted a search yet.
def dataframe_required(view_func):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        df = request.session.get('df',None)
        if df is None:
            return django.http.HttpResponseRedirect('/')
    return wrapper