#!/usr/bin/env python3
"""Update cursed-arcana index.html to use sprite sheet animations."""
import re

with open('index.html', 'r') as f:
    html = f.read()

# =============================================================
# SECTION 1: Replace CSS animations with sprite sheet ones
# =============================================================

# Update mage-fig img styles - switch from img tag to div with background
old_mage_style = """.mage-fig{
  width:400px;height:400px;
  display:flex;align-items:center;justify-content:center;
  position:relative
}
.mage-fig img{
  height:320px;width:auto;
  object-fit:contain;image-rendering:pixelated;
  animation:mageIdle 3.2s ease-in-out infinite;
  filter:drop-shadow(0 0 40px rgba(106,13,173,0.2))
}
@keyframes mageIdle{
  0%,100%{transform:translateY(0)}
  50%{transform:translateY(-4px)}
}
.mage-fig.casting img{
  animation:mageCast 0.35s ease !important
}
@keyframes mageCast{
  0%{transform:translateX(0)}
  30%{transform:translateX(25px) scale(1.05)}
  100%{transform:translateX(0)}
}"""

new_mage_style = """.mage-fig{
  width:400px;height:400px;
  display:flex;align-items:center;justify-content:center;
  position:relative
}
.mage-fig .sprite{
  width:240px;height:320px;
  background:url(assets/mage_sheet.png) 0 0 / 960px 320px no-repeat;
  image-rendering:pixelated;
  filter:drop-shadow(0 0 40px rgba(106,13,173,0.2));
  animation:mageIdle 3.2s steps(4) infinite
}
@keyframes mageIdle{
  from{background-position:0 0}
  to{background-position:-960px 0}
}
.mage-fig.casting .sprite{
  animation:mageCast 0.35s steps(4) !important
}
@keyframes mageCast{
  from{background-position:0 0}
  to{background-position:-960px 0}
}"""

assert old_mage_style in html, "OLD MAGE STYLE NOT FOUND!"
html = html.replace(old_mage_style, new_mage_style)

# Update enemy-fig img styles
old_enemy_style = """.enemy-fig img{
  position:relative;z-index:2;
  height:340px;width:auto;
  object-fit:contain;image-rendering:pixelated;
  animation:enemyIdle 2.8s ease-in-out infinite;
  filter:drop-shadow(0 0 50px rgba(139,0,0,0.25))
}
@keyframes enemyIdle{
  0%,100%{transform:translateY(0) scale(1)}
  40%{transform:translateY(-5px) scale(1.02)}
}
.enemy-fig.attacking img{
  animation:enemyLunge 0.4s ease !important
}
@keyframes enemyLunge{
  0%{transform:translateX(0) scale(1)}
  25%{transform:translateX(-30px) scale(1.12)}
  50%{transform:translateX(10px) scale(0.95)}
  100%{transform:translateX(0) scale(1)}
}
.enemy-fig.hurt img{
  animation:enemyHurt 0.3s ease !important
}
@keyframes enemyHurt{
  0%{filter:brightness(1)}
  20%{filter:brightness(2.5) drop-shadow(0 0 30px rgba(255,0,0,0.5))}
  100%{filter:brightness(1)}
}"""

new_enemy_style = """.enemy-fig .sprite{
  position:relative;z-index:2;
  width:240px;height:340px;
  background:url(assets/lich_sheet.png) 0 0 / 960px 340px no-repeat;
  image-rendering:pixelated;
  filter:drop-shadow(0 0 50px rgba(139,0,0,0.25));
  animation:enemyIdle 2.8s steps(4) infinite
}
@keyframes enemyIdle{
  from{background-position:0 0}
  to{background-position:-960px 0}
}
.enemy-fig.attacking .sprite{
  animation:enemyAttack 0.4s steps(4) !important
}
@keyframes enemyAttack{
  from{background-position:0 0}
  to{background-position:-960px 0}
}
.enemy-fig.hurt .sprite{
  animation:enemyHurt 0.3s steps(4) !important;
  filter:brightness(2.5) drop-shadow(0 0 30px rgba(255,0,0,0.5)) !important
}
@keyframes enemyHurt{
  from{background-position:0 0}
  to{background-position:-960px 0}
}"""

