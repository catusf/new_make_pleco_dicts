# Refine data extraction step by step
import json
import re
import unicodedata

# Input text data
raw = """
一	<d-prono>yī</d-prono><d-meta>Bộ: 一 - Nhất</d-meta><d-meta>Số nét: 1</d-meta><d-meta>Hán Việt: NHẤT</d-meta><d-def>1. số một; nhất; một。数目，最小的正整数。参看〖数字〗。</d-def><d-def>2. đồng nhất; như nhau。同一。</d-def><d-eg>一视同仁。</d-eg><d-eg-tsl>đối xử bình đẳng</d-eg-tsl><d-eg>咱们是一家人。</d-eg><d-eg-tsl>chúng ta là người trong một nhà.</d-eg-tsl><d-eg>你们一路走。</d-eg><d-eg-tsl>các anh cùng đi chung đường.</d-eg-tsl><d-eg>这不是一码事。</d-eg><d-eg-tsl>đây không phải là cùng một việc.</d-eg-tsl><d-def>3. cái khác; một cái khác。另一。</d-def><d-eg>番茄一名西红柿。</d-eg><d-eg-tsl>cà chua còn có tên khác là tây hồng thị.</d-eg-tsl><d-def>4. cả; đầy。全；满。</d-def><d-eg>一冬</d-eg><d-eg-tsl>cả mùa đông</d-eg-tsl><d-eg>一生</d-eg><d-eg-tsl>cả đời</d-eg-tsl><d-eg>一路平安。</d-eg><d-eg-tsl>lên đường bình yên; thượng lộ bình an.</d-eg-tsl><d-eg>一屋子人。</d-eg><d-eg-tsl>trong nhà đầy người</d-eg-tsl><d-eg>一身的汗。</d-eg><d-eg-tsl>mồ hôi đầy người</d-eg-tsl><d-def>5. một lòng; dốc lòng; chuyên nhất。专一。</d-def><d-eg>一心一意</d-eg><d-eg-tsl>toàn tâm toàn ý; một lòng một dạ.</d-eg-tsl><d-meta2>6. một lát; một chút (biểu thị làm lần một lần, hoặc động tác xảy ra ngắn ngủi, hoặc làm thử)。表示动作是一次，或表示动作是短暂的，或表示动作是试试的。</d-meta2><d-def>a. (Dùng giữa động từ lặp lại phần lớn là đőn âm)。用在重叠的动词(多为单音)中间。</d-def><d-eg>歇一歇</d-eg><d-eg-tsl>nghỉ một lát</d-eg-tsl><d-eg>笑一笑</d-eg><d-eg-tsl>cười một cái</d-eg-tsl><d-eg>让我闻一闻</d-eg><d-eg-tsl>cho tôi ngửi một chút</d-eg-tsl><d-def>b. (Dùng sau động từ, trước động lượng từ)。用在动词之后，动量词之前。</d-def><d-eg>笑一声</d-eg><d-eg-tsl>cười một tiếng</d-eg-tsl><d-eg>看一眼</d-eg><d-eg-tsl>nhìn một cái</d-eg-tsl><d-eg>让我们商量一下。</d-eg><d-eg-tsl>để chúng tôi thương lượng xem.</d-eg-tsl><d-def>7. một cái (Dùng trước động từ hoặc động lượng từ, biểu thị làm trước một động tác nào đó, phần sau thường nói về kết quả của động tác đó.)。用在动词或动量词前面，表示先做某个动作(下文说明动作结果)。</d-def><d-eg>一跳跳了过去。</d-eg><d-eg-tsl>nhảy một cái là qua ngay</d-eg-tsl><d-eg>他在旁边一站，再也不说什么。</d-eg><d-eg-tsl>nó đứng bên cạnh không nói tiếng nào.</d-eg-tsl><d-def>8. một lúc。一旦； 一经。</d-def><d-eg>一失足成千古恨。</d-eg><d-eg-tsl>nhất thất túc thành thiên cổ hận (một lần sảy chân để hận ngàn đời; một sai lầm để hận mãi mãi.)</d-eg-tsl><d-meta>Trợ từ</d-meta><d-def>9. vậy (dùng trước từ nào đó để tăng thêm ngữ khí)。助词，用在某些词前加强语气。</d-def><d-eg>一何速也。</d-eg><d-eg-tsl>sao nhanh vậy</d-eg-tsl><d-eg>为害之甚，一至于此！</d-eg><d-eg-tsl>tác hại vô cùng！</d-eg-tsl><d-meta2><d-meta-title>Ghi chú:</d-meta-title> (Chú ý: chữ &#8216;nhất&#8217; nếu đứng một mình hoặc đứng ở cuối câu thì đọc thành thanh 1, đứng trước thanh 4 thì đọc thành thanh 2, đứng trước thanh 1, 2 và 3 thì đọc thành thanh 4.)。注意：&#8216;一&#8217;字单用或在一词一句末尾念阴平，如&#8216;十一、一一得一&#8217;在去声字前念阳平，如&#8216;一半、一共&#8217;，在阴平、阳平、上声字前念去声，如&#8216;一天、一年、一点&#8217;。</d-meta2><d-def>10. nhất (một cấp độ trong âm nhạc Trung Quốc, dùng làm kí hiệu ghi âm trong nhạc phổ, tương đương với số 7 trong giản phổ.)。中国民族音乐音阶上的一级，乐谱上用做记音符号，相当于简谱的'7ò'。参看〖工尺〗。</d-def><d-meta2><d-meta-title>Từ ghép:</d-meta-title><br>一把手、一把死拿、一把抓、一百一、一败涂地、一般、一般见识、一斑、一板一眼、一半、一…半…、一半天、一包在内、一辈子、一本万利、一本正经、一鼻孔出气、一笔带过、一笔勾销、一笔抹杀、一臂之力、一边、一边倒、一表非凡、一表人才、一并、一波三折、一波未平，一波又起、一…不…、一不做，二不休、一步登天、一步一个脚印儿、一差二错、一刹那、一刬、一?、一倡百和、一唱一和、一朝天子一朝臣、一尘不染、一成不变、一程子、一筹、一筹莫展、一触即发、一触即溃、一锤定音、一锤子买卖、一次能源、一次性、一从、一蹴而就、一搭两用儿、一带、一旦、一刀两断、一刀切、一道、一得之功、一得之愚、一点儿、一丁点儿、一定、一定之规、一动、一度、一端、一多半、一…而…、一而再，再而三、一二、一…二…、一二·九运动、一发、一发千钧、一帆风顺、一反常态、一风吹、一概、一概而论、一干、一竿子到底、一个巴掌拍不响、一个劲儿、一个萝卜一个坑儿、一个心眼儿、一共、一股劲儿、一股脑儿、一鼓作气、一贯、一棍子打死、一锅端、一锅粥、一锅煮、一国三公、一呼百应、一忽儿、一晃、一晃、一会儿、一己、一技之长、一家之言、一见如故、一见钟情、一箭双雕、一经、一径、一…就…、一举、一举两得、一蹶不振、一刻、一空、一孔之见、一口、一口气、一块儿、一来二去、一览、一览表、一揽子、一劳永逸、一力、一例、一连、一连串、一连气儿、一了百了、一鳞半爪、一零儿、一流、一溜风、一溜儿、一溜歪斜、一溜烟、一路、一律、一落千丈、一马当先、一马平川、一脉相传、一毛不拔、一门心思、一面、一面儿理、一面之词、一面之交、一鸣惊人、一命呜呼、一木难支、一目了然、一目十行、一年到头、一年生、一念之差、一诺千金、一拍即合、一盘棋、一盘散沙、一旁、一炮打响、一偏、一片冰心、一瞥、一贫如洗、一品锅、一品红、一暴十寒、一齐、一起、一气、一气呵成、一窍不通、一切、一清早、一穷二白、一丘之貉、一人得道，鸡犬升天、一任、一仍旧贯、一日千里、一日三秋、一日之雅、一如、一如既往、一色、一霎、一身、一身两役、一身是胆、一神教、一审、一生、一失足成千古恨、一时、一时半会儿、一时一刻、一世、一事、一事无成、一视同仁、一是一，二是二、一手、一手一足、一手遮天、一水儿、一顺儿、一瞬、一丝、一丝不苟、一丝不挂、一丝一毫、一死儿、一似、一塌刮子、一塌糊涂、一潭死水、一体、一天、一天到晚、一条龙、一条藤儿、一条心、一同、一统、一通、一头、一头儿沉、一团和气、一团漆黑、一团糟、一退六二五、一碗水端平、一网打尽、一往情深、一往无前、一望无际、一味、一文不名、一窝蜂、一无、一无是处、一无所有、一五一十、一物降一物、一息尚存、一席话、一席之地、一系列、一下、一线、一相情愿、一向、一小儿、一笑置之、一些、一泻千里、一蟹不如一蟹、一心、一心一德、一心一意、一新、一星半点儿、一星儿、一行、一言既出，驷马难追、一言堂、一言以蔽之、一氧化碳、一样、一叶弊目、一叶知秋、一一、一…一…、一衣带水、一意孤行、一应、一隅、一隅三反、一语破的、一元化、一元论、一再、一…再…、一早、一朝、一朝一夕、一针见血、一枕黄粱、一阵、一阵风、一知半解、一直、一纸空文、一致、一掷千金、一准、一字长蛇阵、一字千金、一字一板、一总</d-meta2><d-prono>yí</d-prono><d-meta>Bộ: 一(Nhất)</d-meta><d-meta>Hán Việt: NHẤT</d-meta><d-def>số một (xem '一')。见'一' (yī)。</d-def><d-prono>ý</d-prono><d-meta>Bộ: 一(Nhất)</d-meta><d-meta>Hán Việt: NHẤT</d-meta><d-def>một; nhất。见'一'yī。</d-def>
一?二八事变	<d-prono>yī·èrbā shìbiàn</d-prono><d-def>Biến cố ngày 28 tháng 1</d-def><d-meta2>一•二八事变（日本称上海事变或第一次上海事变、淞沪战争）1932年于中国上海发生，是日本于1931年九一八事变后，为了把由北向南的入侵计划改变为由东向西，以有利于长期作战，而在上海主动发起的一场战役，1932年1月28日夜间，日本侵略军由租界向闸北一带进攻，驻守上海的19路军奋起抵抗，开始了淞沪抗战。时间长达一个多月。由于国民党政府坚持不抵抗政策，破坏淞沪抗战，19路军被迫撤离上海。在英、美、法等国调停下，国民党政府和日本签订了卖国的《淞沪停战协定》。</d-meta2><d-meta2>Biến cố ngày 28 tháng 1 (Nhật gọi là Biến cố Thượng Hải, Biến cố Thượng Hải lần thứ nhất, Chiến tranh Tùng Hộ) diễn ra vào năm 1932 tại Thượng Hải, Trung Quốc. Sau Biến cố ngày 18 tháng 9 năm 1931, Nhật đổi kế hoạc xâm lược từ bắc xuống nam thành từ đông sang tây. Đêm 28 tháng 1, Nhật chủ động tấn công từ vùng tô giới đến Hạp Bắc, tuyến quân 19 đóng giữ ở Thượng Hải vùng lên chống cự, bắt đầu cuộc kháng chiến Tùng Hộ, kéo dài hơn 1 tháng. Vì chính sách kiên quyết không chống cự của chính quyền Quốc Dân Đảng nên đã phá hỏng cuộc kháng chiến Tùng Hộ, tuyến quân 19 bị dồn rút lui khỏi Thượng Hải. Dưới sự điều đình của ba nước Anh, Mỹ và Pháp, chính phủ Quốc Dân Đảng đã ký hiệp định bán nước “Hiệp định đình chiến Tùng Hộ” với quân Nhật.</d-meta2>
塥	<d-prono>gé</d-prono><d-meta>Bộ: 土 - Thổ</d-meta><d-meta>Số nét: 13</d-meta><d-meta>Hán Việt: CÁCH</d-meta><d-def>1.đất cát (thường dùng làm tên đất)。沙地。多用于地名，如青草塥(在安徽)。</d-def><d-def>2.sa mạc。沙碛。</d-def>
塨	<d-prono>gōng</d-prono><d-meta>Bộ: 土 - Thổ</d-meta><d-meta>Số nét: 13</d-meta><d-meta>Hán Việt: CUNG</d-meta><d-def>Cung (dùng làm tên người, Lý Cung, học giả đầu thời Thanh, Trung Quốc)。用于人名，李塨，清初学者。</d-def>
"""  # noqa: E501

