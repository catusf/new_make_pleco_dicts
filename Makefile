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