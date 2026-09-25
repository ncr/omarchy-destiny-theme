"""Common editorial grid for the 34 retained technical plates.

Design units are independent of native resolution. The notes and signature have
separate measured regions; illustration callouts must not enter the footer.
"""
from sheet import ARC, GOLD

# Explanatory metadata belongs to the dossier, not a second centre footer.
MAIN_CONTEXT = {
 'truth-lamp': ('HUMAN FAMILY / SCHEMATIC STAND-INS',
                'NO ROBOTS. JUST AWKWARD SILENCES.'),
 'proxy': ('PX-1 / MORNING ROUTE', '10 km / OWNER STILL ASLEEP'),
 'quantum-simulator': ('AXONOMETRIC CUTAWAY / SERVICE CONFIGURATION',),
}

ORIGINAL = {
 'quantum-simulator': ('ERRORS ALSO NEED MANAGEMENT', 'Logical qubits are encoded across physical qubits. The two counts are not interchangeable.', ('ENCODE', 'CHECK', 'CORRECT'), 'THE ERROR BUDGET HAS REQUESTED A LARGER BUDGET.'),
 'sky-racer': ('PILOT STILL REQUIRED', 'Tilted thrust provides acceleration as well as lift. The pilot remains part of the payload.', ('LIFT', 'BANK', 'RECOVER'), 'AUTOPILOT DOES NOT ACCEPT DARES.'),
 'fusion-transport': ('HEAT MUST LEAVE THE SHIP', 'Propulsion and waste heat share a reactor. Radiators are part of the vehicle, not optional luggage.', ('BURN', 'COAST', 'BRAKE'), 'CABIN BAGGAGE EXCLUDES ANOTHER REACTOR.'),
 'greener': ('RELATIVE SUCCESS', 'The target follows the neighbour. A better lawn can therefore make this lawn temporarily worse.', ('SCAN', 'COMPARE', 'OUTGROW'), 'PEACE TREATY SOLD SEPARATELY.'),
 'cortical-mesh': ('CHANNELS ARE NOT THOUGHTS', 'Electrode activity is a signal to decode. A million channels do not make a million readable thoughts.', ('SENSE', 'ENCODE', 'DECODE'), 'INNER MONOLOGUE REMAINS POORLY DOCUMENTED.'),
 'bounder': ('THE HUMAN IS THE PAYLOAD', 'The spring follows the boot through the stride. A joint may rotate; its mounting does not change sides.', ('LOAD', 'RELEASE', 'RECOVER'), 'GRAVITY HAS NOT SIGNED THE WAIVER.'),
 'air-refinery': ('CARBON IS NOT THE ENERGY SUPPLY', 'Captured carbon and water are feedstocks. Energy must enter separately before fuel can leave.', ('CAPTURE', 'CONVERT', 'REFINE'), 'THE EXHAUST DOES NOT PAY THE ELECTRICITY BILL.'),
 'aroma-organ': ('A RECIPE IS NOT A RECEPTOR MAP', 'The valve program meters a blend. It does not establish what a human observer will perceive.', ('METER', 'MIX', 'CLEAR'), 'NOSTALGIA IS NOT A CALIBRATION STANDARD.'),
 'tether-climber': ('THE BEAM PAYS FOR THE CLIMB', 'Traction transfers force into the ribbon. Beamed power supplies energy; the ribbon supplies the route.', ('ACQUIRE', 'GRIP', 'CLIMB'), 'PLEASE KEEP ALL PLANETS INSIDE THE VEHICLE.'),
 'truth-lamp': ('ACCURACY IS NOT DIPLOMACY', 'The lamp claims to detect disbelief, not objective truth. The dinner still requires an off switch.', ('LISTEN', 'INFER', 'REGRET'), 'DESSERT IS AN UNSUPERVISED LEARNING EVENT.'),
 'organ-foundry': ('PRINTED IS NOT READY', 'Cell placement is followed by perfusion and maturation. The diagram is a concept, not an implant clearance.', ('PRINT', 'PERFUSE', 'MATURE'), 'PLEASE DO NOT SELECT DRAFT QUALITY.'),
 'volumetric-stage': ('A VOLUME NEEDS A MEDIUM', 'Addressed particles provide the visible points. Timing, illumination and particle control must agree.', ('ADDRESS', 'EXCITE', 'REFRESH'), 'APPLAUSE IS NOT AN OPTICAL FEEDBACK LOOP.'),
 'proxy': ('DELEGATION HAS LIMITS', 'The robot completes the run. The owner receives the record; the owner does not receive the workout.', ('DELEGATE', 'RUN', 'CLAIM'), 'FITNESS TRANSFER NOT FOUND IN PROTOCOL.'),
 'presence-rig': ('THE FLOOR IS PART OF THE GAME', 'The suit, roller deck and overhead tether share the motion envelope. The human remains inside it.', ('TRACK', 'RESIST', 'RELEASE'), 'REALITY WILL RESUME AFTER THE NEXT CHECKPOINT.'),
}


def note_box(s):
    # Both triptych formats: notes under C, dedicated signature bay to the right.
    # The legacy non-triptych layout retains its compact fallback.
    return (s.W-670, s.H-264, 430) if s.wide else (242, 422, 425)


def signature_box(s):
    return (s.W-133, s.H-158, 78) if s.wide else (s.W-242, 910, 92)


def field_notes(s, d):
    x,y,w=note_box(s)
    def tx(t,xx,yy,size=7,a=.76,**kw):
        return s.text(t,xx,yy,size,track=.08,a=a,**kw)
    s.ln(x,y-12,x+w,y-12,.23,.5)
    tx('FIELD NOTES / '+d['kind'].upper(),x,y,6.5,.62)
    yy=y+21
    for line in s.wrap(d['fact'],w,8,.08):
        tx(line,x,yy,8,.85);yy+=12
    yy+=11
    for label,value in d['rows']:
        # Never shrink or truncate narrative facts to force them into the grid.
        assert s.measure(label,5.8,.08)+s.measure(value,5.8,.08)+18<w, (label,value)
        tx(label,x,yy,5.8,.53);tx(value,x+w,yy,5.8,.81,align='r');yy+=15
    context=MAIN_CONTEXT.get(s.subject,())
    if hasattr(s,'entry'):
        context=(s.entry['model']+' / '+s.entry['domain'].upper(),)
    s.main_context_notes=context
    if context:
        s.ln(x,yy-3,x+w,yy-3,.18,.45)
        yy+=12
        for note in context:
            for line in s.wrap(note,w,7,.08):
                tx(line,x,yy,7,.65);yy+=12
    bottom=yy
    assert bottom < s.H-72, (s.subject,bottom)
    s.field_notes_bounds=(x,y-12,x+w,bottom)


def original_notes(s):
    subject=getattr(s,'subject',None)
    if subject not in ORIGINAL:return
    import json
    from pathlib import Path
    title,fact,process,note=ORIGINAL[subject]
    rows=json.loads(Path(__file__).with_name('original_field_notes.json').read_text())[subject]
    field_notes(s,dict(kind='concept specification',fact=fact,rows=rows,process=process))
    # A short editorial heading fills the compact column previously left blank.
    if not s.wide:
        s.text(title,242,362,9,track=.12,a=.83)
        s.text('DESIGN DOSSIER / FICTIONAL PERFORMANCE TARGETS',242,385,5.8,track=.1,a=.48)
    from triptych import punchline
    punchline(s,note)
