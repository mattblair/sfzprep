# sfzprep 

A very rough draft of:

A tool to generate an [SFZ file](https://sfzformat.com) and sample set compatiable with [AudioKit](https://audiokit.io)'s [AKSampler](https://audiokit.io/docs/Classes/AKSampler.html) from a folder of AIFF files created using MainStage 3's Auto Sampler feature. My main sound sources (for now) are software synths in Ableton Live, but this process will work for sampling hardware synths, or any software synth which can act as a Rewire Device.

## Next Steps

* Move hard-coded values into command line arguments
* Introspect velocity and sample distance values
* Optionally convert AIFF to compressed .wv files
* Debug looping
* Improve handling for low and high end of sample pitch range
* Document the full process, from Ableton to app integration

## Requirements

* Python 3.6 or higher
* AudioKit

### Optional

* Mainstage 3's Auto Sampler feature
* Rewire (for sampling a soft synth)
* [WavPack](http://www.wavpack.com/downloads.html) for compressing samples

## Additional Resources

* Source for the [SFZ extension](https://github.com/AudioKit/AudioKit/blob/master/AudioKit/Common/Nodes/Playback/Samplers/Sampler/AKSampler%2BSFZ.swift) of AKSampler
* [Sampling Synths with Auto Sampler in MainStage 3](https://decrypto.net/sampling-synths-with-auto-sampler-in-mainstage-3/)

