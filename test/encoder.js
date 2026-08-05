var stream = require('stream');
var lame = require('../');
var assert = require('assert');
var Readable = stream.Readable;

function collect (readable) {
  return new Promise(function (resolve, reject) {
    var chunks = [];
    readable.on('data', function (chunk) {
      chunks.push(chunk);
    });
    readable.on('error', reject);
    readable.on('end', function () {
      resolve(Buffer.concat(chunks));
    });
  });
}

function pcmFixture (frames, channels) {
  var output = Buffer.alloc(frames * channels * 2);
  var offset = 0;

  for (var frame = 0; frame < frames; frame++) {
    var sample = Math.round(Math.sin(frame / 12) * 10000);
    for (var channel = 0; channel < channels; channel++) {
      output.writeInt16LE(sample, offset);
      offset += 2;
    }
  }

  return output;
}

describe('Encoder', function () {
  var format = {
    channels: 2,
    bitDepth: 16,
    sampleRate: 44100
  };

  it('should encode PCM data to MP3 data', function () {
    var input = Readable.from([ pcmFixture(4096, format.channels) ]);
    var encoder = new lame.Encoder(format);

    assert.equal(typeof encoder._transform, 'function');
    assert(encoder.readable);
    assert(encoder.writable);

    return collect(input.pipe(encoder)).then(function (output) {
      assert(output.length > 0);
    });
  });

  it('should round-trip encoded data through the decoder', function () {
    var input = Readable.from([ pcmFixture(4096, format.channels) ]);

    return collect(input.pipe(new lame.Encoder(format))).then(function (encoded) {
      var decoder = new lame.Decoder();
      var decodedFormat;

      decoder.on('format', function (value) {
        decodedFormat = value;
      });

      return collect(Readable.from([ encoded ]).pipe(decoder)).then(function (decoded) {
        assert(encoded.length > 0);
        assert(decoded.length > 0);
        assert(decodedFormat);
        assert.equal(decodedFormat.sampleRate, format.sampleRate);
        assert.equal(decodedFormat.channels, format.channels);
        assert.equal(decodedFormat.bitDepth, format.bitDepth);
      });
    });
  });

  it('should reject unsupported PCM formats', function () {
    assert.throws(function () {
      new lame.Encoder({ bitDepth: 8, signed: false });
    }, /unsupported PCM format/);
  });
});
