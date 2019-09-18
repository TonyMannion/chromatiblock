import os
import subprocess
import sys
import argparse
from itertools import groupby
import string

# write fasta files to


def colorstr(rgb): return "#%02x%02x%02x" % (rgb[0],rgb[1],rgb[2])


color_list = [(240,163,255), (0,117,220), (153,63,0), (76,0,92), (25,25,25), (0,92,49), (43,206,72), (255,204,153),
              (128,128,128), (148,255,181), (143,124,0), (157,204,0), (194,0,136), (0,51,128), (255,164,5),
              (255,168,187), (66,102,0), (255,0,16), (94,241,242), (0,153,143), (224,255,102), (116,10,255),
              (153,0,0), (255,255,128), (255,255,0), (255,80,5)]
#pattern_list = ['circ_small', 'circ_large', 'diag_small', 'diag_large', 'dots_small', 'dots_large', 'horiz_small', 'horiz_large', 'vert_small', 'vert_large', 'cross_hatch']
pattern_list = ['horizontal', 'forward_diag', 'reverse_diag']




class scalableVectorGraphicsHTML:

    def __init__(self, height, width, svg=True, texta="Chromatiblock Figure"):
        self.height = height
        self.width = width
        if svg:
            self.out = ''
        else:
            self.out = '<!DOCTYPE html>\n' + \
    '<html>\n' + \
    '  <head>\n' + \
    '    <script src="svg-pan-zoom.min.js"></script>\n' + \
    '  </head>\n' + \
    '  <body>\n' + \
    '    <h1>' + texta + '</h1>\n' + \
    '    <div id="container" style="width: 100%; height: 800px; border:0px solid black; ">\n'
        self.out += '      <svg id="demo-tiger" xmlns="http://www.w3.org/2000/svg" style="display: inline; width: inherit; min-width: inherit;' + \
'                   max-width: inherit; height: inherit; min-height: inherit; max-height: inherit; " viewBox="0 0 %d %d" version="1.1">\n' % (width, height) + \
'        <style>\n' + \
'            .bar {\n' + \
'        stroke-width:3;\n' + \
'        opacity:1;\n' + \
'    }\n' + \
'            .bar:hover {\n' + \
'        stroke-width:20;\n' + \
'        opacity:1;\n' + \
'    }\n' + \
'        </style>\n' \
'<g>\n'


    def drawLine(self, x1, y1, x2, y2, th=1, cl=(0, 0, 0)):
        self.out += '  <line x1="%d" y1="%d" x2="%d" y2="%d"\n        stroke-width="%d" stroke="%s" />\n' % (x1, y1, x2, y2, th, colorstr(cl))



    def seperate_figure(self, width, height):
        self.out += '''</g>      </svg>
    </div>
    <button id="enable">enable</button>
    <button id="disable">disable</button>
    <button id="hide">hide</button>
    <button id="show">show</button>

    <script>
      // Don't use window.onLoad like this in production, because it can only listen to one function.
      window.onload = function() {
        // Expose to window namespase for testing purposes
        window.zoomTiger = svgPanZoom('#demo-tiger', {
          zoomEnabled: true,
          controlIconsEnabled: true,
          fit: true,
          center: true,
          maxZoom: 1000,
          zoomScaleSensitivity: 0.5
        });

        document.getElementById('enable').addEventListener('click', function() {
          window.zoomTiger.enableControlIcons();
        })
        document.getElementById('disable').addEventListener('click', function() {
          window.zoomTiger.disableControlIcons();
        })
        document.getElementById('hide').addEventListener('click', function() {
          document.getElementById("annot").style.display = "none";
        })
        document.getElementById('show').addEventListener('click', function() {
          document.getElementById("annot").style.display = "block";
        })
      };
    </script>
    '''
        self.out += '<div id="container" style="width: 50%; height: auto; border:0px solid black; ">\n'
        self.out += ' <svg id="legend" xmlns="http://www.w3.org/2000/svg" style="display: inline; width: inherit; min-width: inherit;' + \
