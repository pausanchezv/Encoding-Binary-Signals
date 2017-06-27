#!/bin/bin/python
# -*- coding: utf-8 -*-

"""
****************************************************
* PROGRAMA DE CODIFICACIONS DE SEQÜÈNCIES BINÀRIES *
****************************************************

Autors: Pau Sanchez Valdivieso i Albert Espín Román
"""

import matplotlib.pyplot as plt
import numpy as np


def complementary(bit):
    """Retorna el valor de bit contrari al que ha arribat"""

    return 1 if bit == 0 else 0


def non_return_to_zero_encoding(sequence):
    """
    **** NON ZERO TO RETURN ENCODING ****

    Aquesta codifiació retorna la seqüència sense canvis.
    """

    return sequence


def non_return_to_zero_level_encoding(sequence):
    """
    **** NON ZERO TO RETURN LEVEL ENCODING ****

    Aquesta codificació retorna un pols negatiu pels 1s i
    manté un valor zero pels 0s.
    """

    return [int(-1 if x == 1 else 0) for x in sequence]


def non_return_to_zero_inverted_encoding(sequence):
    """
     **** NON ZERO TO RETURN INVERTED ENCODING ****

    Aquesta codificació realitza una transició (de valor alt si era baix,
    i viceversa) si rep un 1, i manté el valor que portava si rep un 0.
    """

    out_sequence = [sequence[0]]

    for i in range(1, len(sequence)):

        if sequence[i] == 0:

            out_bit = out_sequence[-1]

        else:

            out_bit = complementary(out_sequence[-1])

        out_sequence.append(out_bit)

    return out_sequence


def bipolar_AMI_encoding(sequence):
    """
    **** BIPOLAR AMI ENCODING ****

    En aquesta codificació, quan s'assigna un impuls positiu al primer '1',
    llavors al següent caldrà assignar-li un impuls negatiu i així
    successivament. Per tant assignarem de manera alterna impulsos positius
    i negatius als '1' lògics de la seqüència donada. Als '0' sempre correspon
    un '0' a la codificació.
    """

    is_up = False
    out_sequence = []

    for x in sequence:

        if not x:
            out_sequence.append(0)
        else:
            if is_up:
                out_sequence.append(-1)
                is_up = False
            else:
                out_sequence.append(1)
                is_up = True

    return tuple(out_sequence)


def bipolar_pseudoternary_encoding(sequence):
    """
    **** BIPOLAR PSEUDOTERNARY ENCODING ****

    En aquesta codificació el bit '1' es representa per absència de senyal. El
    '0' es representa, llavors, mitjançant polsos de polaritat alternada.
    """

    is_up = False
    out_sequence = []

    for x in sequence:

        if x:
            out_sequence.append(0)
        else:
            if is_up:
                out_sequence.append(-1)
                is_up = False
            else:
                out_sequence.append(1)
                is_up = True

    return tuple(out_sequence)


def manchester_encoding(sequence):
    """
    **** MANCHESTER ENCODING ****

    Els codis de Manchester tenen una transició a la meitat del període de cada bit.
    Introduïm una seqüència high to low si el bit és '0', mentre que inserim una
    seqüència low to high en aquells casos els quals el bit observat és '1'.
    """

    out_sequence = []

    for x in sequence:

        if x:
            out_sequence.append(-1)
            out_sequence.append(1)

        else:
            out_sequence.append(1)
            out_sequence.append(-1)

    return out_sequence


def differential_manchester_encoding(sequence):
    """
    **** DIFFERENTIAL MANCHESTER ENCODING ****

    Aquesta codificació té dos valors diferents per cicle de rellotge,
    ja que sempre fa un canvi de flanc a la meitat del cicle. Si la
    seqüència d'entrada té un 1, produeix un canvi a l'inici del cicle
    (i de nou a la meitat, com hem dit), altrament no hi ha canvi de
    flanc fins a la meitat del mateix.
    """

    out_sequence = []

    for i in range(len(sequence)):

        previous_out_bit = 0 if not out_sequence else out_sequence[-1]

        first_half_bit = previous_out_bit if sequence[i] == 0 \
            else complementary(previous_out_bit)

        second_half_bit = complementary(first_half_bit)

        out_sequence.append(first_half_bit)
        out_sequence.append(second_half_bit)

    return out_sequence


