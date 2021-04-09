import BaseNews


class AttackCell(BaseNews):
	huffman_prefix = 2

    def __init__(self, x = None, y = None):
        self.x = x;
        self.y = y;

    def encode(self, writer):
        writer.write(huffman_prefix, 2);
        writer.write(x, 8);
        writer.write(y, 8);

    def decode(self, reader):
        self.x = reader.read(8);
        self.y = reader.read(8);
