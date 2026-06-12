import re
with open("doc/ja/classkeyhac__keymap_1_1_keymap.html", encoding="utf-8") as f:
    text = f.read()
matches = re.findall(r'<td class="memItemRight" valign="bottom">.*?<a.*?>(.*?)</a>', text)
for m in matches:
    print(m)
