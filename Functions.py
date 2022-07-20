import sqlite3
import ctypes
import time

from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QPushButton, QLabel, QWidget, QComboBox
from PyQt5.Qt import QSize
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5 import QtMultimedia
from Classes import SettingsForm, InfoForm, PauseForm, RecordsForm, Song, GameEnd


def opredelenie_const(self):
    user32 = ctypes.windll.user32
    self.screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    self.setFixedSize(self.screensize[0], self.screensize[1])
    self.main_window_icon = QIcon('Images\\пианино.png')
    self.setWindowIcon(self.main_window_icon)
    self.setWindowTitle('Черное & Белое')

    self.player = QtMultimedia.QMediaPlayer()
    self.volume = self.player.volume()
    self.block_timer = QTimer(self)

    self.key_1 = Qt.Key_A
    self.key_2 = Qt.Key_S
    self.key_3 = Qt.Key_D
    self.key_4 = Qt.Key_F

    self.keys = {Qt.Key_Q: 'Q', Qt.Key_W: 'W', Qt.Key_E: 'E', Qt.Key_R: 'R', Qt.Key_T: 'T',
                 Qt.Key_Y: 'Y', Qt.Key_U: 'U', Qt.Key_I: 'I',
                 Qt.Key_O: 'O', Qt.Key_P: 'P', Qt.Key_A: 'A', Qt.Key_S: 'S', Qt.Key_D: 'D',
                 Qt.Key_F: 'F', Qt.Key_G: 'G',
                 Qt.Key_H: 'H', Qt.Key_J: 'J', Qt.Key_K: 'K', Qt.Key_L: 'L',
                 Qt.Key_Z: 'Z', Qt.Key_X: 'X', Qt.Key_C: 'C', Qt.Key_V: 'V', Qt.Key_B: 'B', Qt.Key_N: 'N',
                 Qt.Key_M: 'Z', Qt.Key_1: '1', Qt.Key_2: '2', Qt.Key_3: '3', Qt.Key_4: '4',
                 Qt.Key_5: '5', Qt.Key_6: '6', Qt.Key_7: '7', Qt.Key_8: '8', Qt.Key_9: '9', Qt.Key_0: '0'}

    self.records_form = RecordsForm(self, self.screensize)
    self.settings_form = SettingsForm(self, self.screensize)
    self.pause_form = PauseForm(self, self.screensize)
    self.info_form = InfoForm(self, self.screensize)
    self.end_form = GameEnd(self, self.screensize, 0, 0, key=0)
    self.key = False

    self.start_pause = 0
    self.end_pause = 0

    self.score = 0

    self.bricks = []
    self.ids = []
    self.songs = []
    self.song_1 = Song(self, self.screensize, 1)
    self.song_1.times = ['0.7234745025634766', '1.243994951248169', '1.9235103130340576',
                         '2.635852813720703', '3.363412380218506', '4.051926851272583',
                         '4.803742408752441', '5.1638453006744385', '5.515552997589111',
                         '5.875871658325195', '6.227403163909912', '7.372378349304199',
                         '7.7075653076171875', '9.16366195678711', '9.771977424621582',
                         '10.219284772872925', '10.587011098861694', '12.051957130432129',
                         '13.163301467895508', '13.516071557998657', '14.203255653381348',
                         '15.020211219787598', '15.611274242401123', '16.395256757736206',
                         '17.067310094833374', '18.227240562438965', '18.572246313095093',
                         '18.91554856300354', '19.27506375312805', '19.627299070358276',
                         '19.99530339241028', '20.371569871902466', '21.091155767440796',
                         '21.4433491230011', '21.795762062072754', '22.195345163345337',
                         '22.54736876487732', '22.89157199859619', '23.252382278442383',
                         '24.019596338272095', '24.33919906616211', '24.659162521362305',
                         '25.059515237808228', '25.435572385787964', '25.787761211395264',
                         '26.172325611114502', '26.899561882019043', '27.22772240638733',
                         '27.571619749069214', '28.299562454223633', '28.62679362297058',
                         '29.03528881072998', '29.771687984466553', '30.132356882095337',
                         '30.499563694000244', '30.859466075897217', '31.24346160888672',
                         '31.603193283081055', '31.955438375473022', '32.69156551361084',
                         '32.98789381980896', '33.33955216407776', '33.70757555961609',
                         '34.419565200805664', '35.17936563491821', '35.87588953971863', '36.66833257675171',
                         '37.45972228050232', '38.10034155845642', '38.80336236953735']
    self.song_1.times_lines = [3, 2, 1, 0, 2, 3, 0, 1, 2, 0,
                               3, 1, 2, 0, 3, 2, 1, 0, 3, 2,
                               1, 3, 0, 1, 2, 0, 3, 1, 0, 2,
                               1, 3, 0, 2, 1, 3, 2, 1, 0, 2,
                               3, 0, 1, 3, 2, 1, 3, 2, 1, 3,
                               0, 2, 3, 0, 2, 1, 3, 0, 1, 3,
                               0, 1, 3, 2, 0, 1, 2, 3, 1, 0]
    self.song_1.fname = 'Music\\Гравити Фолз.mp3'

    self.song_2 = Song(self, self.screensize, 2)
    self.song_2.times = ['0.5653388500213623', '0.9974358081817627', '1.5575623512268066', '3.805083990097046',
                         '4.277210712432861', '4.828761339187622', '7.076806306838989', '7.6048362255096436',
                         '8.108816862106323', '10.012872457504272', '10.74892520904541', '11.357351779937744',
                         '13.31779670715332', '13.972944259643555', '14.55707597732544', '16.565529346466064',
                         '17.268688917160034', '18.076871633529663', '19.845271825790405', '20.50141954421997',
                         '21.181573390960693', '23.060998678207397', '23.749154329299927', '24.48531985282898',
                         '26.221713066101074', '26.813846349716187', '27.14992332458496', '27.533010482788086',
                         '27.95810556411743', '28.34119153022766', '28.74128293991089', '29.149375438690186',
                         '29.581472635269165', '29.96555995941162', '30.34964680671692', '30.78174376487732',
                         '31.149826765060425', '31.557919025421143', '31.974013566970825', '32.34209656715393',
                         '32.77319383621216', '33.14127707481384', '33.533367395401', '33.90945076942444',
                         '34.317543745040894', '34.78965187072754', '35.189741373062134', '35.58983087539673',
                         '36.03793263435364', '36.26998591423035', '36.437023401260376', '36.749093532562256',
                         '36.97314381599426', '37.109174728393555', '37.454253911972046', '37.629292726516724',
                         '37.7893283367157', '37.99737548828125', '38.43747520446777', '38.82156181335449',
                         '39.309672832489014', '39.717763900756836', '40.117854595184326', '40.453930616378784',
                         '40.86202335357666', '41.27711725234985', '41.701213121414185', '42.06980061531067',
                         '42.533560276031494', '42.726301193237305', '42.90134119987488', '43.16540026664734',
                         '43.365445375442505', '43.7015221118927', '43.949578046798706', '44.14962363243103',
                         '44.54171133041382', '44.73393988609314', '44.910013914108276', '45.3091037273407',
                         '45.73403263092041', '45.93407702445984', '46.11711859703064', '46.46123766899109',
                         '46.893515825271606', '47.301608085632324', '47.517493724823', '47.73439598083496',
                         '47.95729064941406', '48.18934392929077', '48.589433670043945', '48.99039816856384',
                         '49.333335876464844', '49.54938459396362', '49.73342561721802', '50.14930319786072',
                         '50.54916787147522', '50.98126530647278', '51.31744575500488', '51.789960622787476',
                         '52.22205877304077', '52.64515495300293', '53.04524564743042', '53.445335149765015',
                         '53.87743282318115', '54.053473711013794', '54.34153890609741', '54.54958629608154',
                         '54.95767855644226', '55.173725843429565', '55.5098021030426', '55.90189075469971',
                         '56.29398036003113', '56.67806649208069', '57.09316062927246', '57.47724747657776',
                         '57.869335651397705', '58.24542045593262', '58.73353171348572', '58.957581758499146',
                         '59.39768099784851', '59.87778949737549', '60.30188751220703', '60.709978342056274',
                         '61.08606290817261', '61.445143938064575', '61.94925832748413', '62.133299589157104',
                         '62.389358043670654', '62.70142841339111', '63.125523805618286', '63.54161882400513',
                         '63.901700258255005', '64.34179902076721', '64.68589425086975', '65.16598629951477',
                         '65.34902763366699', '65.69310474395752', '65.98117065429688', '66.36625742912292',
                         '66.81335830688477', '67.25445818901062', '67.5575258731842', '67.98162174224854',
                         '68.47773480415344', '68.66077637672424', '69.2459077835083', '69.72601628303528',
                         '70.07709670066833', '70.44517922401428', '70.81326293945312', '71.2213544845581',
                         '71.66145491600037', '72.09355235099792', '72.50964736938477', '72.88579773902893',
                         '73.31782817840576', '73.70991683006287', '74.14201593399048', '74.55811047554016',
                         '74.98120522499084', '75.36529159545898', '75.7493782043457', '76.14946842193604',
                         '76.55856108665466', '76.7656078338623', '77.02966856956482', '77.29372811317444',
                         '77.46976804733276', '77.76583433151245', '78.16592454910278', '78.59002041816711',
                         '78.95010232925415', '79.29317998886108', '79.74928307533264', '79.9093189239502',
                         '80.2053861618042', '80.58147072792053', '80.78151679039001', '81.09358739852905',
                         '81.3416428565979', '81.50167989730835', '82.14982509613037', '82.62946891784668',
                         '83.07757091522217', '83.4456536769867', '83.87775206565857', '84.24583578109741',
                         '84.67793297767639', '85.06902050971985', '85.50111865997314', '85.8772041797638',
                         '86.28529572486877', '86.70238995552063', '87.08565044403076', '87.49362969398499',
                         '87.86966037750244', '88.30964207649231', '88.70952653884888', '89.08562850952148',
                         '89.50962805747986', '89.66966438293457', '90.03762745857239', '90.20561909675598',
                         '90.67760753631592', '90.82961773872375', '90.98965406417847', '91.35759592056274',
                         '91.86158895492554', '92.26146006584167', '92.74162220954895', '92.89360928535461',
                         '93.30988073348999', '93.50992631912231', '93.94902539253235', '94.12506484985352',
                         '94.59767293930054', '94.96575498580933', '95.32583689689636', '95.62190318107605',
                         '96.06200385093689', '96.23704266548157', '96.6931459903717', '97.18125677108765',
                         '97.64536094665527', '98.02144646644592', '98.43754005432129', '98.89364457130432',
                         '99.28573274612427', '99.67782044410706', '100.06090712547302', '100.44599413871765',
                         '100.861088514328', '101.28518390655518', '101.73328590393066', '102.1173722743988',
                         '102.54246926307678', '102.93355679512024', '103.34165048599243', '103.71773362159729',
                         '104.14983201026917', '104.36488032341003', '104.52591705322266', '104.90200114250183',
                         '105.3260977268219', '105.7812008857727', '106.12527918815613', '106.55837655067444',
                         '106.93346118927002', '107.3415539264679', '107.78165364265442', '108.16574025154114',
                         '108.50981760025024', '108.86189675331116', '109.30999851226807', '109.81311202049255',
                         '110.1811957359314', '110.59028744697571', '111.00538325309753', '111.41347479820251',
                         '111.78955864906311', '112.22965931892395', '112.60574316978455', '113.03784251213074',
                         '113.40492510795593', '113.83802318572998', '114.26211881637573', '114.68621492385864',
                         '115.02228951454163', '115.47739338874817', '115.94949984550476', '116.30157971382141',
                         '116.70967173576355', '117.12576603889465', '117.50185012817383', '117.90194177627563',
                         '118.270024061203', '118.6861183643341', '119.1092140674591', '119.50130295753479',
                         '119.89339184761047', '120.30949401855469', '120.718186378479', '121.15743613243103',
                         '121.92527198791504', '122.66208004951477', '123.25420761108398', '124.2624351978302',
                         '125.06962656974792', '125.86181116104126', '126.51796388626099', '127.45414733886719',
                         '128.35814571380615', '129.14945697784424', '129.88589143753052', '130.81310963630676',
                         '131.65330171585083', '132.41347336769104', '133.2776665687561', '133.72576904296875',
                         '134.11785769462585', '134.47793817520142', '134.9100365638733', '135.1010799407959',
                         '135.2691171169281', '135.6221969127655', '136.101309299469', '136.56531763076782',
                         '136.97341346740723', '137.3493435382843', '137.7334303855896', '138.13331866264343',
                         '138.2933554649353', '138.65344405174255', '139.0134983062744', '139.39759039878845',
                         '139.73351526260376', '140.17361450195312', '140.52569437026978', '140.88578271865845',
                         '141.38987135887146', '141.52490210533142', '141.8539764881134', '142.21405863761902',
                         '142.55766320228577', '142.98176169395447', '143.37385082244873', '143.77394604682922',
                         '144.13402605056763', '144.65414667129517', '144.7971796989441', '145.1972758769989',
                         '145.46933722496033', '145.8774299621582', '146.26951789855957', '146.64560627937317',
                         '147.04570198059082', '147.397780418396', '147.58982467651367', '147.89389967918396',
                         '148.06193828582764', '148.4300193786621', '148.75809478759766', '149.13317894935608',
                         '149.53324580192566', '149.92533445358276', '150.34989190101624', '150.70997524261475',
                         '151.11006832122803', '151.27711367607117', '151.58184432983398', '151.94192600250244',
                         '152.29401183128357', '152.74111247062683', '153.17319560050964', '153.5742859840393',
                         '153.94937205314636', '154.39747262001038', '154.54950618743896', '154.97360229492188',
                         '155.27787494659424', '155.49403071403503', '155.82929682731628', '156.17403101921082',
                         '156.49415016174316', '156.86923742294312', '157.2052788734436', '157.61335635185242',
                         '157.76532793045044', '158.1973283290863', '158.36517190933228', '158.74923610687256',
                         '158.92536520957947', '159.31783032417297', '159.67731094360352', '160.09396767616272',
                         '160.44598078727722', '160.8620777130127', '161.22977447509766', '161.59728813171387',
                         '162.02189707756042', '162.52602887153625', '162.92516779899597', '163.29399013519287',
                         '163.68635416030884', '164.1260108947754', '164.4861068725586', '164.89337491989136',
                         '165.30178689956665', '165.72588562965393', '166.11001205444336', '166.55800104141235',
                         '166.95802855491638', '167.34919047355652', '167.76607489585876', '168.11000442504883',
                         '168.54985928535461', '168.98130655288696', '169.35786867141724', '169.7578558921814',
                         '170.11816382408142', '170.54913020133972', '170.98216891288757', '171.37391185760498',
                         '171.79019331932068', '172.19792938232422', '172.62122082710266', '173.02151727676392',
                         '173.4214632511139', '173.82219767570496', '174.23818731307983', '174.61321759223938',
                         '175.0378179550171', '175.46998143196106', '175.88607597351074', '176.30200910568237',
                         '176.67010378837585', '177.10132789611816', '177.49401903152466', '177.91803789138794',
                         '178.30225276947021', '178.7169246673584', '179.0777726173401', '179.47728061676025',
                         '179.86937284469604', '180.27822732925415', '180.64594101905823', '181.08588218688965',
                         '181.50111627578735', '181.91717672348022', '182.31727504730225', '182.75790929794312',
                         '183.15010976791382', '183.53315663337708', '183.91725420951843', '184.36531448364258',
                         '184.77332949638367', '185.16514539718628', '185.59032082557678', '186.00551438331604',
                         '186.3892467021942', '186.78933930397034', '187.1653015613556', '187.5653350353241',
                         '187.90935921669006', '188.42143321037292', '188.82132482528687', '189.2452962398529',
                         '189.67734289169312', '190.05424189567566', '190.43730998039246', '190.8372631072998',
                         '191.24534630775452', '191.64538288116455', '192.02155423164368', '192.429381608963',
                         '192.81344652175903', '193.277845621109', '193.62247252464294', '194.05357718467712',
                         '194.47732591629028', '194.90202641487122', '195.2221007347107', '195.66154885292053',
                         '196.05333971977234', '196.51738023757935', '196.89334774017334', '197.30937314033508',
                         '197.70235633850098', '198.1653881072998', '198.5253348350525', '198.9336130619049',
                         '199.30976009368896', '199.76601719856262', '200.16533422470093', '200.52541542053223',
                         '200.86168789863586', '201.22150588035583', '201.76566648483276']
    self.song_2.times_lines = [1, 2, 0, 1, 2, 0, 3, 1, 2, 0, 1, 3, 0,
                               2, 1, 0, 2, 1, 3, 2, 0, 1, 3, 2, 1, 3,
                               0, 2, 3, 1, 0, 2, 1, 0, 2, 3, 1, 2, 3,
                               1, 0, 3, 1, 0, 2, 1, 3, 0, 1, 3, 0, 1,
                               2, 0, 1, 2, 0, 3, 1, 0, 2, 3, 0, 1, 2,
                               0, 1, 2, 0, 1, 2, 0, 1, 2, 3, 0, 1, 3,
                               2, 0, 3, 1, 2, 3, 0, 2, 1, 3, 2, 0, 3,
                               2, 0, 1, 3, 2, 1, 0, 3, 1, 0, 3, 1, 2,
                               0, 1, 2, 3, 0, 2, 3, 0, 1, 3, 2, 1, 3,
                               0, 1, 2, 3, 1, 0, 2, 1, 3, 0, 2, 1, 0,
                               2, 3, 1, 0, 3, 2, 0, 1, 3, 2, 1, 3, 0,
                               2, 3, 1, 0, 2, 1, 3, 0, 1, 2, 3, 0, 1,
                               3, 2, 0, 1, 3, 0, 1, 2, 3, 0, 2, 1, 0,
                               2, 3, 0, 2, 3, 0, 2, 1, 0, 3, 1, 0, 3,
                               1, 2, 3, 1, 2, 3, 0, 1, 2, 0, 3, 2, 0,
                               3, 1, 0, 2, 1, 3, 2, 1, 3, 0, 1, 3, 2,
                               0, 3, 1, 2, 0, 3, 2, 0, 1, 3, 2, 1, 0,
                               3, 1, 2, 0, 1, 2, 3, 0, 1, 2, 0, 1, 3,
                               0, 1, 2, 0, 3, 1, 2, 3, 1, 0, 3, 1, 2,
                               0, 1, 2, 3, 1, 2, 3, 0, 2, 3, 0, 1, 2,
                               0, 1, 2, 3, 0, 2, 3, 0, 2, 3, 1, 0, 2,
                               1, 3, 2, 1, 3, 0, 2, 3, 0, 1, 3, 2, 1,
                               3, 2, 1, 3, 2, 0, 1, 2, 0, 3, 2, 0, 1,
                               3, 0, 2, 3, 1, 0, 3, 2, 0, 3, 2, 1, 0,
                               3, 1, 2, 0, 1, 2, 0, 3, 2, 0, 1, 2, 0,
                               1, 2, 0, 3, 1, 0, 2, 1, 3, 2, 0, 3, 1,
                               0, 2, 3, 0, 2, 1, 0, 2, 1, 3, 0, 1, 3,
                               2, 0, 3, 2, 0, 3, 1, 0, 3, 1, 0, 3, 2,
                               0, 3, 1, 0, 3, 1, 2, 3, 1, 2, 0, 3, 2,
                               0, 3, 1, 2, 0, 3, 2, 1, 3, 2, 0, 3, 2,
                               1, 0, 3, 2, 1, 3, 2, 1, 0, 2, 1, 0, 3,
                               2, 0, 3, 2, 0, 1, 2, 0, 3, 1, 0, 2, 3,
                               1, 2, 3, 0, 2, 3, 0, 2, 3, 1, 0, 2, 1,
                               3, 0, 2, 1, 3, 0, 1, 2, 0, 1, 3, 0, 2,
                               3, 0, 1, 3, 2, 0, 3, 2, 0, 1, 3, 0, 2,
                               3, 0, 1, 3, 2, 0, 3, 1, 2, 0, 1, 3, 2,
                               0, 1, 2, 3, 0, 2, 1, 0, 3, 1, 0]
    self.song_2.fname = 'Music\\Три дня дождя - Демоны.mp3'

    self.songs = [self.song_1, self.song_2]


