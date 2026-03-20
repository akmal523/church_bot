import asyncio
import urllib.parse
from database.db import engine, Base, City, Church, ScheduleType
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

def gmap(address: str):
    return f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(address)}"

def ymap(address: str):
    return f"https://yandex.ru/maps/?text={urllib.parse.quote(address)}"

CITIES = [
    {"ru": "Алмалык", "en": "Almalyk", "uz": "Олмалиқ", "uzl": "Olmaliq"},
    {"ru": "Ангрен", "en": "Angren", "uz": "Ангрен", "uzl": "Angren"},
    {"ru": "Андижан", "en": "Andijan", "uz": "Андижон", "uzl": "Andijon"},
    {"ru": "Ахангаран", "en": "Akhangaran", "uz": "Оҳангарон", "uzl": "Ohangaron"},
    {"ru": "Бекабад", "en": "Bekabad", "uz": "Бекобод", "uzl": "Bekobod"},
    {"ru": "Бухара", "en": "Bukhara", "uz": "Бухоро", "uzl": "Buxoro"},
    {"ru": "Газалкент", "en": "Gazalkent", "uz": "Ғазалкент", "uzl": "G'azalkent"},
    {"ru": "Гулистан", "en": "Gulistan", "uz": "Гулистон", "uzl": "Guliston"},
    {"ru": "Денау", "en": "Denau", "uz": "Денов", "uzl": "Denov"},
    {"ru": "Джизак", "en": "Jizzakh", "uz": "Жиззах", "uzl": "Jizzax"},
    {"ru": "Достабад", "en": "Dostabad", "uz": "Дўстобод", "uzl": "Do'stobod"},
    {"ru": "Зарафшан", "en": "Zarafshan", "uz": "Зарафшон", "uzl": "Zarafshon"},
    {"ru": "Каган", "en": "Kagan", "uz": "Когон", "uzl": "Kogon"},
    {"ru": "Карши", "en": "Karshi", "uz": "Қарши", "uzl": "Qarshi"},
    {"ru": "Каттакурган", "en": "Kattakurgan", "uz": "Каттақўрғон", "uzl": "Kattaqo'rg'on"},
    {"ru": "Коканд", "en": "Kokand", "uz": "Қўқон", "uzl": "Qo'qon"},
    {"ru": "Красногорск", "en": "Krasnogorsk", "uz": "Красногорск", "uzl": "Krasnogorsk"},
    {"ru": "Кувасай", "en": "Kuvasay", "uz": "Қувасой", "uzl": "Quvasoy"},
    {"ru": "Навои", "en": "Navoi", "uz": "Навоий", "uzl": "Navoiy"},
    {"ru": "Наманган", "en": "Namangan", "uz": "Наманган", "uzl": "Namangan"},
    {"ru": "Нукус", "en": "Nukus", "uz": "Нукус", "uzl": "Nukus"},
    {"ru": "Самарканд", "en": "Samarkand", "uz": "Самарқанд", "uzl": "Samarqand"},
    {"ru": "Сырдарья", "en": "Syrdarya", "uz": "Сирдарё", "uzl": "Sirdaryo"},
    {"ru": "Ташкент", "en": "Tashkent", "uz": "Тошкент", "uzl": "Toshkent"},
    {"ru": "Термез", "en": "Termez", "uz": "Термиз", "uzl": "Termiz"},
    {"ru": "Ургенч", "en": "Urgench", "uz": "Урганч", "uzl": "Urganch"},
    {"ru": "Учкудук", "en": "Uchkuduk", "uz": "Учқудуқ", "uzl": "Uchquduq"},
    {"ru": "Фергана", "en": "Fergana", "uz": "Фарғона", "uzl": "Farg'ona"},
    {"ru": "Хаваст", "en": "Khavast", "uz": "Ховос", "uzl": "Xovos"},
    {"ru": "Чиназ", "en": "Chinaz", "uz": "Чиноз", "uzl": "Chinoz"},
    {"ru": "Чирчик", "en": "Chirchik", "uz": "Чирчиқ", "uzl": "Chirchiq"},
    {"ru": "Янгиюль", "en": "Yangiyul", "uz": "Янгийўл", "uzl": "Yangiyo'l"},
]

