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
	bunzip2 -f -k $<

dict/TrungViet-big.txt: data/new_reccommendations.json data/dict_data.json
	uv run python make_trung_viet_dict.py --dict-size=big

tv_big: dict/TrungViet-big.txt

tv_mid:
	uv run python make_trung_viet_dict.py --dict-size=mid

tv_small:
	uv run python make_trung_viet_dict.py --dict-size=small
