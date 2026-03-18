def absorptionE5_RhO2(properties):
    from benchmark.vasp_incar.evaluate import evaluate_incar_task
    return evaluate_incar_task(properties, "absorptionE5_RhO2")
