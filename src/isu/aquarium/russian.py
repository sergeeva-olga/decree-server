# encoding: utf-8
# Технический русский
import types
import re

casemap = {
    "и": "N",
    "р": "G",
    "д": "D",
    "в": "A",
    "т": "T",
    "п": "P",
    "И": "N",
    "Р": "G",
    "Д": "D",
    "В": "A",
    "Т": "T",
    "П": "P",
    "N": "N",
    "G": "G",
    "D": "D",
    "A": "A",
    "T": "T",
    "P": "P",
}

N = "N"
G = "G"
D = "D"
A = "A"
T = "T"
P = "P"
F = 'F'
M = 'M'

FN = 'FamilyName'
Name = 'FirstName'
SN = 'SecondName'

# somekind of default case
kind2th = {N: "_", G: "а", D: "_", A: "а",
           T: "ем", P: "е"}  # 2-th case of cases

endings = (
    ("ева",
        {N: "_", G: "евой", D: "евой", A: "еву", T: "евой", P: "евой"},
     (F, FN)),
    # last is (Gender, NamePart), if it cannot be deterined FOR SHURE
    # None (Undefined) is used.
    ("Шота",  {N: "_", G: "Шоты",  D: "Шоте",  A: "Шоту", T: "Шотой", P: "Шоте"},
        (M, Name)),
    ("ова", {N: "_", G: "овой", D: "овой", A: "ову", T: "овой", P: "овой"},
        (F, FN)),
    ("оглы", {N: "_", G: "_", D: "_", A: "_", T: "_", P: "_"},
        (M, SN)),
    ("кызы", {N: "_", G: "_", D: "_", A: "_", T: "_", P: "_"},
        (M, SN)),
    ("евич", {N: "_", G: "евича", D: "евичу", A: "евича", T: "евичем", P: "евиче"},
        (M, SN)),
    ("ович", {N: "_", G: "овича", D: "овичу", A: "овича", T: "овичем", P: "овиче"},
        (M, SN)),
    ("кий",  {N: "_", G: "кого",  D: "кому",  A: "кого", T: "ким", P: "ком"},
        (M, FN)),
    ("ная",  {N: "_", G: "ной",  D: "ной",  A: "ной", T: "ной", P: "ной"},
        (F, FN)),
    ("цкая",  {N: "_", G: "цкой",  D: "цкой",  A: "цкую", T: "цкой", P: "цкой"},
        (F, FN)),
    ("ская",  {N: "_", G: "ской",  D: "ской",  A: "скую", T: "ской", P: "ской"},
        (F, FN)),
    ("ющий",  {N: "_", G: "ющего",  D: "ющему",  A: "ющего", T: "ющим", P: "ющем"},
        (None, None)),
    ("ющая",  {N: "_", G: "ющей",  D: "ющей",  A: "ющей", T: "ющей", P: "ющей"},
        (None, None)),
    ("кая",  {N: "_", G: "кой",  D: "кой",  A: "кой", T: "кой", P: "кой"},
        (F, FN)),
    ("чая",  {N: "_", G: "чей",  D: "чей",  A: "чей", T: "чей", P: "чей"},
        (F, FN)),
    ("Илья",  {N: "_", G: "Ильи",  D: "Илье",  A: "Илью",  T: "Ильей", P: "Илье"},
        (F, FN)),
    ("бек",  {N: "_", G: "_а",  D: "_у",  A: "_а",  T: "_ом", P: "_е"},
        (None, None)),
    ("лод",  {N: "_", G: "_а",  D: "_у",  A: "_а",  T: "_ом", P: "_е"},
        (None, None)),
    ("лья",  {N: "_", G: "льи",  D: "льи",  A: "лью",  T: "льей", P: "льи"},
        (None, None)),
    ("лия",  {N: "_", G: "лии",  D: "лии",  A: "лию",  T: "лией", P: "лии"},
        (None, None)),
    ("ерт",  {N: "_", G: "_а",  D: "_у",  A: "_а",  T: "_ом", P: "_е"},
        (None, None)),
    ("ами",  {N: "_", G: "_",  D: "_",  A: "_",  T: "_", P: "_"},
        (None, None)),
    ("али",  {N: "_", G: "_",  D: "_",  A: "_",  T: "_", P: "_"},
        (None, None)),
    ("ия",  {N: "_", G: "ии",  D: "ии",  A: "ию", T: "ией", P: "ии"},
        (F, Name)),
    ("Ия",  {N: "_", G: "Ии",  D: "Ие",  A: "Ию", T: "Ией", P: "Ие"},
        (F, Name)),
    ("ие",  {N: "_", G: "ия",  D: "ию",  A: "ие", T: "ием", P: "ии"},
        (None, None)),
    ("ий",  {N: "_", G: "ия",  D: "ию",  A: "ия", T: "ием", P: "ии"},
        (M, Name)),
    ("ый",  {N: "_", G: "ого",  D: "ому",  A: "ого", T: "ым", P: "ом"},
        (M, Name)),
    ("ай",  {N: "_", G: "ая",  D: "аю",  A: "ая", T: "аем", P: "ае"},
        (M, Name)),
    ("ей",  {N: "_", G: "ея",  D: "ею",  A: "ея", T: "еем",  P: "ее"},
        (M, Name)),
    ("ов",  {N: "_", G: "_а",  D: "_у",  A: "_а", T: "_ым", P: "_е"},
        (M, FN)),
    ("ав",  {N: "_", G: "_а",  D: "_у",  A: "_а", T: "_ом", P: "_е"},
        (M, FN)),
    ("ат",  {N: "_", G: "_а",  D: "_у",  A: "_а", T: "_ом", P: "_е"},
        (M, FN)),
    ("ах",  {N: "_", G: "_а",  D: "_у",  A: "_а", T: "_ом", P: "_е"},
        (M, FN)),
    #("лев",  {N:"_", G:"льва",  D:"льву",  A:"льва", T:"львом", P:"льве"},
    #    (M,FN)),
    ("Лев",  {N: "_", G: "Льва",  D: "Льву",  A: "Льва", T: "Львом", P: "Льве"},
        (M, FN)),
    ("ев",  {N: "_", G: "_а",  D: "_у",  A: "_а", T: "_ым", P: "_е"},
        (M, FN)),
    ("еб",  {N: "_", G: "_а",  D: "_у",  A: "_а", T: "_ом", P: "_е"},
        (M, FN)),    ("ец",  {N: "_", G: "_",  D: "_",  A: "_", T: "_", P: "_"},
                      (M, FN)),
    ("ёв",  {N: "_", G: "_а",  D: "_у",  A: "_а", T: "_ым", P: "_е"},
        (M, FN)),
    ("ён",  {N: "_", G: "_а",  D: "_у",  A: "_а", T: "_ом", P: "_е"},
        (M, FN)),
    ("ен",  {N: "_", G: "_а",  D: "_у",  A: "_а", T: "_ом", P: "_е"},
        (M, FN)),
    ("ус",  {N: "_", G: "_а",  D: "_у",  A: "_а", T: "_ом", P: "_е"},
        (None, None)),
    ("утин",  {N: "_", G: "_а",  D: "_у",  A: "_а", T: "_ым", P: "_е"},
        (M, None)),
    ("етин",  {N: "_", G: "_а",  D: "_у",  A: "_а", T: "_ым", P: "_е"},
        (M, None)),
    ("отин",  {N: "_", G: "_а",  D: "_у",  A: "_а", T: "_ым", P: "_е"},
        (M, FN)),
    ("тин",  {N: "_", G: "_а",  D: "_у",  A: "_а", T: "_ом", P: "_е"},
        (M, None)),
    ("ин",  {N: "_", G: "_а",  D: "_у",  A: "_а", T: "_ым", P: "_е"},
        (M, None)),
    ("им",  {N: "_", G: "_а",  D: "_у",  A: "_а", T: "_ом", P: "_е"},
        (M, None)),
    ("иф",  {N: "_", G: "_а",  D: "_у",  A: "_а", T: "_ом", P: "_е"},
        (M, None)),
    ("ит",  {N: "_", G: "_а",  D: "_у",  A: "_а", T: "_ом", P: "_е"},
        (M, None)),
    ("ук",  {N: "_", G: "_а",  D: "_у",  A: "_а", T: "_ом", P: "_е"},
        (M, None)),
    ("ём",  {N: "_", G: "_а",  D: "_у",  A: "_а", T: "_ом", P: "_е"},
        (M, None)),
    ("ем",  {N: "_", G: "_а",  D: "_у",  A: "_а", T: "_ом", P: "_е"},
        (M, None)),
    ("ын",  {N: "_", G: "_а",  D: "_у",  A: "_а", T: "_ым", P: "_е"},
        (M, Name)),
    ("ис",  {N: "_", G: "_а",  D: "_у",  A: "_а", T: "_ом", P: "_е"},
        (M, None)),
    ("ипп",  {N: "_", G: "_а",  D: "_у",  A: "_а", T: "_ом", P: "_е"},
        (M, None)),
    ("ид",  {N: "_", G: "_а",  D: "_у",  A: "_а", T: "_ом", P: "_е"},
        (M, None)),
    ("ик",  {N: "_", G: "_а",  D: "_у",  A: "_а", T: "_ом", P: "_е"},
        (M, None)),
    ("ел",  {N: "_", G: "ла",  D: "лу",  A: "ла", T: "лом", P: "ле"},
        (M, None)),
    ("илл",  {N: "_", G: "илла",  D: "иллу",  A: "илла", T: "иллом", P: "илле"},
        (M, None)),
    ("ил",  {N: "_", G: "ила",  D: "илу",  A: "ила", T: "илом", P: "иле"},
        (M, None)),
    ("ан",  {N: "_", G: "_а",  D: "_у",  A: "_а", T: "_ом", P: "_е"},
        (M, Name)),
    ("сад",  {N: "_", G: "_а",  D: "_у",  A: "_а", T: "_ом", P: "_е"},
        (M, Name)),
    ("ян",  {N: "_", G: "_а",  D: "_у",  A: "_а", T: "_ом", P: "_е"},
        (M, Name)),
    ("Ян",  {N: "_", G: "_а",  D: "_у",  A: "_а", T: "_ом", P: "_е"},
        (M, Name)),
    ("он",  {N: "_", G: "_а",  D: "_у",  A: "_а", T: "_ом", P: "_е"},
        (M, Name)),
    ("ам",  {N: "_", G: "_а",  D: "_у",  A: "_а", T: "_ом", P: "_е"},
        (M, Name)),
    ("рд",   {N: "_", G: "_а",  D: "_у",  A: "_а", T: "_ом", P: "_е"},
        (M, Name)),
    ("рк",   {N: "_", G: "_а",  D: "_у",  A: "_а", T: "_ом", P: "_е"},
        (M, Name)),
    ("овь",  {N: "_", G: "ови",  D: "ови",  A: "овь", T: "овью", P: "ови"},  # не склоняет
        (F, Name)),
    ("р",   {N: "_", G: "_а",  D: "_у",  A: "_а", T: "_ом", P: "_е"},
        (M, Name)),
    ("Майя", {N: "_", G: "Майи", D: "Майе", A: "Майе", T: "Майей", P: "Майе"},
        (None, None)),
    ("Мая", {N: "_", G: "Майи", D: "Мае", A: "Мае", T: "Маей", P: "Мае"},
        (None, None)),
    ("убина", {N: "_", G: "убиной", D: "убиной", A: "убиной", T: "убиной", P: "убиной"},
        (None, None)),
    ("ыбина", {N: "_", G: "ыбиной", D: "ыбиной", A: "ыбину", T: "ыбиной", P: "ыбиной"},
        (None, None)),
    ("хина", {N: "_", G: "хиной", D: "хиной", A: "хиной", T: "хиной", P: "хиной"},
        (None, None)),
    ("тарина", {N: "_", G: "тарины", D: "тарине", A: "тарину", T: "тариной", P: "тарине"},
        (None, None)),
    ("Марина", {N: "_", G: "Марины", D: "Марине", A: "Марину", T: "Мариной", P: "Марине"},
        (None, None)),
    ("арина", {N: "_", G: "ариной", D: "ариной", A: "арину", T: "ариной", P: "ариной"},
        (None, None)),
    ("юлина", {N: "_", G: "юлиной", D: "юлиной", A: "юлину", T: "юлиной", P: "юлиной"},
        (None, None)),
    ("итина", {N: "_", G: "итиной", D: "итиной", A: "итину", T: "итиной", P: "итиной"},
        (None, None)),
    ("утина", {N: "_", G: "утиной", D: "утиной", A: "утину", T: "утиной", P: "утиной"},
        (None, None)),
    ("ятина", {N: "_", G: "ятиной", D: "ятиной", A: "ятину", T: "ятиной", P: "ятиной"},
        (None, None)),
    ("аина", {N: "_", G: "аины", D: "аине", A: "аину", T: "аиной", P: "аине"},
        (None, None)),
    ("Кристина", {N: "_", G: "Кристины", D: "Кристине", A: "Кристину", T: "Кристиной", P: "Кристине"},
        (None, None)),
    ("Эльвина", {N: "_", G: "Эльвины", D: "Эльвине", A: "Эльвину", T: "Эльвиной", P: "Эльвине"},
        (None, None)),
    ("Нина", {N: "_", G: "Нины", D: "Нине", A: "Нину", T: "Ниной", P: "Нине"},
        (None, None)),
    ("Дина", {N: "_", G: "Дины", D: "Дине", A: "Дину", T: "Диной", P: "Дине"},
        (None, None)),
    ("анина", {N: "_", G: "аниной", D: "аниной", A: "анину", T: "аниной", P: "аниной"},
        (None, None)),
    ("енина", {N: "_", G: "ениной", D: "ениной", A: "енину", T: "ениной", P: "ениной"},
        (None, None)),
    ("инина", {N: "_", G: "ининой", D: "ининой", A: "инину", T: "ининой", P: "ининой"},
        (None, None)),
    ("нтонина", {N: "_", G: "нтонины", D: "нтонине", A: "нтонину", T: "нтониной", P: "нтонине"},
        (None, None)),
    ("онина", {N: "_", G: "ониной", D: "ониной", A: "онину", T: "ониной", P: "ониной"},
        (None, None)),
    ("унина", {N: "_", G: "униной", D: "униной", A: "унину", T: "униной", P: "униной"},
        (None, None)),
    ("шнина", {N: "_", G: "шниной", D: "шниной", A: "шнину", T: "шниной", P: "шниной"},
        (None, None)),
    ("стина", {N: "_", G: "стиной", D: "стиной", A: "стину", T: "стиной", P: "стиной"},
        (None, None)),
    ("мнина", {N: "_", G: "мниной", D: "мниной", A: "мнину", T: "мниной", P: "мниной"},
        (None, None)),
    ("лена", {N: "_", G: "лены", D: "лене", A: "лену", T: "леной", P: "лене"},
        (None, None)),
    ("ена", {N: "_", G: "ены", D: "еной", A: "ену", T: "еной", P: "ене"},
        (None, None)),
    ("гея", {N: "_", G: "геи", D: "гее", A: "гею", T: "геей", P: "гее"},
        (None, None)),
    ("ына", {N: "_", G: "ыной", D: "ыной", A: "ыну", T: "ыной", P: "ыной"},
        (None, None)),
    ("снина", {N: "_", G: "сниной", D: "сниной", A: "снину", T: "сниной", P: "сниной"},
        (None, None)),
    ("нина", {N: "_", G: "нины", D: "нине", A: "нину", T: "ниной", P: "нине"},
        (None, None)),
    ("трина", {N: "_", G: "триной", D: "триной", A: "трину", T: "триной", P: "триной"},
        (None, None)),
    ("дрина", {N: "_", G: "дриной", D: "дриной", A: "дрину", T: "дриной", P: "дриной"},
        (None, None)),
    ("орина", {N: "_", G: "ориной", D: "ориной", A: "орину", T: "ориной", P: "ориной"},
        (None, None)),
    ("атерина", {N: "_", G: "атерины", D: "атерине", A: "атерину", T: "атериной", P: "атерине"},
        (None, None)),
    ("ерина", {N: "_", G: "ериной", D: "ериной", A: "ерину", T: "ериной", P: "ериной"},
        (None, None)),
    ("рина", {N: "_", G: "рины", D: "рине", A: "рину", T: "риной", P: "рине"},
        (None, None)),
    ("фина", {N: "_", G: "фины", D: "фине", A: "фину", T: "финой", P: "фине"},
        (None, None)),
    ("лина", {N: "_", G: "лины", D: "лине", A: "лину", T: "линой", P: "лине"},
        (None, None)),
    ("лен", {N: "_", G: "лена", D: "лену", A: "лена", T: "леном", P: "лене"},
        (None, None)),
    ("риппина", {N: "_", G: "риппины", D: "риппине", A: "риппину", T: "риппиной", P: "риппине"},
        (None, None)),
    ("рипина", {N: "_", G: "рипины", D: "рипине", A: "рипину", T: "рипиной", P: "рипине"},
        (None, None)),
    ("тина", {N: "_", G: "тины", D: "тине", A: "тину", T: "тиной", P: "тине"},
        (None, None)),
    ("бина", {N: "_", G: "бины", D: "бине", A: "бину", T: "биной", P: "бине"},
        (None, None)),
    ("ина", {N: "_", G: "иной", D: "иной", A: "ину", T: "иной", P: "иной"},
        (None, None)),
    ("ич", {N: "_", G: "ича", D: "ичу", A: "ича", T: "ичем", P: "иче"},
        (None, None)),
    ("ых",  {N: "_", G: "ых",   D: "ых",   A: "ых",  T: "ых",  P: "ых"},
        (None, None)),
    ("сип",  {N: "_", G: "_а",   D: "_у",   A: "_а",  T: "_ом",  P: "_е"},
        (None, None)),
    ("их",  {N: "_", G: "их",   D: "их",   A: "их",  T: "их",  P: "их"},
        (None, None)),
    ("ика",   {N: "_", G: "ики",   D: "ике",   A: "ику",  T: "икой",  P: "ике"},
        (None, None)),
    ("а",   {N: "_", G: "ы",   D: "е",   A: "у",  T: "ой",  P: "е"},
        (None, None)),
    ("мя",  {N: "_", G: "мени", D: "мени", A: "мя", T: "менем", P: "мени"},
        (None, None)),
    ("ня",  {N: "_", G: "ни",  D: "не",  A: "ню", T: "ней", P: "не"},
        (None, None)),
    ("тя",  {N: "_", G: "ти",  D: "те",  A: "тю", T: "тей", P: "те"},
        (None, None)),
    ("дя",  {N: "_", G: "ди",  D: "де",  A: "дю", T: "дей", P: "де"},
        (F, Name)),
    ("еля",  {N: "_", G: "ели",  D: "еле",  A: "елю", T: "елей", P: "еле"},
        (F, Name)),
    ("Эля",  {N: "_", G: "Эли",  D: "Эле",  A: "Элю", T: "Элей", P: "Эле"},
        (F, Name)),
    ("эля",  {N: "_", G: "эли",  D: "эле",  A: "элю", T: "элей", P: "эле"},
        (F, Name)),
    ("лля",  {N: "_", G: "лли",  D: "лле",  A: "ллю", T: "ллей", P: "лле"},
        (F, Name)),
    ("лли",  {N: "_", G: "_",  D: "_",  A: "_", T: "_", P: "_"},
        (M, Name)),
    ("рь",  {N: "_", G: "ря",  D: "рю",  A: "ря",  T: "рем", P: "ре"},
        (None, None)),
    ("ль",  {N: "_", G: "ля",  D: "лю",  A: "ля",  T: "лем", P: "ле"},
        (None, None)),
    ("оя",   {N: "_", G: "ои",   D: "ое",   A: "ою",  T: "оей",  P: "ое"},
        (None, None)),
    ("ая",   {N: "_", G: "ой",   D: "ой",   A: "ую",  T: "ой",  P: "ой"},
        (None, None)),
    ("ской",   {N: "_", G: "ского", D: "скому", A: "ского",  T: "ским",   P: "ском"},
        (M, FN)),
    ("ой",   {N: "_", G: "ого",   D: "ому",   A: "ого",  T: "ым",  P: "ом"},
        (None, None)),
    ("ья",   {N: "_", G: "ьи",   D: "ье",   A: "ью",  T: "ьей",  P: "ье"},
        (None, None)),
    ("ся",   {N: "_", G: "си",   D: "се",   A: "сю",  T: "сей",  P: "се"},
        (None, None)),
    ("я",   {N: "_", G: "и",   D: "е",   A: "у",  T: "ой",  P: "е"},
        (None, None)),
    ("о",   {N: "_", G: "_",   D: "_",   A: "_",  T: "_",   P: "_"},
        (None, None)),
    ("г",   {N: "_", G: "_а",   D: "_у",   A: "_а",  T: "_ом",   P: "_е"},
        (None, None)),
    ("оп",   {N: "_", G: "_а",   D: "_у",   A: "_а",  T: "_ом",   P: "_е"},
        (None, None)),
    ("ть",   {N: "_", G: "ери", D: "ери", A: "_",  T: "ерью",   P: "ери"},
        (None, None)),
    #("юк",   {N:"_", G:"_", D:"_", A:"_",  T:"_",   P:"_"},
    #    (F,FN)),
    #("як",   {N:"_", G:"_", D:"_", A:"_",  T:"_",   P:"_"},
    #    (F,FN)),
    ("юк",   {N: "_", G: "_а", D: "_у", A: "_а",  T: "_ом",   P: "_е"},
        (M, FN)),
    ("як",   {N: "_", G: "_а", D: "_у", A: "_а",  T: "_ом",   P: "_е"},
        (M, FN)),
    ("ок",   {N: "_", G: "ка", D: "ку", A: "ка",  T: "ком",   P: "ке"},
        (M, FN)),
    ("ак",   {N: "_", G: "_а", D: "_у", A: "_а",  T: "_ом",   P: "_е"},
        (M, FN)),
    ("уп",   {N: "_", G: "_а", D: "_у", A: "_а",  T: "_ом",   P: "_е"},
        (M, FN)),
    ("ас",   {N: "_", G: "_а", D: "_у", A: "_а",  T: "_ом",   P: "_е"},
        (M, FN)),
    ("иши",   {N: "_", G: "_", D: "_", A: "_",  T: "_",   P: "_"},
        (M, FN)),
    ("ской",   {N: "_", G: "_ского", D: "_скому", A: "_ского",  T: "_ским",   P: "_ском"},
        (M, FN)),
    ("мидт",   {N: "_", G: "_а", D: "_у", A: "_а",  T: "_ом",   P: "_е"},
        (M, FN)),
    ("швили",   {N: "_", G: "_", D: "_", A: "_",  T: "_",   P: "_"},
        (M, FN)),
    ("швилли",   {N: "_", G: "_", D: "_", A: "_",  T: "_",   P: "_"},
        (M, FN)),
    ("дзе",   {N: "_", G: "_", D: "_", A: "_",  T: "_",   P: "_"},
        (M, FN)),
)

