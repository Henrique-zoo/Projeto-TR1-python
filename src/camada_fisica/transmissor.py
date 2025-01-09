from math import sin, cos, pi

class Transmissor:
    def __init__(self, amplitude: float, frequencia: float, fase: float):
        """
        Construtor com valores padrão para amplitude, frequencia e fase (serão configurados pelo usuário via GUI)
        """
        self.amplitude = amplitude
        self.frequencia = frequencia
        self.fase = fase
        self.modDigital : int

    def gerador_bit_stream(self, mensagem: str) -> list[bool]: # Converte uma mensagem em um trem de bits.
        return [int(char) for char in mensagem]

    def nzr_polar(self, bit_stream: list[bool]) -> list[int]:
        """
        Aplica modulação NZR Polar no trem de bits.
        """
        self.modDigital = 1
        return [1 if bit else -1 for bit in bit_stream] # Deixa 1 onde é 1 e coloca -1 onde é 0

    def manchester(self, bit_stream: list[bool]) -> list[int]:
        """
        Aplica modulação Manchester no trem de bits.
        """
        self.modDigital = 2
        i : int = 0
        clk : bool = 0
        dig_signal : list[int] = []
        
        while i < len(bit_stream): # repetimos o processo até i atingir o tamanho do bit_stream (quando o tamanho do vetor dig_signal for 2 vezes maior que o do vetor bit_stream)
            dig_signal.append(bit_stream[i] ^ clk) # colocamos o xor entre o clock e o bit de entrada no sinal de saída
            i += 1 * clk # incrementamos i na batida do clock
            clk = not clk # fazemos o clock bater a cada dois ciclos do while
            
        return dig_signal

    def bipolar(self, bit_stream: list[bool]) -> list[int]:
        """
        Aplica modulação Bipolar no trem de bits.
        """
        self.modDigital = 3
        last_one : int = 1
        dig_signal : list[int] = []
        
        for bit in bit_stream:
            if not bit:
                dig_signal.append(0)
            else:
                dig_signal.append(last_one = -last_one)
                
        return dig_signal
    
    def ask(self, dig_signal: list[int], amp_zero: int, amp_one: int, sample: int) -> list[int]:
        signal : list[int] = list(range(len(dig_signal) * sample))
        nzr_polar : bool = self.modDigital == 1
        for i in range(len(dig_signal)):
            for j in range(sample):
                if (abs(dig_signal[i]) and not nzr_polar) or dig_signal[i]:
                    signal[i * sample + j] = amp_one*sin((2 * pi * self.frequencia * j / sample + self.fase)) # A * sen (2pi*f*t + ø)
                else:
                    signal[i * sample + j] = amp_zero*sin((2 * pi * self.frequencia * j / sample + self.fase))
                    
        return signal
    
    def fsk(self, dig_signal: list[int], f_zero: int, f_one: int, sample: int) -> list[int]:
        signal : list[int] = list(range(len(dig_signal) * sample))
        nzr_polar : bool = self.modDigital == 1
        for i in range(len(dig_signal)):
            for j in range(sample):
                if (abs(dig_signal[i]) and not nzr_polar) or dig_signal[i]:
                    signal[i * sample + j] = self.amplitude*sin((2 * pi * f_one * j / sample + self.fase)) # A * sen (2pi*f*t + ø)
                else:
                    signal[i * sample + j] = self.amplitude*sin((2 * pi * f_zero * j / sample + self.fase))
                    
        return signal
    
    def qam_mapping(self, dig_signal: list[int]):
        #Define o mapeamento dos bits para símbolos QAM (8-QAM neste caso)

        symbol_map = {
            ('0', '0', '0'):       (1, 1),
            ('0', '0', '1'):      (1, -1),
            ('0', '1', '0'):      (-1, 1),
            ('0', '1', '1'):     (-1, -1),
            ('1', '0', '0'):   (1/3, 1/3),
            ('1', '0', '1'):  (1/3, -1/3),
            ('1', '1', '0'):  (-1/3, 1/3),
            ('1', '1', '1'):  (-1/3, -1/3)
        }
        symbols = []
        # Itera sobre o sinal digital em blocos de 3 bits
        for i in range(0, len(dig_signal), 3):
            # Obtém um bloco de 3 bits e mapeia para o símbolo correspondente
            bits = tuple(dig_signal[i:i + 3])
            symbols.append(symbol_map[bits])
        return symbols

    def qam8_modulation(self,dig_signal, sample=200):
        #Troca -1 por 0 para permitir o mapeamento na constelação QAM
        if isinstance(dig_signal,str) != True:
            sinal=''
            for i in range(len(dig_signal)):
                char=f"{dig_signal[i]}"
                if char=="-1":
                    char="0"
                sinal=sinal+char
            dig_signal=sinal
        if len(dig_signal)%3!=0:
            dig_signal=dig_signal+"0"
        symbols=self.qam_mapping(dig_signal)
        signal=[]
        for symbol in symbols:
            for i in range(sample):
                signal.append(symbol[0] * cos(2 * pi+i/2) + symbol[1] * sin(2 * pi +i/2))
        return signal

