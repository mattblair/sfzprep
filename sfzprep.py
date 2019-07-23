# python3.6+ 

# assumption: Each sample has the naming convention use by AutoSampler: 
# <patch_name>-<note_name>-<velocity>-<xxxx>.aif

import os
from pathlib import Path
import shutil
import aifc
from math import floor, ceil

from midiutils import note_name_to_midi_note_number

# TODO: make some or all of these args or kwargs

target_extension = "aif"

sample_distance = 3 # in semitones

# TODO: restructure to pass this in via command line, or introspect by iterating all files first
velocity_mapping = {
    "42": 0,
    "73": 43,
    "101": 74,
    "127": 102
}

original_samples_directory = "~/Music/Audio Music Apps/Samples/Auto Sampled/funkyOrganTest/"
output_directory = "~/Documents/codeProjects/sfzprep/test2"

output_path = Path(output_directory).expanduser()
try:
    output_path.mkdir()
except FileExistsError as err:
    print(err)

# https://github.com/chris1610/pbpython/blob/master/extras/Pathlib-Cheatsheet.pdf
samplespath = Path(original_samples_directory).expanduser()

patch_name = ""
sfz_string = ""

for samplepath in samplespath.glob('*.aif'):    
    split_string = samplepath.stem.split("-")

    patch_name = split_string[0]
    pitch_name = split_string[1]
    sample_velocity = split_string[2]

    # TODO: conditionally convert sample to Wav/wv here, depending on target_extension
    # TODO: any reason to preserve the last four characters of the stem designated by AutoSampler?
    sample_target_name = f"{patch_name}-{pitch_name}-{sample_velocity}.{target_extension}"
    sample_target_path = output_path / sample_target_name
    shutil.copy(samplepath, sample_target_path)

    # https://docs.python.org/3/library/aifc.html
    #aiff_file = aifc.open(samplepath)
    with aifc.open(samplepath.as_posix()) as aiff_file:

        # use getmarkers() to introspect
        # TODO: Are start and end supported? Check AKSampler code...
        start = aiff_file.getmark(1)
        end = aiff_file.getmark(2)
        loop_start = aiff_file.getmark(3)[1]
        loop_end = aiff_file.getmark(4)[1]

        # or save this in a data structure and convert to strings at the end?

        # Based on example from ROM Player
        # <group>lokey=0 hikey=51 pitch_keycenter=48 pitch_keytrack=100
        #<region> lovel=000 hivel=127 amp_velcurve_127=1 loop_mode=loop_sustain loop_start=105304 loop_end=271114 sample=samples/TX Chorus Bras-000-048-c2.aif

        keycenter = note_name_to_midi_note_number(pitch_name)

        if sample_distance % 2 == 0:

            lokey = keycenter - (sample_distance/2)
            hikey = keycenter + (sample_distance/2) - 1
        else:
            lokey = keycenter - floor(sample_distance/2)
            hikey = keycenter + ceil(sample_distance/2) - 1

        # TODO: What is pitch_keytrack?

        # TODO: calculate low velocity range based on breakpoints! use the next lower value than the velocity, or 0
        # if the velocity value is the lowest in the array, than lovel is 0
        # else it's the next lowest +1
        # temporary fix
        try:
            low_velocity = velocity_mapping[sample_velocity]
        except:
            print("ERROR: low velocity for %s is not defined." % sample_velocity)
            low_velocity = 0
        
        # TODO: do velocity/pitch values need to be left-padded with 0's? only lovel was in the example

        # TODO: What is amp_velcurve_127 ?

        sfz_string += f"<group>lokey={lokey} hikey={hikey} pitch_keycenter={keycenter} pitch_keytrack=100\n"
        sfz_string += f"<region> lovel={low_velocity} hivel={sample_velocity} amp_velcurve_127=1 loop_mode=loop_sustain loop_start={loop_start} loop_end={loop_end} sample={sample_target_name}\n"

        # TODO: what elements can you move up to global? Does AKSampler support that?


print(sfz_string)

with open(output_path / f"{patch_name}.sfz", 'w') as sfz_writer:
    sfz_writer.write(sfz_string) 