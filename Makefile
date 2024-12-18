setup:
	pip install uv
	uv sync
	playwright install chromium --with-deps --only-shell

clean:
	git clean -fdx