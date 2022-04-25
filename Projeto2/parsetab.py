
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'Chars Comment END Error Id Ignore Index Info Left Literals Precedence Python Regex Return Right Section Tokens Tvalue Value\n\tply : commentary\n\t\t| section\n\t\t| atribution\n\t\t| atribution commentary\n\t\t| lex\n\t\t| lex commentary\n\t\t| yacc\n\t\t| yacc commentary\n\t\t| python\n\t\t|\n\t\n\tcommentary : Comment Info END\n\t\n\tsection : Section END\n\t\n\tatribution : Id \'=\' exp\n\t\t\t   | Id \'=\' Chars\n\t\t\t   | Id \'=\' list\n\t\t\t   | Id \'=\' dic\n\t\t\t   | Index \'=\' exp\n\t\t\t   | Index \'=\' Chars\n\t\t\t   | Index \'=\' list\n\t\t\t   | Index \'=\' dic\n\t\t\t   | Index \'=\' Index\n\t\n\texp : Value\n\t\t| exp \'+\' Value\n\t\t| exp \'-\' Value\n\t\t| exp \'/\' Value\n\t\t| exp \'*\' Value\n\t\t| \'-\' Value\n\t\n\tlex : regex\n\t\t| reservedWordsLex\n\t\t| erro\n\t\n\tregex : Regex Return regexTuple\n\t\n\treservedWordsLex : Tokens \'=\' list \n\t\t\t\t     | Literals \'=\' list\n\t\t\t\t     | Literals \'=\' Chars \n\t\t\t\t     | Ignore \'=\' Chars\n\t\n\terro : \'.\' reservedFunctions\n\t\n\treservedFunctions : Error Info END\n\n\t\n\tyacc : reservedWordsYacc\n\t\t | productions\n\t\n\treservedWordsYacc : Precedence \'=\' listOfTuples\n\t\n\tproductions : Id \':\' production Info\n\t\t\t\t| Id \':\' production\n\t\n\tpython : Python\n\t\t   | Info\n\t\n\tlist : \'[\' Empty \']\'\n\t\t | \'[\' elems \']\'\n\t\n\tlistOfTuples : \'[\' precs \']\'\n\t\n\tprecs : \'(\' tupleforPrec \')\'\n\t\t  | precs \',\' \'(\' tupleforPrec \')\'\n\t\n\ttupleforPrec : "\'" Left "\'" \',\' elems\n\t\t  \t     | "\'" Right "\'"  \',\' elems\n\t\n\tregexTuple : "(" "\'" Id "\'" "," Tvalue ")"\n\t\n\tdic : \'{\' Empty \'}\'\n\t\t| \'{\' conj \'}\'\n\t\n\tconj : Value \':\' Value\n\t\t | Chars \':\' Chars\n\t\t | Value \':\' Chars\n\t\t | Chars \':\' Value\n\t\t | conj \',\' Value \':\' Value\n\t\t | conj \',\' Chars \':\' Chars\n\t\t | conj \',\' Value \':\' Chars\n\t\t | conj \',\' Chars \':\' Value\n\t\n\tproduction : \'<\' items \'>\' \n\t\n\titems : Id\n\t\t  | items Id\n\t\n\titems : Chars\n\t\t  | items Chars\n\t\n\telems : "\'" Id "\'"\n\t\t  | elems \',\' "\'" Id "\'"\n\t\n\telems : Chars\n\t\t  | elems \',\' Chars\n\t\n\tEmpty :\n\t'
    
