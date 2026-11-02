"""Writes the cleanup quest phase as WolvenKit JSON.

The phase waits until the q305 convoy chase is over (or the quest is done),
then switches off the ambush effects and lighting that the ambush cutscene
leaves switched on, and restores the catwalk and billboards it removes.

Usage: python make_questphase.py <output .questphase.json>
"""
import json
import sys

FX = "#loc_q305_netwatch_ambush_fx"
LIGHTING = "#loc_q305_netwatch_ambush_lighting"
STORM = "#loc_q305_netwatch_ambush_fx_storm"
SCENES = "#q305_05_ambush_scenes"
BARRELS = [
    "#decoset_trash_barrel_fire_a",
    "#decoset_trash_barrel_fire_a_001",
    "#decoset_trash_barrel_fire_a_v2",
    "#decoset_trash_barrel_fire_a_v2_001",
    "#decoset_trash_barrel_fire_a_v2_002",
    "#decoset_trash_barrel_fire_a_v2_003",
]

# (prefab, [(variant, show)])
VARIANTS = [
    (FX, [
        ("fx_after_detonation", 0),
        ("fx_boom_car", 0),
        ("fx_blackwall_EMP", 0),
        ("fx_blackwall_first_discharge", 0),
        ("fx_blackwall_second_discharge", 0),
        ("fx_blackwall_third_discharge", 0),
    ]),
    (SCENES, [("q305_ambush_blackwall", 0)]),
    ("#q305_ambush", [("q305_vfa_during_ambush", 0)]),
    ("#q305_ambush_smokescreen", [("smokescreen", 0)]),
    ("#q305_street_lamp_vfx_impulse", [("q305_after_ambush_vfx", 0)]),
    # The catwalk with billboards that the crash in the cutscene destroys.
    # These are the states the cutscene itself uses to reset the scene.
    # #q305_destruction sits inside the blockout prefab.
    ("#loc_q305_netwatch_ambush_blockout", [
        ("sign_before_explosion", 1),
        ("sign_after_explosion", 0),
    ]),
    ("#q305_destruction", [
        ("car_hit_before", 1),
        ("car_hit_before_screen_a", 1),
        ("car_hit_after", 0),
        ("q305_group_screen_b_emp_cutscene", 0),
    ]),
    (STORM, [("q305_NetwatchAmbushThunderstormFX", 0), ("storm_dissapear", 0)]),
    (LIGHTING, [
        ("q305_lights_blackout", 0),
        ("after_explosion", 0),
        ("chase_rain", 0),
        ("ambush_start", 0),
        ("ambush_start_cloud_trigger", 0),
        ("ambush_maxtac_scene", 0),
        ("ambush_maxtac_fight", 0),
        ("ambush_maxtac_fight_trigger", 0),
        ("fail_trigger", 0),
        ("balcony_scene_light", 0),
        ("drone_color_grade", 0),
        ("johnny_scene_light", 0),
        ("johnny_scene_light_a", 0),
        ("johnny_scene_light_b", 0),
    ]),
] + [(b, [("fx_q305_ambush_fire", 0), ("fx_fire", 1)]) for b in BARRELS]

# Any of these starts the cleanup. q305_main_part_done is set late in the
# chase, once the player drops into the tunnel, far from the ambush street.
# The others cover saves where the quest's own cleanup or ending ran.
TRIGGER_FACTS = ["q305_main_part_done", "q305_chase_deco_clean_done", "q305_done"]
DONE_FACT = "ambush_aftermath_fix_done"


class H:
    """An object written once with a HandleId, then as HandleRefId."""
    def __init__(self, data):
        self.data = data


def cname(v):
    return {"$type": "CName", "$storage": "string", "$value": v}


def socket(name, type_):
    return H({"$type": "questSocketDefinition", "connections": [],
              "name": cname(name), "type": type_})


def connect(src, dst):
    c = H({"$type": "graphGraphConnectionDefinition",
           "destination": dst, "source": src})
    src.data["connections"].append(c)
    dst.data["connections"].append(c)


def node(type_, id_, sockets, **fields):
    d = {"$type": type_, "id": id_}
    d.update(fields)
    d["sockets"] = sockets
    return H(d)


def build():
    nodes = []
    inp_out = socket("Out", "Output")
    nodes.append(node("questInputNodeDefinition", 0,
                      [socket("CutDestination", "CutDestination"), inp_out],
                      socketName=cname("In1")))

    wdm_in = socket("In", "Input")
    wdm_out = socket("Out", "Output")
    end_in = socket("In", "Input")

    for i, fact in enumerate(TRIGGER_FACTS):
        p_in, p_out = socket("In", "Input"), socket("Out", "Output")
        connect(inp_out, p_in)
        connect(p_out, wdm_in)
        cond = H({"$type": "questFactsDBCondition", "type": H({
            "$type": "questVarComparison_ConditionType",
            "comparisonType": "Greater", "factName": fact, "value": 0})})
        nodes.append(node("questPauseConditionNodeDefinition", 2 + i,
                          [socket("CutDestination", "CutDestination"), p_in, p_out],
                          condition=cond))

    params = [{
        "$type": "questTogglePrefabVariant_NodeTypeParams",
        "prefabNodeRef": {"$type": "NodeRef", "$storage": "string", "$value": ref},
        "variantStates": [{"$type": "questVariantState", "name": cname(n), "show": s}
                          for n, s in states],
    } for ref, states in VARIANTS]
    nodes.append(node("questWorldDataManagerNodeDefinition", 10,
                      [socket("CutDestination", "CutDestination"), wdm_in, wdm_out],
                      type=H({"$type": "questTogglePrefabVariant_NodeType",
                              "params": params})))

    # Marks that the cleanup ran, so it can be checked from the CET console.
    fact_in, fact_out = socket("In", "Input"), socket("Out", "Output")
    connect(wdm_out, fact_in)
    nodes.append(node("questFactsDBManagerNodeDefinition", 11,
                      [socket("CutDestination", "CutDestination"), fact_in, fact_out],
                      type=H({"$type": "questSetVar_NodeType", "factName": DONE_FACT,
                              "setExactValue": 1, "value": 1})))

    connect(fact_out, end_in)
    nodes.append(node("questOutputNodeDefinition", 1,
                      [socket("CutDestination", "CutDestination"), end_in],
                      socketName=cname("Out1"), type="Terminating"))

    return {
        "$type": "questQuestPhaseResource",
        "cookingPlatform": "PLATFORM_PC",
        "graph": H({"$type": "questGraphDefinition", "nodes": nodes}),
        "inplacePhases": [],
        "phasePrefabs": [],
    }


def serialize(root):
    ids = {}

    def walk(o):
        if isinstance(o, H):
            if id(o) in ids:
                return {"HandleRefId": str(ids[id(o)])}
            ids[id(o)] = len(ids)
            return {"HandleId": str(ids[id(o)]), "Data": walk(o.data)}
        if isinstance(o, dict):
            return {k: walk(v) for k, v in o.items()}
        if isinstance(o, list):
            return [walk(v) for v in o]
        return o

    return walk(root)


def main(out_path):
    doc = {
        "Header": {"WolvenKitVersion": "10.0.0-beta.2-nightly.2026-10-31",
                   "WKitJsonVersion": "0.0.9", "GameVersion": 2500,
                   "DataType": "CR2W"},
        "Data": {"Version": 195, "BuildVersion": 0,
                 "RootChunk": serialize(build()), "EmbeddedFiles": []},
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=2)


if __name__ == "__main__":
    main(sys.argv[1])