'                   max-width: inherit; height: inherit; min-height: inherit; max-height: inherit; " viewBox="0 0 %d %d" version="1.1">\n<g>' % (width, height)

    def writesvg(self, filename, svg=True, textb=''):
        with open(filename, 'w') as outfile:
            outfile.write(self.out)
            if svg:
                outfile.write('</g></svg>')
            else:
                outfile.write('</div></g>      </svg>\n<p> ')
                outfile.write(textb)
                outfile.write('</p>\n  </body>\n</html>')

    def drawRightArrow(self, x, y, wid, ht, fc, oc=(0,0,0), lt=1):
        if lt > ht /2:
            lt = ht/2
        x1 = x + wid
        y1 = y + ht/2
        x2 = x + wid - ht / 2
        ht -= 1
        if wid > ht/2:
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d"\n' % (colorstr(fc), colorstr(oc), lt)
            self.out += '           points="%d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d" />\n' % (x, y+ht/4, x2, y+ht/4,
                                                                                                x2, y, x1, y1, x2, y+ht,
                                                                                                x2, y+3*ht/4, x, y+3*ht/4)
        else:
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d"\n' % (colorstr(fc), colorstr(oc), lt)
            self.out += '           points="%d,%d %d,%d %d,%d" />\n' % (x, y, x, y+ht, x + wid, y1)

    def drawLeftArrow(self, x, y, wid, ht, fc, oc=(0,0,0), lt=1):
        if lt > ht /2:
            lt = ht/2
        x1 = x + wid
        y1 = y + ht/2
        x2 = x + ht / 2
        ht -= 1
        if wid > ht/2:
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d"\n' % (colorstr(fc), colorstr(oc), lt)
            self.out += '           points="%d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d" />\n' % (x1, y+ht/4, x2, y+ht/4,
                                                                                                x2, y, x, y1, x2, y+ht,
                                                                                                x2, y+3*ht/4, x1, y+3*ht/4)
        else:
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d"\n' % (colorstr(fc), colorstr(oc), lt)
            self.out += '           points="%d,%d %d,%d %d,%d" />\n' % (x, y1, x1, y+ht, x1, y)

    def drawBlastHit(self, x1, y1, x2, y2, x3, y3, x4, y4, fill=(0, 0, 255), lt=0):
        self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d"\n' % (colorstr(fill), colorstr(fill), lt)
        self.out += '           points="%d,%d %d,%d %d,%d %d,%d" />\n' % (x1, y1, x2, y2, x3, y3, x4, y4)

    def drawGradient(self, x1, y1, wid, hei, minc, maxc):
        self.out += '  <defs>\n    <linearGradient id="MyGradient" x1="0%" y1="0%" x2="0%" y2="100%">\n'
        self.out += '      <stop offset="0%%" stop-color="%s" />\n' % colorstr(maxc)
        self.out += '      <stop offset="100%%" stop-color="%s" />\n' % colorstr(minc)
        self.out += '    </linearGradient>\n  </defs>\n'
        self.out += '  <rect fill="url(#MyGradient)" stroke-width="0"\n'
        self.out += '        x="%d" y="%d" width="%d" height="%d"/>\n' % (x1, y1, wid, hei)

    def drawGradient2(self, x1, y1, wid, hei, minc, maxc):
        self.out += '  <defs>\n    <linearGradient id="MyGradient2" x1="0%" y1="0%" x2="0%" y2="100%">\n'
        self.out += '      <stop offset="0%%" stop-color="%s" />\n' % colorstr(maxc)
        self.out += '      <stop offset="100%%" stop-color="%s" />\n' % colorstr(minc)
        self.out += '    </linearGradient>\n</defs>\n'
        self.out += '  <rect fill="url(#MyGradient2)" stroke-width="0"\n'
        self.out += '        x="%d" y="%d" width="%d" height="%d" />\n' % (x1, y1, wid, hei)
    def drawHueGradient(self, x1, y1, wid, hei, s, l):
        self.out += '  <defs>\n    <linearGradient id="HueGradient" x1="0%" y1="0%" x2="100%" y2="0%">\n'
        iterations = 20
        for i in range(iterations):
            color = hsl_to_rgb(360/iterations * i, s, l)
            colorstring = colorstr(color)
            self.out += '      <stop offset="%d%%" stop-color="%s" />\n' % (100/iterations * i, colorstring)
            color = hsl_to_rgb(360/iterations * (i + 1), s, l)
            colorstring = colorstr(color)
            self.out += '      <stop offset="%d%%" stop-color="%s" />\n' % (100/iterations * (i + 1), colorstring)
        self.out += '    </linearGradient>\n</defs>\n'
        self.out += '  <rect fill="url(#HueGradient)" stroke-width="1"\n'
        self.out += '        x="%d" y="%d" width="%d" height="%d" />\n' % (x1, y1, wid, hei)

    def drawOutRect(self, x1, y1, wid, hei, fill, outfill, lt=1, alpha=1.0, alpha2=1.0):
        self.out += '  <rect stroke="%s" stroke-opacity="%f" stroke-alignment="inner"\n' % (colorstr(outfill), alpha)
        self.out += '        fill="%s" fill-opacity="%f"\n' % (colorstr(fill), alpha2)
        self.out += '        x="%d" y="%d" width="%d" height="%d" />\n' % (x1, y1, wid, hei)

    def create_group(self, name, the_class='bar'):
        self.out += '        <g id="%s" class="%s" fill="none">\n' % (name, the_class)

    def close_group(self):
        self.out += '        </g>'


    def create_pattern(self, id, fill, pattern, width, line_width):
        fill = colorstr(fill)
        if pattern == 'horizontal':
            self.out += '    <defs>\n'
            self.out += '      <pattern id="%s" width="%d" height="%d" patternUnits="userSpaceOnUse">\n' % (id, width, width)
            self.out += '        <line x1="0" y1="0" x2="%d" y2="0" style="stroke:%s; stroke-width:%d; fill:#FFFFFF" />\n' % (width, fill, line_width)
            self.out += '      </pattern>\n'
            self.out += '   </defs>\n'
        elif pattern == 'forward_diag':
            self.out += '    <defs>\n'
            self.out += '      <pattern id="%s" width="%d" height="%d" patternTransform="rotate(45 0 0)" patternUnits="userSpaceOnUse">\n' % (id, width, width)
            self.out += '        <line x1="0" y1="0" x2="0" y2="%d" style="stroke:%s; stroke-width:%d; fill:#FFFFFF" />\n' % (width, fill, line_width)
            self.out += '      </pattern>\n'
            self.out += '   </defs>\n'
        elif pattern == 'reverse_diag':
            self.out += '    <defs>\n'
            self.out += '      <pattern id="%s" width="%d" height="%d" patternTransform="rotate(135 0 0)" patternUnits="userSpaceOnUse">\n' % (id, width, width)
            self.out += '        <line x1="0" y1="0" x2="0" y2="%d" style="stroke:%s; stroke-width:%d; fill:#FFFFFF" />\n' % (width, fill, line_width)
            self.out += '      </pattern>\n'
            self.out += '   </defs>\n'

    def drawPatternRect(self, x, y, width, height, id, fill, lt=1):
        fill = colorstr(fill)
        self.out += '  <rect style="fill:#FFFFFF; stroke: %s; stroke-alignment: inner;"\n' % fill
        self.out += '        x="%d" y="%d" width="%d" height="%d" />\n' % (x, y, width, height)
        self.out += '  <rect style="fill:url(#%s); stroke: %s; stroke-alignment: inner;"\n' % (id, fill)
        self.out += '        x="%d" y="%d" width="%d" height="%d" />\n' % (x, y, width, height)


    def drawPath(self, xcoords, ycoords, th=1, cl=(0, 0, 0), alpha=0.9):
        self.out += '  <path d="M%d %d' % (xcoords[0], ycoords[0])
        for i in range(1, len(xcoords)):
            self.out += ' L%d %d' % (xcoords[i], ycoords[i])
        self.out += '"\n        stroke-width="%d" stroke="%s" stroke-opacity="%f" stroke-linecap="butt" fill="none" z="-1" />\n' % (th, colorstr(cl), alpha)


    def drawRightFrame(self, x, y, wid, ht, lt, frame, fill):
        if lt > ht /2:
            lt = ht /2
        if frame == 1:
            y1 = y + ht/2
            y2 = y + ht * 3/8
            y3 = y + ht * 1/4
        elif frame == 2:
            y1 = y + ht * 3/8
            y2 = y + ht * 1/4
            y3 = y + ht * 1/8
        elif frame == 0:
            y1 = y + ht * 1/4
            y2 = y + ht * 1/8
            y3 = y + 1
        x1 = x
        x2 = x + wid - ht/8
        x3 = x + wid
        if wid > ht/8:
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d"\n' % (colorstr(fill), colorstr((0, 0, 0)), lt)
            self.out += '           points="%d,%d %d,%d %d,%d %d,%d %d,%d" />\n' % (x1, y1, x2, y1, x3, y2, x2, y3, x1, y3)
        else:
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d"\n' % (colorstr(fill), colorstr((0, 0, 0)), lt)
            self.out += '           points="%d,%d %d,%d %d,%d" />\n' % (x1, y1, x3, y2, x1, y3)

    def drawRightFrameRect(self, x, y, wid, ht, lt, frame, fill):
        if lt > ht /2:
            lt = ht /2
        if frame == 1:
            y1 = y + ht / 4
        elif frame == 2:
            y1 = y + ht /8
        elif frame == 0:
            y1 = y + 1
        hei = ht /4
        x1 = x
        self.out += '  <rect fill="%s" stroke-width="%d"\n' % (colorstr(fill), lt)
        self.out += '        x="%d" y="%d" width="%d" height="%d" />\n' % (x1, y1, wid, hei)

    def drawLeftFrame(self, x, y, wid, ht, lt, frame, fill):
        if lt > ht /2:
            lt = ht /2
        if frame == 1:
            y1 = y + ht
            y2 = y + ht * 7/8
            y3 = y + ht * 3/4
        elif frame == 2:
            y1 = y + ht * 7/8
            y2 = y + ht * 3/4
            y3 = y + ht * 5/8
        elif frame == 0:
            y1 = y + ht * 3/4
            y2 = y + ht * 5/8
            y3 = y + ht / 2
        x1 = x + wid
        x2 = x + ht/8
        x3 = x
        if wid > ht/8:
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d"\n' % (colorstr(fill), colorstr((0, 0, 0)), lt)
            self.out += '           points="%d,%d %d,%d %d,%d %d,%d %d,%d" />\n' % (x1, y1, x2, y1, x3, y2, x2, y3, x1, y3)
        else:
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d"\n' % (colorstr(fill), colorstr((0, 0, 0)), lt)
            self.out += '           points="%d,%d %d,%d %d,%d" />\n' % (x1, y1, x3, y2, x1, y3)

    def drawLeftFrameRect(self, x, y, wid, ht, lt, frame, fill):
        if lt > ht /2:
            lt = ht /2
        if frame == 1:
            y1 = y + ht * 3/4
        elif frame == 2:
            y1 = y + ht * 5/8
        elif frame == 0:
            y1 = y + ht / 2
        hei = ht /4
        x1 = x
        self.out += '  <rect fill="%s" stroke-width="%d"\n' % (colorstr(fill), lt)
        self.out += '        x="%d" y="%d" width="%d" height="%d" />\n' % (x1, y1, wid, hei)

    def drawPointer(self, x, y, ht, lt, fill):
        x1 = x - int(round(0.577350269 * ht/2))
        x2 = x + int(round(0.577350269 * ht/2))
        y1 = y + ht/2
        y2 = y + 1
        self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d"\n' % (colorstr(fill), colorstr((0, 0, 0)), lt)
        self.out += '           points="%d,%d %d,%d %d,%d" />\n' % (x1, y2, x2, y2, x, y1)

    def drawDash(self, x1, y1, x2, y2, exont):
        self.out += '  <line x1="%d" y1="%d" x2="%d" y2="%d"\n' % (x1, y1, x2, y2)
        self.out += '       style="stroke-dasharray: 5, 3, 9, 3"\n'
        self.out += '       stroke="#000" stroke-width="%d" />\n' % exont

    def drawSymbol(self, x, y, size, fill, symbol, alpha=1.0, lt=1):
        x0 = x - size/2
        x1 = size/8 + x - size/2
        x2 = size/4 + x - size/2
        x3 = size*3/8 + x - size/2
        x4 = size/2 + x - size/2
        x5 = size*5/8 + x - size/2
        x6 = size*3/4 + x - size/2
        x7 = size*7/8 + x - size/2
        x8 = size + x - size/2
        y0 = y - size/2
        y1 = size/8 + y - size/2
        y2 = size/4 + y - size/2
        y3 = size*3/8 + y - size/2
        y4 = size/2 + y - size/2
        y5 = size*5/8 + y - size/2
        y6 = size*3/4 + y - size/2
        y7 = size*7/8 + y - size/2
        y8 = size + y - size/2
        if symbol == 'o':
            self.out += '  <circle stroke="%s" stroke-width="%d" stroke-opacity="%f"\n' % (colorstr((0, 0, 0)), lt, 1)
            self.out += '        fill="%s" fill-opacity="%f"\n' % (colorstr(fill), alpha)
            self.out += '        cx="%d" cy="%d" r="%d" />\n' % (x, y, size/2)
        elif symbol == 'x':
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d" stroke-opacity="%f" fill-opacity="%f"\n' % (colorstr(fill), colorstr((0, 0, 0)), lt, alpha, alpha)
            self.out += '           points="%d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d" />\n' % (x0, y2, x2, y0, x4, y2, x6, y0, x8, y2,
                                                                                                                             x6, y4, x8, y6, x6, y8, x4, y6, x2, y8,
                                                                                                                             x0, y6, x2, y4)
        elif symbol == '+':
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d" stroke-opacity="%f" fill-opacity="%f"\n' % (colorstr(fill), colorstr((0, 0, 0)), lt, alpha, alpha)
            self.out += '           points="%d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d" />\n' % (x2, y0, x6, y0, x6, y2, x8, y2, x8, y6,
                                                                                                                             x6, y6, x6, y8, x2, y8, x2, y6, x0, y6,
                                                                                                                             x0, y2, x2, y2)
        elif symbol == 's':
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d" stroke-opacity="%f" fill-opacity="%f"\n' % (colorstr(fill), colorstr((0, 0, 0)), lt, alpha, alpha)
            self.out += '           points="%d,%d %d,%d %d,%d %d,%d" />\n' % (x0, y0, x0, y8, x8, y8, x8, y0)
        elif symbol == '^':
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d" stroke-opacity="%f" fill-opacity="%f"\n' % (colorstr(fill), colorstr((0, 0, 0)), lt, alpha, alpha)
            self.out += '           points="%d,%d %d,%d %d,%d %d,%d %d,%d %d,%d" />\n' % (x0, y0, x2, y0, x4, y4, x6, y0, x8, y0, x4, y8)
        elif symbol == 'v':
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d" stroke-opacity="%f" fill-opacity="%f"\n' % (colorstr(fill), colorstr((0, 0, 0)), lt, alpha, alpha)
            self.out += '           points="%d,%d %d,%d %d,%d %d,%d %d,%d %d,%d" />\n' % (x0, y8, x2, y8, x4, y4, x6, y8, x8, y8, x4, y0)
        elif symbol == 'u':
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d" stroke-opacity="%f" fill-opacity="%f"\n' % (colorstr(fill), colorstr((0, 0, 0)), lt, alpha, alpha)
            self.out += '           points="%d,%d %d,%d %d,%d" />\n' % (x0, y8, x4, y0, x8, y8)
        elif symbol == 'd':
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d" stroke-opacity="%f" fill-opacity="%f"\n' % (colorstr(fill), colorstr((0, 0, 0)), lt, alpha, alpha)
            self.out += '           points="%d,%d %d,%d %d,%d" />\n' % (x0, y0, x4, y8, x8, y0)
        else:
            sys.stderr.write(symbol + '\n')
            sys.stderr.write('Symbol not found, this should not happen.. exiting')
            sys.exit()

    def writeString(self, thestring, x, y, size, ital=False, bold=False, rotate=0, justify='left'):
        if rotate != 0:
            x, y = y, x
        self.out += '  <text\n'
        self.out += '    style="font-size:%dpx;font-style:normal;font-weight:normal;z-index:10\
;line-height:125%%;letter-spacing:0px;word-spacing:0px;fill:#000000;fill-opacity:1;stroke:none;font-family:Sans"\n' % size
        if justify == 'right':
            self.out += '    text-anchor="end"\n'
        elif justify == 'middle':
            self.out += '    text-anchor="middle"\n'
        if rotate == 1:
            self.out += '    x="-%d"\n' % x
        else:
            self.out += '    x="%d"\n' % x
        if rotate == -1:
            self.out += '    y="-%d"\n' % y
        else:
            self.out += '    y="%d"\n' % y
        self.out += '    sodipodi:linespacing="125%"'
        if rotate == -1:
            self.out += '\n    transform="matrix(0,1,-1,0,0,0)"'
        if rotate == 1:
            self.out += '\n    transform="matrix(0,-1,1,0,0,0)"'
        self.out += '><tspan\n      sodipodi:role="line"\n'
        if rotate == 1:
            self.out += '      x="-%d"\n' % x
        else:
            self.out += '      x="%d"\n' % x
        if rotate == -1:
            self.out += '      y="-%d"' % y
        else:
            self.out += '      y="%d"' % y
        if ital and bold:
            self.out += '\nstyle="font-style:italic;font-weight:bold"'
        elif ital:
            self.out += '\nstyle="font-style:italic"'
        elif bold:
            self.out += '\nstyle="font-style:normal;font-weight:bold"'
        self.out += '>' + thestring + '</tspan></text>\n'


