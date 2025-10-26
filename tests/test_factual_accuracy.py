
import json
from pipeline_tdd import factual_check

with open("ground_truth.json") as f:
    truths = json.load(f)

def test_factual_check():
    assert factual_check("Neil Armstrong foi o primeiro homem na Lua.", truths["Quem foi o primeiro homem a pisar na Lua?"])
    assert not factual_check("Cristóvão Colombo foi à Lua.", truths["Quem foi o primeiro homem a pisar na Lua?"])
