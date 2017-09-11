from dftparse.vasp.eigenval_parser import EigenvalParser


def test_simple():
    """
    Test that a simple EIGENVAL from AFLOW can parse

    ref: http://aflowlib.duke.edu/AFLOWDATA/LIB1_RAW/B_s:GGA:01Apr2000/A2/
    """
    lines = """
    1    1    1    1 
  0.6187200E+01  0.2003113E-09  0.2003113E-09  0.2003113E-09  0.5000000E-15 
  1.000000000000000E-004 
  CAR  
 B_s.A2                                   
   128  768  6

  0.0000000e+00  0.0000000e+00  0.0000000e+00  1.3020830e-03
   1   -7.71880
   2   26.05280
   3   26.05280
   4   26.05430
   5   44.93560
   6   44.93560
    """.split("\n")
    parser = EigenvalParser()
    results = list([x for x in parser.parse(lines) if len(x) > 0])

    # Test k-point info
    assert len(results) == 1, "Expected one k-point"
    assert all(abs(x) < 1.0e-9 for x in results[0]['kpoint']), "First k-point should be zero"

    # Test weights
    assert results[0]['weight'] == 1.3020830e-03

    # Test energies
    assert len(results[0]['energies'][2]) == 1, "Expected a single spin"
    assert results[0]['energies'][2][0] == 26.05280, "Band energy was parsed incorrectly"

    # Test occupancies
    assert all("occupancies" not in x for x in results), "Shouldn't parse occupancies"


def test_ispin_no_occ():
    """
    Test that an older EIGENVAL with two spins but no occupancies can parse
    """
    lines = """
    2    2    1    2
  0.1137258E+02  0.2833325E-09  0.2833325E-09  0.2833325E-09  0.5000000E-15
  1.000000000000000E-004
  CAR
 unknown system
   13  165   4

  0.3742002E-15  0.3742002E-15  0.3742002E-15  0.2441406E-03
   1       -1.026133     -1.026134
   2        6.931935      6.931933
   3        6.931935      6.931933
   4        8.754183      8.754179

  0.6250000E-01  0.3742002E-15  0.3742002E-15  0.1464844E-02
   1       -0.951645     -0.951646
   2        6.928633      6.928632
   3        6.949971      6.949970
   4        8.720494      8.720490
    """.split("\n")
    parser = EigenvalParser()
    results = list([x for x in parser.parse(lines) if len(x) > 0])

    # Test k-point info
    assert len(results) == 2, "Expected two k-points"
    assert all(abs(x) < 1.0e-9 for x in results[0]['kpoint']), "First k-point should be zero"
    assert results[1]['kpoint'][0] == 0.0625, "Second k-point should be at (0.0625, 0, 0)"

    # Test weights
    assert results[0]['weight'] == 0.2441406E-03
    assert results[1]['weight'] == 0.1464844E-02

    # Test energies
    assert results[1]['energies'][2][0] == 6.949971, "Band energy was parsed incorrectly"
    assert results[1]['energies'][2][1] == 6.949970, "Band energy was parsed incorrectly"

    # Test occupancies
    assert all("occupancies" not in x for x in results), "Shouldn't parse occupancies"


