#!/usr/bin/env bash
# ==============================================================================
# build-docs.sh — Static Packaging Pipeline for Design Patterns Documentation
# Compiles 28 chapters into _site/ directory for GitHub Pages
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
SITE_DIR="${ROOT_DIR}/_site"

CYAN='\033[0;36m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}🏗️ Packaging Design Patterns Living Documentation into _site/...${NC}"

# Clean existing build output
rm -rf "${SITE_DIR}"
mkdir -p "${SITE_DIR}/catalog"

# Run compiler
python3 "${SCRIPT_DIR}/build-docs.py"

# Verify critical artifacts exist
for asset in index.html style.css app.js catalog/manifest.json; do
  if [ ! -f "${SITE_DIR}/${asset}" ]; then
    echo -e "${RED}❌ Fatal: Missing compiled asset: ${SITE_DIR}/${asset}${NC}"
    exit 1
  fi
done

# Touch .nojekyll so GitHub Pages does not run Jekyll processing
touch "${SITE_DIR}/.nojekyll"

BUNDLE_SIZE_MB=$(du -sm "${SITE_DIR}" | cut -f1)
echo -e "${GREEN}✅ Build succeeded! Static bundle packaged into _site/ (${BUNDLE_SIZE_MB}MB).${NC}"
