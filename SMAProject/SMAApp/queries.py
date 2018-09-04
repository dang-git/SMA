from SMAApp.models import Snapshot, User, Names, Idioms, Boosters, BaseForms, Lexicons, Negate, Emojis
from SMAApp import globals
from mongoengine.queryset.visitor import Q
from mongoengine.queryset import DoesNotExist, NotUniqueError
# Returns a snapshot list containing tuples with snapshot id and its text
# in this format [(id1,text1),(id2,text2)]
def get_snapshot_list(userid):
    snapshot_list = []
    snap = ()
    # Used aggregate to get the number of snaphots a user has.
    # Particularly this:  'snapshotCount': {'$size': '$snapshots'}
    # set fields with 1 so they will be available in the result
    pipeline = { '$project':{'snapshots': 1, 'snapshotCount': {'$size': '$snapshots'}}}        
    # dummy_id = '5b570b5b55d14c15804bf846'
    for user in User.objects(_id=userid).aggregate(pipeline):
        for snapshot in user['snapshots']:
            snap = (snapshot['value'],snapshot['text']) 
            snapshot_list.append(snap)

    # snapshot_list = [(snapshotObj._id,snapshotObj.snapshot_name) for snapshotObj in Snapshot.objects(owner=globals.snapshot_owner)]
    return snapshot_list

def check_if_email_exists(email):
    is_exists = False
    if User.objects(email=email):
        is_exists = True
    return is_exists


# SMA Words

    """ NAMES """

def get_names():
    name_list = []
    for namesObj in Names.objects(owner="default"):
        name_list.append(namesObj.name)
    print("NAME LENGTH:", len(name_list))
    return name_list

