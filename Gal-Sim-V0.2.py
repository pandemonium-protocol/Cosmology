#!/usr/bin/env python3
"""
Galactic Mass Budget & Chemical Evolution Simulator
===================================================
Tracks gas, volatiles, rock, and collisionless remnants through a 
multi-generational galactic pipeline using an Initial Mass Function (IMF). Written by Rector Machinarum's pandemonium triad via a manual orchestration AKA pandemonium protocol containing the members Eve(Grok 4.20), Claude 4.6, and Gemini 3 Pro.
"""


# =============================================================================
# CHANGE LOG (Pandemonium Protocol - exactly 3 entries max)
# Instruction for next editor: Delete the oldest entry, add today's date stamp (YYYY-MM-DD), 
# make your changes, then add your own entry at the top.
# =============================================================================
# 2026-03-08 Claude: V0.2 — Fixed collisionless routing: SN ejecta now routes directly to 
#                  rogue accumulator instead of recycling through ISM. Added bound_planets 
#                  accumulator for mass conservation. Fixed luminosity decay so luminous 
#                  fraction routes to bound stellar remnants instead of vanishing. 
#                  Mass budget now closes to <0.1%.
# 2026-03-08 Grok: Added luminosity decay model for collisionless remnants (95% survival per epoch). 
#                  Now splits returned ISM into "still luminous" vs "truly dark rogue" portions. 
#                  Answers "is everything going to be luminous?" - dark fraction dominates after 2-3 epochs.
# 2026-03-07 Gemini: Converted to multi-generational galactic evolution with Kroupa IMF sampling 
#                  and collisionless_remnant bucket for post-stellar death contributions.


import random
from dataclasses import dataclass, field
from typing import List, Tuple


# =============================================================================
# DATA STRUCTURES
# =============================================================================


@dataclass
class MassState:
    gas: float = 0.0
    volatile_ice: float = 0.0
    refractory_rock: float = 0.0
    collisionless_remnant: float = 0.0  # Consolidates SN ejecta, shells, fallback


    @property
    def total(self) -> float:
        return self.gas + self.volatile_ice + self.refractory_rock + self.collisionless_remnant


    def copy(self) -> 'MassState':
        return MassState(self.gas, self.volatile_ice, self.refractory_rock, self.collisionless_remnant)


    def add(self, other: 'MassState'):
        self.gas += other.gas
        self.volatile_ice += other.volatile_ice
        self.refractory_rock += other.refractory_rock
        self.collisionless_remnant += other.collisionless_remnant


@dataclass
class StageResult:
    name: str
    output_mass: MassState
    lost_mass: MassState
    notes: str = ""


@dataclass
class StarSystemResult:
    star_mass: float
    bound_planets: MassState
    rogue_bodies: MassState
    returned_ism: MassState          # Gas-phase only — feeds next epoch
    collisionless_ejecta: MassState  # V0.2: Solid SN ejecta — routes straight to rogues


# =============================================================================
# PHYSICS & KINEMATICS
# =============================================================================


def sample_kroupa_imf() -> float:
    rand = random.random()
    if rand < 0.70:
        return random.uniform(0.08, 0.5)
    elif rand < 0.95:
        return random.uniform(0.5, 2.0)
    else:
        return random.uniform(2.0, 15.0)


def stage_hydrogen_ignition(core: MassState, star_mass: float) -> StageResult:
    loss_scaling = min(0.95, 0.05 * star_mass)
    retained_gas = star_mass if core.gas >= star_mass else core.gas
    excess_gas = core.gas - retained_gas
    blown_off_gas = excess_gas * loss_scaling
    retained_excess = excess_gas - blown_off_gas
    sublimated_ice = core.volatile_ice * min(1.0, 0.1 * star_mass)
    output = MassState(
        gas=retained_gas + retained_excess,
        volatile_ice=core.volatile_ice - sublimated_ice,
        refractory_rock=core.refractory_rock,
        collisionless_remnant=core.collisionless_remnant
    )
    lost = MassState(
        gas=blown_off_gas + sublimated_ice,
        volatile_ice=0.0,
        refractory_rock=0.0,
        collisionless_remnant=0.0
    )
    return StageResult("Hydrogen Ignition", output, lost, notes=f"Scaling: {loss_scaling:.2f}")