kinds = {
    1: {N: "_", G: "ы", D: "е", A: "у", T: "ой", P: "е"},
    2: {N: "_", G: "а", D: "у", A: "_", T: "ом", P: "е"},
    3: {N: "_", G: "и", D: "и", A: "_", T: "_ю", P: "и"},
}

midname_gender = {
    "M": ("ович", "евич", "оглы", "льич", "зьмич"),
    "F": ("овна", "евна", "кызы", "инична")
}

# в остальных случаях считаем окончанием последнюю гласную, 2 склонением

vovels = "уеыаоэяию"


def normalize_case(case):
    if case == "":
        return "N"
    return casemap[case[0]]


def correct(word):
    a = word.replace("чы", "чи")
    a = a.replace("шы", "ши")
    a = a.replace("щы", "щи")

    a = a.replace("чю", "чу")
    a = a.replace("щю", "щу")

    a = a.replace("чя", "ча")
    a = a.replace("щя", "ща")

    a = a.replace("йа", "я")
    a = a.replace("йу", "ю")
    a = a.replace("йо", "ё")
    a = a.replace("йэ", "е")
    a = a.replace("йя", "я")
    a = a.replace("йю", "ю")
    a = a.replace("йё", "ё")
    a = a.replace("йе", "е")

    a = a.replace("йи", "и")

    a = a.replace("гы", "ги")

    a = a.replace("льныя", "льного")

    return a