def insert_names():    
    names = ['camacho', 'jason', 'ron', 'alcantara-banaybanay', 'rob', 'cynthia', 'sonja', 'roy', 'gahon', 'mejia', 'rosales', 'tuba', 'maquilan', 'galvez', 'abdurahman', 'jerome', 'jessie', 'rutor', 'pedro', 'keith', 'sabalburo', 'marissa', 'santosghel', 'april', 'anjannette', 'riza', 'salido', 'rg', 'tj', 'balderama', 'estanislao', 'oliveros', 'tvpatrol', 'scarlett', 'icasiano-ruiz', 'dela', 'secondez,ly', 'labong', 'ayyie', 'augusto', 'hannah', 'aurora', 'gerodias', 'evardome', 'jacq', 'vera', 'bugna', 'lhenyet', 'sol', 'besinal', 'ivanong', 'hya', 'joed', 'ofrin', 'erlinda', 'esperanza', 'dumaguing', 'philippines', 'solatorio', 'michael', 'dia', 'ryan', 'ri', 'p', 'harry', 'elah', 'venus', 'caryl', 'orzo', 'louie', 'zabarte', 'inot', 'zhav', 'tel', 'osinsao', 'musñgi', 'teo', 'jerelyn', 'abarquez', 'falcis', 'jc', 'galay', 'mangaliman', 'marilyn', 'arnold', 'rodmar', 'elise', 'redrose', 'belleza', 'capalad', 'rosauro', 'celestino', 'jochelle', 'cely', 'vitorillo', 'kris', 'canales', 'barrientos', 'lising', 'laurence', 'haze', 'binabay', 't', 'joycie', 'net', 'roann', 'jayson', 'phoebe', 'christian', 'dahl', 'laborre', 'therese', 'henry', 'jasmine', 'avigail', 'leo', 'ching', 'simon', 'janessa', 'jhunski', 'josol', 'odero', 'pacis', 'relly', 'terrence', 'bemon', 'calter', 'marionne', 'heracleo', 'louise', 'nodalo', 'alyssa', 'raffytulfo', 'aki', 'ramos', 'lizette', 'cindy', 'dasco', 'cathy', 'janice', 'rlndblnsg', 'dre', 'agustin', 'jann', 'robillos', 'sirc', 'mendozadel', 'apple', 'apyang', 'julie', 'boqx', 'bro', 'rhonn', 'austria', 'alinsod', 'aimee', 'kristina', 'elizaga', 'baltazar', 'gagalang', 'ishibashi', 'trinidad', 'angelo', 'cha', 'tels', 'jayme', 'andaya', 'barrios', 'mendoza', 'nava', 'charie', 'aya', 'ambid', 'elleyn', 'rodriguez', 'salash', 'presquito', 'bonilla', 'chu', 'galguerra', 'morc', 'jonathan', 'seguerra', 'baba', 'escalona', 'miayo', 'sarmiento', 'baliuag', 'aiza', 'israel', 'yvaine', 'casey', 'barcellano', 'dios', 'tesalona', 'zamora', 'chastine', 'secuya', 'conje', 'esquivel', 'te', 'ma', 'caguiat', 'rayson', 'gabriel', 'mo', 'krizza', 'albon', 'jude', 'mj', 'nina', 'arches', 'archer', 'del', 'era', 'flo', 'julliane', 'bojo', 'ernest', 'olivar', 'dee', 'zafe', 'heart', 'gerly', 'rappler', 'shara', 'milagrosa', 'amalia', 'dato-on', 'honey', 'naome', 'allauigan', 'daiserie', 'malig-on', 'nobleza', 'tan', 'agena', 'angielyn', 'sis', 'mendoza-del', 'reyespia', 'silos', 'russelloto', 'roderos', 'lorisse', 'cabrillos', 'ava', 'camille', 'brian', 'sia', 'mayores', 'gallart', 'mari', 'reyes', 'enz', 'fortaliza', 'divo', 'masujer', 'mar', 'dadia', 'elizabeth', 'gmanews', 'ayala', 'may', 'alojado', 'hong', 'alegre', 'ronald', 'levi', 'margret', 'actiontv', 'rosanna', 'mai', 'alindada', 'avengers', 'malena', 'a', 'abe', 'beltran', 'azzupary', 'pamparo-castrillo', 'rosalinda', 'arciento', 'q', 'umagang', 'claire', 'riezel', 'martina', 'pangilinan-po', 'gerard', 'buge', 'paz', 'castillejos',
    'sd', 'shiela', 'voluntarioso', 'navarroanj', 'johnell', 'josephine', 'quiño', 'orana', 'yvonne', 'emmanuel', 'caudilla', 'modesto', 'mabel', 'dagaraga', 'mallari', 'glen', 'jian', 'josie', 'runas', 'zepeda', 'amaloveina', 'yucai', 'lu', 'dolly', 'romarico', 'santelices', 'taylo', 'esem', 'rara', 'jady', 'balungcas', 'barbosa', 'dacumos', 'vhie', 'notario', 'diko', 'jvr', 'dan', 'jadloc', 'tanzie', 'flordeliza', 'caampued', 'cendy', 'baillo', 'alojchristine', 'dalusong', 'adri', 'odee', 'son', 'rhym', 'bryan', 'vidal', 'ruby', 'usman', 'jenina', 'james', 'tere', 'fhei', 'l', 'alexis', 'nerecena', 'cammille', 'wong', 'jefferson', 'mead', 'lheyann', 'bong', 'alice', 'deguzman', 'em', 'guinto', 'jenn', 'rachelle', 'cecille', 'rojas', 'alojadoacatherine', 'katrina', 'sardeniola', 'guilangue', 'macabanti-geronimo', 'marcos', 'girl', 'nanit', 'aldrin', 'marius', 'angulo', 'rey', 'ibarra', 'ernie', 'garcia', 'gonzales', 'robert', 'pajiji', 'kenn', 'keno', 'lagumbay', 'mandz', 'zanchez', 'charlyne', 'daniel', 'ren', 'dominguiano', 'gutierrez', ',buan', 'generoso', 'dahleng', 'lorgene', 'ella', 'rj', 'benjamin', 'torres', 'harold', 'clarence', 'alban', 'lawrence', 'ganzon', 'caronan', 'perucho', 'fred', 'mikhail', 'jhenni', 'jill', 'yuri', 'carl', 'ramoy', 'asi', 'romualdo', 'ariane', 'princess', 'esteves', 'asmaira', 'marla', 'yara', 'dorlyn', 'ate', 'watisdis', 'g', 'cañeda', 'cadiz', 'barbara', 'helen', 'gelyn', 'marlo', 'david', 'katniss', 'nalzaro', 'mae', 'isa', 'quinto', 'tyntine', 'legaspi', 'nebrida', 'cangas', 'paclibar', 'albarido', 'pangilinan', 'dione', 'justine', 'ong', 'famor', 'jesus', 'bernadette', 'pamparo-castrillolouise', 'mel', 'jazz', 'pablo', 'rona', 'jerizza', 'scent', 'mervyn', 'lazala', 'reinier', 'combate', 'ian', 'castaneda', 'castillo', 'imelda', 'perado', 'isadel', 'pilarca', 'magcawas', 'ramssel', 'aldwin', 'patiño', 'mayvelle', 'gilbert', 'john', 'jen', 'genesis', 'rosario', 'cabral', 'vargasmaglalang', 'padrinao-villanueva', 'acogido', 'taylo-', 'villanueva', 'silang', 'carmi', 'valencia', 'grace', 'valdz', 'rollie', 'king', 'vienne', 'man-on', 'jayjay', 'treb', 'maricel', 'manlapaz', 'capili', 'cristobal', 'abs-cbn', 'genson', 'salazar', 'lourdes', 'sophia', 'and', 'ver-dee', 'jinky', 'aquino', 'ana', 'lhene', 'ann', 'ram', 'francial', 'dungog-romagos', 'canlapan', 'mararac', 'quilinguing', 'herlene', 'kevin', 'ray', 'poblete', 'sotelo', 'ybanez', 'lamsen', 'maximo', 'mia', 'lim', 'ecalnir', '-', 'oh', 'roehl', 'aisha', 'chiong', 'fajilan', 'rowen', 'arazas', 'jhen', 'fayot', 'emalyn', 'mamhie', 'santiago', 'mariz', 'abella', 'manette', 'alcantara', 'unang', 'hazel', 'maris', 'jeph', 'jazziel', 'kelly', 'caponpon', 'sapo', 'charm', 'villafuerte', 'bh3', 'marie', 'fria', 'maria', 'don', 'besas', 'ofiana', 'flor', 'ylime', 'm', 'paru', 'saguinsin', 'lujera', 'bulan', 'charmaeine', 'brey', 'renier', 'gabaleo', 'ramososhasha', 'daluz', 'arjaybaluyot', 'zacarias', 'ralph', 
    'charles', 'niel', 'jarder', 'troy', 'merin', 'perlas', 'sarenbeniga', 'cabeliza', 'sangalang', 'florentino', 'kale', 'figueroa', 'cyril', 'leigh', 'cherryl', 'jay', 'jabee', 'locsin', 'ayen', 'mitzi', 'tanya', 'aldo', 'botabara', 'alocha', 'jam', 'gideon', 'aby', 'vierneza', 'caroline', 'sieg', 'ruiz', 'rica', 'boris', 'angieline', 'adviento', 'couz', 'jomar', 'criste', 'de', 'dc', 'b', 'cora', 'dy', 'uy', 'kayganda', 'gen', 'rondez', 'alexander', 'buan', 'dianne', 'casabuena', 'joanne', 'emm', 'corvin', 'lala', 'remata', 'charleane', 'felipe', 'jaime', 'roger', 'aris', 'jeosh', 'allito', 'dagtaagta', 'leynes', 'bam', 'jovie', 'khristine', 'rfl', 'carrillo', 'eiram', 'nixx', 'agulto', 'cao', 'buscagan', 'isabel', 'roque', 'ablen', 'leslie', 'rmg', 'ricyet', 'bautista', 'troilus', 'nimfa', 'angie', 'corro', 'caster', 'cheska', 'dexter', 'jennyrose', 'mitch', 'gayjow', 'apol', 'arlyn', 'mamayay', 'verbo', 'rito', 'aranza', 'isha', 'morales', 'marvin', 'zabala', 'palogan', 'jasmin', 'baltar', 'tania', 'dhianne', 'rimas', 'jov', 'domo', 'joy', 'herrera', 'valerie', 'antoniano', 'jr', 'hirit', 'javierariane', 'nikka', 'manalili', 'yba', 'selene', 'news', 'ravela', 'lopez', 'loudine', 'manabat', 'c', 'javier', 'almonguera', 'jm', 'jocelyn', 'edgar', 'vincharl', 'shankanecai', 'soriano', 'tolentino', 'milo', 'jonas', 's', 'com', 'eto', 'con', 'ayeeh', 'oswa', 'mangilit', 'co', 'jeff', 'toni', 'cinth', 'durante', 'cla', 'guzman', 'karen', 'rae', 'esbra', 'kev', 'baccay', 'magbanua', 'sherwin', 'san', 'carpio', 'rrvee', 'kinjan', 'karlo', 'lanymay', 'odey', 'karla', 'elmer', 'teus', 'kasten', 'mark', 'olave', 'raffy', 'mikee', 'yan', 'noel', 'razzie', 'pj', 'quintong', 'zobel', 'mary', 'caloi', 'hernandez', 'roselyn', 'mike', 'cecile', 'dhey', 'chua', 'gemma', 'mahusay', 'dhes', 'andrew', 'gan', 'fritz', 'andrei', 'dote', 'taboadabas', 'mhee', 'quilapio', 'aileen', 'kerstin', 'judee', 'remy', 'deden', 'cepriano', 'calderonukaren', 'castro', 'n', 'dacanay', 'capinpin', 'aldie', 'margie', 'maravilla-casacop', 'vicky', 'jerald', 'drewan', 'archie', 'veronica', 'parugrug', 'bustarde', 'portugal', 'susana', 'cabangon', 'veras', 'shamy', 'yam', 'ii', 'rio', 'oquindo', 'majano', 'perez', 'jingco', 'zandro', 'boom', 'zaldy', 'ayuban', 'ignacio', 'santos', 'guzman-francisco', 'cascabel', 'pau', 'aldana', 'belle', 'edwin', 'macalalad', 'bella', 'leoniño', 'rules', 'ocampo', 'jepher', 'naces', 'claridad', 'miya', 'pam', 'paoner', 'brigente', 'calacday', 'raymond', 'leonie', 'condes', 'talaban', 'kit', 'palabrica', 'cudiamat', 'kim', 'dayan', 'villegas', 'vargas', 'gaspay', 'villa', 'arra', 'albesa', 'blanco', 'meazel', 'antonio', 'portillo', 'jessica', 'toy', 'espiritu', 'llanto', 'jayvee', 'legera', 'denjie', 'burgos', 'alvin', 'bonecille', 'jexter', 'rhoen', 'hervas', 'celzo', 'bes', 'jaul', 'oxford', 'jonard', 'ethel', 'patsy', 'laurel', 'paul', 'montañez', 'riachelle', 'rochelle', 'trins', 'bry', 'rose', 'gma', 
    'gorme', 'tin', 'balubar', 'rubio', 'bobis', 'samuel', 'tuway', 'viansuaverdez', 'ada', 'bagacina', 'yopo', 'panara-ag', 'alcala', 'venzon', 'jake', 'clirkz', 'sunico', 'vanessa', 'granados', 'sabdaniaira', 'cruz', 'recy', 'malubay', 'tolentino-miano', 'alida', 'lanie', 'enriquez', 'mariah', 'margiemel', 'popoy', 'rozend', 'christine', 'verner', 'paradagomez', 'salinas', 'edjen', 'cayabyab', 'arthur', 'gumana', 'rhodora', 'talosig', 'martin', 'ivan', 'mamagat', 'chico', 'love', 'salih', 'dimapilis', 'manaay', 'lazarte', 'macario', 'shen', 'chrissele', 'tulod', 'denice', 'nagal', 'donald', 'francisco', 'rhazel', 'gracia', 'dimaano', 'cebrero', 'bagtas', 'alfaize', 'marzan', 'caredz', 'manahan', 'isagan', 'cavada', 'masaybeng', 'irma', 'rmarie', 'bagos', 'jelka', 'mhendie', 'oblanca', 'cnn', 'anne', 'dizon', 'marit', 'anna', 'arnel', 'mante', 'sarah', 'abanes', 'emms', 'gmax', 'briones', 'bogie', 'reza', 'palisoc', 'marquez', 'rosal', 'oliver', 'pascual', 'yolly', 'ross', 'francis', 'diosa', 'russell', 'shine', 'conrad', 'cerafica', 'justin', 'adzwiya', 'linsangan', 'jay-ar', 'o', 'hilarion', 'wolf', 'kpn', 'tomo', 'segovia', 'maurin', 'hazey', 'dulay', 'reycie', 'carolyn', 'costumbrado', 'obrero', 'miranda', 'catherine', 'retchie', 'gleng', 'yap', 'martinez', 'lacerna', 'paches', 'magbitang', 'mauie', 'diala', 'joyce', 'arvin', 'gomez', 'cajeta', 'joemar', 'jing', 'qadriyyah', 'delos', 'ortiz', 'neser', 'pauline', 'loo', 'ponce', 'imperial', 'joseph', 'daniell', 'shella', 'dioso', 'jayron', 'jane', 'pilares', 'labaco', 'gil', 'dutchque', 'vicente', 'pauyon', 'bobadilla', 'gulmatico', 'vasquez', 'arceta', 'kristian', 'jun', 'mc', 'marge', 'concepcion', 'mercado', 'funda', 'lans', 'pepperminty', 'khim', 'jumawid', 'ladines', 'alvero', 'kiitt', 'erick', 'paires', 'salome', 'angcao', 'maglalang', 'merilyn', 'manuel', 'taguibao', 'madz', 'bermas', 'krizzie', 'molato', 'kathy', 'ae', 'chad', 'ghaneza', 'sarsola', 'russelle', 'draculan', 'al', 'añonuevo', 'au', 'lher', 'aristotle', 'kho', 'abarilla', 'grafil', 'lyn', 'claudine', 'eric', 'fajie', 'ronil', 'tita', 'polangco', 'guarin', 'evilla', 'sumampong', 'quinjacob', 'abigail', 'lendy', 'nick', 'jona', 'feliciano', 'nico', 'oscar', 'rosalita', 'njie', 'rigonan', 'riam', 'garcera', 'tess', 'cyrmyn', 'jestoni', 'cabrera', 'chavez', 'ku', 'iza', 'janella', 'papa', 'acosta', 'medina', 'regalario', 'margaret', 'maureen', 'macallop', 'lacaba', 'abanes-escalona', 'terry', 'sai-rex', 'cabuang', 'valderama', 'urbano', 'jones', 'miles', 'sayson', 'news5', 'geraldine', 'hadap', 'dumalag', 'krystyn', 'aiko', 'elizalde', 'dinia']
    # names = ['camacho']
    new_names = names
    # new_names = get_unique_from_list(names,get_names_list())
    names_to_db = []
    for name in names:
        namesObj = Names(name=name, owner="default")
        names_to_db.append(namesObj)

    # write_concern={'continue_on_error':True} is used so that inserting docs will still continue
    # even when an error occurs. like duplicate values
    try:
        Names.objects.insert(names_to_db, write_concern={'continue_on_error':True})
    except NotUniqueError:
        pass