SCHEDULE_TYPES = [
    {"name_ru": "Будний", "name_en": "Weekday"},
    {"name_ru": "Воскресный", "name_en": "Sunday"},
    {"name_ru": "Праздничный", "name_en": "Feast Day"},
]

FULL_CHURCHES = [
    (0, "Храм Успения Пресвятой Богородицы", "Church of the Dormition", "Успение ибодатхонаси", "Uspeniye ibodatxonasi", "г. Алмалык, 104-й квартал, ул. Алпомыш 29", "Almalyk, 104th block, Alpomysh st. 29", "Олмалиқ ш., 104-мавзе, Алпомиш кўч. 29", "Olmaliq sh., 104-mavze, Alpomish ko'ch. 29", "+998 90 348 36 29", "Настоятель: иерей Павел Былин", "Rector: Priest Pavel Bylin", "Раҳбар: руҳоний Павел Былин", "Rahbar: ruhoniy Pavel Bilin", 40.845891, 69.607110),
    (1, "Молитвенный дом в честь иконы «Взыскание погибших»", "Prayer House 'Seeker of the Perishing'", "«Взыскание погибших» ибодат уйи", "«Vziskaniye pogibshix» ibodat uyi", "г. Ангрен, ул. Алмалыкская, 33", "Angren, Almalykskaya st., 33", "Ангрен ш., Олмалиқ кўч., 33", "Angren sh., Olmaliq ko'ch., 33", "", "Настоятель: священник Алексий Балухатин", "Rector: Priest Alexy Balukhatin", "Раҳбар: руҳоний Алексий Балухатин", "Rahbar: ruhoniy Aleksiy Baluxatin", 41.019761, 70.074228),
    (2, "Молитвенный дом Всех святых", "Prayer House of All Saints", "Барча Муқаддаслар ибодат уйи", "Barcha Muqaddaslar ibodat uyi", "г. Андижан, ул. Мусаева, 10", "Andijan, Musaev st., 10", "Андижон ш., Мусаев кўч., 10", "Andijon sh., Musayev ko'ch., 10", "+998 74 224 37 87", "Настоятель: священник Игорь Максудов", "Rector: Priest Igor Maksudov", "Раҳбар: руҳоний Игорь Максудов", "Rahbar: ruhoniy Igor Maksudov", 40.783300, 72.333300),
    (3, "Молитвенный дом святого апостола Фомы", "Prayer House of Apostle Thomas", "Ҳаворий Фома ибодат уйи", "Havoriy Foma ibodat uyi", "г. Ахангаран, 53-й квартал, ул. Ахунбабаева, д. 2", "Akhangaran, 53rd block, Akhunbabaev st., 2", "Оҳангарон ш., 53-мавзе, Охунбобоев кўч., 2", "Ohangaron sh., 53-mavze, Oxunboboev ko'ch., 2", "+998 371 645 25 92", "Настоятель: священник Алексей Биренбаум", "Rector: Priest Alexey Birenbaum", "Раҳбар: руҳоний Алексей Биренбаум", "Rahbar: ruhoniy Aleksey Birenbaum", 40.900000, 69.633300),
    (4, "Храм Сретения Господня", "Church of the Meeting of the Lord", "Сретение ибодатхонаси", "Sreteniye ibodatxonasi", "г. Бекабад, ул. Поповича, 2", "Bekabad, Popovich st., 2", "Бекобод ш., Попович кўч., 2", "Bekobod sh., Popovich ko'ch., 2", "+998 97 702 53 37", "Настоятель: священник Лука Иргашев", "Rector: Priest Luka Irgashev", "Раҳбар: руҳоний Лука Иргашев", "Rahbar: ruhoniy Luka Irgashev", 40.217699, 69.265804),
    (5, "Храм Архистратига Михаила", "Church of Archangel Michael", "Фаришта Микоил ибодатхонаси", "Farishta Mikoil ibodatxonasi", "г. Бухара, ул. Карши Дарвоза, 4", "Bukhara, Karshi Darvoza st., 4", "Бухоро ш., Қарши Дарвоза кўч., 4", "Buxoro sh., Qarshi Darvoza ko'ch., 4", "+998 65 223 78 34", "Настоятель: священник Леонид Петров", "Rector: Priest Leonid Petrov", "Раҳбар: руҳоний Леонид Петров", "Rahbar: ruhoniy Leonid Petrov", 39.771445, 64.433424),
    (6, "Молитвенный дом «Всех скорбящих Радосте»", "Prayer House 'Joy of All Who Sorrow'", "«Всех скорбящих Радосте» ибодат уйи", "«Vsex skorbyashix Radoste» ibodat uyi", "г. Газалкент, ул. Дустлик, 15", "Gazalkent, Dustlik st., 15", "Ғазалкент ш., Дўстлик кўч., 15", "G'azalkent sh., Do'stlik ko'ch., 15", "+998 71 742 71 12", "Настоятель: протоиерей Борис Маслаков", "Rector: Archpriest Boris Maslakov", "Раҳбар: бош руҳоний Борис Маслаков", "Rahbar: bosh ruhoniy Boris Maslakov", 41.558300, 69.770800),
    (7, "Храм святителя Николая", "Church of St. Nicholas", "Авлиё Николай ибодатхонаси", "Avliyo Nikolay ibodatxonasi", "г. Гулистан, ул. Туркестанская, 94", "Gulistan, Turkestan st., 94", "Гулистон ш., Туркистон кўч., 94", "Guliston sh., Turkiston ko'ch., 94", "+998 67 225 08 86", "Настоятель: протоиерей Павел Сергеев", "Rector: Archpriest Pavel Sergeev", "Раҳбар: бош руҳоний Павел Сергеев", "Rahbar: bosh ruhoniy Pavel Sergeyev", 40.489700, 68.784200),
    (8, "Молитвенный дом Покрова", "Prayer House of the Intercession", "Покров ибодат уйи", "Pokrov ibodat uyi", "г. Денау, ул. Нозима Мирзаева, 46", "Denau, Nozim Mirzaev st., 46", "Денов ш., Нозим Мирзаев кўч., 46", "Denov sh., Nozim Mirzayev ko'ch., 46", "+998 37 641 24 522", "Настоятель: священник Леонид Химониди", "Rector: Priest Leonid Khimonidi", "Раҳбар: руҳоний Леонид Химониди", "Rahbar: ruhoniy Leonid Ximonidi", 38.266700, 67.898900),
    (9, "Храм святителя Николая", "Church of St. Nicholas", "Авлиё Николай ибодатхонаси", "Avliyo Nikolay ibodatxonasi", "г. Джизак, ул. О. Азимова, 7", "Jizzakh, O. Azimov st., 7", "Жиззах ш., О. Азимов кўч., 7", "Jizzax sh., O. Azimov ko'ch., 7", "+998 72 222 21 93", "Настоятель: священник Николай Клименко", "Rector: Priest Nikolay Klimenko", "Раҳбар: руҳоний Николай Клименко", "Rahbar: ruhoniy Nikolay Klimenko", 40.115800, 67.842200),
    (10, "Свято-Покровский женский монастырь", "Holy Intercession Convent", "Покров аёллар монастыри", "Pokrov ayollar monastiri", "г. Достабад, ул. Баркамол овлод, 85", "Dostabad, Barkamol avlod st., 85", "Дўстобод ш., Баркамол авлод кўч., 85", "Do'stobod sh., Barkamol avlod ko'ch., 85", "+998 91 301 45 59", "И.о. настоятельницы: монахиня Евгения", "Acting Abbess: Nun Evgenia", "Раҳбар в.б.: роҳиба Евгения", "Rahbar v.b.: rohiba Yevgeniya", 40.966700, 68.816700),
    (11, "Храм Святителя Николая", "Church of St. Nicholas", "Авлиё Николай ибодатхонаси", "Avliyo Nikolay ibodatxonasi", "г. Зарафшан, ул. Мира, 1", "Zarafshan, Mira st., 1", "Зарафшон ш., Мира кўч., 1", "Zarafshon sh., Mira ko'ch., 1", "+998 79 574 52 56", "Настоятель: священник Артемий Пономарев", "Rector: Priest Artemy Ponomarev", "Раҳбар: руҳоний Артемий Пономарев", "Rahbar: ruhoniy Artemiy Ponomarev", 41.573900, 64.198600),
    (12, "Храм Святителя Николая", "Church of St. Nicholas", "Авлиё Николай ибодатхонаси", "Avliyo Nikolay ibodatxonasi", "г. Каган, ул. Истирохат, 186", "Kagan, Istirokhat st., 186", "Когон ш., Истироҳат кўч., 186", "Kogon sh., Istirohat ko'ch., 186", "+998 36 552 224 01", "Настоятель: протоиерей Сергий Заворотнев", "Rector: Archpriest Sergiy Zavorotnev", "Раҳбар: бош руҳоний Сергий Заворотнев", "Rahbar: bosh ruhoniy Sergiy Zavorotnev", 39.723300, 64.549200),
    (13, "Молитвенный дом Покрова", "Prayer House of the Intercession", "Покров ибодат уйи", "Pokrov ibodat uyi", "г. Карши, ул. Бозор, 1", "Karshi, Bozor st., 1", "Қарши ш., Бозор кўч., 1", "Qarshi sh., Bozor ko'ch., 1", "+998 37 522 713 41", "Настоятель: священник Владимир Матвеев", "Rector: Priest Vladimir Matveev", "Раҳбар: руҳоний Владимир Матвеев", "Rahbar: ruhoniy Vladimir Matveyev", 38.866700, 65.800000),
    (14, "Молитвенный дом князя Владимира", "Prayer House of St. Vladimir", "Князь Владимир ибодат уйи", "Knyaz Vladimir ibodat uyi", "г. Каттакурган, ул. Закира Рахманова, 7", "Kattakurgan, Zakir Rakhmanov st., 7", "Каттақўрғон ш., Зокир Раҳмонов кўч., 7", "Kattaqo'rg'on sh., Zokir Rahmonov ko'ch., 7", "+998 66 455 49 90", "Настоятель: священник Тимофей Фишелев", "Rector: Priest Timofey Fishelev", "Раҳбар: руҳоний Тимофей Фишелев", "Rahbar: ruhoniy Timofey Fishelev", 39.898300, 65.595800),
    (15, "Храм Казанской иконы Божией Матери", "Church of the Kazan Icon", "Қозон ибодатхонаси", "Qozon ibodatxonasi", "г. Коканд, ул. Урдатоги, 70", "Kokand, Urdatogi st., 70", "Қўқон ш., Ўрдатоғи кўч., 70", "Qo'qon sh., O'rdatog'i ko'ch., 70", "+998 73 553 06 79", "Настоятель: священник Григорий Химониди", "Rector: Priest Grigory Khimonidi", "Раҳбар: руҳоний Григорий Химониди", "Rahbar: ruhoniy Grigoriy Ximonidi", 40.528600, 70.942500),
    (16, "Молитвенный дом мучениц Веры, Надежды, Любови", "Prayer House of Martyrs Faith, Hope, Love", "Имон, Умид, Муҳаббат ибодат уйи", "Imon, Umid, Muhabbat ibodat uyi", "г. Красногорск", "Krasnogorsk", "Красногорск ш.", "Krasnogorsk sh.", "+998 90 965 34 48", "Настоятель: священник Игорь Сладков", "Rector: Priest Igor Sladkov", "Раҳбар: руҳоний Игорь Сладков", "Rahbar: ruhoniy Igor Sladkov", 41.150000, 69.666700),
    (17, "Храм праведного Иоанна Кронштадтского", "Church of St. John of Kronstadt", "Иоанн Кронштадтский ибодатхонаси", "Ioann Kronshtadtskiy ibodatxonasi", "г. Кувасай, ул. Мустакиллик, 21", "Kuvasay, Mustakillik st., 21", "Қувасой ш., Мустақиллик кўч., 21", "Quvasoy sh., Mustaqillik ko'ch., 21", "+998 37 337 307 56", "Настоятель: иерей Александр Боготобин", "Rector: Priest Alexander Bogotobin", "Раҳбар: руҳоний Александр Боготобин", "Rahbar: ruhoniy Aleksandr Bogotobin", 40.300000, 71.966700),
    (18, "Храм Преподобного Сергия Радонежского", "Church of St. Sergius of Radonezh", "Сергий Радонежский ибодатхонаси", "Sergiy Radonejskiy ibodatxonasi", "г. Навои, ул. Ибн-Сино, 26а", "Navoi, Ibn-Sino st., 26a", "Навоий ш., Ибн Сино кўч., 26а", "Navoiy sh., Ibn Sino ko'ch., 26a", "+998 79 223 22 28", "Настоятель: протоиерей Леонид Козин", "Rector: Archpriest Leonid Kozin", "Раҳбар: бош руҳоний Леонид Козин", "Rahbar: bosh ruhoniy Leonid Kozin", 40.084400, 65.379200),
    (19, "Храм Архангела Михаила", "Church of Archangel Michael", "Фаришта Микоил ибодатхонаси", "Farishta Mikoil ibodatxonasi", "г. Наманган, ул. Темир йул, 50", "Namangan, Temir yul st., 50", "Наманган ш., Темир йўл кўч., 50", "Namangan sh., Temir yo'l ko'ch., 50", "+998 69 237 16 28", "Настоятель: священник Владимир Платонов", "Rector: Priest Vladimir Platonov", "Раҳбар: руҳоний Владимир Платонов", "Rahbar: ruhoniy Vladimir Platonov", 41.000000, 71.666700),
    (20, "Храм великомученика Пантелеимона", "Church of St. Panteleimon", "Муқаддас Пантелеимон ибодатхонаси", "Muqaddas Panteleimon ibodatxonasi", "г. Нукус, ул. Таттбаева, 7а", "Nukus, Tattbaev st., 7a", "Нукус ш., Таттбаев кўч., 7а", "Nukus sh., Tattbayev ko'ch., 7a", "", "Настоятель: иеромонах Спиридон (Поздеев)", "Rector: Hieromonk Spiridon (Pozdeev)", "Раҳбар: иеромонах Спиридон (Поздеев)", "Rahbar: iyeromonax Spiridon (Pozdeyev)", 42.461900, 59.616600),
    (21, "Храм великомученика Георгия Победоносца", "Church of St. George the Victorious", "Муқаддас Георгий ибодатхонаси", "Muqaddas Georgiy ibodatxonasi", "г. Самарканд, ул. Бирлик, 66", "Samarkand, Birlik st., 66", "Самарқанд ш., Бирлик кўч., 66", "Samarqand sh., Birlik ko'ch., 66", "+998 66 233 05 42", "Настоятель: священник Тимофей Фишелев", "Rector: Priest Timofey Fishelev", "Раҳбар: руҳоний Тимофей Фишелев", "Rahbar: ruhoniy Timofey Fishelev", 39.654200, 66.959700),
    (21, "Собор святителя Алексия", "Cathedral of St. Alexis", "Авлиё Алексий собори", "Avliyo Aleksiy sobori", "г. Самарканд, ул. Бобир-Мирзо, 1", "Samarkand, Bobir-Mirzo st., 1", "Самарқанд ш., Бобур Мирзо кўч., 1", "Samarqand sh., Bobur Mirzo ko'ch., 1", "+998 66 233 54 80", "Настоятель: священник Игорь Бабаков", "Rector: Priest Igor Babakov", "Раҳбар: руҳоний Игорь Бабаков", "Rahbar: ruhoniy Igor Babakov", 39.654200, 66.959700),
    (21, "Храм Покрова Пресвятой Богородицы", "Church of the Intercession", "Покров ибодатхонаси", "Pokrov ibodatxonasi", "г. Самарканд, ул. Хусейн Бойкаро, 24", "Samarkand, Khuseyn Boykaro st., 24", "Самарқанд ш., Ҳусайн Бойқаро кўч., 24", "Samarqand sh., Husayn Boyqaro ko'ch., 24", "+998 66 233 26 54", "Настоятель: протоиерей Роман Загребельный", "Rector: Archpriest Roman Zagrebelny", "Раҳбар: бош руҳоний Роман Загребельный", "Rahbar: bosh ruhoniy Roman Zagrebelniy", 39.654200, 66.959700),
    (22, "Храм Покрова Пресвятой Богородицы", "Church of the Intercession", "Покров ибодатхонаси", "Pokrov ibodatxonasi", "г. Сырдарья, ул. Гулистан, 97", "Syrdarya, Gulistan st., 97", "Сирдарё ш., Гулистон кўч., 97", "Sirdaryo sh., Guliston ko'ch., 97", "+998 67 337 72 13", "Настоятель: протоиерей Сергий Коновалов", "Rector: Archpriest Sergiy Konovalov", "Раҳбар: бош руҳоний Сергий Коновалов", "Rahbar: bosh ruhoniy Sergiy Konovalov", 40.850000, 68.666700),
    (23, "Кафедральный собор Успения Божией Матери", "Holy Dormition Cathedral", "Успение кафедрал собори", "Uspeniye kafedral sobori", "г. Ташкент, ул. Авлиёота, 91", "Tashkent, Avliyoota st., 91", "Тошкент ш., Авлиёота кўч., 91", "Toshkent sh., Avliyoota ko'ch., 91", "+998 71 255 81 05", "Настоятель: митрополит Викентий", "Rector: Metropolitan Vikenty", "Раҳбар: митрополит Викентий", "Rahbar: mitropolit Vikentiy", 41.290777, 69.278988),
    (23, "Храм князя Александра Невского", "Church of St. Alexander Nevsky", "Александр Невский ибодатхонаси", "Aleksandr Nevskiy ibodatxonasi", "г. Ташкент, ул. Боткина, 106", "Tashkent, Botkina st., 106", "Тошкент ш., Боткин кўч., 106", "Toshkent sh., Botkin ko'ch., 106", "+998 71 289 57 39", "Настоятель: протоиерей Сергий Стаценко", "Rector: Archpriest Sergiy Statsenko", "Раҳбар: бош руҳоний Сергий Стаценко", "Rahbar: bosh ruhoniy Sergiy Statsenko", 41.307400, 69.314190),
    (23, "Храм священномученика Ермогена", "Church of Hieromartyr Hermogenes", "Муқаддас Ермоген ибодатхонаси", "Muqaddas Yermogen ibodatxonasi", "г. Ташкент, ул. Ойшаханум, 1-й туп., 3", "Tashkent, Oishakhanum st., 1st dead end, 3", "Тошкент ш., Ойшахоним кўч., 1-берк, 3", "Toshkent sh., Oyshaxonim ko'ch., 1-berk, 3", "+998 71 266 80 72", "Настоятель: священник Владимир Поляк", "Rector: Priest Vladimir Polyak", "Раҳбар: руҳоний Владимир Поляк", "Rahbar: ruhoniy Vladimir Polyak", 41.331806, 69.352109),
    (23, "Храм князя Владимира", "Church of St. Vladimir", "Князь Владимир ибодатхонаси", "Knyaz Vladimir ibodatxonasi", "г. Ташкент, ул. Катартал, Домрабадское кладбище №2", "Tashkent, Katartal st., Domrabad Cemetery 2", "Тошкент ш., Қатортол кўч., Домробод қабристони №2", "Toshkent sh., Qatortol ko'ch., Domrobod qabristoni №2", "+998 71 279 46 08", "Настоятель: протоиерей Игорь Балухатин", "Rector: Archpriest Igor Balukhatin", "Раҳбар: бош руҳоний Игорь Балухатин", "Rahbar: bosh ruhoniy Igor Baluxatin", 41.258100, 69.191700),
    (23, "Свято-Троице-Никольский монастырь", "Holy Trinity-St. Nicholas Convent", "Авлиё Троица-Николай монастыри", "Avliyo Troitsa-Nikolay monastiri", "г. Ташкент, ул. 8 марта, 7", "Tashkent, 8 March st., 7", "Тошкент ш., 8 март кўч., 7", "Toshkent sh., 8 mart ko'ch., 7", "+998 71 291 69 60", "Настоятельница: игуменья Екатерина", "Abbess: Hegumenia Ekaterina", "Раҳбар: игуменья Екатерина", "Rahbar: igumenya Yekaterina", 41.295300, 69.284200),
    (24, "Храм князя Александра Невского", "Church of St. Alexander Nevsky", "Александр Невский ибодатхонаси", "Aleksandr Nevskiy ibodatxonasi", "г. Термез, ул. Сафара Сахибова", "Termez, Safar Sakhibov st.", "Термиз ш., Сафар Соҳибов кўч.", "Termiz sh., Safar Sohibov ko'ch.", "+998 76 223 04 11", "Настоятель: священник Родион Исмаилов", "Rector: Priest Rodion Ismailov", "Раҳбар: руҳоний Родион Исмаилов", "Rahbar: ruhoniy Rodion Ismailov", 37.224200, 67.278300),
    (25, "Храм патриарха Иова Многострадального", "Church of Patriarch Job the Long-Suffering", "Патриарх Иов ибодатхонаси", "Patriarx Iov ibodatxonasi", "г. Ургенч, ул. Ешлик 20/1", "Urgench, Yeshlik st., 20/1", "Урганч ш., Ёшлик кўч., 20/1", "Urganch sh., Yoshlik ko'ch., 20/1", "+998 62 224 26 82", "Настоятель: иеромонах Варлаам (Подмарьков)", "Rector: Hieromonk Varlaam (Podmarkov)", "Раҳбар: иеромонах Варлаам (Подмарьков)", "Rahbar: iyeromonax Varlaam (Podmarkov)", 41.550000, 60.633300),
    (26, "Храм всех святых", "Church of All Saints", "Барча Муқаддаслар ибодатхонаси", "Barcha Muqaddaslar ibodatxonasi", "г. Учкудук, 6 квартал, им. Амира Темура, 28", "Uchkuduk, 6th block, Amir Temur st., 28", "Учқудуқ ш., 6-мавзе, Амир Темур кўч., 28", "Uchquduq sh., 6-mavze, Amir Temur ko'ch., 28", "+998 43 659 23 15", "Настоятель: священник Георгий Фоминов", "Rector: Priest Georgy Fominov", "Раҳбар: руҳоний Георгий Фоминов", "Rahbar: ruhoniy Georgiy Fominov", 42.155300, 63.555800),
    (27, "Храм Сергия Радонежского", "Church of St. Sergius of Radonezh", "Сергий Радонежский ибодатхонаси", "Sergiy Radonejskiy ibodatxonasi", "г. Фергана, ул. Саккокий, 8", "Fergana, Sakkokiy st., 8", "Фарғона ш., Саккокий кўч., 8", "Farg'ona sh., Sakkokiy ko'ch., 8", "+998 73 226 29 10", "Настоятель: протоиерей Игорь Ходырев", "Rector: Archpriest Igor Khodyrev", "Раҳбар: бош руҳоний Игорь Ходырев", "Rahbar: bosh ruhoniy Igor Xodirev", 40.384200, 71.784400),
    (28, "Молитвенный дом святителя Николая", "Prayer House of St. Nicholas", "Авлиё Николай ибодат уйи", "Avliyo Nikolay ibodat uyi", "г. Янгиер, пос. Хаваст, ул. Ахмад Ясовий, 97", "Yangiyer, Khavast settlement, Akhmad Yasoviy st., 97", "Янгиер ш., Ховос пос., Аҳмад Яссавий кўч., 97", "Yangiyer sh., Xovos pos., Ahmad Yassaviy ko'ch., 97", "+998 36 737 463 27", "Настоятель: иеромонах Никон (Будура)", "Rector: Hieromonk Nikon (Budura)", "Раҳбар: иеромонах Никон (Будура)", "Rahbar: iyeromonax Nikon (Budura)", 40.266700, 68.816700),
    (29, "Храм преподобного Александра", "Church of St. Alexander", "Александр ибодатхонаси", "Aleksandr ibodatxonasi", "Чиназский район, пос. Янги-Чиназ, ул. Дустлик, 2а", "Chinaz district, Yangi-Chinaz, Dustlik st., 2a", "Чиноз тумани, Янги Чиноз пос., Дўстлик кўч., 2а", "Chinoz tumani, Yangi Chinoz pos., Do'stlik ko'ch., 2a", "", "Настоятель: священник Алексий Ляпин", "Rector: Priest Alexy Lyapin", "Раҳбар: руҳоний Алексий Ляпин", "Rahbar: ruhoniy Aleksiy Lyapin", 40.941900, 68.750000),
    (30, "Свято-Троице-Георгиевский монастырь", "Holy Trinity-St. George Monastery", "Авлиё Троица-Георгий монастыри", "Avliyo Troitsa-Georgiy monastiri", "гор. Чирчик, проспект А. Навои, 1а", "Chirchik, A. Navoi ave., 1a", "Чирчиқ ш., А. Навоий шоҳ кўч., 1а", "Chirchiq sh., A. Navoiy shoh ko'ch., 1a", "+998 70 715 50 33", "Настоятель: митрополит Викентий", "Rector: Metropolitan Vikenty", "Раҳбар: митрополит Викентий", "Rahbar: mitropolit Vikentiy", 41.466700, 69.583300),
    (31, "Храм «Взыскание погибших»", "Church 'Seeker of the Perishing'", "«Взыскание погибших» ибодатхонаси", "«Vziskaniye pogibshix» ibodatxonasi", "г. Янгиюль, ул. Чарикова, 264", "Yangiyul, Charikov st., 264", "Янгийўл ш., Чариков кўч., 264", "Yangiyo'l sh., Charikov ko'ch., 264", "+998 71 202 46 32", "Настоятель: протоиерей Александр Гречушкин", "Rector: Archpriest Alexander Grechushkin", "Раҳбар: бош руҳоний Александр Гречушкин", "Rahbar: bosh ruhoniy Aleksandr Grechushkin", 41.116700, 69.050000)
]