MAX_LINES = 5000000000000


def split_and_clean_def(line):
    # Split the input string into individual lines

    # # Match the split pattern with Chinese characters
    # SPLIT_DEF_PATTERN = r"(.*?)((?:[\u4e00-\u9fff]+.*))"
    # STRIP_CHARS = "。；，"

    # match = re.match(SPLIT_DEF_PATTERN, line.strip())
    # result = {}
    try:
        items = line.split("。")
        definition = items[0]
        chinese_definition = items[1]
    except:
        definition = line
        chinese_definition = ""

    return {
        "vietnamese": replace_html_ref(definition),
        "chinese": replace_html_ref(chinese_definition),
    }


lines = [line.strip() for line in raw.split("\n") if line.strip()]

with open("lv/LacViet-zh-vi.html.tab", "r", encoding="utf-8") as file:
    lines = file.readlines()

    print(f"Read {len(lines)} lines")

data_array = {}

### Tách ra <d-meta2><d-meta-title>: Bắt đầu ghi chú
### Sau đó thay <d-meta2> bằng <d-def>
### Not a valid block: <d-prono><d-meta2><d-meta-title>Từ phồn thể:</d-meta-title> (與)</d-meta2>
### Có TH pinyin bi5 sai 一事	<d-prono>yīsh́</d-prono>