def define_kind(word):
    done = 0
    for (last, kind, _) in endings:
        if word.endswith(last):
            semiroot = word[:-len(last)]
            done = 1
            break
    if not done:
        kind = kind2th
        last = word[-1]
        if last in vovels:
            semiroot = word[:-1]
        else:
            semiroot = word
            last = ""
    return (semiroot, last, kind)


def make_case(word, case="N"):
    case = normalize_case(case)
    (semiroot, last, kind) = define_kind(word)
    new_last = kind[case]
    new_last = new_last.replace("_", last)
    answer = semiroot + new_last
    if word == "Майя" or word == "Мая":
        return answer
    return correct(answer)


def make_all(text, case="N"):
    text = text.strip()
    items = text.split(" ")
    l = []
    for i in items:
        l.append(make_case(i, case))
    return " ".join(l)


def determine_gender(text, default):
    """Defines gender, returns 'M' or 'F'"""
    if type(text) == bytes:
        wordlist = text.strip().split()
    else:
        wordlist = text   # suppose it be a list or tuple
    rc = None
    for word in wordlist:
        for gender, l in list(midname_gender.items()):
            for ending in l:
                if word.endswith(ending):
                    if rc in ["M", None]:
                        rc = gender
                    else:
                        return gender
    if rc is None:
        return default
    else:
        return rc