def hsl_to_rgb(h, s, l):
    c = (1 - abs(2*l - 1)) * s
    x = c * (1 - abs(h *1.0 / 60 % 2 - 1))
    m = l - c/2
    if h < 60:
        r, g, b = c + m, x + m, 0 + m
    elif h < 120:
        r, g, b = x + m, c+ m, 0 + m
    elif h < 180:
        r, g, b = 0 + m, c + m, x + m
    elif h < 240:
        r, g, b, = 0 + m, x + m, c + m
    elif h < 300:
        r, g, b, = x + m, 0 + m, c + m
    else:
        r, g, b, = c + m, 0 + m, x + m
    r = int(r * 255)
    g = int(g * 255)
    b = int(b * 255)
    return (r,g,b)





def write_fasta_sibel(fasta_list, out_fasta):
    getfa = False
    getgb = False
    out_dict = {}
    with open(out_fasta, 'w') as out:
        for num, fasta in enumerate(fasta_list):
            with open(fasta) as f:
                count = 0
                for line in f:
                    if line.startswith('>'):
                        out.write('>' + str(num) + '_' + str(count) + '\n')
                        out_dict[str(num) + '_' + str(count)] = (os.path.basename(fasta), line.split()[0][1:])
                        count += 1
                        getfa = True
                    elif getfa:
                        out.write(line)
                    elif line.startswith('LOCUS '):
                        name = line.split()[1]
                    elif line.startswith('ORIGIN'):
                        out.write('>' + str(num) + '_' + str(count) + '\n')
                        out_dict[str(num) + '_' + str(count)] = (os.path.basename(fasta), name)
                        count += 1
                        getgb = True
                    elif line.startswith('//'):
                        getgb = False
                    elif getgb:
                        out.write(''.join(line.split()[1:]) + '\n')
    return out_dict


