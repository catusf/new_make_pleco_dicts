TODO
[ ] Fix LacViet issues

- [ ] Có nên copy các item trong TrungViet vào LacViet ko?

- [ ] Manual review pinyin in data/lacviet_parsed_issues.json

- [ ] Rules regex bị sai: "vietnamese"
   "一动不如一静": [
      {
         "definitions": [
            {
               "examples": [],
               "vietnamese": "没有把握或无益的事，还是不做为好",
               "chinese": "比喻多一事不如少一事"
            },
            {
               "examples": [],
               "vietnamese": "lấy tĩnh chế động; một sự nhịn, chín sự lành; nếu không nắm chắc hoặc thấy không có  lợi ích gì thì tốt nhất không hành động",
               "chinese": ""
            }
         ],
         "metadata": {
            "Hán Việt": "NHẤT ĐỘNG BẤT NHƯ NHẤT TĨNH"
         },

[ ] Thay git lfs bằng bz2 file (sau khi download file từ lfs)
[ ] Với các từ có nhiều cách đọc và nghĩa khác, khi export ra non-pleco thì chỉ export ra 1 line
[ ] Creats json file
[ ] Use json file to create dict
[ ] Add decompositions for char without definitions (searcher.definition_lookup(char) => none but decomposer.tree(char) or IDS => not None)
[X] Add mnemonics from https://rtega.be/chmn/
[X] Add radical info page
[X] Add Radicals order by pinyin
[X] Tạo lại Hanzii dict, bỏ bớt new line
[ ] Add non-decomposable chars list
[ ] Why decompose 朩 here while it is a ? 
[X] Add suggested item from top 5000 HSK words
[X] Store data in XML/JSON
[X] Extract examples into list
[X] Make Chinese text blue, and từ loại grey
[X] Only include items from top_24k and top_100k
[x] Use Taiwan MOE dictionary to find opposite words (antonyms)
[X] Check words that have puntuations at the end
[x] Add missing radical 丷
[x] Check missing radical in definitions such as ⺌
[x] Use function to find radical pinyin and meaning, use namedtuple
[x] Add variants from Radicals to char_dict

# Steps
[ ] Convert Thienchuu to same format
[ ] Add remaining Thienchuu
[ ] Get list on un-covered items in 75k list
[ ] Add list of HSK: All level
[ ] Lấy danh sách OpenSubstitles 
[ ] Check lenght of definitions, examples and recommedations

