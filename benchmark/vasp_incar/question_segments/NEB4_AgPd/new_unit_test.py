def NEB4_AgPd(properties):
    from benchmark.vasp_incar.evaluate import evaluate_incar_task
    return evaluate_incar_task(properties, "NEB4_AgPd")
