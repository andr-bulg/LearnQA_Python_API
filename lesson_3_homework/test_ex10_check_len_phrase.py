def test_check_len_phrase():
    phrase = input("Введите фразу, длина которой меньше 15 символов: ")
    assert len(phrase) < 15, "Длина фразы больше или равна 15 символам"