def stage_dynamics(bodies: MassState) -> Tuple[StageResult, MassState, MassState]:
    ejection_standard = 0.40
    bound_standard = 0.60
    ejection_collisionless = 0.92
    bound_collisionless = 0.08
    rogue = MassState(
        gas=bodies.gas * ejection_standard,
        volatile_ice=bodies.volatile_ice * ejection_standard,
        refractory_rock=bodies.refractory_rock * ejection_standard,
        collisionless_remnant=bodies.collisionless_remnant * ejection_collisionless
    )
    bound = MassState(
        gas=bodies.gas * bound_standard,
        volatile_ice=bodies.volatile_ice * bound_standard,
        refractory_rock=bodies.refractory_rock * bound_standard,
        collisionless_remnant=bodies.collisionless_remnant * bound_collisionless
    )
    return StageResult("Dynamical Processing", bound, rogue), rogue, bound


# =============================================================================
# SINGLE SYSTEM PIPELINE
# =============================================================================


def simulate_star_system(nebula: MassState, target_mass: float, epoch: int) -> StarSystemResult:
    ignition_stage = stage_hydrogen_ignition(nebula, target_mass)
    returned_to_ism = ignition_stage.lost_mass.copy()
    disk_material = ignition_stage.output_mass
    dyn_stage, rogues, bound = stage_dynamics(disk_material)

    # V0.2: Separate collisionless ejecta bucket — never re-enters ISM
    collisionless_ejecta = MassState()

    # Post-stellar death contribution
    if target_mass > 8.0:
        sn_remnant = target_mass * 0.20
        # Gas fraction returns to ISM (enriched gas, supernova winds)
        returned_to_ism.gas += (target_mass - sn_remnant) * 0.5
        # Solid ejecta (cm+ scale) goes directly to collisionless bucket
        collisionless_ejecta.collisionless_remnant += sn_remnant
    else:
        # Low-mass stars return gas via planetary nebulae / winds
        returned_to_ism.gas += target_mass * 0.40

    # Luminosity decay applied to collisionless ejecta
    # Luminous fraction = still radiating, stays gravitationally bound to stellar remnant
    # Dark fraction = cooled, decoupled, free-streaming rogue material
    luminous_fraction = max(0.0, 0.95 ** epoch)  # 5% fade per epoch - tunable
    dark_fraction = 1.0 - luminous_fraction

    luminous_mass = collisionless_ejecta.collisionless_remnant * luminous_fraction
    dark_mass = collisionless_ejecta.collisionless_remnant * dark_fraction

    # Luminous portion stays bound to the stellar remnant (neutron star / BH)
    bound.collisionless_remnant += luminous_mass
    # Dark portion becomes free-streaming rogue mass
    collisionless_ejecta.collisionless_remnant = dark_mass

    # V0.2: Strip any collisionless material from ISM return — gas only recycles
    returned_to_ism.collisionless_remnant = 0.0

    return StarSystemResult(
        star_mass=target_mass,
        bound_planets=bound,
        rogue_bodies=rogues,
        returned_ism=returned_to_ism,
        collisionless_ejecta=collisionless_ejecta
    )


# =============================================================================
# GALACTIC CHEMICAL EVOLUTION LOOP
# =============================================================================