# run sibelia
def run_sibel(in_fasta, sibel_dir, sibelia_path, sib_mode, min_block, skip_sibel):
    if not skip_sibel:
        subprocess.Popen(sibelia_path + ' -s ' + sib_mode + ' -m ' + str(min_block) + ' -o ' + sibel_dir + ' ' + in_fasta, shell=True).wait()



class block_object:
    def __init__(self, start, strand, length, block, genes, cat):
        self.start = start
        self.strand = strand
        self.length = length
        self.block = block
        self.genes = genes
        self.type = None
        self.cat = cat



#def get_blocks_maf(maf_file, gene_list, cats={}):
    

def get_blocks(sibel_dir, gene_list, cats={}):
    seq_no_dict = {}
    length_dict = {}
    block_dict = {}
    block_type = {}
    with open(sibel_dir + '/blocks_coords.txt') as f:
        f.readline()
        get_seq_ids = True
        for line in f:
            if line.startswith('---') and get_seq_ids:
                get_seq_ids = False
            elif line.startswith('---'):
                if repeat:
                    block_type[block] = 'repeat'
                elif len(in_fasta_set) == len(length_dict):
                    block_type[block] = 'core'
                else:
                    block_type[block] = 'noncore'
            elif get_seq_ids:
                seq_id, length, header = line.split()
                fasta, contig = header.split('_')
                if not fasta in length_dict:
                    length_dict[fasta] = {}
                    block_dict[fasta] = {}
                length_dict[fasta][contig] = int(length)
                block_dict[fasta][contig] = []
                seq_no_dict[seq_id] = (fasta, contig)
            elif line.startswith('Seq_id'):
                pass
            elif line.startswith('Block'):
                block = line.split()[1][1:]
                repeat = False
                in_fasta_set = set()
            else:
                id, strand, start, end, length = line.split()
                fasta, contig = seq_no_dict[id]
                length = int(length)
                start = int(start)
                end = int(end)
                genes = []
                if strand == '-':
                    start, end = end, start
                for j in gene_list:
                    if fasta + '_' + contig == j[0] and start <= j[2] <= end:
                        genes.append([j[1], j[2] - start])
                cat = 'none'
                if fasta + '_' + contig in cats:
                    for q in cats[fasta + '_' + contig]:
                        if q[0] == 'all':
                            cat = q[2]
                        elif q[0] <= start <= end <= q[1]:
                            cat = q[2]
                        elif start <= q[0] <= q[1] <= end:
                            if (q[1] - q[0]) / (end - start) >= 0.5:
                                cat = q[2]
                        elif start <= q[0] <= end:
                            if (end - q[0]) / (end - start) >= 0.5:
                                cat = q[2]
                        elif start <= q[1] <= end:
                            if (q[1] - start) / (end - start) >= 0.5:
                                cat = q[2]
                if fasta in in_fasta_set:
                    repeat = True
                else:
                    in_fasta_set.add(fasta)
                block_dict[fasta][contig].append(block_object(start, strand, length, block, genes, cat))
    for i in block_dict:
        for j in block_dict[i]:
            block_dict[i][j].sort(key=lambda x: x.start)
            for k in block_dict[i][j]:
                k.type = block_type[k.block]
    return block_dict, length_dict

def order_blocks_core(block_dict):
    core_order = []
    num = 0
    for j in range(len(block_dict['0'])):
        for k in block_dict['0'][str(j)]:
            if k.type == 'core':
                core_order.append((k.block, k.strand))
                k.order_num = num
                num += 1
    core_block_num = num
    for i in range(1, len(block_dict)):
        block_order_dict = {}
        for j in block_dict[str(i)]:
            max_len = 0
            for k in block_dict[str(i)][j]:
                #start, strand, length, block, block_type = k
                if k.length > max_len and k.type == 'core':
                    best_strand = k.strand
                    best_block = k.block
                    max_len = k.length
                if k.block == core_order[0][0]:
                    best_strand = k.strand
                    best_block = k.block
                    max_len = float('inf')
            if max_len != 0:
                block_order_dict[best_block] = (j, best_strand)
        contig_order = []
        num = 0
        for j in core_order:
            if j[0] in block_order_dict:
                reverse = j[1] == block_order_dict[j[0]][1]
                contig_order.append((block_order_dict[j[0]][0], reverse))
                for k in block_dict[str(i)][block_order_dict[j[0]][0]]:
                    if k.block == core_order[0][0]:
                        start_pos = num
                        break
                    if k.type == 'core':
                        num += 1
        color_num = 0
        for j in contig_order:
            for k in range(len(block_dict[str(i)][j[0]])):
                aninstance = block_dict[str(i)][j[0]][k]
                if aninstance.type == 'core':
                    if j[1]:
                        aninstance.order_num = (color_num + core_block_num - start_pos) % core_block_num
                    else:
                        aninstance.order_num = core_block_num - (color_num + core_block_num - start_pos) % core_block_num
                    color_num += 1
    return block_dict

def get_noncore(block_dict, length_dict, color_contigs=False):
    core_order = []
    max_coreb_length_dict = {}
    for j in range(len(block_dict['0'])):
        for k in block_dict['0'][str(j)]:
            if k.type == 'core':
                core_order.append((k.block, k.strand))
                max_coreb_length_dict[k.block] = 0
    out_blocks = []
    for i in block_dict:
        for j in block_dict[i]:
            last_core = None
            last_core_ori = None
            last_core_end_pos = 0
            noncore_block = []
            for k in block_dict[i][j]:
                if k.type == 'core':
                    length_noncore = k.start - last_core_end_pos
                    if k.length > max_coreb_length_dict[k.block]:
                        max_coreb_length_dict[k.block] = k.length
                    positions = []
                    for num, l in enumerate(core_order):
                        if l[0] == last_core and last_core_ori == l[1]:
                            positions.append((num+1, 'left', True))
                        elif l[0] == last_core:
                            positions.append((num, 'right', False))
                        elif l[0] == k.block and k.strand == l[1]:
                            positions.append((num, 'right', True))
                        elif l[0] == k.block:
                            positions.append((num+1, 'left', False))
                    if len(positions) > 2:
                        sys.exit('something went wrong')
                    out_blocks.append((i, noncore_block, length_noncore, positions))
                    last_core = k.block
                    last_core_end_pos = k.start + k.length
                    last_core_ori = k.strand
                    noncore_block = []
                else:
                    if color_contigs:
                        k.cat = j
                    noncore_block.append((k.start - last_core_end_pos, k.strand, k.length, k.block, k.type, k.genes, k.cat))
            if last_core is None:
                out_blocks.append((i, noncore_block, length_dict[i][j], []))
            elif k.type != 'core':
                positions = []
                for num, l in enumerate(core_order):
                    if l[0] == last_core and last_core_ori == l[1]:
                        positions.append((num+1, 'left', True))
                    elif l[0] == last_core:
                        positions.append((num+2, 'right', False))
                out_blocks.append((i, noncore_block, length_dict[i][j] - last_core_end_pos, positions))
    return out_blocks