def person_data(text, default=None):
    """Defines gender, returns 'M' or 'F'"""
    if type(text) == bytes:
        wordlist = text.strip().split()
    else:
        wordlist = text   # suppose it be a list or tuple
    rc = None
    i = 0
    otch = -1
    gender_rc = None
    names = []
    # log=open("aa.log","a")
    for word in wordlist:
        for gender, list in list(midname_gender.items()):
            for ending in list:
                #log.write(ending+" "+word+" "+str(word.endswith(ending))+"\n")
                if word.endswith(ending):
                    if gender_rc in ["M", None]:
                        gender_rc = gender
                        otch = i
                        #log.write("ok "+str(gender))
                        break
        if otch != i:
            names.append(word)
        i += 1
    if rc is None:
        gen = default
    names.append(wordlist[otch])
    if gender_rc == "M":
        names.append("М")
    elif gender_rc == "F":
        names.append("Ж")
    names.append(gender_rc)
    # log.write(str(gender_rc))
    return names


_mark2 = [1, 2]


def gender(text, male, female, default=_mark2):
    ''' Returns _male_ or _female_ value,
    depending on guessed gender according to _text_.
    If _default_ is given, then if
       the guess has been failed, the guess is default.
    _Default_ = None results in empty string'''
    rc = determine_gender(text, default=default)
    if rc == 'M':
        return male
    elif rc == 'F':
        return female
    elif rc is None:
        return ""
    elif rc == _mark2:
        raise ValueError('cannot guess the gender')
    else:
        return default


