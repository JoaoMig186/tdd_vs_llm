
from pipeline_tdd import coherence_check

def test_coherence_check():
    assert coherence_check("A Lua é o satélite natural da Terra. Ela reflete a luz do Sol.")
    assert not coherence_check("Lua.")
