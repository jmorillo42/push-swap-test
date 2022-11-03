
PUSH_SWAP = '../push-swap/push_swap'

CHECKER = '../push-swap/checker'

# 🇪🇸 FORMATO: (<NÚMERO|TEXTO>, <NÚMERO|TEXTO>, ...),
# 🇪🇸 NOTA: Si la entrada consiste en un único elemento, debe seguirse el formato: (<NUMERO|TEXTO>,),
INPUT_TESTS=(
    (),
    ('',),
    (' ',),
    ('+',),
    ('-',),
    (0,),
    ('-0',),
    ('+0',),
    (' 0',),
    ('0 ',),
    (' 0 ',),
    (42,),
    (-42,),
    ('+42',),
    ('-+42',),
    ('--42',),
    ('+-42',),
    ('++42',),
    ('-42-',),
    ('-42A',),
    (' 42 ',),
    ('00000000000000000000042',),
    (' 00000000000000000000042',),
    ('+00000000000000000000042',),
    ('-00000000000000000000042',),
    ('00000000000000000000042 ',),
    (2147483647,),
    (2147483648,),
    (-2147483648,),
    (-2147483649,),
    (12345678901234567890,),
    ('+12345678901234567890',),
    ('-12345678901234567890',),
    (' 12345678901234567890',),
    ('A',),
    ('FOOBAR',),
    (42, 'FOOBAR'),
    ('42 FOOBAR'),
    ('00000000000000000000042', '000000000000000000000'),
    ('+00000000000000000000042', '+000000000000000000000'),
    ('-00000000000000000000000', '-000000000000000000042'),
    ('-00000000000000000000000', '+000000000000000000000'),
    (1, '', 2),
    (42, 42),
    (1, 42, 2, '+42', 3),
    (' 3 2 6 5 4 1 ',),
    (3, 2, '6 5 4', 1),
    (3, 2, '6 5 A', 1),
    (3, '2 6', 5, '4 1'),
    (-17, -13, -11, -7, -5, -3, -2, '-0', 2, 3, 5, 7, 11, 13, 17),
)

# 🇪🇸 NOTA: No se recomiendan combinaciones de más de 6 números
COMB_ALL_TESTS = (3, )

# 🇪🇸 NOTA: No se recomiendan combinaciones de más de 6 números
COMB_STAT_TESTS = (2, 3, 4, 5)

# 🇪🇸 FORMATO: <NÚMEROS>,
SEQ_TESTS = (
    50,
    100,
    250,
    500,
)

# 🇪🇸 FORMATO: (<NÚMEROS>, <ITERACIONES>),
RANDOM_TESTS = (
    (6, 80),
    (10, 70),
    (15, 60),
    (25, 50),
    (50, 40),
    (80, 30),
    (100, 100),
    (125, 20),
    (250, 20),
    (500, 50),
)
