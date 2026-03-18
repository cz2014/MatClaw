def absorptionE8_Pt(properties):
    from benchmark.vasp_incar.evaluate import evaluate_incar_task
    return evaluate_incar_task(properties, "absorptionE8_Pt")
