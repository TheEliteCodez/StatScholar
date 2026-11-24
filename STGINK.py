# Compact 5x7 glyphs provide labels at actual graph coordinates. PlotLib's
# text_at positions whole rows, so it cannot attach labels to individual marks.
_CHARS='0123456789CVTSHPE=-+./etzxbarphdl'
_GLYPHS=b'>QIE>\x00B\x7f@\x00BaQIF!AEK1\x18\x14\x12\x7f\x10\'EEE9<JII0\x01q\t\x05\x036III6\x06II)\x1e>AAA"\x1f @ \x1f\x01\x01\x7f\x01\x01FIII1\x7f\x08\x08\x08\x7f\x7f\t\t\t\x06\x7fIIIA\x14\x14\x14\x14\x14\x08\x08\x08\x08\x08\x08\x08>\x08\x08\x00``\x00\x00 \x10\x08\x04\x028TTT\x18\x04?D@ DdTLDD(\x10(D\x7fHDD8 TTTx|\x08\x04\x04\x08|\x14\x14\x14\x08\x7f\x08\x04\x04x8DDH\x7f\x00A\x7f@\x00'

def line(plt,x1,y1,x2,y2):
  plt.line(x1,209-y1,x2,209-y2)

def ink(plt,text,x,y,color):
  x=max(1,min(318-(6*len(text)-1),x))
  plt.pen('medium','solid');plt.color(255,255,255)
  for row in range(-1,8): line(plt,x-1,y+row,x+6*len(text),y+row)
  plt.pen('thin','solid');plt.color(*color)
  for char in text:
    index=_CHARS.find(char)
    if index<0:index=_CHARS.find(char.lower())
    glyph=_GLYPHS[5*index:5*index+5] if index>=0 else b'\x00'*5
    for col,bits in enumerate(glyph):
      for row in range(7):
        if bits & (1<<row):
          line(plt,x+col,y+row,x+col+.3,y+row)
          if row<6 and bits & (1<<(row+1)):
            line(plt,x+col,y+row,x+col,y+row+1)
          if col<4:
            for r in range(max(0,row-1),min(7,row+2)):
              if glyph[col+1] & (1<<r): line(plt,x+col,y+row,x+col+1,y+r)
    x+=6

def tag(plt,text,x,y,color,boxes):
  width=6*len(text)-1
  left=max(1,min(318-width,x+6 if x>=159.5 else x-width-6))
  if y<55: left=1 if x<159.5 else 318-width
  wanted=max(36,min(82,y-15))
  for top in (wanted,36,46,56,66,76,86):
    if all(left+width+2<a or left>b+2 or top+9<c or top>d+2 for a,b,c,d in boxes): break
  boxes.append((left,left+width,top,top+7))
  plt.color(*color)
  line(plt,left+width/2,top+8,x,y)
  ink(plt,text,left,top,color)
