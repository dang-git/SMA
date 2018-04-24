# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 14:06:20 2017

@author: user
"""

import re
import pandas as pd
from wordcloud import WordCloud
from wordcloud import ImageColorGenerator
from PIL import Image
import numpy as np

def return_wordcloud(data):
    message = ''
    for i in list(range(0, len(data))):
        speech = re.sub(r'@\w+', ' ', data['tweet'][int(i)])
        speech = re.sub(r'https://t.co/\w+', ' ', speech).lower()
        speech = re.sub(r'https:\/\/\S+(\/\S+)*(\/)?', ' ', speech)
        speech = re.sub(r'http:\/\/\S+(\/\S+)*(\/)?', ' ', speech)
        speech = re.sub(r'\r', ' ', speech)
        speech = re.sub(r'\n', ' ', speech)
        speech = re.sub(r'\xbd', ' ', speech)
        speech = re.sub(r'\xbb', ' ', speech)
        speech = re.sub(r'\xbf', ' ', speech)
        speech = re.sub(r'\xbc', ' ', speech)
        speech = re.sub(r'<[^<>]+>', ' ', speech)
        speech = re.sub('[^a-zA-Z-]', ' ', speech)
        message = message + ' ' + speech
    stops = list(pd.read_csv("stops.csv", header=None)[0])
    names = ['camacho', 'jason', 'ron', 'alcantara-banaybanay', 'rob', 'cynthia', 'sonja', 'roy', 'gahon', 'mejia', 'rosales', 'tuba', 'maquilan', 'galvez', 'abdurahman', 'jerome', 'jessie', 'rutor', 'pedro', 'keith', 'sabalburo', 'marissa', 'santosghel', 'april', 'anjannette', 'riza', 'salido', 'rg', 'tj', 'balderama', 'estanislao', 'oliveros', 'tvpatrol', 'scarlett', 'icasiano-ruiz', 'dela', 'secondez,ly', 'labong', 'ayyie', 'augusto', 'hannah', 'aurora', 'gerodias', 'evardome', 'jacq', 'vera', 'bugna', 'lhenyet', 'sol', 'besinal', 'ivanong', 'hya', 'joed', 'ofrin', 'erlinda', 'esperanza', 'dumaguing', 'philippines', 'solatorio', 'michael', 'dia', 'ryan', 'ri', 'p', 'harry', 'elah', 'venus', 'caryl', 'orzo', 'louie', 'zabarte', 'inot', 'zhav', 'tel', 'osinsao', 'musñgi', 'teo', 'jerelyn', 'abarquez', 'falcis', 'jc', 'galay', 'mangaliman', 'marilyn', 'arnold', 'rodmar', 'elise', 'redrose', 'belleza', 'capalad', 'rosauro', 'celestino', 'jochelle', 'cely', 'vitorillo', 'kris', 'canales', 'barrientos', 'lising', 'laurence', 'haze', 'binabay', 't', 'joycie', 'net', 'roann', 'jayson', 'phoebe', 'christian', 'dahl', 'laborre', 'therese', 'henry', 'jasmine', 'avigail', 'leo', 'ching', 'simon', 'janessa', 'jhunski', 'josol', 'odero', 'pacis', 'relly', 'terrence', 'bemon', 'calter', 'marionne', 'heracleo', 'louise', 'nodalo', 'alyssa', 'raffytulfo', 'aki', 'ramos', 'lizette', 'cindy', 'dasco', 'cathy', 'janice', 'rlndblnsg', 'dre', 'agustin', 'jann', 'robillos', 'sirc', 'mendozadel', 'apple', 'apyang', 'julie', 'boqx', 'bro', 'rhonn', 'austria', 'alinsod', 'aimee', 'kristina', 'elizaga', 'baltazar', 'gagalang', 'ishibashi', 'trinidad', 'angelo', 'cha', 'tels', 'jayme', 'andaya', 'barrios', 'mendoza', 'nava', 'charie', 'aya', 'ambid', 'elleyn', 'rodriguez', 'salash', 'presquito', 'bonilla', 'chu', 'galguerra', 'morc', 'jonathan', 'seguerra', 'baba', 'escalona', 'miayo', 'sarmiento', 'baliuag', 'aiza', 'israel', 'yvaine', 'casey', 'barcellano', 'dios', 'tesalona', 'zamora', 'chastine', 'secuya', 'conje', 'esquivel', 'te', 'ma', 'caguiat', 'rayson', 'gabriel', 'mo', 'krizza', 'albon', 'jude', 'mj', 'nina', 'arches', 'archer', 'del', 'era', 'flo', 'julliane', 'bojo', 'ernest', 'olivar', 'dee', 'zafe', 'heart', 'gerly', 'rappler', 'shara', 'milagrosa', 'amalia', 'dato-on', 'honey', 'naome', 'allauigan', 'daiserie', 'malig-on', 'nobleza', 'tan', 'agena', 'angielyn', 'sis', 'mendoza-del', 'reyespia', 'silos', 'russelloto', 'roderos', 'lorisse', 'cabrillos', 'ava', 'camille', 'brian', 'sia', 'mayores', 'gallart', 'mari', 'reyes', 'enz', 'fortaliza', 'divo', 'masujer', 'mar', 'dadia', 'elizabeth', 'gmanews', 'ayala', 'may', 'alojado', 'hong', 'alegre', 'ronald', 'levi', 'margret', 'actiontv', 'rosanna', 'mai', 'alindada', 'avengers', 'malena', 'a', 'abe', 'beltran', 'azzupary', 'pamparo-castrillo', 'rosalinda', 'arciento', 'q', 'umagang', 'claire', 'riezel', 'martina', 'pangilinan-po', 'gerard', 'buge', 'paz', 'castillejos',
         'sd', 'shiela', 'voluntarioso', 'navarroanj', 'johnell', 'josephine', 'quiño', 'orana', 'yvonne', 'emmanuel', 'caudilla', 'modesto', 'mabel', 'dagaraga', 'mallari', 'glen', 'jian', 'josie', 'runas', 'zepeda', 'amaloveina', 'yucai', 'lu', 'dolly', 'romarico', 'santelices', 'taylo', 'esem', 'rara', 'jady', 'balungcas', 'barbosa', 'dacumos', 'vhie', 'notario', 'diko', 'jvr', 'dan', 'jadloc', 'tanzie', 'flordeliza', 'caampued', 'cendy', 'baillo', 'alojchristine', 'dalusong', 'adri', 'odee', 'son', 'rhym', 'bryan', 'vidal', 'ruby', 'usman', 'jenina', 'james', 'tere', 'fhei', 'l', 'alexis', 'nerecena', 'cammille', 'wong', 'jefferson', 'mead', 'lheyann', 'bong', 'alice', 'deguzman', 'em', 'guinto', 'jenn', 'rachelle', 'cecille', 'rojas', 'alojadoacatherine', 'katrina', 'sardeniola', 'guilangue', 'macabanti-geronimo', 'marcos', 'girl', 'nanit', 'aldrin', 'marius', 'angulo', 'rey', 'ibarra', 'ernie', 'garcia', 'gonzales', 'robert', 'pajiji', 'kenn', 'keno', 'lagumbay', 'mandz', 'zanchez', 'charlyne', 'daniel', 'ren', 'dominguiano', 'gutierrez', ',buan', 'generoso', 'dahleng', 'lorgene', 'ella', 'rj', 'benjamin', 'torres', 'harold', 'clarence', 'alban', 'lawrence', 'ganzon', 'caronan', 'perucho', 'fred', 'mikhail', 'jhenni', 'jill', 'yuri', 'carl', 'ramoy', 'asi', 'romualdo', 'ariane', 'princess', 'esteves', 'asmaira', 'marla', 'yara', 'dorlyn', 'ate', 'watisdis', 'g', 'cañeda', 'cadiz', 'barbara', 'helen', 'gelyn', 'marlo', 'david', 'katniss', 'nalzaro', 'mae', 'isa', 'quinto', 'tyntine', 'legaspi', 'nebrida', 'cangas', 'paclibar', 'albarido', 'pangilinan', 'dione', 'justine', 'ong', 'famor', 'jesus', 'bernadette', 'pamparo-castrillolouise', 'mel', 'jazz', 'pablo', 'rona', 'jerizza', 'scent', 'mervyn', 'lazala', 'reinier', 'combate', 'ian', 'castaneda', 'castillo', 'imelda', 'perado', 'isadel', 'pilarca', 'magcawas', 'ramssel', 'aldwin', 'patiño', 'mayvelle', 'gilbert', 'john', 'jen', 'genesis', 'rosario', 'cabral', 'vargasmaglalang', 'padrinao-villanueva', 'acogido', 'taylo-', 'villanueva', 'silang', 'carmi', 'valencia', 'grace', 'valdz', 'rollie', 'king', 'vienne', 'man-on', 'jayjay', 'treb', 'maricel', 'manlapaz', 'capili', 'cristobal', 'abs-cbn', 'genson', 'salazar', 'lourdes', 'sophia', 'and', 'ver-dee', 'jinky', 'aquino', 'ana', 'lhene', 'ann', 'ram', 'francial', 'dungog-romagos', 'canlapan', 'mararac', 'quilinguing', 'herlene', 'kevin', 'ray', 'poblete', 'sotelo', 'ybanez', 'lamsen', 'maximo', 'mia', 'lim', 'ecalnir', '-', 'oh', 'roehl', 'aisha', 'chiong', 'fajilan', 'rowen', 'arazas', 'jhen', 'fayot', 'emalyn', 'mamhie', 'santiago', 'mariz', 'abella', 'manette', 'alcantara', 'unang', 'hazel', 'maris', 'jeph', 'jazziel', 'kelly', 'caponpon', 'sapo', 'charm', 'villafuerte', 'bh3', 'marie', 'fria', 'maria', 'don', 'besas', 'ofiana', 'flor', 'ylime', 'm', 'paru', 'saguinsin', 'lujera', 'bulan', 'charmaeine', 'brey', 'renier', 'gabaleo', 'ramososhasha', 'daluz', 'arjaybaluyot', 'zacarias', 'ralph', 
         'charles', 'niel', 'jarder', 'troy', 'merin', 'perlas', 'sarenbeniga', 'cabeliza', 'sangalang', 'florentino', 'kale', 'figueroa', 'cyril', 'leigh', 'cherryl', 'jay', 'jabee', 'locsin', 'ayen', 'mitzi', 'tanya', 'aldo', 'botabara', 'alocha', 'jam', 'gideon', 'aby', 'vierneza', 'caroline', 'sieg', 'ruiz', 'rica', 'boris', 'angieline', 'adviento', 'couz', 'jomar', 'criste', 'de', 'dc', 'b', 'cora', 'dy', 'uy', 'kayganda', 'gen', 'rondez', 'alexander', 'buan', 'dianne', 'casabuena', 'joanne', 'emm', 'corvin', 'lala', 'remata', 'charleane', 'felipe', 'jaime', 'roger', 'aris', 'jeosh', 'allito', 'dagtaagta', 'leynes', 'bam', 'jovie', 'khristine', 'rfl', 'carrillo', 'eiram', 'nixx', 'agulto', 'cao', 'buscagan', 'isabel', 'roque', 'ablen', 'leslie', 'rmg', 'ricyet', 'bautista', 'troilus', 'nimfa', 'angie', 'corro', 'caster', 'cheska', 'dexter', 'jennyrose', 'mitch', 'gayjow', 'apol', 'arlyn', 'mamayay', 'verbo', 'rito', 'aranza', 'isha', 'morales', 'marvin', 'zabala', 'palogan', 'jasmin', 'baltar', 'tania', 'dhianne', 'rimas', 'jov', 'domo', 'joy', 'herrera', 'valerie', 'antoniano', 'jr', 'hirit', 'javierariane', 'nikka', 'manalili', 'yba', 'selene', 'news', 'ravela', 'lopez', 'loudine', 'manabat', 'c', 'javier', 'almonguera', 'jm', 'jocelyn', 'edgar', 'vincharl', 'shankanecai', 'soriano', 'tolentino', 'milo', 'jonas', 's', 'com', 'eto', 'con', 'ayeeh', 'oswa', 'mangilit', 'co', 'jeff', 'toni', 'cinth', 'durante', 'cla', 'guzman', 'karen', 'rae', 'esbra', 'kev', 'baccay', 'magbanua', 'sherwin', 'san', 'carpio', 'rrvee', 'kinjan', 'karlo', 'lanymay', 'odey', 'karla', 'elmer', 'teus', 'kasten', 'mark', 'olave', 'raffy', 'mikee', 'yan', 'noel', 'razzie', 'pj', 'quintong', 'zobel', 'mary', 'caloi', 'hernandez', 'roselyn', 'mike', 'cecile', 'dhey', 'chua', 'gemma', 'mahusay', 'dhes', 'andrew', 'gan', 'fritz', 'andrei', 'dote', 'taboadabas', 'mhee', 'quilapio', 'aileen', 'kerstin', 'judee', 'remy', 'deden', 'cepriano', 'calderonukaren', 'castro', 'n', 'dacanay', 'capinpin', 'aldie', 'margie', 'maravilla-casacop', 'vicky', 'jerald', 'drewan', 'archie', 'veronica', 'parugrug', 'bustarde', 'portugal', 'susana', 'cabangon', 'veras', 'shamy', 'yam', 'ii', 'rio', 'oquindo', 'majano', 'perez', 'jingco', 'zandro', 'boom', 'zaldy', 'ayuban', 'ignacio', 'santos', 'guzman-francisco', 'cascabel', 'pau', 'aldana', 'belle', 'edwin', 'macalalad', 'bella', 'leoniño', 'rules', 'ocampo', 'jepher', 'naces', 'claridad', 'miya', 'pam', 'paoner', 'brigente', 'calacday', 'raymond', 'leonie', 'condes', 'talaban', 'kit', 'palabrica', 'cudiamat', 'kim', 'dayan', 'villegas', 'vargas', 'gaspay', 'villa', 'arra', 'albesa', 'blanco', 'meazel', 'antonio', 'portillo', 'jessica', 'toy', 'espiritu', 'llanto', 'jayvee', 'legera', 'denjie', 'burgos', 'alvin', 'bonecille', 'jexter', 'rhoen', 'hervas', 'celzo', 'bes', 'jaul', 'oxford', 'jonard', 'ethel', 'patsy', 'laurel', 'paul', 'montañez', 'riachelle', 'rochelle', 'trins', 'bry', 'rose', 'gma', 
         'gorme', 'tin', 'balubar', 'rubio', 'bobis', 'samuel', 'tuway', 'viansuaverdez', 'ada', 'bagacina', 'yopo', 'panara-ag', 'alcala', 'venzon', 'jake', 'clirkz', 'sunico', 'vanessa', 'granados', 'sabdaniaira', 'cruz', 'recy', 'malubay', 'tolentino-miano', 'alida', 'lanie', 'enriquez', 'mariah', 'margiemel', 'popoy', 'rozend', 'christine', 'verner', 'paradagomez', 'salinas', 'edjen', 'cayabyab', 'arthur', 'gumana', 'rhodora', 'talosig', 'martin', 'ivan', 'mamagat', 'chico', 'love', 'salih', 'dimapilis', 'manaay', 'lazarte', 'macario', 'shen', 'chrissele', 'tulod', 'denice', 'nagal', 'donald', 'francisco', 'rhazel', 'gracia', 'dimaano', 'cebrero', 'bagtas', 'alfaize', 'marzan', 'caredz', 'manahan', 'isagan', 'cavada', 'masaybeng', 'irma', 'rmarie', 'bagos', 'jelka', 'mhendie', 'oblanca', 'cnn', 'anne', 'dizon', 'marit', 'anna', 'arnel', 'mante', 'sarah', 'abanes', 'emms', 'gmax', 'briones', 'bogie', 'reza', 'palisoc', 'marquez', 'rosal', 'oliver', 'pascual', 'yolly', 'ross', 'francis', 'diosa', 'russell', 'shine', 'conrad', 'cerafica', 'justin', 'adzwiya', 'linsangan', 'jay-ar', 'o', 'hilarion', 'wolf', 'kpn', 'tomo', 'segovia', 'maurin', 'hazey', 'dulay', 'reycie', 'carolyn', 'costumbrado', 'obrero', 'miranda', 'catherine', 'retchie', 'gleng', 'yap', 'martinez', 'lacerna', 'paches', 'magbitang', 'mauie', 'diala', 'joyce', 'arvin', 'gomez', 'cajeta', 'joemar', 'jing', 'qadriyyah', 'delos', 'ortiz', 'neser', 'pauline', 'loo', 'ponce', 'imperial', 'joseph', 'daniell', 'shella', 'dioso', 'jayron', 'jane', 'pilares', 'labaco', 'gil', 'dutchque', 'vicente', 'pauyon', 'bobadilla', 'gulmatico', 'vasquez', 'arceta', 'kristian', 'jun', 'mc', 'marge', 'concepcion', 'mercado', 'funda', 'lans', 'pepperminty', 'khim', 'jumawid', 'ladines', 'alvero', 'kiitt', 'erick', 'paires', 'salome', 'angcao', 'maglalang', 'merilyn', 'manuel', 'taguibao', 'madz', 'bermas', 'krizzie', 'molato', 'kathy', 'ae', 'chad', 'ghaneza', 'sarsola', 'russelle', 'draculan', 'al', 'añonuevo', 'au', 'lher', 'aristotle', 'kho', 'abarilla', 'grafil', 'lyn', 'claudine', 'eric', 'fajie', 'ronil', 'tita', 'polangco', 'guarin', 'evilla', 'sumampong', 'quinjacob', 'abigail', 'lendy', 'nick', 'jona', 'feliciano', 'nico', 'oscar', 'rosalita', 'njie', 'rigonan', 'riam', 'garcera', 'tess', 'cyrmyn', 'jestoni', 'cabrera', 'chavez', 'ku', 'iza', 'janella', 'papa', 'acosta', 'medina', 'regalario', 'margaret', 'maureen', 'macallop', 'lacaba', 'abanes-escalona', 'terry', 'sai-rex', 'cabuang', 'valderama', 'urbano', 'jones', 'miles', 'sayson', 'news5', 'geraldine', 'hadap', 'dumalag', 'krystyn', 'aiko', 'elizalde', 'dinia']
    words = message.split(' ')
    words = [w for w in words if not w in stops]
    words = [w for w in words if not w in names]
    words = list(filter(None, words))
    for i in range(0, len(words)):
        if "bwas" in words[i]: 
            words[i] = "bawas"
        if "bawas" in words[i]: 
            words[i] = "bawas"
        if "withdraw" in words[i]: 
            words[i] = "withdraw"
        if words[i] in ['nawidraw', 'winidraw', 'wothdraw', 'widrawal', 'widrawals', 'winithdraw', 'wedrawhin', 'nagwidraw', 'witdrawals', 'winiwidraw', 'withraw', 'widraw', 'wedraw', 'mawdraw', 'mgwdraw', 'witdrawan', 'wiwiwdraw', 'wiwidrwhn', 'widroha']: 
            words[i] = "withdraw"
        if "balik" in words[i]: 
            words[i] = "balik"
        if "inconven" in words[i]: 
            words[i] = "inconvenient"
        if "service" in words[i]: 
            words[i] = "service"
        if "system" in words[i]: 
            words[i] = "system"
        if "tagal" in words[i]: 
            words[i] = "tagal"
        if "tiwala" in words[i]: 
            words[i] = "tiwala"
        if "twala" == words[i]: 
            words[i] = "tiwala"
        if "transfer" in words[i]: 
            words[i] = "transfer"
        if "trust" in words[i]: 
            words[i] = "trust"
        if "secur" in words[i]: 
            words[i] = "security"
        if "hacked" in words[i]: 
            words[i] = "hack"
        if  words[i] in ['banks', 'banko']: 
            words[i] = "bank"
        if "problem" in words[i]: 
            words[i] = "problema"
        if "errors" == words[i]: 
            words[i] = "error"
        if words[i] in ['ty', 'tnx', 'thx', 'thnx', 'thank']: 
            words[i] = "thanks"
        if words[i] in ['nawalang', 'mawawala', 'nawawala', 'wlng', 'nawawalan', 'nawalan', 'walang', 'mawala', 'nawala', 'wla', 'nawawalang', 'wlang', 'nwala', 'mawalan']: 
            words[i] = "wala"
        if words[i] in ['nakawan', 'ninakawan', 'nanakawan']: 
            words[i] = "nakaw"
        if words[i] in ['fufund', 'fund', 'funds']: 
            words[i] = "fund"
        message = ''
        for i in range(0, len(words)):
            message = message + ' ' + words[i]
        #wordcloud background picture
        img = Image.open('bg.png')
        img = img.resize((900,550), Image.ANTIALIAS)
        hcmask = np.array(img)
        image_colors = ImageColorGenerator(hcmask)
        wc = WordCloud(background_color = '#ffffff', max_words = 300, mask = hcmask, stopwords = stops)
        wc.generate(message)
        wc.recolor(color_func = image_colors)
        # saves wordcloud as png files
        wc.to_file("wordcloud.png")