def get_unique_from_list(old_list, new_list):
    old_list = get_names_list()
    new_list = ['sasa']
    filtered_list = list(set(new_list) - set(old_list))
    return filtered_list



    """ NEGATE """

def get_negates():
    negate_list = []
    for negateObj in Negate.objects(owner="default"):
        negate_list.append(negateObj.word)
    print("Negates LENGTH:", len(negate_list))
    return negate_list

def insert_negates():
    negates = \
    ["aint", "arent", "cannot", "cant", "couldnt", "darent", "didnt", "doesnt",
    "ain't", "aren't", "can't", "couldn't", "daren't", "didn't", "doesn't",
    "dont", "hadnt", "hasnt", "havent", "isnt", "mightnt", "mustnt", "neither",
    "don't", "hadn't", "hasn't", "haven't", "isn't", "mightn't", "mustn't",
    "neednt", "needn't", "never", "none", "nope", "nor", "not", "nothing",
    "nowhere", "oughtnt", "shant", "shouldnt", "uhuh", "wasnt", "werent",
    "oughtn't", "shan't", "shouldn't", "uh-uh", "wasn't", "weren't",
    "without", "wont", "wouldnt", "won't", "wouldn't", "rarely", "seldom",
    "despite", "nobody", "noone", "no"]
    # new_negates = get_unique_from_list(negates,get_negate_list())
    negates_to_db = []
    for negate in negates:
        negatesObj = Negate(word=negate,owner="default")
        negates_to_db.append(negatesObj)

    try:
        Negate.objects.insert(negates_to_db, write_concern={'continue_on_error':True})
        # Names.objects.insert(names_to_db, write_concern={'continue_on_error':True})
    except NotUniqueError:
        pass
    # negate = Negate()
    # negate.negate_list = negate_list 
    # negate.negate_owner = "default"
    # negate.save()

