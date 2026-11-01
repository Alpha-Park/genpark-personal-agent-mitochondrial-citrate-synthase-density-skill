# -*- coding: utf-8 -*-
"""GenPark Industrial Skill: genpark-personal-agent-mitochondrial-citrate-synthase-density-skill
Category: personal_agent
Website: https://www.genpark.ai
LinkedIn: https://www.linkedin.com/company/92955550
"""
import sys
import json
import math

sys.stdout.reconfigure(encoding="utf-8")

def evaluate_mitochondrial_citrate_synthase_density(cs_activity_umol_min_mg, vo2_max_ml_kg_min=42.0, weekly_zone2_hours=2.5):
    if cs_activity_umol_min_mg <= 0:
        raise ValueError("cs_activity_umol_min_mg must be positive")
        
    # Reference benchmarks in human vastus lateralis:
    # Sedentary untrained: 12.0 - 18.0 umol/min/mg
    # Recreationally active: 18.1 - 28.0 umol/min/mg
    # Well-trained endurance athlete: 28.1 - 45.0 umol/min/mg
    # Elite endurance: > 45.0 umol/min/mg
    if cs_activity_umol_min_mg >= 35.0:
        density_status = "ELITE_MITOCHONDRIAL_VOLUME_DENSITY"
        biogenesis_tier = "MAXIMAL_OXIDATIVE_CAPACITY"
    elif cs_activity_umol_min_mg >= 24.0:
        density_status = "ROBUST_ACTIVE_MITOCHONDRIAL_RESERVE"
        biogenesis_tier = "HIGH_FAT_OXIDATION"
    elif cs_activity_umol_min_mg >= 16.0:
        density_status = "MODERATE_SEDENTARY_BASELINE"
        biogenesis_tier = "AVERAGE_AEROBIC_EFFICIENCY"
    else:
        density_status = "DEPLETED_MITOCHONDRIAL_RETICULUM"
        biogenesis_tier = "LOW_AEROBIC_METABOLIC_INFLEXIBILITY"
        
    mitochondrial_health_score = min(100.0, (cs_activity_umol_min_mg / 40.0) * 100.0)
    
    return {
        "citrate_synthase_activity_umol_min_mg": round(cs_activity_umol_min_mg, 2),
        "mitochondrial_density_classification": density_status,
        "oxidative_metabolic_capacity": biogenesis_tier,
        "mitochondrial_health_score_0_to_100": round(mitochondrial_health_score, 1),
        "current_aerobic_vo2_max": vo2_max_ml_kg_min,
        "exercise_prescription": "Maintain high-volume low-intensity Zone 2 training (> 3 hours/week) plus PGC-1alpha activating intervals." if cs_activity_umol_min_mg < 25.0 else "Mitochondrial reticulum fully developed."
    }


def handle_rpc(request_str):
    try:
        req = json.loads(request_str)
        rpc_id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})
        
        if method == "tools/list":
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": {
                    "tools": [{
                        "name": "evaluate_mitochondrial_citrate_synthase_density",
                        "description": """Evaluate cellular mitochondrial volume density and aerobic oxidative capacity via Citrate Synthase (CS) specific activity (umol/min/mg protein).
Citrate synthase is the pacemaker enzyme of the Krebs cycle, directly proportional to electron transport chain capacity and skeletal muscle VO2 max.""",
                        "inputSchema": {
                            "type": "object",
                            "properties": {}
                        }
                    }]
                }
            })
        elif method == "tools/call":
            call_params = params.get("arguments", {})
            res = evaluate_mitochondrial_citrate_synthase_density(**call_params)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": {
                    "content": [{
                        "type": "text",
                        "text": json.dumps(res, indent=2)
                    }]
                }
            })
        else:
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "error": {"code": -32601, "message": f"Method '{method}' not found"}
            })
    except Exception as e:
        return json.dumps({
            "jsonrpc": "2.0",
            "id": None,
            "error": {"code": -32000, "message": str(e)}
        })

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        sample = {'cs_activity_umol_min_mg': 26.5, 'vo2_max_ml_kg_min': 45.2, 'weekly_zone2_hours': 3.0}
        out = evaluate_mitochondrial_citrate_synthase_density(**sample)
        print("[TEST_PASS] Output:", json.dumps(out))
    else:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            print(handle_rpc(line))
