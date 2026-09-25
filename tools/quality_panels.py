"""Reviewable quality-pass drawings; deterministic paths, type and data labels."""
import math
from century.render import draw_view,callouts
from sheet import WHITE,ARC,GOLD


def main_hardware(s,slug,mx,my):
    entry={'slug':slug,'number':0}
    anchors=draw_view(s,entry,'A',mx,my-20,652,675)
    callouts(s,entry,anchors,mx,my)


def component(s,slug,key,cx,cy,w,h):
    return draw_view(s,{'slug':slug,'number':0},key,cx,cy,w,h)


def aroma_detail(s,rx):
    component(s,'aroma-command','A',rx,313,350,270)
    s.view_label(rx,495,'C','ODOUR COMMAND PATH','METERING HARDWARE / SIX OF 96 CHANNELS SHOWN')


def aroma_program(s,rx):
    # The local recipe is a declared example, not fabricated receptor measurements.
    s.text('ILLUSTRATIVE VALVE PROGRAM',rx-171,543,7,track=.12,a=.73)
    s.text('NOT A RECEPTOR RESPONSE / NO NAMED ODOUR',rx-171,561,5.6,track=.08,a=.49)
    starts=(.10,.20,.05,.42,.32,.63);durations=(.32,.42,.18,.31,.52,.19)
    for i,(a,d) in enumerate(zip(starts,durations)):
        y=585+i*20
        s.text('V'+str(i+1).zfill(2),rx-171,y+3,6,track=.08,a=.65)
        s.ln(rx-128,y,rx+123,y,.13,.45)
        s.ln(rx-128+251*a,y,rx-128+251*(a+d),y,.82,2,color=ARC)
    s.text('SCRIPTED DUTY WINDOWS / NOT MEASURED',rx-171,724,5.7,track=.08,a=.52)
    s.text('A RECIPE IS NOT A PERCEPTION MODEL.',rx-171,752,6.2,track=.09,a=.7,color=GOLD)


def aroma(s,rx):
    aroma_detail(s,rx)
    aroma_program(s,rx)