# def insert_negate(negate_list):
#     try:
#         Negate.objects.get(negate_owner="default").update(add_to_set__negate_list=negate_list)
#     except Negate.DoesNotExist:
#         insert_negate_list(negate_list)

# def insert_negate(negate_list):
#     try:
#         Negate.objects.get(negate_owner="default").update(add_to_set__negate_list=negate_list)
#     except Negate.DoesNotExist:
#         insert_negate_list(negate_list)

def insert_idioms():
    SPECIAL_CASE_IDIOMS = \
    {"the shit": 3, "the bomb": 3, "bad ass": 1.5, "yeah right": -2,
    "cut the mustard": 2, "kiss of death": -1.5, "hand to mouth": -2,
    "$ hungry": -3, "money hungry": -3, "dollar hungry": -3, "ok fine": -1,
    "no response": -2, "can't book": -2, "don't book": -3, "give refund": -3,
    "no refund": -2, "@delta next time": 1, "see you @delta": 1,
    "pilot didn't show": -3, "not apologize": -2, "you suck": -3,
    "thank for nothing": -2, "can't check in": -2, "cant check in": -2,
    "website isn't work": -2, "send me expired": -2,
    "pilots haven't arrive": -2, "not well": -1, "not okay": -1,
    "hard time": -1, "thank you": 1, "thank u": 1, "share in metrobank plunged": -1}

    # insert idioms dict into a list, structure will be: [{'key1':1},{'key2':2}]
    # dict_list = convert_dict_to_list(SPECIAL_CASE_IDIOMS, False)

    idioms_dict = SPECIAL_CASE_IDIOMS
    idioms_list = []
    for key, value in idioms_dict.items():
        # emojiObj = Emojis()
        # dict_for_db = {}
        idiomObj = Idioms(word = key, measure = value, owner="default")
        # dict_for_db[dict_keyname] = key
        # dict_for_db[dict_valuename] = value
        idioms_list.append(idiomObj)

    try:
        Idioms.objects.insert(idioms_list, write_concern={'continue_on_error':True})
    except NotUniqueError:
        pass



    # for key, value in SPECIAL_CASE_IDIOMS.items():
    #     idioms_dict = {}
    #     idioms_dict["word"] = key
    #     idioms_dict["measure"] = value
    #     dict_list.append(idioms_dict)


    # idiomsObj = Idioms()
    # idiomsObj.idiom_list = dict_list
    # idiomsObj.idiom_owner = "default"
    # idiomsObj.save()

    # Adding a new field sample
    # Idioms.objects(idiom_owner='default').update(set__idiom_test="yes")

