#!/bin/bash
# Generate sprite sheets from existing sprites for Cursed Arcana
# Each sprite sheet is a horizontal strip of frames for CSS animation

ASSETS="assets"
OUT="$ASSETS"

# ============================================================
# 1. MAGE sprite sheet (4 frames: idle → attack windup → attack peak → recover)
# ============================================================
echo "=== Making MAGE sprite sheet ==="
MAGE_SRC="$ASSETS/player_mage_flipped.png"
MAGE_DIR="/tmp/mage_frames"
mkdir -p "$MAGE_DIR"

# Get original dimensions
W=$(identify -format '%w' "$MAGE_SRC")
H=$(identify -format '%h' "$MAGE_SRC")
echo "  Mago: ${W}x${H}"

# Frame 0: idle (original)
cp "$MAGE_SRC" "$MAGE_DIR/frame0.png"

# Frame 1: slight lean forward (attack windup)
convert "$MAGE_SRC" -distort SRT '1.02,0 1.05,0.5 0,0' -crop "${W}x${H}+0+0" +repage "$MAGE_DIR/frame1.png"

# Frame 2: attack peak - lean forward + brighter
convert "$MAGE_SRC" \( -clone 0 -distort SRT '1.03,0 1.1,0.5 0,0' \) -delete 0 -crop "${W}x${H}+0+0" +repage -modulate 120,100,100 "$MAGE_DIR/frame2.png"

# Frame 3: recover back to idle  
convert "$MAGE_SRC" -distort SRT '0.98,0 1.02,-0.5 0,0' -crop "${W}x${H}+0+0" +repage "$MAGE_DIR/frame3.png"

# Combine horizontally into sprite sheet
convert "$MAGE_DIR/frame0.png" "$MAGE_DIR/frame1.png" "$MAGE_DIR/frame2.png" "$MAGE_DIR/frame3.png" +append "$OUT/mage_sheet.png"
echo "  → $OUT/mage_sheet.png ($(identify -format '%wx%h' "$OUT/mage_sheet.png"))"

# ============================================================
# 2. LICH sprite sheet (4 frames: idle → attack windup → lunge → recover)
# ============================================================
echo "=== Making LICH sprite sheet ==="
LICH_SRC="$ASSETS/enemy_lich_flipped.png"
LICH_DIR="/tmp/lich_frames"
mkdir -p "$LICH_DIR"

W=$(identify -format '%w' "$LICH_SRC")
H=$(identify -format '%h' "$LICH_SRC")
echo "  Lich: ${W}x${H}"

# Frame 0: idle (original)
cp "$LICH_SRC" "$LICH_DIR/frame0.png"

# Frame 1: lean forward (windup) - scale slightly up
convert "$LICH_SRC" -distort SRT '0.98,0 1.05,0.5 0,0' -crop "${W}x${H}+0+0" +repage "$LICH_DIR/frame1.png"

# Frame 2: attack lunge - bigger, brighter
convert "$LICH_SRC" \( -clone 0 -distort SRT '0.95,0 1.15,0.5 0,0' \) -delete 0 -crop "${W}x${H}+0+0" +repage -modulate 130,100,100 -fill red -colorize 10 "$LICH_DIR/frame2.png"

# Frame 3: recover
convert "$LICH_SRC" -distort SRT '1.02,0 0.98,-0.5 0,0' -crop "${W}x${H}+0+0" +repage "$LICH_DIR/frame3.png"

# Combine horizontally
convert "$LICH_DIR/frame0.png" "$LICH_DIR/frame1.png" "$LICH_DIR/frame2.png" "$LICH_DIR/frame3.png" +append "$OUT/lich_sheet.png"
echo "  → $OUT/lich_sheet.png ($(identify -format '%wx%h' "$OUT/lich_sheet.png"))"

# ============================================================
# 3. Magic projectile sprite sheet (4 frames growing/shrinking)
# ============================================================
echo "=== Making MAGIC BOLT sprite sheet ==="
BOLT_DIR="/tmp/bolt_frames"
mkdir -p "$BOLT_DIR"

# Create a small magic bolt image from the mage (crop purple area)
# Generate a simple bolt with ImageMagick
for i in 0 1 2 3; do
  S=$((40 + i * 12))
  O=$(echo "0.3 + $i * 0.15" | bc)
  convert -size ${S}x${S} xc:none \
    -fill 'rgba(106,13,173,0.8)' -draw "circle $((S/2)),$((S/2)) $((S/2)),2" \
    -fill 'rgba(150,50,200,0.3)' -draw "circle $((S/2)),$((S/2)) $((S/2-5)),2" \
    -fill 'rgba(200,100,255,0.6)' -draw "circle $((S/2)),$((S/2)) $((S/4)),$((S/4))" \
    "$BOLT_DIR/bolt${i}.png"
done

# Combine
convert "$BOLT_DIR/bolt0.png" "$BOLT_DIR/bolt1.png" "$BOLT_DIR/bolt2.png" "$BOLT_DIR/bolt3.png" +append "$OUT/bolt_sheet.png"
echo "  → $OUT/bolt_sheet.png ($(identify -format '%wx%h' "$OUT/bolt_sheet.png"))"

# ============================================================
# Cleanup
# ============================================================
rm -rf /tmp/mage_frames /tmp/lich_frames /tmp/bolt_frames

echo ""
echo "=== DONE ==="
ls -la "$OUT/"*_sheet.png