def make_human_case(text, case='N', def_gender=None):
    if isinstance(text, str):
        wordlist = text.strip().split()
        wastext = 1
    else:
        wordlist = text   # suppose it be a list or tuple
        wastext = 0
    if def_gender is None:
        def_gender = gender(wordlist, 'M', 'F', '_')
    if def_gender == 'M':
        answer = []
        for word in wordlist:
            answer.append(make_case(word, case))
    else:
        # print "++++"; asd
        # gender = 'F'
        # Женская фамилия на а, я - склоняется, остальные нет
        answer = []
        for word in wordlist:
            #~ namepart=None
            #~ for (e, kinds, gen_def) in endings:
                #~ if word.endswith(e):
                    #~ (gender_, namepart)=gen_def
                    #~ break
            #~ print "---", word, gen_def
            # if namepart==FN:    # Family Name
            if word[-1] in ['а', 'я'] or word == "Любовь":  # Заплатка
                decl_word = make_case(word, case)
            else:
                print(':1:', word)
                decl_word = word
            # else:
            #    decl_word=make_case(word, case)
            answer.append(decl_word)
    if wastext:
        return " ".join(answer)
    else:
        return answer

### Utilitar functions (for tests) ###


def make_cases(word, cases=None):
    if cases is None:
        cases = [N, G, D, A, T, P]
    answer = []
    for case in cases:
        answer.append(make_case(word, case))
    return answer


