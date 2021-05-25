import sys

from kospeech.audio.rnnoise import RNNoise

denoiser = RNNoise()
stream = sys.stdin.buffer
input_data = stream.read(480 * 2)
va_prob, denoised_data = denoiser.process_frame(input_data)

print(denoised_data)