def get_idioms():
    SPECIAL_CASE_IDIOMS = {}
    for idiomsObj in Idioms.objects(owner="default"):
        SPECIAL_CASE_IDIOMS[idiomsObj.word] = idiomsObj.measure
    print("IDIOMS LENGTH:", len(SPECIAL_CASE_IDIOMS))
    return SPECIAL_CASE_IDIOMS

    """ BOOSTERS """

def insert_boosters():
    print("Boosters")
    B_INCR = 0.293
    B_DECR = -0.293

    BOOSTER_DICT = \
    {"absolutely": B_INCR, "amazingly": B_INCR, "awfully": B_INCR,
    "completely": B_INCR, "considerably": B_INCR, "decidedly": B_INCR,
    "deeply": B_INCR, "effing": B_INCR, "enormously": B_INCR,
    "entirely": B_INCR, "especially": B_INCR, "exceptionally": B_INCR,
    "extremely": B_INCR, "fabulously": B_INCR, "flipping": B_INCR,
    "flippin": B_INCR, "fricking": B_INCR, "frickin": B_INCR,
    "frigging": B_INCR, "friggin": B_INCR, "fully": B_INCR, "fucking": B_INCR,
    "greatly": B_INCR, "hella": B_INCR, "highly": B_INCR, "hugely": B_INCR,
    "incredibly": B_INCR, "intensely": B_INCR, "majorly": B_INCR, "more": B_INCR,
    "most": B_INCR, "particularly": B_INCR, "purely": B_INCR, "quite": B_INCR,
    "really": B_INCR, "remarkably": B_INCR, "so": B_INCR, "substantially": B_INCR,
    "thoroughly": B_INCR, "totally": B_INCR, "tremendously": B_INCR,
    "uber": B_INCR, "unbelievably": B_INCR, "unusually": B_INCR,
    "utterly": B_INCR, "very": B_INCR, "super": B_INCR, "almost": B_DECR,
    "barely": B_DECR, "hardly": B_DECR, "just enough": B_DECR, "kind of": B_DECR,
    "kinda": B_DECR, "kindof": B_DECR, "kind-of": B_DECR, "less": B_DECR,
    "little": B_DECR, "marginally": B_DECR, "occasionally": B_DECR,
    "partly": B_DECR, "scarcely": B_DECR, "slightly": B_DECR, "somewhat": B_DECR,
    "sort of": B_DECR, "sorta": B_DECR, "sortof": B_DECR, "sort-of": B_DECR}


    # dict_list = convert_dict_to_list(BOOSTER_DICT, False)

    # dict_list = []
    # for key, value in BOOSTER_DICT.items():
    #     booster_dict = {}
    #     booster_dict["word"] = key
    #     booster_dict["measure"] = value
    #     dict_list.append(booster_dict)

    # boosterObj = Boosters()
    # boosterObj.booster_list = dict_list
    # boosterObj.owner = "default"
    # boosterObj.save()

    booster_list = []
    for key, value in BOOSTER_DICT.items():
        # emojiObj = Emojis()
        # dict_for_db = {}
        boosterObj = Boosters(word = key, measure = value, owner="default")
        # dict_for_db[dict_keyname] = key
        # dict_for_db[dict_valuename] = value
        booster_list.append(boosterObj)

    try:
        Boosters.objects.insert(booster_list, write_concern={'continue_on_error':True})
    except NotUniqueError:
        pass