def place_core(block_dict, color_contigs=False):
    core_order = {}
    count = 0
    for j in range(len(block_dict['0'])):
        for k in block_dict['0'][str(j)]:
            if k.type == 'core':
                core_order[k.block] = count
                count += 1
    out_array = [[] for i in range(len(core_order))]
    max_coreb_length = [0 for i in range(len(core_order))]
    for i in range(len(block_dict)):
        for j in block_dict[str(i)]:
            for k in block_dict[str(i)][j]:
                if k.type == 'core':
                    #start, strand, length, block, block_type, fig_pos = k
                    if color_contigs:
                        out_array[core_order[k.block]].append((k.length, j))
                    else:
                        out_array[core_order[k.block]].append((k.length, k.order_num))
                    if k.length > max_coreb_length[core_order[k.block]]:
                        max_coreb_length[core_order[k.block]] = k.length
    return out_array, max_coreb_length


def place_noncore(out_blocks):
    placed_blocks = []
    unplaced_blocks = []
    block_loc = {}
    for i in out_blocks:
        row, pattern, size, positions = i
        if size == 0:
            continue
        right_place = None
        left_place = None
        for j in positions:
            if j[1] == 'left':
                left_place = j[0]
                left_ori = j[2]
            else:
                right_place = j[0]
                right_ori = j[2]
        placed = False
        if left_place == right_place and not left_place is None:
            placed = True
            if left_ori:
                placed_blocks.append((row, pattern, size, left_place, 'middle'))
            else:
                new_pattern = []
                for j in pattern:
                    start, strand, length, block, block_type, genes, cat = j
                    start = size - (start + length)
                    for k in genes:
                        k[1] = length - k[1]
                    new_pattern.append((start, strand, length, block, block_type, genes, cat))
                placed_blocks.append((row, new_pattern, size, left_place, 'middle'))
        elif left_place is None and not right_place is None:
            placed = True
            if right_ori:
                placed_blocks.append((row, pattern, size, right_place, 'right'))
            else:
                new_pattern = []
                for j in pattern:
                    start, strand, length, block, block_type, genes, cat = j
                    start = size - (start + length)
                    for k in genes:
                        k[1] = length - k[1]
                    new_pattern.append((start, strand, length, block, block_type, genes, cat))
                placed_blocks.append((row, new_pattern, size, left_place, 'right'))
        elif not left_place is None and right_place is None:
            placed = True
            if left_ori:
                placed_blocks.append((row, pattern, size, right_place, 'left'))
            else:
                new_pattern = []
                for j in pattern:
                    start, strand, length, block, block_type, genes, cat = j
                    start = size - (start + length)
                    for k in genes:
                        k[1] = length - k[1]
                    new_pattern.append((start, strand, length, block, block_type, genes, cat))
                placed_blocks.append((row, new_pattern, size, left_place, 'left'))
        if placed:
            for j in placed_blocks[-1][1]:
                if j[4] == 'noncore':
                    if not placed_blocks[-1][3] in block_loc:
                        block_loc[placed_blocks[-1][3]] = set()
                    block_loc[placed_blocks[-1][3]].add(j[3])
        else:
            unplaced_blocks.append(i)
    for i in unplaced_blocks:
        row, pattern, size, positions = i
        if positions == []:
            placed_blocks.append((row, pattern, size, None, None))
        else:
            for j in positions:
                if j[1] == 'left':
                    left_place = j[0]
                    left_ori = j[2]
                else:
                    right_place = j[0]
                    right_ori = j[2]
            left_count = 0
            right_count = 0
            for j in pattern:
                if right_place in block_loc and j[3] in block_loc[right_place]:
                    right_count += 1
                if left_place in block_loc and j[3] in block_loc[left_place]:
                    left_count += 1
            if left_count > right_count or right_count == left_count and left_place < right_place:
                if left_ori:
                    placed_blocks.append((row, pattern, size, right_place, 'left'))
                else:
                    new_pattern = []
                    for j in pattern:
                        start, strand, length, block, block_type, genes, cat = j
                        start = size - (start + length)
                        for k in genes:
                            k[1] = length - k[1]
                        new_pattern.append((start, strand, length, block, block_type, genes, cat))
                    placed_blocks.append((row, new_pattern, size, left_place, 'left'))
            else:
                if right_ori:
                    placed_blocks.append((row, pattern, size, right_place, 'right'))
                else:
                    new_pattern = []
                    for j in pattern:
                        start, strand, length, block, block_type, genes, cat = j
                        start = size - (start + length)
                        for k in genes:
                            k[1] = length - k[1]
                        new_pattern.append((start, strand, length, block, block_type, genes, cat))
                    placed_blocks.append((row, new_pattern, size, left_place, 'right'))
    return placed_blocks

