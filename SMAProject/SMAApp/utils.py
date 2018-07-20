# This removes a dot from keys
# because mongodb doesnt allow keys with dots or $
def removedotsonkey(dictionary):
    for key in dictionary:
        if key.find('.') != -1 :
            newkey = key.replace(".","")
            dictionary[newkey] = dictionary.pop(key)
    return dictionary

# This returns lda_data keys into their original names
def restoreldakeynames(dictionary):
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