async def seed() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        city_objects = []
        for c in CITIES:
            obj = City(name_ru=c["ru"], name_en=c["en"], name_uz=c["uz"], name_uzl=c["uzl"])
            session.add(obj)
            city_objects.append(obj)
        await session.flush()

        for st in SCHEDULE_TYPES:
            session.add(ScheduleType(name_ru=st["name_ru"], name_en=st["name_en"]))

        for c_idx, name_ru, name_en, name_uz, name_uzl, addr_ru, addr_en, addr_uz, addr_uzl, phone, desc_ru, desc_en, desc_uz, desc_uzl, lat, lon in FULL_CHURCHES:
            obj = Church(
                city_id=city_objects[c_idx].id,
                name_ru=name_ru, name_en=name_en, name_uz=name_uz, name_uzl=name_uzl,
                address_ru=addr_ru, address_en=addr_en, address_uz=addr_uz, address_uzl=addr_uzl,
                latitude=lat, longitude=lon, phone=phone,
                description_ru=desc_ru, description_en=desc_en, description_uz=desc_uz, description_uzl=desc_uzl,
                google_maps_url=gmap(addr_ru), yandex_maps_url=ymap(addr_ru)
            )
            session.add(obj)
            
        await session.commit()

if __name__ == "__main__":
    asyncio.run(seed())
