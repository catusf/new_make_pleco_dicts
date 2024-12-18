for %f in (dict\*.tab) do pyglossary --ui=none --read-format=Tabfile --write-format=Yomichan --source-lang=zh --target-lang=vi --name="%~nf" "%f" "dict\%~nf.zip"
