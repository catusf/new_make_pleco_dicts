setup:
	pip install uv
	uv sync
	playwright install chromium --with-deps --only-shell

clean:
	git clean -fdx

scrape_first:
	uv run python scrape_hanzii_net-first.py

scrape_second:
	uv run python scrape_hanzii_net-second.py

%.json: %.json.bz2
	@if [ ! -f $@ ] || [ $< -nt $@ ]; then \
	    bunzip2 -f -k $<; \
	fi

dict/TrungViet-big.txt: data/new_reccommendations.json data/dict_data.json
	uv run python make_trung_viet_dict.py --dict-size=big

tv_big: dict/TrungViet-big.txt

tv_mid:
	uv run python make_trung_viet_dict.py --dict-size=mid

tv_small:
	uv run python make_trung_viet_dict.py --dict-size=small

tv_all: tv_big tv_mid tv_small

lacviet:
#	uv run python lacviet_extract.py
	uv run python lacviet_fix_data.py
	uv run python lacviet_make_dict.py

to_html:
	uv run python pleco_to_html_tsv.py

to_bz2:
	bzip2 -z -f dict/TrungViet-big.txt
	bzip2 -z -f dict/TrungViet-big.tab

gen_lv_tab:
#	pyglossary --remove-html=script,a,span,link,span lv/LacViet-vi-zh.ifo tests/lv/LacViet-vi-zh.html.tab
	pyglossary --remove-html=script,a,span,link,span lv/LacViet-zh-vi.ifo tests/lv/LacViet-zh-vi.html.tab

gen_lv_raw:
#	pyglossary tests/lv/LacViet-vi-zh.ifo lv/LacViet-vi-zh.tab
	pyglossary lv/LacViet-zh-vi.ifo lv/LacViet-zh-vi.tab
	
