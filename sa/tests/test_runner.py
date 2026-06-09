import os
import tempfile
import json
from sa.runner import invoke_sa

def test_invoke_sa():
    arch_model = {
        "entities": [
            {"id": "s1", "c4_type": "system", "requirement_ids": ["req1"]}
        ]
    }
    requirements_data = {
        "asrs": ["req1"],
        "non_asr": []
    }
    
    with tempfile.TemporaryDirectory() as temp_dir:
        final_state = invoke_sa(arch_model, requirements_data, temp_dir)
        
        assert "final_report" in final_state
        report = final_state["final_report"]
        
        assert report["summary"]["grade"] in ["F", "D"] # 15 points is a D or F
        assert report["summary"]["total_score"] == 15.0
        
        assert os.path.exists(os.path.join(temp_dir, "scoring_report.json"))
        assert os.path.exists(os.path.join(temp_dir, "scoring_report.md"))
        
        with open(os.path.join(temp_dir, "scoring_report.json"), "r") as f:
            data = json.load(f)
            assert data["summary"]["grade"] == "F"
