#!/usr/bin/env python

import time
import math

import HC595_shift_reg as shifter

reg = shifter.HC595()



seq = [ [ 1, 0, 0, 0,  1, 0, 0, 0,  1, 0, 0, 0,  1, 0, 1, 0 ],
        [ 0, 0, 1, 0,  0, 1, 0, 1,  0, 1, 0, 1,  0, 1, 0, 1 ],
        [ 1, 0, 0, 0,  1, 0, 0, 0,  0, 0, 0, 0,  0, 0, 0, 0 ],
        [ 0, 0, 0, 0,  0, 0, 0, 0,  1, 0, 0, 0,  1, 0, 0, 0 ],
        [ 1, 0, 0, 1,  0, 0, 1, 0,  1, 0, 0, 1,  0, 0, 1, 0 ] ]

#seq = [ [ 1, 0, 0, 0,  1, 0, 0, 0,  1, 0, 0, 0,  1, 0, 1, 0 ],
#        [ 0, 0, 1, 0,  0, 0, 1, 0,  0, 0, 1, 0,  0, 1, 0, 1 ],
#        [ 1, 0, 0, 0,  0, 0, 0, 0,  1, 0, 1, 0,  0, 0, 0, 0 ],
#        [ 0, 0, 0, 0,  1, 0, 0, 0,  0, 0, 0, 0,  1, 0, 0, 0 ],
#        [ 0, 0, 0, 0,  0, 0, 1, 0,  0, 0, 0, 0,  0, 0, 1, 1 ] ]
        
#seq = [ [ 1, 0, 0, 0,  0, 0, 0, 0  ],
#        [ 0, 1, 0, 0,  0, 0, 0, 0  ],
#        [ 0, 0, 1, 0,  0, 0, 0, 0  ],
#        [ 0, 0, 0, 1,  0, 0, 0, 0  ],
#        [ 0, 0, 0, 0,  1, 0, 0, 0  ] ]

#seq = [ 1, 0, 0, 0, 1, 0, 0, 0,  1, 0, 1, 0, 1, 0, 1, 0,  1, 0, 0, 1, 0, 0, 1, 0,   1, 0, 0, 1, 0, 0, 1, 1 ]
seq_step = 0

val = [ 0 ]
lfo = 3.141596

period = 0.215
while True:

    lfo = lfo + .17
    mag = 0.5 + 0.5 * math.cos( lfo )
    print( mag )
    ontime = 0.008 + 0.007 * mag
    offtime = period - ontime
    
    val[ 0 ] = 0;
    
    for trk in range( 0, 5 ):
    
        if seq[ trk ][ seq_step ] == 1:    
            val[ 0 ] = val[ 0 ] + ( 1 << trk )
            #val[ 0 ] = val[ 0 ] | 0xff
            
    print( val )
    reg.write( val )
    time.sleep( ontime )

    val[ 0 ] = 0x00
    print( val )
    reg.write( val )
    time.sleep( offtime )

    seq_step = seq_step + 1
    if seq_step >= 16:
        seq_step = 0
        
    
    
    
    





