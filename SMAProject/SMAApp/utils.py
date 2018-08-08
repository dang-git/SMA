
import ast
import functools
import django.http
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


# Prevents users from accessing a page when they are not logged in yet.
# To use: just put @login_required on top of a method you want to be restricted.
# Note: make sure you import this by placing: "from .utils import login_required" on the file that this will be used
def login_required(view_func):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.session.get('isloggedin'):
            return django.http.HttpResponseRedirect('/diagnostics/')

        return django.http.JsonResponse('Unauthorized', status=401,safe=False)
    return wrapper