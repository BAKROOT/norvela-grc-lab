#!/usr/bin/env bash
# Verify the GRC lab is up. Run from anywhere.
set -uo pipefail

ok=0; bad=0
check() {
  local name="$1" url="$2" expect="${3:-}"
  local code
  code=$(curl -sk -o /dev/null -w '%{http_code}' --max-time 6 "$url" 2>/dev/null) || code="000"
  if [[ "$code" =~ ^(200|302|301|401|403)$ ]]; then
    printf '  \033[32m OK \033[0m %-24s %s (HTTP %s)\n' "$name" "$url" "$code"; ok=$((ok+1))
  else
    printf '  \033[31mDOWN\033[0m %-24s %s %s\n' "$name" "$url" "${expect:+— $expect}"; bad=$((bad+1))
  fi
}

echo
echo "GRC LAB HEALTHCHECK"
echo "==================="
echo
echo "Core GRC platform:"
check "CISO Assistant"  "https://localhost:8443"  "start it from its own repo: ./docker-compose.sh"
check "SimpleRisk"      "http://localhost:8080"   "optional"
echo
echo "Assessment targets:"
check "Juice Shop"      "http://localhost:3000"
check "DVWA"            "http://localhost:8081"
echo
echo "Evidence estate:"
check "OpenSearch"      "http://localhost:9200"
check "Dashboards"      "http://localhost:5601"
check "Mailpit"         "http://localhost:8025"
echo
echo "Scanning (optional profile):"
check "GVM/OpenVAS"     "https://localhost:9392"  "docker compose --profile scanning up -d"
echo
echo "Local tooling:"
for t in prowler oscap docker python3; do
  if command -v "$t" >/dev/null 2>&1; then
    printf '  \033[32m OK \033[0m %-24s %s\n' "$t" "$(command -v "$t")"; ok=$((ok+1))
  else
    printf '  \033[33mMISS\033[0m %-24s not installed\n' "$t"
  fi
done
echo
python3 - <<'PY' 2>/dev/null || echo "  python deps: install with  pip install numpy matplotlib pandas openpyxl"
mods = ["numpy", "matplotlib", "pandas", "openpyxl"]
missing = []
for m in mods:
    try:
        __import__(m)
    except ImportError:
        missing.append(m)
print("  python deps:", "all present" if not missing else "MISSING -> " + ", ".join(missing))
PY
echo
echo "-------------------------------------------"
printf 'Reachable: %d   Not reachable: %d\n' "$ok" "$bad"
[[ $bad -eq 0 ]] && echo "Lab is ready." || echo "Bring up what you need — not everything is required for every phase."
echo