def get_boosters():
    BOOSTER_DICT = {}
    # booster_list = []
    for boosterObj in Boosters.objects(owner="default"):
        BOOSTER_DICT[boosterObj.word] = boosterObj.measure
        # booster_list = boosters.booster_list
    # for x in booster_list:
        # BOOSTER_DICT[x['word']] = x['measure']
    print("Booster LENGTH:", len(BOOSTER_DICT))
    return BOOSTER_DICT

    """ BASE FORMS """

def insert_baseforms(base_forms):
    print("BASE_FORMS")
    # base_forms = {}
    # base_forms = {'asker':'4','aski':'askar','ask':'leava'}

    # bf = BaseForms.objects(id='5b801eab55d14c13a8492c55').update(set__verbs=base_forms)

    # dict_list = convert_dict_to_list(base_forms, True)
    # bf = BaseForms()
    # bf.baseform_list = dict_list
    # bf.baseform_owner = "default"
    # bf.save()


    # bf.verbs = base_forms
    # bf.owner = 'default'
    # bf.save()



    

    # BaseForms(baseform_list=[BaseFormWord(word="Nurem",baseform="Nurema"),
    # BaseFormWord(word="Nuremi",baseform="Nuremi")]).save()

    # bf.baseform_owner = "default"
    # bf.save()
    # dict_list = convert_dict_to_list(base_forms, True)
    # BaseForms.objects(baseform_owner="test").update(add_to_set__baseform_list=dict_list)

    # p = BaseForms.objects(baseform_owner="default",baseform_list="ask").count()
    # print(p)

    # baseformsObj = BaseForms()
    # baseformsObj.baseform_list = dict_list
    # baseformsObj.baseform_owner = "default"
    # baseformsObj.save()

    baseform_list = []
    for key, value in base_forms.items():
        baseformObj = BaseForms(word = key, baseform = value, owner="default")
        baseform_list.append(baseformObj)

    try:
        BaseForms.objects.insert(baseform_list, write_concern={'continue_on_error':True})
    except NotUniqueError:
        pass