def B8ZS_encoding(input_sequence):
    """
    **** BZ8S ENCODING ****

    Per generar aquesta condificació ho farem a partir de la seqüència AMI corresponent
    a la seqüència d'entrada.

    El primer que farem serà cercar aquelles seqüències de 8 zeros de mida.
    És a dir, quan apareixen 8 "zeros" consecutius, s'introdueixen canvis artificials en
    el patró basats en la polaritat de l'últim bit 'un' codificat:

    V: Violació, manté la polaritat anterior en la seqüència.
    B: Transició, inverteix la polaritat anterior en la seqüència.
    Els vuit zeros se substitueixen per la seqüència: 000V B0VB

    La seqüència dependrà de si el bit anterior a la seqüència és positiu o negatiu.
    """

    SUBSEQ_LAST_BOTTOM = [0, 0, 0, -1, 1, 0, 1, -1]
    SUBSEQ_LAST_TOP = [0, 0, 0, 1, -1, 0, -1, 1]

    AMI_sequence = list(bipolar_AMI_encoding(input_sequence))

    zeros_index = []
    i, num_zeros = 0, 0

    while i < len(AMI_sequence):

        if not AMI_sequence[i]:
            num_zeros += 1
            if not num_zeros % 8:
                zeros_index.append(i - (8 - 1))
        else:
            num_zeros = 0

        i += 1

    out_sequence = AMI_sequence

    for zero in zeros_index:

        if AMI_sequence[zero - 1] == -1:
            out_sequence[zero: zero + 8] = SUBSEQ_LAST_BOTTOM

        if AMI_sequence[zero - 1] == 1:
            out_sequence[zero: zero + 8] = SUBSEQ_LAST_TOP

    return tuple(out_sequence)


def HDB3_encoding(input_sequence):
    """
    **** HBD3 ENCODING ****

    Per generar aquesta condificació ho farem a partir de la seqüència AMI corresponent
    a la seqüència d'entrada.

    El primer que farem serà cercar aquelles seqüències de 4 zeros de mida.

    Quan apareixen més de tres zeros consecutius, aquests s'agrupen de 4 en 4, i se
    substitueix cada grup 0000 per una de les seqüències següents d'impulsos: B00V o 000V.

    -B Indica un impuls amb diferent signe que l'impuls anterior. Per tant, B manté la llei
    d'alternança d'impulsos, o llei de bipolaritat, amb la resta d'impulsos transmesos.

    -V Indica un impuls del mateix signe que l'impuls que li precedeix, violant per tant la
    llei de bipolaritat.

    El grup 0000 se substitueix per B00V quan és parell el nombre d'impulsos entre la violació
    V anterior i la que s'ha d'introduir.

    El grup 0000 se substitueix per 000V quan és imparell el nombre d'impulsos entre la violació
    V anterior i la que s'ha d'introduir.
    """

    BOOV_TOP = [1, 0, 0, 1]
    BOOV_BOTTOM = [-1, 0, 0, -1]
    OOOV_TOP = [0, 0, 0, 1]
    OOOV_BOTTOM = [0, 0, 0, -1]

    AMI_sequence = list(bipolar_AMI_encoding(input_sequence))

    zeros_index = []
    i, num_zeros = 0, 0

    while i < len(AMI_sequence):

        if not AMI_sequence[i]:
            num_zeros += 1

            if not num_zeros % 4:

                current_index_zero = i - (4 - 1)

                if len(zeros_index) == 0:

                    if current_index_zero % 2:
                        zeros_index.append([current_index_zero, "ISODD"])
                    else:
                        zeros_index.append([current_index_zero, "ISPAIR"])
                else:
                    previous_index_zero = zeros_index[-1][0]
                    diff = previous_index_zero + 3
                    diff = current_index_zero - diff - 1

                    if diff % 2:
                        zeros_index.append([current_index_zero, "ISODD"])
                    else:
                        zeros_index.append([current_index_zero, "ISPAIR"])
        else:
            num_zeros = 0

        i += 1

    out_sequence = AMI_sequence

    for zero in zeros_index:

        if zero[1] == 'ISPAIR':
            if AMI_sequence[zero[0] - 1] == -1:
                out_sequence[zero[0]: zero[0] + 4] = BOOV_TOP

            if AMI_sequence[zero[0] - 1] == 1:
                out_sequence[zero[0]: zero[0] + 4] = BOOV_BOTTOM

        if zero[1] == 'ISODD':
            if AMI_sequence[zero[0] - 1] == -1:
                out_sequence[zero[0]: zero[0] + 4] = OOOV_BOTTOM

            if AMI_sequence[zero[0] - 1] == 1:
                out_sequence[zero[0]: zero[0] + 4] = OOOV_TOP

    return out_sequence