def opredelenie_main_menu(self):
    self.background = QLabel(self)
    self.background.resize(self.screensize[0], self.screensize[1])
    self.background.move(0, 0)
    self.pixmap_background = QPixmap('Images\\piano_background.jpg').scaled(self.screensize[0], self.screensize[1])
    self.background.setPixmap(self.pixmap_background)

    self.play_button = QPushButton('ИГРАТЬ', self.background)
    self.play_button.move(round(0.2 * self.screensize[0]), round(0.76 * self.screensize[1]))
    self.play_button.resize(round(0.6 * self.screensize[0]), round(0.16 * self.screensize[1]))
    self.play_button.setFont(QFont("Times", self.screensize[0] // 53, QFont.Bold))
    self.play_button.clicked.connect(self.menu_pesen)

    self.title_1 = QLabel(self.background)
    self.title_1.resize(660, 320)
    self.title_1.setText("""ЧЕРНОЕ""")
    self.title_1.setFont(QFont("Gabriola", round(self.screensize[0] // 22)))
    self.title_1.move(round(self.screensize[0] - 700) // 2, 0)
    self.title_1.setStyleSheet('color: white')

    self.title_2 = QLabel(self.background)
    self.title_2.resize(660, 320)
    self.title_2.setText("""&""")
    self.title_2.setFont(QFont("Gabriola", round(self.screensize[0] // 22)))
    self.title_2.move(round(self.screensize[0] - 100) // 2, 100)

    self.title_3 = QLabel(self.background)
    self.title_3.resize(660, 320)
    self.title_3.setText("""БЕЛОЕ""")
    self.title_3.setFont(QFont("Gabriola", round(self.screensize[0] // 22)))
    self.title_3.move(self.screensize[0] // 2, 200)

    self.icon_records = QIcon()
    self.icon_records.addPixmap(QPixmap('Images\\кубок.png'))
    self.table_of_records = QPushButton(self.background)
    self.table_of_records.resize(round(0.05 * self.screensize[0]), round(0.05 * self.screensize[0]))
    self.table_of_records.setIcon(self.icon_records)
    self.table_of_records.setIconSize(
        QSize(round(0.05 * self.screensize[0]) - 10, round(0.05 * self.screensize[0]) - 10))
    self.table_of_records.clicked.connect(self.records)

    self.icon_settings = QIcon()
    self.icon_settings.addPixmap(QPixmap('Images\\настройки.png'))
    self.settings_button = QPushButton(self.background)
    self.settings_button.resize(round(0.05 * self.screensize[0]), round(0.05 * self.screensize[0]))
    self.settings_button.move((self.screensize[0] - (round(0.05 * self.screensize[0]) * 2)), 0)
    self.settings_button.setIcon(self.icon_settings)
    self.settings_button.setIconSize(
        QSize(round(0.05 * self.screensize[0]) - 10, round(0.05 * self.screensize[0]) - 10))
    self.settings_button.clicked.connect(self.settings)

    self.icon_info = QIcon()
    self.icon_info.addPixmap(QPixmap('Images\\информация.png'))
    self.info = QPushButton(self.background)
    self.info.resize(round(0.05 * self.screensize[0]), round(0.05 * self.screensize[0]))
    self.info.move(self.screensize[0] - round(0.05 * self.screensize[0]), 0)
    self.info.setIcon(self.icon_info)
    self.info.setIconSize(QSize(round(0.05 * self.screensize[0]) - 10, round(0.05 * self.screensize[0]) - 10))
    self.info.clicked.connect(self.open_info)


def opredelenie_menu_pesen(self):
    self.play_button_2 = QPushButton(self.play_button.text(), self.background)
    self.play_button_2.setFont(self.play_button.font())
    self.play_button_2.move(round(0.5 * self.screensize[0]), round(0.76 * self.screensize[1]))
    self.play_button_2.resize(round(0.4 * self.screensize[0]), round(0.16 * self.screensize[1]))
    self.play_button_2.clicked.connect(self.song)

    self.return_icon = QIcon()
    self.return_icon.addPixmap(QPixmap('Images\\exit.png'))
    self.return_main_menu = QPushButton(self.background)
    self.return_main_menu.resize(round(0.05 * self.screensize[0]), round(0.05 * self.screensize[0]))
    self.return_main_menu.move(self.screensize[0] - round(0.05 * self.screensize[0]), 0)
    self.return_main_menu.setIcon(self.return_icon)
    self.return_main_menu.setIconSize(
        QSize(round(0.05 * self.screensize[0]) - 10, round(0.05 * self.screensize[0]) - 10))
    self.return_main_menu.clicked.connect(self.main_menu)

    self.choice_songs = QComboBox(self.background)
    self.choice_songs.resize(0.4 * self.screensize[0], 0.1 * self.screensize[1])
    self.choice_songs.move(0.05 * self.screensize[0], 0.25 * self.screensize[1])
    self.con = sqlite3.connect('records.db')
    self.cur = self.con.cursor()
    self.choice_songs.addItem('Добавить песню')
    self.data = self.cur.execute("""SELECT Название, Рекорд, Скорость FROM songs""").fetchall()
    for i in range(len(self.cur.execute("""SELECT id FROM songs""").fetchall())):
        item = f'{self.data[i][0]}       Рекорд: {self.data[i][1]}      Скорость: {self.data[i][2]}'
        self.choice_songs.addItem(item)
    self.choice_songs.setFont(QFont('Times', 22))


def opredelenie_song(self):
    self.song_background = QLabel(self)
    self.song_background.resize(self.screensize[0], self.screensize[1])
    self.song_background.move(0, 0)
    self.pixmap_song_background = QPixmap('Images\\song_background_update.png').scaled(self.screensize[0],
                                                                                       self.screensize[1])
    self.song_background.setPixmap(self.pixmap_song_background)
    self.pause = QPushButton(self.song_background)
    self.icon_pause = QIcon()
    self.icon_pause.addPixmap(QPixmap('Images\\pause.png'))
    self.pause.resize(round(0.05 * self.screensize[0]), round(0.05 * self.screensize[0]))
    self.pause.move(self.screensize[0] - round(0.05 * self.screensize[0]), 0)
    self.pause.setIcon(self.icon_pause)
    self.pause.setIconSize(
        QSize(round(0.05 * self.screensize[0]) - 10, round(0.05 * self.screensize[0]) - 10))
    self.pause.clicked.connect(self.open_pause)

    self.label_game_1 = QLabel(self.song_background)
    self.label_game_1.move(self.screensize[0] * 0.1, self.screensize[1] * 0.05)
    self.label_game_1.resize(self.screensize[0] * 0.8, self.screensize[1] * 0.03)
    self.label_game_1.setStyleSheet('background-color: rgb(0, 0, 0)')

    self.label_game_2 = QLabel(self.song_background)
    self.label_game_2.move(self.screensize[0] * 0.1, self.screensize[1] * 0.05)
    self.label_game_2.resize(self.screensize[0] * 0.02, self.screensize[1] * 0.8)
    self.label_game_2.setStyleSheet('background-color: rgb(0, 0, 0)')

    self.label_game_4 = QLabel(self.song_background)
    self.label_game_4.move(self.screensize[0] * 0.88, self.screensize[1] * 0.05)
    self.label_game_4.resize(self.screensize[0] * 0.02, self.screensize[1] * 0.8)
    self.label_game_4.setStyleSheet('background-color: rgb(0, 0, 0)')

    self.label_game_3 = QLabel(self.song_background)
    self.label_game_3.move(self.screensize[0] * 0.1, self.screensize[1] * 0.82)
    self.label_game_3.resize(self.screensize[0] * 0.8, self.screensize[1] * 0.04)
    self.label_game_3.setStyleSheet('background-color: rgb(255, 0, 0)')

    self.label_key_1 = QLabel(self.label_game_3)
    self.label_key_1.setText(self.keys[self.key_1])
    self.label_key_1.move(round(self.screensize[0] * 0.115), 5)
    self.label_key_1.setFont(QFont('Times', 14))

    self.label_key_2 = QLabel(self.label_game_3)
    self.label_key_2.setText(self.keys[self.key_2])
    self.label_key_2.move(round(self.screensize[0] * 0.305), 5)
    self.label_key_2.setFont(QFont('Times', 14))

    self.label_key_3 = QLabel(self.label_game_3)
    self.label_key_3.setText(self.keys[self.key_3])
    self.label_key_3.move(round(self.screensize[0] * 0.495), 5)
    self.label_key_3.setFont(QFont('Times', 14))

    self.label_key_4 = QLabel(self.label_game_3)
    self.label_key_4.setText(self.keys[self.key_4])
    self.label_key_4.move(round(self.screensize[0] * 0.685), 5)
    self.label_key_4.setFont(QFont('Times', 14))

    self.label_1 = QLabel(self)
    self.label_1.move(self.screensize[0] * 0.45, self.screensize[1] * 0.34)
    self.label_1.resize(125, 200)
    self.label_1.setFont(QFont('Times', 160))
    self.label_1.setStyleSheet('background-color: rgba(255, 255, 255, 0)')
    self.label_1.setStyleSheet('color: rgb(255, 0, 0)')
    self.label_1.setVisible(False)

    self.label_press = QLabel(self.label_game_3)
    self.label_press.move(self.screensize[0] * 0.02, 0)
    self.label_press.resize(self.screensize[0] * 0.19, self.screensize[1] * 0.04)
    self.label_press.setStyleSheet('background-color: rgb(0, 0, 0)')
    self.label_press.setVisible(False)

    self.label_score = QLabel(self.song_background)
    self.label_score.move(20, 5)
    self.label_score.resize(130, 100)
    self.label_score.setText('Счет:' + '\n  ' + str(self.score))
    self.label_score.setFont(QFont('Times', 34))
    self.label_score.setStyleSheet('color: rgb(255, 0, 0)')
