#!/usr/bin/env python3

import os
import csv
import lameenc
import wave
import io

out_dir = 'out'


def write_replacement(path, encoding, n_samples, n_channels, sample_rate):
    destination = os.path.join(out_dir, path)
    destination_dir = os.path.split(destination)[0]
    os.makedirs(destination_dir, exist_ok=True)

    sample_width = 2  # 16 bit
    samples = bytes(n_samples * n_channels * sample_width)

    # Generate a silent WAV file in memory.
    with io.BytesIO() as f:
        wav = wave.open(f, mode='wb')
        wav.setnchannels(n_channels)
        wav.setframerate(sample_rate)
        wav.setsampwidth(sample_width)
        wav.writeframes(samples)
        wav.close()
        f.seek(0)
        wav_data = f.read()

    if encoding == 'mp3':
        encoder = lameenc.Encoder()
        encoder.set_bit_rate(64)
        encoder.set_in_sample_rate(sample_rate)
        encoder.set_channels(n_channels)
        encoder.set_quality(7)  # 2-highest, 7-fastest
        mp3_data = encoder.encode(wav_data) + encoder.flush()
        with open(destination, 'wb') as f:
            f.write(mp3_data)
    elif encoding == 'wav':
        with open(destination, 'wb') as f:
            f.write(wav_data)
    else:
        print(f"Unknown encoding for {path}. Skipped!")


def main():
    with open('bad.csv', 'r', newline='') as f:
        reader = csv.DictReader(f)
        for value in reader:
            write_replacement(
                path=value['path'],
                encoding=value['encoding'],
                n_samples=int(value['n_samples']),
                n_channels=int(value['n_channels']),
                sample_rate=int(value['sample_rate']),
            )


if __name__ == '__main__':
    main()
