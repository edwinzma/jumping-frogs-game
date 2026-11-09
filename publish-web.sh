#!/bin/bash

set -e

if [ -z "$GOATCOUNTER_CODE" ]; then
  echo "GOATCOUNTER_CODE is not set"
  exit 1
fi

echo "Building browser version..."
python -m pygbag --build webgame

echo "Refreshing docs folder..."
rm -rf docs/*
cp -R webgame/build/web/* docs/

echo "Adding GoatCounter..."
python3 - <<PY
from pathlib import Path
import os

index = Path("docs/index.html")
html = index.read_text()

code = os.environ["GOATCOUNTER_CODE"]

snippet = f'''
<script
  data-goatcounter="https://{code}.goatcounter.com/count"
  async
  src="//gc.zgo.at/count.js">
</script>
'''

if "goatcounter.com/count" not in html:
    html = html.replace("</body>", snippet + "\n</body>")
    index.write_text(html)
    print("GoatCounter added")
else:
    print("GoatCounter already present")
PY

echo "Done."