def make_all_cases(text, cases=None):
    if cases is None:
        cases = [N, G, D, A, T, P]
    answer = []
    for case in cases:
        answer.append(make_all(text, case))
    return answer


def make_all_human_cases(text, cases=None):
    if cases is None:
        cases = [N, G, D, A, T, P]
    answer = []
    for case in cases:
        answer.append(make_human_case(text, case))
    return answer


def pprint(s):
    l = list(map(lambda x, y: (x, y), s, ["И", "Р", "Д", "В", "Т", "П"]))
    for (v, k) in l:
        print(k, '=', v)

# Convert numbers to textual representation

DICT = {
    0: "",
    1: "один",
    2: "два",
    3: "три",
    4: "четыре",
    5: "пять",
    6: "шесть",
    7: "семь",
    8: "восемь",
    9: "девять",
    10: "десять",
    11: "одиннадцать",
    12: "двенадцать",
    13: "тринадцать",
    14: "четырнадцать",
    15: "пятнадцать",
    16: "шестнадцать",
    17: "семнадцать",
    18: "восемнадцать",
    19: "девятнадцать",
    20: "двадцать",
    30: "тридцать",
    40: "сорок",
    50: "пятьдесят",
    60: "шестьдесят",
    70: "семьдесят",
    80: "восемьдесят",
    90: "девяносто",
    100: "сто",
    200: "двести",
    300: "триста",
    400: "четыреста",
    500: "пятьсот",
    600: "шестьсот",
    700: "семьсот",
    800: "восемьсот",
    900: "девятьсот",
    1000: "тысяч",
    1000000: "миллион",
    1000000000: "миллиард"
}