def get_baseforms():
    BASEFORM_DICT = {}
    for baseformObj in BaseForms.objects(owner="default"):
        BASEFORM_DICT[baseformObj.word] = baseformObj.baseform
    print("BS LENGTH:", len(BASEFORM_DICT))
    return BASEFORM_DICT

def update_baseforms():
    q = BaseForms.objects(owner="test",baseform_list__match={"word":"ask", "baseform":"nurema"})
    q.update(set__baseform_list__S__baseform="nurems")
    # print(q._query)

    """ LEXICONS """

def get_lexicons():
    LEXICON_DICT = {}
    for lexiconObj in Lexicons.objects(owner="default"):
        LEXICON_DICT[lexiconObj.word] = lexiconObj.measure
    print("LEXICON LENGTH:", len(LEXICON_DICT))
    return LEXICON_DICT

def insert_lexicon(lex_dict):
    # print("lexi here")
    # dict_list = convert_dict_to_list(lex_dict, False)
    # lexicon = Lexicons()
    # lexicon.lexicon_list = dict_list
    # lexicon.lexicon_owner = "default"
    # lexicon.save()    

    lexicon_list = []
    for key, value in lex_dict.items():
        # emojiObj = Emojis()
        # dict_for_db = {}
        lexiconObj = Lexicons(word = key, measure = value, owner="default")
        # dict_for_db[dict_keyname] = key
        # dict_for_db[dict_valuename] = value
        lexicon_list.append(lexiconObj)

    try:
        Lexicons.objects.insert(lexicon_list, write_concern={'continue_on_error':True})
    except NotUniqueError:
        pass

def update_individual_lexicon(lexicon_dict):
    Lexicons.objects(owner="test",lexicon_list__match={"word":"ask", "baseform":"nurema"})