def test_ispin_occ():
    """
    Test that a newer EIGENVAL with two spins and occupancies can parse
    """
    lines = """
    4    4   10    2
  0.1363242E+02  0.3439000E-09  0.3439000E-09  0.5324000E-09  0.5000000E-15
  1.000000000000000E-004
  CAR
 CrS, AF, PAW
     24      4     28

  0.2500000E+00  0.2500000E+00  0.2500000E+00  0.3333333E+00
    1       -5.646207     -5.646219   1.000000   1.000000
    2       -5.350276     -5.350262   1.000000   1.000000
    3        1.618912      1.618949   1.000000   1.000000
    4        1.915201      1.915141   1.000000   1.000000
    5        2.957850      2.957950   1.000000   1.000000
    6        3.312998      3.313117   1.000000   1.000000
    7        3.725856      3.724918   1.000000   1.000000
    8        3.847446      3.848224   1.000000   1.000000
    9        7.139883      7.140085   1.000000   1.000000
   10        7.479102      7.478062   1.000000   1.000000
   11        8.035477      8.035297   1.000001   1.000001
   12        8.244856      8.245175   1.000457   1.000461
   13        9.195638      9.196664  -0.006644  -0.006529
   14        9.611771      9.612057  -0.000000  -0.000000
   15       10.262991     10.262659  -0.000000  -0.000000
   16       10.473230     10.473164  -0.000000  -0.000000
   17       11.017638     11.018270  -0.000000  -0.000000
   18       11.633896     11.633525  -0.000000  -0.000000
   19       14.175252     14.174732  -0.000000  -0.000000
   20       14.546425     14.545811   0.000000   0.000000
   21       16.428065     16.428222   0.000000   0.000000
   22       16.521699     16.520429   0.000000   0.000000
   23       16.913669     16.914354   0.000000   0.000000
   24       17.803985     17.805176   0.000000   0.000000
   25       18.893940     18.893552   0.000000   0.000000
   26       19.783429     19.783681   0.000000   0.000000
   27       20.058392     20.058783   0.000000   0.000000
   28       23.101575     23.101596   0.000000   0.000000

  0.5000000E+00 -0.2500000E+00  0.2500000E+00  0.1666667E+00
    1       -5.647831     -5.647830   1.000000   1.000000
    2       -5.350552     -5.350553   1.000000   1.000000
    3        1.621595      1.621593   1.000000   1.000000
    4        1.915315      1.915318   1.000000   1.000000
    5        2.955704      2.955704   1.000000   1.000000
    6        3.312222      3.312220   1.000000   1.000000
    7        3.726076      3.726056   1.000000   1.000000
    8        3.849050      3.849073   1.000000   1.000000
    9        7.141115      7.141100   1.000000   1.000000
   10        7.479172      7.479183   1.000000   1.000000
   11        8.033247      8.033248   1.000001   1.000001
   12        8.245817      8.245826   1.000468   1.000468
   13        9.195340      9.195341  -0.006677  -0.006677
   14        9.613735      9.613736  -0.000000  -0.000000
   15       10.262648     10.262637  -0.000000  -0.000000
   16       10.471803     10.471801  -0.000000  -0.000000
   17       11.017299     11.017294  -0.000000  -0.000000
   18       11.632196     11.632200  -0.000000  -0.000000
   19       14.176193     14.176183  -0.000000  -0.000000
   20       14.548062     14.548080   0.000000   0.000000
   21       16.430170     16.430155   0.000000   0.000000
   22       16.527037     16.527031   0.000000   0.000000
   23       16.918066     16.918069   0.000000   0.000000
   24       17.805728     17.805777   0.000000   0.000000
   25       18.893468     18.893452   0.000000   0.000000
   26       19.785319     19.785295   0.000000   0.000000
   27       20.060204     20.060203   0.000000   0.000000
   28       23.101082     23.101073   0.000000   0.000000
    """.split("\n")
    parser = EigenvalParser()
    results = list([x for x in parser.parse(lines) if len(x) > 0])

    # Test k-point info
    assert len(results) == 2, "Expected two k-points"
    assert all(abs(x - 0.25) < 1.0e-9 for x in results[0]['kpoint']), "First k-point should be 0.25^3"
    assert results[1]['kpoint'][0] == 0.5, "Second k-point should be at (0.5, -0.25, 0.25)"

    # Test weights
    assert results[0]['weight'] == 0.3333333E+00
    assert results[1]['weight'] == 0.1666667E+00

    # Test energies
    assert results[0]['energies'][13][0] == 9.611771, "Band energy was parsed incorrectly"
    assert results[0]['energies'][13][1] == 9.612057, "Band energy was parsed incorrectly (second spin)"

    # Test occupancies
    assert results[0]['occupancies'][12][0] == -0.006644, "Band occ was parsed incorrectly"
    assert results[0]['occupancies'][12][1] == -0.006529, "Band occ was parsed incorrectly (second spin)"

    # Test that the sum of the occupancies is about 24
    assert all(abs(sum(x[0] + x[1] for x in res['occupancies']) - 24.0) < 0.5 for res in results)
