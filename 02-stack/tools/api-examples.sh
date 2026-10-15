#!/usr/bin/env bash
# CISO Assistant REST API — examples for the Norvela lab.
#
# Creates the "Norvela Pay" domain, the five perimeters, and imports
# 03-workbooks/assets.csv as assets. Read it before you run it: driving the
# GRC platform through its API is a portfolio skill in its own right.
#
# Prerequisites
#   1. CISO Assistant running at https://localhost:8443 (see SETUP.md Part 1)
#   2. A Personal Access Token: profile menu -> Personal access tokens
#   3. curl and python3
#
# Usage
#   export CA_TOKEN='<your personal access token>'
#   bash tools/api-examples.sh            # run from 02-stack/
#
# Notes
#   - Auth header is "Authorization: Token <token>" — Token, NOT Bearer.
#   - Field names follow the community edition API at the time of writing.
#     If a call returns 400, check the live schema: run the backend with
#     DJANGO_DEBUG=True and open /api/schema/swagger/.
#   - -k accepts the lab's self-signed certificate. Lab only.
set -euo pipefail

BASE="${CA_URL:-https://localhost:8443}/api"
: "${CA_TOKEN:?export CA_TOKEN first (Personal Access Token from your CISO Assistant profile)}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ASSETS_CSV="${HERE}/../../03-workbooks/assets.csv"

api() {  # api METHOD PATH [JSON]
  local method="$1" path="$2" body="${3:-}"
  curl -sSk -X "$method" "${BASE}${path}" \
    -H "Authorization: Token ${CA_TOKEN}" \
    -H "Content-Type: application/json" \
    ${body:+-d "$body"}
}

json_field() { python3 -c "import sys,json; print(json.load(sys.stdin)$1)"; }

echo "== 1. Who am I? (sanity check of the token)"
api GET "/iam/current-user/" | python3 -m json.tool | head -20 || true

echo "== 2. Create the domain (a 'folder' in the API)"
DOMAIN_ID=$(api POST "/folders/" \
  '{"name":"Norvela Pay","description":"Lab domain: fictional EU payment institution"}' \
  | json_field "['id']")
echo "   domain id: ${DOMAIN_ID}"

echo "== 3. Create the five perimeters"
for p in PayRails Vault Flow Sentinel Corporate; do
  api POST "/perimeters/" \
    "{\"name\":\"${p}\",\"folder\":\"${DOMAIN_ID}\",\"lc_status\":\"in_prod\"}" \
    | json_field "['name']" | sed 's/^/   created perimeter: /'
done

echo "== 4. Import assets.csv"
# Assets that support a critical or important function are imported as
# Primary (PR); everything else as Support (SP). Challenge that mapping —
# it is a scoping decision, and Phase 2 asks you to defend it.
python3 - "$ASSETS_CSV" "$DOMAIN_ID" <<'PY' | while IFS= read -r payload; do
import csv, json, sys
path, folder = sys.argv[1], sys.argv[2]
with open(path, newline="", encoding="utf-8") as fh:
    for r in csv.DictReader(fh):
        print(json.dumps({
            "name": f"{r['asset_id']} {r['asset_name']}",
            "description": (f"{r['asset_type']} | owner: {r['owner']} | "
                            f"{r['environment']} | {r['hosting_location']} | "
                            f"source: {r['source_inventory']} | {r['notes']}"),
            "type": "PR" if r["supports_critical_or_important_function"] == "Yes" else "SP",
            "folder": folder,
        }, ensure_ascii=False))
PY
  api POST "/assets/" "$payload" | json_field ".get('name', 'ERROR: check field names in /api/schema/swagger/')" \
    | sed 's/^/   /'
done

echo "== 5. Read back what you created"
api GET "/assets/?folder=${DOMAIN_ID}" | json_field "['count']" | sed 's/^/   assets in domain: /'

cat <<'EOF'

Next steps worth automating (each is a portfolio piece):
  - POST /api/evidences/          attach OpenSCAP / Prowler reports to controls
  - POST /api/applied-controls/   register the controls you test in Phase 3
  - POST /api/risk-scenarios/     push your rebuilt register from risk-register.xlsx
EOF