def insert_emojis():
    emoji_dict = {
u'\U0001f600': ' emjaaa ',
u'\U0001f601': ' emjaab ',
u'\U0001f602': ' emjaac ',
u'\U0001f603': ' emjaad ',
u'\U0001f604': ' emjaae ',
u'\U0001f605': ' emjaaf ',
u'\U0001f606': ' emjaag ',
u'\U0001f609': ' emjaah ',
u'\U0001f60a': ' emjaai ',
u'\U0001f60b': ' emjaaj ',
u'\U0001f60e': ' emjaak ',
u'\U0001f60d': ' emjaal ',
u'\U0001f618': ' emjaam ',
u'\U0001f617': ' emjaan ',
u'\U0001f619': ' emjaao ',
u'\U0001f61a': ' emjaap ',
u'\u263a': ' emjaaq ',
u'\U0001f642': ' emjaar ',
u'\U0001f917': ' emjaas ',
u'\U0001f607': ' emjaat ',
u'\U0001f913': ' emjaau ',
u'\U0001f611': ' emjaav ',
u'\U0001f60f': ' emjaaw ',
u'\U0001f623': ' emjaax ',
u'\U0001f625': ' emjaay ',
u'\U0001f62b': ' emjaaz ',
u'\U0001f60c': ' emjaba ',
u'\U0001f61b': ' emjabb ',
u'\U0001f61c': ' emjabc ',
u'\U0001f61d': ' emjabd ',
u'\U0001f612': ' emjabe ',
u'\U0001f613': ' emjabf ',
u'\U0001f614': ' emjabg ',
u'\U0001f615': ' emjabh ',
u'\U0001f637': ' emjabi ',
u'\U0001f912': ' emjabj ',
u'\U0001f915': ' emjabk ',
u'\u2639': ' emjabl ',
u'\U0001f641': ' emjabm ',
u'\U0001f616': ' emjabn ',
u'\U0001f61e': ' emjabo ',
u'\U0001f61f': ' emjabp ',
u'\U0001f624': ' emjabq ',
u'\U0001f622': ' emjabr ',
u'\U0001f62d': ' emjabs ',
u'\U0001f626': ' emjabt ',
u'\U0001f627': ' emjabu ',
u'\U0001f628': ' emjabv ',
u'\U0001f629': ' emjabw ',
u'\U0001f62c': ' emjabx ',
u'\U0001f630': ' emjaby ',
u'\U0001f631': ' emjabz ',
u'\U0001f633': ' emjaca ',
u'\U0001f635': ' emjacb ',
u'\U0001f621': ' emjacc ',
u'\U0001f620': ' emjacd ',
u'\U0001f608': ' emjace ',
u'\U0001f47f': ' emjacf ',
u'\U0001f479': ' emjacg ',
u'\U0001f47a': ' emjach ',
u'\U0001f480': ' emjaci ',
u'\u2620': ' emjacj ',
u'\U0001f4a9': ' emjack ',
u'\U0001f63a': ' emjacl ',
u'\U0001f638': ' emjacm ',
u'\U0001f639': ' emjacn ',
u'\U0001f63b': ' emjaco ',
u'\U0001f63c': ' emjacp ',
u'\U0001f63d': ' emjacq ',
u'\U0001f640': ' emjacr ',
u'\U0001f63f': ' emjacs ',
u'\U0001f63e': ' emjact ',
u'\U0001f47c': ' emjacu ',
u'\U0001f486': ' emjacv ',
u'\U0001f64d': ' emjacw ',
u'\U0001f646': ' emjacx ',
u'\U0001f64c': ' emjacy ',
u'\U0001f64f': ' emjacz ',
u'\U0001f491': ' emjada ',
u'\U0001f4aa': ' emjadb ',
u'\u261d': ' emjadc ',
u'\U0001f595': ' emjadd ',
u'\u270c': ' emjade ',
u'\U0001f918': ' emjadf ',
u'\U0001f44c': ' emjadg ',
u'\U0001f44d': ' emjadh ',
u'\U0001f44e': ' emjadi ',
u'\U0001f44a': ' emjadj ',
u'\U0001f44f': ' emjadk ',
u'\U0001f48b': ' emjadl ',
u'\U0001f498': ' emjadm ',
u'\u2764': ' emjadn ',
u'\U0001f493': ' emjado ',
u'\U0001f494': ' emjadp ',
u'\U0001f495': ' emjadq ',
u'\U0001f496': ' emjadr ',
u'\U0001f497': ' emjads ',
u'\U0001f499': ' emjadt ',
u'\U0001f49a': ' emjadu ',
u'\U0001f49b': ' emjadv ',
u'\U0001f49c': ' emjadw ',
u'\U0001f49d': ' emjadx ',
u'\U0001f49e': ' emjady ',
u'\U0001f49f': ' emjadz ',
u'\U0001f451': ' emjaea ',
u'\U0001f335': ' emjaeb ',
u'\U0001f389': ' emjaec ',
u'\U0001f38a': ' emjaed '
}
    print("Inserting emojis")
    # dict_list = convert_dict_to_list(emoji_dict, False)

    emoji_list = []
    for key, value in emoji_dict.items():
        emojiObj = Emojis(word = key, measure = value, owner="default")
        # dict_for_db[dict_keyname] = key
        # dict_for_db[dict_valuename] = value
        emoji_list.append(emojiObj)

    try:
        Emojis.objects.insert(emoji_list, write_concern={'continue_on_error':True})
    except NotUniqueError:
        pass

    # emoji = Emojis()
    # emoji.emoji_list = dict_list
    # emoji.emoji_owner = "default"
    # emoji.save()

def get_emojis():
    EMOJI_DICT = {}
    for emojiObj in Emojis.objects(owner="default"):
        EMOJI_DICT[emojiObj.word] = emojiObj.measure
    print("EMOJI LENGTH:", len(EMOJI_DICT))
    return EMOJI_DICT

def convert_dict_to_list(dictionary, isverbs):
    dict_list = []
    dict_keyname = "word"
    dict_valuename = "measure"
    if isverbs:
        dict_valuename = "baseform"
    # converts {'word':'measure'} into {'word':"literalword",'measure':30}
    for key, value in dictionary.items():
        print(type(value))
        dict_for_db = {}
        dict_for_db[dict_keyname] = key
        dict_for_db[dict_valuename] = value
        dict_list.append(dict_for_db)
    return dict_list
