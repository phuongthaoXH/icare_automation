#!/usr/bin/env bash
# run_tests.sh – Script chạy automated test iCare D02
set -e

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
REPORT_DIR="reports"
mkdir -p "$REPORT_DIR" screenshots

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'

echo -e "${GREEN}══════════════════════════════════════════${NC}"
echo -e "${GREEN}  iCare BHXH – Automated Test Suite      ${NC}"
echo -e "${GREEN}  $(date '+%d/%m/%Y %H:%M:%S')                      ${NC}"
echo -e "${GREEN}══════════════════════════════════════════${NC}"

MODE=${1:-"all"}
ARGS=(
  "--html=${REPORT_DIR}/report_${TIMESTAMP}.html"
  "--self-contained-html"
  "-v" "--tb=short"
)

case "$MODE" in
  smoke)      ARGS+=("-m" "smoke") ;;
  giao_dien)  ARGS+=("-m" "giao_dien") ;;
  chuc_nang)  ARGS+=("-m" "chuc_nang") ;;
  validate)   ARGS+=("-m" "validate") ;;
  phan_quyen) ARGS+=("-m" "phan_quyen") ;;
  exploratory)ARGS+=("-m" "exploratory") ;;
  login)      ARGS+=("tests/test_01_login.py") ;;
  parallel)   ARGS+=("-n" "4" "--dist=loadfile") ;;
  headed)     export HEADLESS=false ;;
  debug)      export HEADLESS=false; export SLOW_MO=800; ARGS+=("-s" "--tb=long") ;;
  all)        echo -e "${YELLOW}▶  Tất cả tests${NC}" ;;
  *)
    echo -e "${RED}Mode không hợp lệ: $MODE${NC}"
    echo "Dùng: all | smoke | giao_dien | chuc_nang | validate | phan_quyen | exploratory | login | parallel | headed | debug"
    exit 1 ;;
esac

echo -e "${YELLOW}▶  pytest ${ARGS[*]}${NC}\n"
python -m pytest "${ARGS[@]}" || EXIT_CODE=$?
EXIT_CODE=${EXIT_CODE:-0}

echo ""
echo -e "${GREEN}══════════════════════════════════════════${NC}"
[ $EXIT_CODE -eq 0 ] \
  && echo -e "${GREEN}  ✅  Tests PASSED!${NC}" \
  || echo -e "${RED}  ❌  Có FAILED tests (code: $EXIT_CODE)${NC}"
echo -e "${GREEN}  Báo cáo: ${REPORT_DIR}/report_${TIMESTAMP}.html${NC}"
echo -e "${GREEN}══════════════════════════════════════════${NC}"
exit $EXIT_CODE
