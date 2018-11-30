#!/usr/bin/env python
# Display a runtext with double-buffering.
from samplebase import SampleBase
from rgbmatrix import graphics
from PIL import Image 
import time

class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
        self.parser.add_argument("-t", "--text", help="The text to scroll on the RGB LED panel", default="irgendwas")

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("/media/external/scripts/fonts/9x18B.bdf")

        titleFont=graphics.Font();
        titleFont.LoadFont("/media/external/scripts/fonts/9x15B.bdf")
        titleColor=graphics.Color(107,169,184);

        smallFont=graphics.Font()
        smallFont.LoadFont("/media/external/scripts/fonts/7x13.bdf")
        smallColor=graphics.Color(255,0,255)

        textColor = graphics.Color(255, 255, 0)
        pos = offscreen_canvas.width
        my_text = self.args.text



#       image = Image.open("twitter.png")
#        image.thumbnail((24, 24), Image.ANTIALIAS)
#        self.matrix.SetImage(image.convert('RGB'))



        i=0
        while True:
            offscreen_canvas.Clear()
            
            # somewhere under the rainbow..
            i = (i + 1) % 256
            colors = wheel(i)
            graphics.DrawText(offscreen_canvas,titleFont,1,11,titleColor,"twitter")
            rainbowColor=graphics.Color(colors[0],colors[1],colors[2]);

            graphics.DrawText(offscreen_canvas,font,2,24,smallColor,"@")
            graphics.DrawText(offscreen_canvas,smallFont,14,23,smallColor,"blinken")
            graphics.DrawText(offscreen_canvas,smallFont,14,33,smallColor,"schild")

            len = graphics.DrawText(offscreen_canvas, font, pos, 44, rainbowColor, my_text)
            pos -= 1
            if (pos + len < 0):
                pos = offscreen_canvas.width

            time.sleep(0.02)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)





def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return 0, 0, 0
    if pos < 85:
        return int(255 - pos * 3), int(pos * 3), 0
    if pos < 170:
        pos -= 85
        return 0, int(255 - pos * 3), int(pos * 3)
    pos -= 170
    return int(pos * 3), 0, int(255 - (pos * 3))




# Main function
if __name__ == "__main__":
    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()
