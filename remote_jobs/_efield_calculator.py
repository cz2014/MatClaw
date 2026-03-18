"""E-field MD via ForceFieldMDMaker + SumCalculator.

UniformElectricForce: ASE calculator for uniform electric field with
per-element Born effective charges.

EFieldMDMaker: ForceFieldMDMaker subclass that overrides the calculator
property to return SumCalculator([DP, UniformElectricForce]).
"""

from dataclasses import dataclass, field as dc_field

import numpy as np
from ase.calculators.calculator import Calculator, all_changes
from atomate2.forcefields.md import ForceFieldMDMaker


class UniformElectricForce(Calculator):
    """ASE calculator: uniform electric field via per-element effective charges.

    F_i = q_i * E   (vectorial, supports arbitrary field direction)
    U   = -sum(q_i * (r_i . E))
    """

    implemented_properties = ["energy", "forces"]

    def __init__(self, efield_charges, field, **kwargs):
        """
        Parameters
        ----------
        efield_charges : dict
            Element symbol -> effective charge (e). E.g. {"Cu": 0.765, "S": -0.085}.
        field : array-like, shape (3,)
            Electric field vector in eV/A/e.
        """
        super().__init__(**kwargs)
        self.efield_charges = efield_charges
        self.field = np.asarray(field, dtype=float)

    def calculate(self, atoms=None, properties=("energy", "forces"),
                  system_changes=all_changes):
        super().calculate(atoms, properties, system_changes)
        charges = np.array(
            [self.efield_charges[s] for s in atoms.get_chemical_symbols()]
        )
        self.results["forces"] = charges[:, None] * self.field[None, :]
        self.results["energy"] = float(
            -np.sum(charges * (atoms.positions @ self.field))
        )


@dataclass
class EFieldMDMaker(ForceFieldMDMaker):
    """ForceFieldMDMaker with external electric field.

    Overrides the calculator property to return SumCalculator([DP, E-field]).
    All other behavior (trajectory, ionic_steps, task document) is inherited.

    Parameters
    ----------
    efield : tuple of 3 floats
        Electric field vector in eV/A/e. E.g. (0, 0, -0.1) for -z field.
    efield_charges : dict
        Element symbol -> Born effective charge. E.g. {"Cu": 0.765, ...}.
    """

    efield: tuple = (0.0, 0.0, 0.0)
    efield_charges: dict = dc_field(default_factory=dict)

    @property
    def calculator(self) -> Calculator:
        from ase.calculators.mixing import SumCalculator
        from deepmd.calculator import DP

        dp = DP(**self.calculator_kwargs)
        ext = UniformElectricForce(
            efield_charges=self.efield_charges,
            field=self.efield,
        )
        return SumCalculator([dp, ext])