def generate_random_sequence(length):
    """ Funció que genera aleatòriament una seqüència de tants bits com s'indiqui"""

    import random
    sequence = []

    for i in range(length):

        sequence.append(1 if random.random() >= 0.5 else 0)

    return sequence


def obtain_modulation_values(modulation_type, sequence, t):
    """
    Funció que determina els valors que tindrà un senyal modulat, resultat
    d'aplicar una determinada funció de modulació a la seqüència binària passada
    per paràmetre

    Tenim tres opcions:
        ASK: els 1s es representen amb sinus, els 0s com a absència de senyal
        FSK: els 1s i els 0s es representen amb sinus a freqüències diferents
        PSK: els 1s es representen amb sinus i els 0s amb un desfassament, aquí cosinus
    """


    division_num = 50
    sin_t = np.array([value + i * (t[1] - t[0]) / division_num for value in t for i in range(division_num)])

    freq_multiplier_1 = 1
    freq_multiplier_2 = 2

    sin_output = []
    for i in range(len(sequence)):

        sequence_bit = sequence[i]

        start_index = i * division_num * 2
        end_index = start_index + division_num * 2
        for j in range(start_index, end_index):

            if sequence_bit == 0:

                sin_value = 0

                if modulation_type == "ASK":
                    sin_value = 0

                elif modulation_type == "FSK":
                    sin_value = np.sin(2 * np.pi * freq_multiplier_2 * sin_t[j])

                elif modulation_type == "PSK":
                    sin_value = np.cos(2 * np.pi * freq_multiplier_1 * sin_t[j])

            else:
                sin_value = 1 * np.sin(2 * np.pi * freq_multiplier_1 * sin_t[j])

            sin_output.append(sin_value)

    return sin_t, sin_output