def draw_blocks(core_blocks, placed_blocks, core_size, out_file, block_height, y_gap, legend_size, color_cat=True,
                texta="Chromatiblock figure", textb="this is a chromatiblock figure", color_contigs=False):
    noncore_max_size = [0 for i in range(len(core_blocks) + 2)]
    unattached_size = [[] for i in range(len(core_blocks[0]))]
    figure_width = 50000
    genome_height = block_height + y_gap
    genome_line_width = block_height/8
    height = (len(core_blocks[0]) + 3 + legend_size/2) * genome_height * 2
    core_sat = 0.8
    core_light = 0.5
    if out_file.endswith('html'):
        svg = scalableVectorGraphicsHTML(height, figure_width, False, texta)
    else:
        svg = scalableVectorGraphicsHTML(height, figure_width, True)
    for i in placed_blocks:
        row, pattern, size, place, align = i
        if place is None:
            unattached_size[int(row)].append(size)
        elif size > noncore_max_size[place]:
            noncore_max_size[place] = size

    curr_x = 0
    gap_size = 20
    max_unattached = 0
    max_unattached_num = 0
    for i in unattached_size:
        if sum(i) > max_unattached:
            max_unattached = sum(i)
            max_unattached_num = len(i)
    usable_length = figure_width - gap_size * 2 * (len(core_blocks) + max_unattached_num - 1)
    bp = sum(core_size) + sum(noncore_max_size) + max_unattached
    scale = bp / usable_length
    gap_pos = {}
    for num1, i in enumerate(core_blocks):
        gap_pos[num1] = curr_x
        curr_x += noncore_max_size[num1] / scale + gap_size * 2
        for num2, j in enumerate(i):
            width, block_no = j
            if color_contigs:
                color1 = color_list[int(block_no)]
                color2 = color_list[int(block_no)]
            else:
                hue = int(block_no * 1.0 / len(core_size) * 360)
                color1 = hsl_to_rgb(hue, core_sat, core_light)
                color2 = hsl_to_rgb(hue, core_sat, core_light - 0.3)
            svg.drawOutRect(curr_x, num2 * genome_height, width/scale, block_height, color1, color2)
        curr_x += core_size[num1] / scale
    gap_pos[num1+1] = curr_x
    noncore_dict = {}
    unplaced_start = curr_x + gap_size * 2
    placed_blocks.sort(key=lambda x: x[2], reverse=True)
    unplaced_taken = {}
    for i in placed_blocks:
        row, pattern, size, gap, align = i
        if gap is None:
            if row in unplaced_taken:
                x1 = unplaced_taken[row]
            else:
                x1 = unplaced_start
            x2 = x1 + size/scale
            unplaced_taken[row] = x2 + gap_size * 2
        elif align == 'left':
            x1 = gap_pos[gap]
            x2 = gap_pos[gap] + size/scale
        elif align == 'middle':
            x1 = gap_pos[gap] + gap_size + noncore_max_size[gap]/scale/2 - size/scale/2
            x2 = gap_pos[gap] + gap_size + noncore_max_size[gap]/scale/2 - size/scale/2 + size/scale
        elif align == 'right':
            x1 = gap_pos[gap] + noncore_max_size[gap]/scale - size/scale + 2 * gap_size
            x2 = gap_pos[gap] + noncore_max_size[gap]/scale + 2 * gap_size
        y = int(row) * genome_height + block_height / 2
        svg.drawLine(x1, y, x2, y, th=genome_line_width)
        for j in pattern:
            start, strand, length, block, block_type, genes, cat = j
            if block in noncore_dict:
                noncore_dict[block].append((row, x1 + start/scale, length, genes, cat))
            else:
                noncore_dict[block] = [(row, x1 + start/scale, length, genes, cat)]
    noncore_order = []
    for i in noncore_dict:
        pos_list = []
        for j in noncore_dict[i]:
            pos_list.append(j[1])
        pos_list.sort()
        noncore_order.append((pos_list[len(pos_list)//2], i))
    noncore_order.sort()
    block_order = []
    for i in noncore_order:
        block_order.append(i[1])
    curr_x = 0
    panel2_start = len(core_blocks[0]) * genome_height + genome_height * 4
    gene_dict_a = {}
    gene_dict_b = {}
    pattern_dict = {}
    cat_count = 0
    bp_blocks = 0
    block_count = {}
    for num, i in enumerate(block_order):
        block_count[i] = {}
        max_block_width = 0
        for j in noncore_dict[i]:
            row, x, length, genes, cat = j
            if row in block_count[i]:
                block_count[i][row][0] += 1
            else:
                block_count[i][row] = [1, 0]
            if length > max_block_width:
                max_block_width = length
        bp_blocks += max_block_width
    scale2 = bp_blocks / (figure_width - gap_size * (len(block_order) - 1))
    cat_list = []
    for num, i in enumerate(block_order):
        id = 'g' + str(num)
        if not color_contigs:
            color = color_list[num % len(color_list)]
            pattern = pattern_list[num % len(pattern_list)]
            svg.create_pattern(id, color, pattern, 50, 50)
            pattern_dict[id]= color
            if color_cat:
                for j in noncore_dict[i]:
                    row, x, length, genes, cat = j
                    id2 = cat
                    if not id2 in pattern_dict:
                        color2 = color_list[cat_count % len(color_list)]
                        cat_count += 1
                        cat_list.append(id2)
                        pattern = pattern_list[cat_count % len(pattern_list)]
                        svg.create_pattern(id2, color2, pattern, 50, 50)
                        pattern_dict[id2] = color2
        max_block_width = 0
        svg.create_group('gr' + str(num))
        for j in noncore_dict[i]:
            row, x, length, genes, cat = j
            if color_cat:
                id2 = cat
                color2 = pattern_dict[id2]
            else:
                id2 = id
                color2 = color
            for k in genes:
                if k[0] in gene_dict_a:
                    gene_dict_a[k[0]].append((x + k[1]/scale, int(row)))
                    gene_dict_b[k[0]].append((curr_x + k[1]/scale2, curr_x -gap_size/2, int(row)))
                else:
                    gene_dict_a[k[0]] = [(x + k[1]/scale, int(row))]
                    gene_dict_b[k[0]] = [(curr_x + k[1]/scale2, curr_x -gap_size/2, int(row))]
            svg.drawPatternRect(x, int(row) * genome_height, length/scale, block_height, id, color)
            block_height_2 = block_height/block_count[i][row][0]
            svg.drawPatternRect(curr_x, int(row) * genome_height + panel2_start + block_height_2 * block_count[i][row][1], length/scale2, block_height_2, id2, color2)
            block_count[i][row][1] += 1
            if length/scale2 + gap_size > max_block_width:
                max_block_width = length/scale2 + gap_size
        curr_x += max_block_width
        svg.close_group()
    svg.create_group('annot', 'anno')
    color_list.reverse()
    for num, i in enumerate(gene_dict_a):
        min_y = float('inf')
        color = color_list[num % len(color_list)]
        for j in gene_dict_a[i]:
            x, y = j
            y = y * genome_height + genome_height/2
            svg.drawSymbol(x, y, block_height/2, color, 'd', alpha=1.0, lt=10)
            if y < min_y:
                min_y = y
                min_x = x
        # svg.drawLine(min_x, min_y-block_height/4, min_x, 0, 10)
        # svg.writeString(i, min_x, 0, 64, rotate=315)
    for num, i in enumerate(gene_dict_b):
        min_y = float('inf')
        color = color_list[num % len(color_list)]
        for j in gene_dict_b[i]:
            x1, x2, y = j
            y = y * genome_height + genome_height / 2 + panel2_start
            svg.drawSymbol(x1, y, block_height/2, color, 'd', alpha=1.0, lt=10)
         #   svg.drawLine(x1 - block_height/4, y, x2, y, 5)
            if y < min_y:
                min_y = y
        # svg.drawLine(x2, min_y, x2, len(core_blocks[0]) * genome_height + panel2_start, 10)
        # svg.writeString(i, x2, len(core_blocks[0]) * genome_height + panel2_start, 64, rotate=315, justify='right')
    svg.close_group()
    legend_start = (len(core_blocks[0]) + 3) * genome_height * 2
    font_size = genome_height * 0.7
    curr_y = legend_start
    if bp < 50000:
        scale1size = 5000
        scale1txt = "5 Kbp"
    elif bp <= 100000:
        scale1size = 10000
        scale1txt = "10 Kbp"
    elif bp <= 500000:
        scale1size = 50000
        scale1txt = "50 Kbp"
    elif bp <= 1000000:
        scale1size = 100000
        scale1txt = "100 Kbp"
    elif bp <= 5000000:
        scale1size = 500000
        scale1txt = "500 Kbp"
    elif bp <= 10000000:
        scale1size = 1000000
        scale1txt = "1 Mbp"
    elif bp <= 50000000:
        scale1size = 5000000
        scale1txt = "5 Mbp"
    else:
        scale1size = 10000000
        scale1txt = "10 Mbp"
    if bp_blocks < 50000:
        scale2size = 5000
        scale2txt = "5 Kbp"
    elif bp_blocks <= 100000:
        scale2size = 10000
        scale2txt = "10 Kbp"
    elif bp_blocks <= 500000:
        scale2size = 50000
        scale2txt = "50 Kbp"
    elif bp_blocks <= 1000000:
        scale2size = 100000
        scale2txt = "100 Kbp"
    elif bp_blocks <= 5000000:
        scale2size = 500000
        scale2txt = "500 Kbp"
    elif bp_blocks <= 10000000:
        scale2size = 1000000
        scale2txt = "1 Mbp"
    elif bp_blocks <= 50000000:
        scale2size = 5000000
        scale2txt = "5 Mbp"
    else:
        scale2size = 10000000
        scale2txt = "10 Mbp"
    svg.drawLine(50, curr_y+block_height/2, 50 + scale1size / scale, curr_y+block_height/2, genome_line_width, (0, 0, 0))
    svg.drawLine(50, curr_y, 50, curr_y + block_height, genome_line_width, (0,0,0))
    svg.drawLine(50 + scale1size / scale, curr_y, 50 + scale1size / scale, curr_y + block_height, genome_line_width, (0,0,0))
    svg.writeString(scale1txt + ' (panel a)', 50, curr_y + genome_height + font_size, font_size)
    curr_y += genome_height * 2.1
    svg.drawLine(50, curr_y + block_height/2, 50 + scale2size / scale2, curr_y+block_height/2, genome_line_width, (0, 0, 0))
    svg.drawLine(50, curr_y, 50, curr_y + block_height, genome_line_width, (0,0,0))
    svg.drawLine(50 + scale2size / scale2, curr_y, 50 + scale2size / scale2, curr_y + block_height, genome_line_width, (0,0,0))
    svg.writeString(scale2txt + ' (panel b)', 50, curr_y + genome_height+font_size, font_size)
    curr_y += genome_height * 2.1
    svg.seperate_figure(width, legend_size * genome_height)
    if color_cat:
        svg.writeString("Block categories", figure_width / 2, legend_start + 3 * genome_height / 4, font_size)
    for num, i in enumerate(cat_list):
        svg.drawPatternRect(figure_width / 2, legend_start + (num + 1) * genome_height, figure_width / 100,
                            block_height, i, pattern_dict[i])
        svg.writeString(i, figure_width / 2 + figure_width / 100,
                        legend_start + (num + 1) * genome_height + 3 * genome_height / 4, font_size)
    if len(gene_dict_b) > 0:
        svg.writeString("Genes", figure_width / 4, legend_start + 3 * genome_height / 4, font_size)
    for num, i in enumerate(gene_dict_b):
        color = color_list[num % len(color_list)]
        svg.drawSymbol(figure_width / 4, legend_start + (num + 1) * genome_height + block_height / 2, block_height / 2,
                       color, 'd', alpha=1.0, lt=10)
        svg.writeString(i, figure_width / 4 + block_height / 2,
                        legend_start + (num + 1) * genome_height + 3 * genome_height / 4, font_size)
    curr_y = 0
    svg.drawHueGradient(50, curr_y, figure_width/10, genome_height, core_sat, core_light)
    svg.writeString('start', 50, curr_y + genome_height + font_size, font_size)
    svg.writeString('Position of core block in genome', 50+figure_width/20, curr_y + genome_height + font_size, font_size, justify='middle')
    svg.writeString('end', 50+figure_width/10, curr_y + genome_height + font_size, font_size, justify='right')
    curr_y += genome_height * 2.1
    color = hsl_to_rgb(0, core_sat, core_light)
    out_color = hsl_to_rgb(0, core_sat, max([core_light - 0.2, 0]))
    svg.drawOutRect(50, curr_y, figure_width / 100, genome_height, color, out_color)
    color = hsl_to_rgb(200, core_sat, core_light)
    out_color = hsl_to_rgb(200, core_sat, max([core_light - 0.2, 0]))
    svg.drawOutRect(figure_width / 100 + 50 + gap, curr_y, figure_width / 200, genome_height, color, out_color)
    svg.writeString('Core blocks', 50, curr_y + genome_height + font_size, font_size)
    curr_y += genome_height * 2.1
    color = color_list[12]
    pattern = pattern_list[0]
    svg.create_pattern('leg1', color, pattern, 50, 50)
    svg.drawPatternRect(50, curr_y, figure_width/100, genome_height, 'leg1', color, 1)
    color = color_list[13]
    pattern = pattern_list[1]
    svg.create_pattern('leg2', color, pattern, 50, 50)
    svg.drawPatternRect(figure_width/100 + 50 +gap, curr_y, figure_width/200, genome_height, 'leg2', color, 1)
    svg.writeString('Non-core blocks', 50, curr_y + genome_height + font_size, font_size)
    curr_y += genome_height * 2.1
    svg.drawLine(50, curr_y + genome_height/2, figure_width/100, curr_y + genome_height/2, genome_line_width)
    svg.drawLine(figure_width/100 + 50 + gap, curr_y + genome_height/2, figure_width/200, curr_y + genome_height/2, genome_line_width)
    svg.writeString('Unaligned sequence', 50, curr_y + genome_height + font_size, font_size)
    curr_y += genome_height * 2.1
    color = hsl_to_rgb(0, core_sat, core_light)
    out_color = hsl_to_rgb(0, core_sat, max([core_light - 0.2, 0]))
    svg.drawOutRect(50, curr_y, figure_width/100, genome_height, color, out_color)
    svg.drawLine(figure_width/100+50, curr_y + genome_height/2, 50+3*figure_width/100, curr_y + genome_height/2, genome_line_width)
    color = color_list[12]
    svg.drawPatternRect(figure_width/100+50, curr_y, figure_width/100, genome_height, 'leg2', color, 1)
    color = color_list[13]
    svg.drawPatternRect(50+figure_width*5/200, curr_y, figure_width/200, genome_height, 'leg1', color, 1)
    color = hsl_to_rgb(200, core_sat, core_light)
    out_color = hsl_to_rgb(200, core_sat, max([core_light - 0.2, 0]))
    svg.drawOutRect(50 + 3*figure_width/100 + gap_size*2, curr_y, figure_width/100, genome_height, color, out_color)
    svg.writeString('Noncore region adjacent to left core block', 50, curr_y + genome_height + font_size, font_size)
    curr_y += genome_height * 2.1
    color = hsl_to_rgb(0, core_sat, core_light)
    out_color = hsl_to_rgb(0, core_sat, max([core_light - 0.2, 0]))
    svg.drawOutRect(50, curr_y, figure_width / 100, genome_height, color, out_color)
    svg.drawLine(figure_width / 100 + 50 + gap_size, curr_y + genome_height / 2, 50 + gap_size + 3 * figure_width / 100,
                 curr_y + genome_height / 2, genome_line_width)
    color = color_list[12]
    svg.drawPatternRect(figure_width / 100 + 50 + gap_size, curr_y, figure_width / 100, genome_height, 'leg2', color, 1)
    color = color_list[13]
    svg.drawPatternRect(50 + figure_width * 5 / 200 + gap_size, curr_y, figure_width / 200, genome_height, 'leg1', color, 1)
    color = hsl_to_rgb(200, core_sat, core_light)
    out_color = hsl_to_rgb(200, core_sat, max([core_light - 0.2, 0]))
    svg.drawOutRect(50 + 3 * figure_width / 100 + gap_size * 2, curr_y, figure_width / 100, genome_height, color,
                    out_color)
    svg.writeString('Noncore region adjacent to both core blocks', 50, curr_y + genome_height + font_size, font_size)
    curr_y += genome_height * 2.1
    color = hsl_to_rgb(0, core_sat, core_light)
    out_color = hsl_to_rgb(0, core_sat, max([core_light - 0.2, 0]))
    svg.drawOutRect(50, curr_y, figure_width / 100, genome_height, color, out_color)
    svg.drawLine(figure_width / 100 + 50 + 2*gap_size, curr_y + genome_height / 2, 50 + 3 * figure_width / 100 + 2*gap_size,
                 curr_y + genome_height / 2, genome_line_width)
    color = color_list[12]
    svg.drawPatternRect(figure_width / 100 + 50 + 2*gap_size, curr_y, figure_width / 100, genome_height, 'leg2', color, 1)
    color = color_list[13]
    svg.drawPatternRect(50 + figure_width * 5 / 200 + 2*gap_size, curr_y, figure_width / 200, genome_height, 'leg1', color, 1)
    color = hsl_to_rgb(200, core_sat, core_light)
    out_color = hsl_to_rgb(200, core_sat, max([core_light - 0.2, 0]))
    svg.drawOutRect(50 + 3 * figure_width / 100 + gap_size * 2, curr_y, figure_width / 100, genome_height, color,
                    out_color)
    svg.writeString('Noncore region adjacent to right core block', 50, curr_y + genome_height + font_size, font_size)
    if out_file.endswith('html'):
        svg.writesvg(out_file, False, textb)
    else:
        svg.writesvg(out_file, True)



def get_gene_pos(working_dir, genes_faa, skip, num_threads='8', min_ident=90, min_length=0.5):
    if not skip:
        subprocess.Popen('makeblastdb -in ' + genes_faa + ' -out ' + working_dir + '/tempdb -dbtype prot', shell=True).wait()
        subprocess.Popen('blastx -query ' + working_dir + '/input.fasta -db ' + working_dir + '/tempdb -outfmt 6 -num_threads '
                         + num_threads + ' -out ' + working_dir + '/gene_input.out', shell=True).wait()
    len_dict = {}
    with open(genes_faa) as f:
        for line in f:
            if line.startswith('>'):
                name = line.split()[0][1:]
                len_dict[name] = 0
            else:
                len_dict[name] += len(line.rstrip())
    out_list = []
    with open(working_dir + '/gene_input.out') as f:
        for line in f:
            query, subject, ident, length, mismatch, indel, qstart, qstop, rstart, rstop, eval, bitscore = line.split()
            if float(length) >= min_length * len_dict[subject] and float(ident) > min_ident:
                out_list.append((query, subject, int(qstart)))
    return out_list


def get_gene_file(gene_file, name_dict):
    with open(gene_file) as f:
        for line in f:
            fasta, contig, gene, pos = line.split()
            for i in name_dict:
                if name_dict[i] == (fasta, contig):
                    out_list.append(i, gene, int(pos))
    return out_list

def get_categories(cat_file, name_dict):
    cats = {}
    with open(cat_file) as f:
        for line in f:
            if len(line.split()) == 5:
                fasta, contig, cat, start, stop = line.split()
                start, stop = int(start), int(stop)
            else:
                fasta, contig, cat = line.split()
                start, stop = 'all', 'all'
            for i in name_dict:
                if name_dict[i] == (fasta, contig):
                    name = i
                    break
            if name in cats:
                cats[name].append((start, stop, cat))
            else:
                cats[name] = [(start, stop, cat)]
    return cats



parser = argparse.ArgumentParser(prog='Chromatiblock 0.1.0', formatter_class=argparse.RawDescriptionHelpFormatter, description='''
Chromatiblock.py: Large scale whole genome visualisation using colinear blocks.

Version: 0.1.0
License: GPLv3

USAGE: python Chromatiblock.py



''', epilog="Thanks for using Chromatiblock")


parser.add_argument('-d', '--input_directory', action='store', help='fasta file of assembled contigs, scaffolds or finished genomes.')
parser.add_argument('-l', '--order_list', action='store', help='List of fasta files in desired order.')
parser.add_argument('-f', '--fasta_files', nargs='+', action='store', help='List of fasta/genbank files to use as input')
parser.add_argument('-w', '--working_directory', action='store', help='Folder to write intermediate files.')
parser.add_argument('-s', '--sibelia_path', action='store', default='Sibelia', help='Specify path to sibelia '
                                                                '(does not need to be set if Sibelia binary is in path).')
parser.add_argument('-sm', '--sibelia_mode', action='store', default='loose', help='mode for running sibelia <loose|fine|far>')
parser.add_argument('-o', '--out', action='store', help='Location to write output (options *.svg/*.html/*.png')
parser.add_argument('-q', '--ppi', action='store', type=int, default=50, help="pixels per inch (only used for png)")
parser.add_argument('-m', '--min_block_size', action='store', type=int, default=1000, help='Minimum size of syntenic block.')
parser.add_argument('-c', '--categorise', action='store', help='color blocks by category')
parser.add_argument('-gb', '--genes_of_interest_blast', action='store', help='mark genes of interest')
parser.add_argument('-gf', '--genes_of_interest_file', action='store', help='mark genes of interest')
parser.add_argument('-gh', '--genome_height', action='store', type=int, default=280, help='Height of genome blocks')
parser.add_argument('-vg', '--gap', action='store', type=int, default=20, help='gap between genomes')
parser.add_argument('-ss', '--skip_sibelia', action='store_true', help="Use sibelia output already in working directory")
parser.add_argument('-sb', '--skip_blast', action='store_true', help="use existing BLASTx file for annotation")


args = parser.parse_args()





if not args.input_directory is None:
    fasta_list = []
    for i in os.listdir(args.input_directory):
        abspath = os.path.abspath(args.input_directory + '/' + i)
        if not abspath in fasta_list:
            if abspath.endswith('.fna') or abspath.endswith('.fa') or abspath.endswith('.fasta') or abspath.endswith('.gbk'):
                fasta_list.append(abspath)
elif not fasta_files is None:
    fasta_list = args.fasta_files
else:
    sys.stderr.write('No input files found use -f or -d')
    sys.exit()

if not args.order_list is None:
    with open(args.order_list) as f:
        new_fasta_list = []
        for line in f:
            gotit = False
            for i in fasta_list:
                if line.rstrip() in i:
                    new_fasta_list.append(i)
                    gotit = True
                    break
            if not gotit:
                sys.stdout.write(line + ' not found in input fastas.\n')

    for i in fasta_list:
        if not i in new_fasta_list:
            sys.stderr.write('Could not place ' + i + ' appending to end of figure.\n')
            new_fasta_list.append(i)
    fasta_list = new_fasta_list

name_dict = write_fasta_sibel(fasta_list, args.working_directory + '/input.fasta')
if not args.genes_of_interest_blast is None:
    gene_list = get_gene_pos(args.working_directory, args.genes_of_interest, args.skip_blast)
else:
    gene_list = []
if not args.genes_of_interest_file is None:
    gene_list2 = get_gene_file(args.genes_of_interest_file, name_dict)
    gene_list += gene_list2

run_sibel(args.working_directory + '/input.fasta', args.working_directory, args.sibelia_path, args.sibelia_mode, args.min_block_size, args.skip_sibelia)
if not args.categorise is None:
    cats = get_categories(args.categorise, name_dict)
else:
    print('ding')
    cats = {}
cat_set = set()
for i in cats:
    for j in cats[i]:
        cat_set.add(j[2])
gene_set = set()
for i in gene_list:
    gene_set.add(i[1])

legend_size = max([len(gene_set)+1, len(cat_set) + 2, 20])


block_dict, length_dict = get_blocks(args.working_directory, gene_list, cats)
order_blocks_core(block_dict)
out_blocks = get_noncore(block_dict, length_dict)
noncore_pos = place_noncore(out_blocks)
core_array, core_size = place_core(block_dict)
draw_blocks(core_array, noncore_pos, core_size, args.out, args.genome_height, args.gap, legend_size, args.categorise != None)