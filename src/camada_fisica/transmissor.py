from math import sin, cos, pi

class Transmissor:
    def __init__(self, amplitude: float, frequencia: float, fase: float):
        """
        Construtor com valores padrão para amplitude, frequencia e fase (serão configurados pelo usuário via GUI)
        """
        self.amplitude = amplitude
        self.frequencia = frequencia
        self.fase = fase

    def gerador_bit_stream(self, mensagem: str) -> list[int]: # Converte uma mensagem em um trem de bits.
        return [int(char) for char in mensagem]

    def nzr_polar(self, bit_stream: list[int]) -> list[int]:
        """
        Aplica modulação NZR Polar no trem de bits.
        """
        return [1 if bit else -1 for bit in bit_stream] # Deixa 1 onde é 1 e coloca -1 onde é 0

    def manchester(self, bit_stream: list[int]) -> list[int]:
        """
        Aplica modulação Manchester no trem de bits.
        """
        i : int = 0
        clk : int = 0
        dig_signal : list[int] = []
        
        while i < len(bit_stream):
            dig_signal.append(bit_stream[i] ^ clk)
            i += 1 * clk
            clk = not clk
            
        return dig_signal

    def bipolar(self, bit_stream: list[int]) -> list[int]:
        """
        Aplica modulação Bipolar no trem de bits.

        :param bit_stream: Trem de bits de entrada
        :return: Trem de bits modulado usando Bipolar
        """
        last_one = 1
        signal = []
        for bit in bit_stream:
            if not bit:
                signal.append(0)
            else:
                signal.append(last_one)
                last_one = -last_one
        return signal
