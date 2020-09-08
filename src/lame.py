import numpy

from src.fade import EOF, BUFFER_SIZE, SAMPLE_RATE, SAMPLE_TYPE, SAMPLE_SIZE

class Encoder(object):
	SILENCE = b'\0' * (SAMPLE_RATE / 1000 * 20 * 4) # 20 ms 16 bit stereo data
	FRAMESIZE = SAMPLE_RATE / 1000 * 20

	def __init__(self, src, channels=2, sampleRate=SAMPLE_RATE, debug=0, sampleType=SAMPLE_TYPE):
		self.channels = channels
		self.frameSize = self.FRAMESIZE
		#self.tempSize = self.frameSize + (self.frameSize + 3) // 4 + 7200 # worst-case estimate
		self.temp = bytearray(self.frameSize * self.channels * SAMPLE_SIZE)
		self.tempSamples = numpy.frombuffer(self.temp, dtype=numpy.int16).reshape((self.frameSize, channels))
		self.view = memoryview(self.temp)
		#self.read = self.write = 0
		self.src = src

	def checkError(self, result):
		if result < 0:
			raise Exception("lame error: %r" % (result,))
		return result

	def read_into(self, buf, ofs, limit):
		if self.src is EOF:
			return 0
		n = min(self.frameSize, limit)
		samples, self.src = self.src.read_into(self.tempSamples, 0, n)
		samplebytes = samples * self.channels * SAMPLE_SIZE
		#sample_array = array.array('h', self.temp[0 : samplebytes])
		#sample_array.byteswap()
		for i in range(0, samplebytes, 2):
			buf[ofs + i] = self.view[i + 1]
			buf[ofs + i + 1] = self.view[i]
		return samplebytes