def convert_1(v):
    l = len(v)
    assert l < 3
    vv = int(v)
    if vv == 0:
        return ""
    else:
        return DICT[vv]


def convert_2(v):
    l = len(v)
    assert l < 3
    vv = int(v)
    if vv == 0:
        return ""
    if l == 2:
        if vv < 20:
            return DICT[vv]
        else:
            return DICT[int(v[0] + "0")] + " " + convert_1(v[1:])
    if l == 1:
        return convert_1(v)


def convert_3(value):
    v = value
    l = len(value)
    assert l < 4
    if l == 3:
        return DICT[int(v[0] + "00")] + " " + convert_2(v[1:])
    if l == 2:
        return convert_2(v)
    if l == 1:
        return convert_1(v)


def _text_money(value):
    value = value.strip()
    value = value.replace(" ", "")

    l = len(value)
    if l <= 3:
        return convert_3(value)
    if l <= 6:
        return convert_3(value[:-3]) + " тысяч " + convert_3(value[-3:])
    if l <= 9:
        return convert_3(value[:-6]) + " миллионов " + convert_3(value[-6:-3]) + " тысяч " + convert_3(value[-3:])
    return "Очень много денег"


def text_money(value):
    try:
        answer = _text_money(value)
    except ValueError:
        return "Неправильно набран номер!"
    answer = answer.replace("один тысяч", "одна тысяча")
    answer = answer.replace("два тысяч", "две тысячи")
    answer = answer.replace("три тысяч", "три тысячи")
    answer = answer.replace("четыре тысяч", "четыре тысячи")

    answer = answer.replace("один миллионов", "один миллион")
    answer = answer.replace("два миллионов", "два миллиона")
    answer = answer.replace("три миллионов", "три миллиона")
    answer = answer.replace("четыре миллионов", "четыре миллиона")

    answer = answer.replace("  ", " ")

    return answer

count_repl = (
    ("один", "первого"),
    ("два", "второго"),
    ("три", "третьего"),
    ("четыре", "четвертого"),
    ("пять", "пятого"),
    ("шесть", "шестого"),
    ("восемь", "восьмого"),
    ("семь", "седьмого"),
    ("ять", "ятого"),
)


def _text_day(day):
    # if day<=0 or day>31:
    #    raise ValueError, "day number is not correct"
    day = str(day)
    answer = text_money(day)
    l = answer.strip().split()
    a = l[:-1]
    answer = l[-1]
    answer = answer.strip()
    if not answer.endswith("дцать"):
        for (k, v) in count_repl:
            answer = answer.replace(k, v)
    answer = answer.replace("ать", "атого")

    return " ".join(a + [answer]).strip()

months = ["января", "февраля", "марта", "апреля", "мая", "июня",
          "июля", "августа", "сентября", "октября", "ноября", "декабря"]


def _text_month(month):
    month = int(month)
    try:
        return months[month - 1]
    except IndexError:
        raise ValueError("wrong month number")

_text_year = _text_day


def text_date(day, month, year):
    try:
        int(day)
        int(month)
        year = int(year)
        if year < 100:
            if year < 54:
                year = 2000 + year
            else:
                year = 1900 + year
        day_t = _text_day(day)
        month_t = _text_month(month)
        year_t = _text_year(year)
    except RuntimeError:
        return "Неправильная дата!"
    except ValueError:
        return "Неправильная дата!"
    if year_t.endswith("две тысячи"):
        year_t = "двухтысячного"
    return " ".join([day_t, month_t, year_t, 'года'])


re_number_str = r"(\d+\.?\/?\d+|\d)"
re_parentsis_str = r"(\s?\([А-Яа-я ]*\))"
re_number = re.compile(re_number_str)
re_parentsis = re.compile(re_parentsis_str)
re_num_and_text = re.compile(re_number_str + "\s" + re_parentsis_str)