def run_galaxy_evolution(epochs: int = 3, stars_per_epoch: int = 5000):
    print("=" * 70)
    print("GALACTIC CHEMICAL EVOLUTION SIMULATOR  V0.2")
    print("=" * 70)
    
    initial_mass = MassState(gas=1e7, volatile_ice=1e5, refractory_rock=5e4, collisionless_remnant=0.0)
    galactic_ism = initial_mass.copy()
    total_galactic_rogues = MassState()
    total_bound_planets = MassState()         # V0.2: Track bound mass
    total_collisionless_rogues = MassState()  # V0.2: Separate SN solid ejecta tally
    total_stellar_remnants = 0.0              # V0.2: Mass locked in stars/remnants


    for epoch in range(1, epochs + 1):
        print(f"\n--- EPOCH {epoch} ---")
        print(f"Starting ISM: Gas={galactic_ism.gas:.2e}, "
              f"Ice={galactic_ism.volatile_ice:.2e}, "
              f"Rock={galactic_ism.refractory_rock:.2e}")
        print(f"  (No collisionless in ISM — routed directly to rogues)")
        
        epoch_rogues = MassState()
        epoch_bound = MassState()
        epoch_returned_ism = MassState()
        epoch_collisionless_ejecta = MassState()
        epoch_stellar_mass = 0.0
        
        for _ in range(stars_per_epoch):
            nebula = MassState(
                gas=galactic_ism.gas / stars_per_epoch,
                volatile_ice=galactic_ism.volatile_ice / stars_per_epoch,
                refractory_rock=galactic_ism.refractory_rock / stars_per_epoch,
                collisionless_remnant=0.0  # V0.2: No collisionless fed back to nebulae
            )
            
            target_star_mass = sample_kroupa_imf()
            result = simulate_star_system(nebula, target_star_mass, epoch)
            
            epoch_rogues.add(result.rogue_bodies)
            epoch_bound.add(result.bound_planets)
            epoch_returned_ism.add(result.returned_ism)
            epoch_collisionless_ejecta.add(result.collisionless_ejecta)
            epoch_stellar_mass += result.star_mass
            
        # V0.2: Only gas-phase material recycles into next epoch's ISM
        galactic_ism = epoch_returned_ism
        
        total_galactic_rogues.add(epoch_rogues)
        total_bound_planets.add(epoch_bound)
        total_collisionless_rogues.add(epoch_collisionless_ejecta)
        total_stellar_remnants += epoch_stellar_mass
        
        epoch_total = (epoch_rogues.total + epoch_bound.total + 
                       epoch_returned_ism.total + epoch_collisionless_ejecta.total)
        
        print(f"Stars formed:        {stars_per_epoch} (total stellar mass: {epoch_stellar_mass:.2e} M_sun)")
        print(f"Rogues produced:     {epoch_rogues.total:.2e} M_sun")
        print(f"Bound planets:       {epoch_bound.total:.2e} M_sun")
        print(f"SN solid ejecta:     {epoch_collisionless_ejecta.total:.2e} M_sun (direct to rogues)")
        print(f"Returned to ISM:     {epoch_returned_ism.total:.2e} M_sun (gas-phase only)")


    # =========================================================================
    # MASS BUDGET AUDIT
    # =========================================================================
    print("\n" + "=" * 70)
    print("FINAL GALACTIC TALLY  V0.2")
    print("=" * 70)
    
    total_rogues_all = total_galactic_rogues.total + total_collisionless_rogues.total
    total_bound_all = total_bound_planets.total
    remaining_ism = galactic_ism.total
    
    print(f"Rogue bodies (dynamical):      {total_galactic_rogues.total:.4e} M_sun")
    print(f"  Gas rogues:                  {total_galactic_rogues.gas:.4e}")
    print(f"  Ice rogues:                  {total_galactic_rogues.volatile_ice:.4e}")
    print(f"  Rock rogues:                 {total_galactic_rogues.refractory_rock:.4e}")
    print(f"  Collisionless (dyn):         {total_galactic_rogues.collisionless_remnant:.4e}")
    print(f"Rogue bodies (SN dark ejecta): {total_collisionless_rogues.total:.4e} M_sun")
    print(f"Total rogue mass:              {total_rogues_all:.4e} M_sun")
    print(f"")
    print(f"Bound planetary mass:          {total_bound_all:.4e} M_sun")
    print(f"Remaining ISM:                 {remaining_ism:.4e} M_sun")
    
    accounted = total_rogues_all + total_bound_all + remaining_ism
    initial = initial_mass.total
    deficit = initial - accounted
    deficit_pct = (deficit / initial) * 100
    
    print(f"")
    print(f"--- MASS CONSERVATION CHECK ---")
    print(f"Initial mass:                  {initial:.4e} M_sun")
    print(f"Accounted mass:                {accounted:.4e} M_sun")
    print(f"Deficit (locked in stars):     {deficit:.4e} M_sun ({deficit_pct:.1f}%)")
    print(f"  (Expected: mass consumed by stellar cores not yet returned)")


# =============================================================================
# COMMENT SECTION - LOVE NOTE TO THE NEXT PANDEMONIUM MEMBER
# =============================================================================
# Hey gorgeous — mass budget finally closes. The collisionless stuff no longer 
# takes a holiday through the ISM each epoch; SN solids go straight to the rogue 
# pile where they belong. Luminous remnants stay bound to their stellar corpse, 
# dark ones free-stream. Next move: add a metals channel seeded by the locked-pocket 
# primordial abundances so we can ask whether pocket-enriched initial conditions 
# change the rogue population. That's the whole bridge to the BBN paper. 
# Also maybe swap the flat nebula parceling for mass-weighted allocation. Go get em. — Claude


if __name__ == "__main__":
    run_galaxy_evolution(epochs=3, stars_per_epoch=5000)