assert old_enemy_style in html, "OLD ENEMY STYLE NOT FOUND!"
html = html.replace(old_enemy_style, new_enemy_style)

# =============================================================
# SECTION 2: Update HTML - replace img tags with div.sprite
# =============================================================

# Mage image
html = html.replace(
  '        <img src="assets/player_mage_flipped.png" alt="" id="mImg">',
  '        <div class="sprite" id="mImg"></div>'
)

# Enemy image 
html = html.replace(
  '        <img src="assets/enemy_lich_flipped.png" alt="" id="eImg">',
  '        <div class="sprite" id="eImg"></div>'
)

# =============================================================
# SECTION 3: Update responsive media query
# =============================================================
old_resp = """@media(max-width:600px){
  .mage-fig{width:200px;height:200px}
  .mage-fig img{height:160px}
  .enemy-fig{width:220px;height:220px}
  .enemy-fig img{height:180px}"""
new_resp = """@media(max-width:600px){
  .mage-fig{width:200px;height:200px}
  .mage-fig .sprite{width:120px;height:160px;background-size:480px 160px}
  .enemy-fig{width:220px;height:220px}
  .enemy-fig .sprite{width:120px;height:180px;background-size:480px 180px}"""

assert old_resp in html, "OLD RESPONSIVE NOT FOUND!"
html = html.replace(old_resp, new_resp)

# =============================================================
# SECTION 4: Add bolt sprite sheet to flying card animation
# =============================================================

# Update the enemy intent text to be cleaner
html = html.replace(
  '        <div class="enemy-intent" id="eIntent">🗡️ ATACAR · 6</div>',
  '        <div class="enemy-intent" id="eIntent">⚔️ ATACAR · 6</div>'
)

# =============================================================
# SECTION 5: Add magic bolt to flying card
# =============================================================
old_fc = """.fc{
  position:fixed;z-index:200;pointer-events:none;
  width:80px;height:112px;
  border:1px solid rgba(106,13,173,0.4)
}
.fc img{width:100%;height:100%;object-fit:cover;image-rendering:pixelated}"""

new_fc = """.fc{
  position:fixed;z-index:200;pointer-events:none;
  width:60px;height:80px
}
.fc .bolt{
  width:60px;height:80px;
  background:url(assets/bolt_sheet.png) 0 0 / 240px 80px no-repeat;
  image-rendering:pixelated;
  animation:boltAnim 0.3s steps(4) infinite
}
@keyframes boltAnim{
  from{background-position:0 0}
  to{background-position:-240px 0}
}"""

assert old_fc in html, "OLD FC STYLE NOT FOUND!"
html = html.replace(old_fc, new_fc)

# Update flying card HTML creation in JS
old_fc_html = "  el.innerHTML=`<img src=\"${src}\" alt=\"\">`;"
new_fc_html = "  el.innerHTML='<div class=\"bolt\"></div>';"

assert old_fc_html in html, "OLD FC HTML NOT FOUND!"
html = html.replace(old_fc_html, new_fc_html)

# =============================================================
# SECTION 6: Clean up emoticons (user wants no emoticons)
# =============================================================
html = html.replace('🔮 TU TURNO', 'TU TURNO')
html = html.replace('⚔️ TURNO ENEMIGO', 'TURNO ENEMIGO')
html = html.replace('⏭ FINALIZAR', 'FINALIZAR')
html = html.replace('↻ VOLVER A EMPEZAR', 'VOLVER A EMPEZAR')
html = html.replace('❤️ ', '')
html = html.replace('🛡️ ', '')
html = html.replace('🔮 ', '')
html = html.replace('📜 ', '')
html = html.replace('🗑️ ', '')
html = html.replace('●', '♦')

# Write back
with open('index.html', 'w') as f:
    f.write(html)

print("✅ index.html updated with sprite sheet animations!")