_lr_action_items = {'$end':([0,1,2,3,4,5,6,7,9,13,14,15,16,17,18,25,26,27,29,37,40,41,42,43,44,45,49,51,52,53,54,55,56,58,59,60,61,63,69,78,83,86,87,88,89,90,91,94,95,99,103,137,],[-10,0,-1,-2,-3,-5,-7,-9,-44,-28,-29,-30,-38,-39,-43,-4,-6,-8,-12,-36,-11,-13,-14,-15,-16,-22,-42,-21,-17,-18,-19,-20,-31,-32,-33,-34,-35,-40,-27,-41,-37,-23,-24,-25,-26,-45,-46,-53,-54,-63,-47,-52,]),'Comment':([0,4,5,6,13,14,15,16,17,37,41,42,43,44,45,49,51,52,53,54,55,56,58,59,60,61,63,69,78,83,86,87,88,89,90,91,94,95,99,103,137,],[8,8,8,8,-28,-29,-30,-38,-39,-36,-13,-14,-15,-16,-22,-42,-21,-17,-18,-19,-20,-31,-32,-33,-34,-35,-40,-27,-41,-37,-23,-24,-25,-26,-45,-46,-53,-54,-63,-47,-52,]),'Section':([0,],[10,]),'Id':([0,50,72,79,80,81,82,100,101,107,],[11,80,93,100,-64,-66,102,-65,-67,121,]),'Index':([0,32,],[12,51,]),'Python':([0,],[18,]),'Info':([0,8,38,49,99,],[9,28,62,78,-63,]),'Regex':([0,],[19,]),'Tokens':([0,],[20,]),'Literals':([0,],[21,]),'Ignore':([0,],[22,]),'.':([0,],[23,]),'Precedence':([0,],[24,]),'END':([10,28,62,],[29,40,83,]),'=':([11,12,20,21,22,24,],[30,32,34,35,36,39,]),':':([11,76,77,110,111,],[31,97,98,122,123,]),'Return':([19,],[33,]),'Error':([23,],[38,]),'Chars':([30,32,35,36,47,48,50,79,80,81,92,96,97,98,100,101,122,123,135,136,],[42,53,60,61,73,77,81,101,-64,-66,108,111,113,114,-65,-67,130,131,73,73,]),'Value':([30,32,46,48,65,66,67,68,96,97,98,122,123,],[45,45,69,76,86,87,88,89,110,112,115,129,132,]),'-':([30,32,41,45,52,69,86,87,88,89,],[46,46,66,-22,66,-27,-23,-24,-25,-26,]),'[':([30,32,34,35,39,],[47,47,47,47,64,]),'{':([30,32,],[48,48,]),'<':([31,],[50,]),'(':([33,64,104,],[57,85,117,]),'+':([41,45,52,69,86,87,88,89,],[65,-22,65,-27,-23,-24,-25,-26,]),'/':([41,45,52,69,86,87,88,89,],[67,-22,67,-27,-23,-24,-25,-26,]),'*':([41,45,52,69,86,87,88,89,],[68,-22,68,-27,-23,-24,-25,-26,]),']':([47,70,71,73,84,108,109,118,128,134,],[-72,90,91,-70,103,-71,-68,-48,-69,-49,]),"'":([47,57,85,92,93,102,117,119,120,121,135,136,],[72,82,106,107,109,116,106,126,127,128,72,72,]),'}':([48,74,75,112,113,114,115,129,130,131,132,],[-72,94,95,-55,-57,-56,-58,-59,-61,-60,-62,]),',':([71,73,75,84,108,109,112,113,114,115,116,118,126,127,128,129,130,131,132,134,138,139,],[92,-70,96,104,-71,-68,-55,-57,-56,-58,124,-48,135,136,-69,-59,-61,-60,-62,-49,92,92,]),')':([73,105,108,109,125,128,133,138,139,],[-70,118,-71,-68,134,-69,137,-50,-51,]),'>':([79,80,81,100,101,],[99,-64,-66,-65,-67,]),'Left':([106,],[119,]),'Right':([106,],[120,]),'Tvalue':([124,],[133,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'ply':([0,],[1,]),'commentary':([0,4,5,6,],[2,25,26,27,]),'section':([0,],[3,]),'atribution':([0,],[4,]),'lex':([0,],[5,]),'yacc':([0,],[6,]),'python':([0,],[7,]),'regex':([0,],[13,]),'reservedWordsLex':([0,],[14,]),'erro':([0,],[15,]),'reservedWordsYacc':([0,],[16,]),'productions':([0,],[17,]),'reservedFunctions':([23,],[37,]),'exp':([30,32,],[41,52,]),'list':([30,32,34,35,],[43,54,58,59,]),'dic':([30,32,],[44,55,]),'production':([31,],[49,]),'regexTuple':([33,],[56,]),'listOfTuples':([39,],[63,]),'Empty':([47,48,],[70,74,]),'elems':([47,135,136,],[71,138,139,]),'conj':([48,],[75,]),'items':([50,],[79,]),'precs':([64,],[84,]),'tupleforPrec':([85,117,],[105,125,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> ply","S'",1,None,None,None),
  ('ply -> commentary','ply',1,'p_ply','teste2.py',269),
  ('ply -> section','ply',1,'p_ply','teste2.py',270),
  ('ply -> atribution','ply',1,'p_ply','teste2.py',271),
  ('ply -> atribution commentary','ply',2,'p_ply','teste2.py',272),
  ('ply -> lex','ply',1,'p_ply','teste2.py',273),
  ('ply -> lex commentary','ply',2,'p_ply','teste2.py',274),
  ('ply -> yacc','ply',1,'p_ply','teste2.py',275),
  ('ply -> yacc commentary','ply',2,'p_ply','teste2.py',276),
  ('ply -> python','ply',1,'p_ply','teste2.py',277),
  ('ply -> <empty>','ply',0,'p_ply','teste2.py',278),
  ('commentary -> Comment Info END','commentary',3,'p_commentary','teste2.py',305),
  ('section -> Section END','section',2,'p_section','teste2.py',312),
  ('atribution -> Id = exp','atribution',3,'p_atribution','teste2.py',322),
  ('atribution -> Id = Chars','atribution',3,'p_atribution','teste2.py',323),
  ('atribution -> Id = list','atribution',3,'p_atribution','teste2.py',324),
  ('atribution -> Id = dic','atribution',3,'p_atribution','teste2.py',325),
  ('atribution -> Index = exp','atribution',3,'p_atribution','teste2.py',326),
  ('atribution -> Index = Chars','atribution',3,'p_atribution','teste2.py',327),
  ('atribution -> Index = list','atribution',3,'p_atribution','teste2.py',328),
  ('atribution -> Index = dic','atribution',3,'p_atribution','teste2.py',329),
  ('atribution -> Index = Index','atribution',3,'p_atribution','teste2.py',330),
  ('exp -> Value','exp',1,'p_exp','teste2.py',337),
  ('exp -> exp + Value','exp',3,'p_exp','teste2.py',338),
  ('exp -> exp - Value','exp',3,'p_exp','teste2.py',339),
  ('exp -> exp / Value','exp',3,'p_exp','teste2.py',340),
  ('exp -> exp * Value','exp',3,'p_exp','teste2.py',341),
  ('exp -> - Value','exp',2,'p_exp','teste2.py',342),
  ('lex -> regex','lex',1,'p_lex','teste2.py',361),
  ('lex -> reservedWordsLex','lex',1,'p_lex','teste2.py',362),
  ('lex -> erro','lex',1,'p_lex','teste2.py',363),
  ('regex -> Regex Return regexTuple','regex',3,'p_regex','teste2.py',370),
  ('reservedWordsLex -> Tokens = list','reservedWordsLex',3,'p_reservedWords','teste2.py',380),
  ('reservedWordsLex -> Literals = list','reservedWordsLex',3,'p_reservedWords','teste2.py',381),
  ('reservedWordsLex -> Literals = Chars','reservedWordsLex',3,'p_reservedWords','teste2.py',382),
  ('reservedWordsLex -> Ignore = Chars','reservedWordsLex',3,'p_reservedWords','teste2.py',383),
  ('erro -> . reservedFunctions','erro',2,'p_erro','teste2.py',420),
  ('reservedFunctions -> Error Info END','reservedFunctions',3,'p_reservedFunctions','teste2.py',427),
  ('yacc -> reservedWordsYacc','yacc',1,'p_yacc','teste2.py',439),
  ('yacc -> productions','yacc',1,'p_yacc','teste2.py',440),
  ('reservedWordsYacc -> Precedence = listOfTuples','reservedWordsYacc',3,'p_reservedWordsYacc','teste2.py',447),
  ('productions -> Id : production Info','productions',4,'p_productions','teste2.py',454),
  ('productions -> Id : production','productions',3,'p_productions','teste2.py',455),
  ('python -> Python','python',1,'p_Pyhton','teste2.py',473),
  ('python -> Info','python',1,'p_Pyhton','teste2.py',474),
  ('list -> [ Empty ]','list',3,'p_list','teste2.py',487),
  ('list -> [ elems ]','list',3,'p_list','teste2.py',488),
  ('listOfTuples -> [ precs ]','listOfTuples',3,'p_listOfTuples','teste2.py',497),
  ('precs -> ( tupleforPrec )','precs',3,'p_precs','teste2.py',504),
  ('precs -> precs , ( tupleforPrec )','precs',5,'p_precs','teste2.py',505),
  ("tupleforPrec -> ' Left ' , elems",'tupleforPrec',5,'p_tupleforPrec','teste2.py',516),
  ("tupleforPrec -> ' Right ' , elems",'tupleforPrec',5,'p_tupleforPrec','teste2.py',517),
  ("regexTuple -> ( ' Id ' , Tvalue )",'regexTuple',7,'p_regexTuple','teste2.py',526),
  ('dic -> { Empty }','dic',3,'p_dic','teste2.py',539),
  ('dic -> { conj }','dic',3,'p_dic','teste2.py',540),
  ('conj -> Value : Value','conj',3,'p_conj','teste2.py',547),
  ('conj -> Chars : Chars','conj',3,'p_conj','teste2.py',548),
  ('conj -> Value : Chars','conj',3,'p_conj','teste2.py',549),
  ('conj -> Chars : Value','conj',3,'p_conj','teste2.py',550),
  ('conj -> conj , Value : Value','conj',5,'p_conj','teste2.py',551),
  ('conj -> conj , Chars : Chars','conj',5,'p_conj','teste2.py',552),
  ('conj -> conj , Value : Chars','conj',5,'p_conj','teste2.py',553),
  ('conj -> conj , Chars : Value','conj',5,'p_conj','teste2.py',554),
  ('production -> < items >','production',3,'p_production','teste2.py',562),
  ('items -> Id','items',1,'p_items_id','teste2.py',569),
  ('items -> items Id','items',2,'p_items_id','teste2.py',570),
  ('items -> Chars','items',1,'p_items_chars','teste2.py',581),
  ('items -> items Chars','items',2,'p_items_chars','teste2.py',582),
  ("elems -> ' Id '",'elems',3,'p_elems_id','teste2.py',596),
  ("elems -> elems , ' Id '",'elems',5,'p_elems_id','teste2.py',597),
  ('elems -> Chars','elems',1,'p_elems_chars','teste2.py',609),
  ('elems -> elems , Chars','elems',3,'p_elems_chars','teste2.py',610),
  ('Empty -> <empty>','Empty',0,'p_Empty','teste2.py',621),
]