def show_menu():
    """ Funció que mostra el menú per a seleccionar la codificació que
    es vol provar (en quant a les modulacions es mostraran sempre les 3
    estudiades, així s'evita que l'usuari hagi d'interactuar tant, tenint
    en compte que com són només 3 les podem mostrar sempre)"""

    print u"PROGRAMA DE MODULACIÓ I CODIFICACIÓ DE SEQÜÈNCIES BINÀRIES"

    sequence_length = 20

    sequence = generate_random_sequence(sequence_length)

    option = 0

    encodings_dict = {1 : non_return_to_zero_encoding,
                      2 : non_return_to_zero_level_encoding,
                      3 : non_return_to_zero_inverted_encoding,
                      4 : bipolar_AMI_encoding,
                      5 : bipolar_pseudoternary_encoding,
                      6 : manchester_encoding,
                      7 : differential_manchester_encoding,
                      8 : B8ZS_encoding,
                      9 : HDB3_encoding}

    while option != -1:

        print u"\nSELECCIONA UNA CODIFICACIÓ A VISUALITZAR\n1. Non-return to Zero\n2. Non-return to Zero-Level\n3. Non-return to Zero-Level Inverted\n4. Bipolar-AMI\n5. Pseudoternary\n6. Manchester\n7. Differential Manchester\n8. B8ZS\n9. HDB3\n0. Generar una nova seqüència.\n-1. Sortir\n"
        option = raw_input(u"Introdueix un nombre d'entre les opcions >> ")

        try:
            option = int(option)

            if 1 <= option <= 9:

                print u"Tanca la finestra de la codificació que s'acaba d'obrir quan vulguis continuar.\n"
                show_encoding(sequence, encodings_dict[option])

            elif option == 0:

                sequence = generate_random_sequence(sequence_length)
                print u"\nS'ha generat una nova seqüència de bits\n"

            elif option != -1:
                print u"\nError: El valor no és un nombre enter al rang permès!\n"

        except ValueError:
            print u"\nError: El valor no és un nombre enter!\n"

    print "\nEl programa ha finalitzat.\n"


def display_lines(axis, positions, *args, **kwargs):
    """ Funció de suport que genera línies a la pantalla """

    if axis == 'x':

        for p in positions:

            plt.axvline(p, *args, **kwargs)
    else:

        for p in positions:

            plt.axhline(p, *args, **kwargs)


def show_encoding(sequence, encoding_function):
    """ Funció que calcula i mostra visualment la modulació i la codificació
     d'una seqüència"""

    '''
    En aquesta funció mostrem l'entrada de rellotge, la seqüència d'entrada, la
    seva versió modulada segons un esquema de modulació i la  versió codificada
    de la seqüència d'entrada d'acord amn un model de codificació. Segons el sistema
    de codificació la seqüència resultant tindrà dos valors per bit o només un.
    Per fer-ho fem servir la llibreria Matplotlib de Python seguint un exemple
    de plotting que hem trobat a internet.
    '''

    use_two_values_per_cycle = encoding_function == manchester_encoding or encoding_function == differential_manchester_encoding

    data = np.repeat(sequence, 2)

    clock = 1 - np.arange(len(data)) % 2

    output_sequence = np.array(encoding_function(sequence))

    out_data = output_sequence if use_two_values_per_cycle else np.repeat(output_sequence, 2)

    t = 0.5 * np.arange(len(data))

    plt.figure(figsize=(12, 12))

    plt.hold(True)
    display_lines('x', range(len(sequence)), color='.5', linewidth=2)
    display_lines('y', [-7, -4, -1, 2, 4], color='.5', linewidth=2)
    plt.step(t, clock + 6, 'b', linewidth=2, where='post', label="Rellotge")
    plt.step(t, data + 4, 'g', linewidth=2, where='post', label=u"Seqüència d'entrada")

    modulation_display_height = 2
    modulation_colors = ['y', 'c', 'm']
    for modulation_type in ["ASK", "FSK", "PSK"]:
        sin_t, sin_output = obtain_modulation_values(modulation_type, sequence, t)
        plt.step(sin_t, np.array(sin_output) + modulation_display_height, modulation_colors.pop(0), linewidth=2, where='post', label=u"Modulació " + modulation_type)
        modulation_display_height -= 3

    plt.step(t, out_data -7, 'r', linewidth=2, where='post', label=u"Seqüència codificada\n({})".format((str(encoding_function.__name__).lower().replace("_", " "))))
    plt.ylim([-9, 8])

    for bit_text, bit in enumerate(sequence):

        plt.text(bit_text + 0.5, 3.5, str(bit))

    plt.legend(fontsize="small")
    plt.title(u"Modulació i codificació d'un senyal")
    plt.gca().axis('off')
    plt.show()


if __name__ == "__main__":
    show_menu()
