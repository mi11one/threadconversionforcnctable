# thread_conversion_for_cnc_table
This is a python script written to use the output from https://github.com/piellardj/image-stylization-threading

The swoopy script converts instructions for a traditional rotary thread art machine into movements a standard cnc router table can understand. 
measurements are swapped to inches and scaled to a 15x20 inch elipse. The elipse is broken up into 6 different zones with unique
offsets for each. the movement around the peg is a half circle going down .125" then a half circle back going up .125". the
tool raises .5" and moves to the next peg. Your Z zero is set just below the top of the peg. 

the peg drill script drills holes for each peg .5" deep. the Z zero is set at the top of the material. 
I intend to update pegdrill script but for now you must manually edit the directory path of the file
you want to open and also the save directory path as well. my apologies. this is temporary. 