def html_char_to_unicode(match):
    char_code = int(match.group(1))  # Extract the number
    return chr(char_code)  # Convert to Unicode characte


def has_combining_diacritical_marks(s):
    # Define the Unicode range for Combining Diacritical Marks
    combining_diacritics_range = re.compile(r"[\u0300-\u036F]")
    # Search for any character in the range
    return bool(combining_diacritics_range.search(s))


def replace_html_ref(text):
    # Replace HTML references like &#466;
    # Then normalize it do the dicritical mark will be combined too

    text = text.replace("&#8220;", "").replace("&#8221;", "")

    text = re.sub(r"&#(\d+);", html_char_to_unicode, text)
    # new_text1 = unicodedata.normalize("NFC", new_text)

    return text


def normalize_nfc(text):
    return unicodedata.normalize("NFC", text)


issues = []

# Extract character
for line in lines[:MAX_LINES]:
    # line = re.sub(
    #     r"&#(\d+);", html_char_to_unicode, line
    # )  # Replace HTML references like &#466;

    # Input text data

    # Initialize structure
    char_result = []

    # Extract character
    character, body = line.strip().split("\t")
    if not character:
        print(f"Invalid line: {line}")
        continue
    # char_result["character"] = character

    PRO_MARK = "<d-prono>"

    blocks = body.strip().split(PRO_MARK)

    if len(blocks) <= 1:
        print(f"Not a valid definition line: {line}")
        continue
    else:
        pronunciation_blocks = [
            PRO_MARK + item.strip() for item in blocks if item.strip()
        ]

    pro_results = []

    for block in pronunciation_blocks:
        result = []
        # Extract pronunciations and definitions
        pronunciations = re.findall(r"<d-prono>(.+?)</d-prono>", block)

        if not pronunciations:
            print(f"Not a valid block: {block}")
            continue

        assert len(pronunciations) == 1

        pronunciation = pronunciations[0]
        meta_blocks = re.findall(r"<d-meta>(.+?)</d-meta>", block)
        definitions = re.findall(r"<d-def>(.+?)</d-def>", block)
        examples = re.findall(r"<d-eg>(.+?)</d-eg>", block)
        translations = re.findall(r"<d-eg-tsl>(.+?)</d-eg-tsl>", block)
        notes = re.findall(r"<d-meta2>(.+?)</d-meta2>", block)

        if has_combining_diacritical_marks(replace_html_ref(pronunciation)):
            issues.append((character, replace_html_ref(pronunciation)))

        # Group data under pronunciations
        prono_data = {
            "pinyin": normalize_nfc(replace_html_ref(pronunciation)),
            "metadata": {},
            "definitions": [],
        }

        for meta_block in meta_blocks:
            try:
                key, value = meta_block.split(":")
            except:
                key = meta_block
                value = ""

            prono_data["metadata"][key.strip()] = value.strip()

        # Extract definitions, examples, and translations
        for i, definition in enumerate(definitions):
            items = split_and_clean_def(definition)
            def_data = {"examples": []}
            def_data.update(items)

            # Match examples with translations
            for ex, ts in zip(examples[i:], translations[i:]):
                def_data["examples"].append({"example": ex, "translation": ts})

            prono_data["definitions"].append(def_data)

        prono_data["notes"] = notes

        # Add notes

        char_result.append(prono_data)

    # Display structured data
    # print(json.dumps(result, ensure_ascii=False, indent=4))

    data_array[character] = char_result

with open("data/lacviet_parsed.json", "w", encoding="utf-8") as file:
    json.dump(data_array, file, ensure_ascii=False, indent=4)

with open("data/pinyin_issues.json", "w", encoding="utf-8") as file:
    json.dump(issues, file, ensure_ascii=False, indent=4)

print(f"Written {len(data_array)} records")