def text_numbers_in_string(s):
    '''После каждой цифры поставить её текстуальное представление.
    Например
    ул. Розы Люксембург, д.135, кв.40
    будет
    ул. Розы Люксембург, д.135 (сто тридцать пять), кв.40 (сорок)
    Метод.
    Распознать цифру, и
       Если после нее идет скобка, то убить скобку с содержимым
    вставить скобку с текстуальным представлением.
    '''
    # if type(s) != types.StringType:
    #    return s
    ns = re.sub(re_parentsis, "", s)
    l = re.split(re_number, ns)
    # print "---", l
    save = 1
    s = ""
    for p in l:
        if save:
            s += p
            save = 0
            continue
        save = 1
        aa = p.split('.')
        bb = p.split('/')
        if len(aa) > 1:
            (a, b) = aa
            if len(b) == 1:
                b = b + '0'
            (at, bt) = (text_money(a).strip(), text_money(b).strip())
            s += "%s.%s (%s целых %s сотых)" % (a, b, at, bt)
        elif len(bb) > 1:
            (a, b) = bb
            s += '%s/%s' % (a, b)
        else:
            s += "%s (%s)" % (p, text_money(p).strip())
    return s


# 54-41-91. 26-62-77
# print text_money("105 104 123")+"

def test_date():
    for i in range(31):
        print(text_date(i + 1, (i % 12) + 1, 1986 + i))
    print(text_money("105 104 123") + " руб.")


def test_names():
    '''
    print "*"*40
    s='ул. Розы Люксембург, д.10, кв.40/9'
    for _ in range(10):
        s=text_numbers_in_string(s)
        print s
    s='ул. Розы Люксембург, д.10, кв.40'
    for _ in range(10):
        s=text_numbers_in_string(s)
        print s
    raise SystemExit, "hi"
    '''
    pprint(make_all_human_cases("Иванов Назарали Иванович"))
    pprint(make_all_human_cases("Руставелли Шота Иванович"))
    pprint(make_all_human_cases("Веснина Нэля Ивановна"))
    pprint(make_all_human_cases("Домнина Нэля Ивановна"))
    pprint(make_all_human_cases("Иванов Всеволод Иванович"))
    pprint(make_all_human_cases("Иванов Шеренбек Иванович"))
    pprint(make_all_human_cases("Зарубина Нэля Ивановна"))
    pprint(make_all_human_cases("Рыбина Нэля Ивановна"))
    pprint(make_all_human_cases("Надежда Ильинична Крупская"))
    pprint(make_all_human_cases("Саутин Игорь Петрович"))
    pprint(make_all_human_cases("Малетин Игорь Петрович"))
    pprint(make_all_human_cases("Шадрина Ия Вановна"))
    pprint(make_all_human_cases("Кузьмич Кузьма Кузьмич"))
    pprint(make_all_human_cases("Донской Илья Кузьмич"))
    pprint(make_all_human_cases("Мотин Илья Кузьмич"))
    pprint(make_all_human_cases("Воронина Ия Вановна"))
    pprint(make_all_human_cases("Костина Ия Вановна"))
    pprint(make_all_human_cases("Пашнина Ия Вановна"))
    pprint(make_all_human_cases("Говорина Ия Вановна"))
    pprint(make_all_human_cases("Капустина Ия Вановна"))
    pprint(make_all_human_cases("Тетерина Ия Вановна"))
    pprint(make_all_human_cases("Пухашвили Вано Иванович"))
    pprint(make_all_human_cases("Меладзе Вано Иванович"))
    pprint(make_all_human_cases("Зарубина Эльвина Ивановна"))
    pprint(make_all_human_cases("Зарубина Дина Ивановна"))
    pprint(make_all_human_cases("Зарубина Руфина Ивановна"))
    pprint(make_all_human_cases("Зарубина Римма Ивановна"))
    pprint(make_all_human_cases("Зарубин Глеб Иванович"))
    pprint(make_all_human_cases("Киркоров Филипп Иванович"))
    pprint(make_all_human_cases("Киркоров Герман Иванович"))
    pprint(make_all_human_cases("Зарубина Вероника Ивановна"))
    pprint(make_all_human_cases("Зарубин Осип Иванович"))
    print("*" * 40)
    pprint(make_all_cases("Тарас"))
    pprint(make_all_cases("Мая"))
    pprint(make_all_cases("Майя"))
    pprint(make_all_cases("Марина"))
    pprint(make_all_cases("Илья"))
    pprint(make_all_cases("Антонина"))
    pprint(make_all_cases("Агриппина"))
    pprint(make_all_cases("Агрипина"))
    pprint(make_all_cases("Кирилл"))
    pprint(make_all_cases("Шмидт"))
    pprint(make_all_cases("Асад"))
    pprint(make_all_cases("Катерина"))
    pprint(make_all_cases("Катерина"))
    pprint(make_all_cases("исполняющий"))
    pprint(make_all_cases("исполняющая"))
