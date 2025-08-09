"""
Tension-Induced Bandgaps Mechanism

Mechanism: Curvature (load) increases effective "tension" in the string/voxel web, 
opening bandgaps that freeze out high-frequency modes.

Motion: High smear adds directional tension along the motion axis → anisotropic bandgaps.
Curvature: Isotropic (or radial) tension increases → global bandgap widening near masses.

Signature: Frequency-dependent slowdowns (dispersion) in strong fields; 
anisotropic effects at high velocity.
"""

import numpy as np
from typing import Dict, Tuple
from ..framework.substrate import DoFMechanism, SubstrateNetwork

class TensionInducedBandgaps(DoFMechanism):
    """
    DoF reduction via tension-induced frequency bandgaps.
    
    Motion and curvature create tension in the substrate network,
    opening bandgaps that make certain vibrational modes inaccessible.
    """
    
    def __init__(self, 
                 base_frequency_range: Tuple[float, float] = (0.1, 10.0),
                 tension_coupling_strength: float = 1.0,
                 bandgap_width_factor: float = 0.5):
        """
        Initialize tension bandgap mechanism.
        
        Args:
            base_frequency_range: (min, max) frequencies in natural units
            tension_coupling_strength: How strongly tension affects bandgaps
            bandgap_width_factor: Relative width of induced bandgaps
        """
        self.freq_min, self.freq_max = base_frequency_range
        self.tension_coupling = tension_coupling_strength
        self.bandgap_factor = bandgap_width_factor
        
        # Create base frequency spectrum
        self.n_modes = 100
        self.base_frequencies = np.linspace(self.freq_min, self.freq_max, self.n_modes)
    
    def compute_tension_tensor(self, s_hat: float, lambda_hat: float) -> np.ndarray:
        """
        Compute the effective tension tensor in the substrate.
        
        Args:
            s_hat: Kinematic smear parameter
            lambda_hat: Gravitational load parameter
            
        Returns:
            3x3 tension tensor
        """
        # Base isotropic tension from curvature
        isotropic_tension = self.tension_coupling * lambda_hat
        
        # Anisotropic tension from motion (along z-axis by convention)
        anisotropic_tension = self.tension_coupling * s_hat**2
        
        # Construct tension tensor
        tension = np.eye(3) * isotropic_tension
        tension[2, 2] += anisotropic_tension  # Extra tension along motion axis
        
        return tension
    
    def compute_bandgap_structure(self, s_hat: float, lambda_hat: float) -> np.ndarray:
        """
        Compute which frequencies are blocked by bandgaps.
        
        Args:
            s_hat: Kinematic smear parameter
            lambda_hat: Gravitational load parameter
            
        Returns:
            Boolean array indicating accessible frequencies
        """
        tension_tensor = self.compute_tension_tensor(s_hat, lambda_hat)
        
        # Compute effective tension magnitude
        tension_magnitude = np.trace(tension_tensor) / 3.0
        
        # Bandgap opens around characteristic frequency
        gap_center = self.freq_min + tension_magnitude * (self.freq_max - self.freq_min)
        gap_width = self.bandgap_factor * tension_magnitude * (self.freq_max - self.freq_min)
        
        # Determine which frequencies are accessible
        accessible = np.ones(self.n_modes, dtype=bool)
        
        # Block frequencies in the bandgap
        gap_mask = (np.abs(self.base_frequencies - gap_center) < gap_width / 2)
        accessible[gap_mask] = False
        
        # Additional high-frequency cutoff from strong tension
        if tension_magnitude > 0.5:
            cutoff_freq = self.freq_max * (1 - tension_magnitude)
            high_freq_mask = self.base_frequencies > cutoff_freq
            accessible[high_freq_mask] = False
        
        return accessible
    
    def compute_dof_reduction(self, 
                            substrate: SubstrateNetwork,
                            s_hat: float, 
                            lambda_hat: float) -> float:
        """
        Compute DoF reduction based on accessible frequency modes.
        
        The fraction of modes that remain accessible after bandgap formation
        determines the effective degrees of freedom.
        """
        accessible_modes = self.compute_bandgap_structure(s_hat, lambda_hat)
        dof_fraction = np.sum(accessible_modes) / len(accessible_modes)
        
        return dof_fraction
    
    def get_signature(self) -> Dict[str, str]:
        """Return observational signatures of tension-induced bandgaps."""
        return {
            "time_dilation": "Frequency-dependent due to selective mode blocking",
            "dispersion": "Strong - different frequencies experience different delays",
            "anisotropy": "Directional bandgaps along motion axis",
            "spectral_distortion": "Characteristic gaps in frequency spectrum",
            "field_dependence": "Bandgap width scales with field strength",
            "polarization_effects": "Different polarizations affected differently"
        }
    
    def compute_dispersion_relation(self, s_hat: float, lambda_hat: float) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute the modified dispersion relation ω(k) with bandgaps.
        
        Returns:
            frequencies, effective_speeds (c_eff = ω/k)
        """
        accessible = self.compute_bandgap_structure(s_hat, lambda_hat)
        
        # Only accessible frequencies contribute
        accessible_freqs = self.base_frequencies[accessible]
        
        # Compute effective speed for each frequency
        # Higher tension → slower propagation for high frequencies
        tension_tensor = self.compute_tension_tensor(s_hat, lambda_hat)
        tension_magnitude = np.trace(tension_tensor) / 3.0
        
        # Simple model: c_eff = c * (1 - α * tension * (ω/ω_max)^2)
        alpha = 0.5  # Coupling strength
        normalized_freqs = accessible_freqs / self.freq_max
        speed_reduction = alpha * tension_magnitude * normalized_freqs**2
        effective_speeds = 1.0 - speed_reduction  # c = 1 in natural units
        effective_speeds = np.maximum(effective_speeds, 0.1)  # Prevent negative speeds
        
        return accessible_freqs, effective_speeds
    
    def plot_bandgap_evolution(self, 
                              s_range: tuple = (0, 0.9),
                              lambda_range: tuple = (0, 0.9),
                              resolution: int = 50):
        """Plot how bandgap structure evolves with motion and curvature."""
        import matplotlib.pyplot as plt
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Test cases for detailed bandgap structure
        test_cases = [
            (0.0, 0.0, "No load"),
            (0.5, 0.0, "Pure motion"),
            (0.0, 0.5, "Pure curvature"), 
            (0.3, 0.4, "Combined")
        ]
        
        for i, (s, l, label) in enumerate(test_cases):
            ax = axes[i//2, i%2]
            
            accessible = self.compute_bandgap_structure(s, l)
            freqs, speeds = self.compute_dispersion_relation(s, l)
            
            # Plot frequency spectrum
            ax.scatter(self.base_frequencies[accessible], 
                      np.ones(np.sum(accessible)), 
                      c='green', alpha=0.7, label='Accessible')
            ax.scatter(self.base_frequencies[~accessible], 
                      np.ones(np.sum(~accessible)), 
                      c='red', alpha=0.7, label='Blocked')
            
            ax.set_xlabel('Frequency')
            ax.set_ylabel('Mode Status')
            ax.set_title(f'{label}: ŝ={s:.1f}, λ̂={l:.1f}')
            ax.legend()
            ax.set_ylim(0.5, 1.5)
        
        plt.tight_layout()
        return fig, axes
    
    def plot_dispersion_curves(self):
        """Plot dispersion relations for different loading conditions."""
        import matplotlib.pyplot as plt
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        test_cases = [
            (0.0, 0.0, 'No load', 'blue'),
            (0.3, 0.0, 'Motion only', 'green'),
            (0.0, 0.3, 'Curvature only', 'red'),
            (0.2, 0.2, 'Combined', 'purple')
        ]
        
        for s, l, label, color in test_cases:
            freqs, speeds = self.compute_dispersion_relation(s, l)
            
            # Plot frequency vs effective speed
            ax1.plot(freqs, speeds, 'o-', color=color, label=label, alpha=0.7)
            
            # Plot DoF fraction
            dof = self.compute_dof_reduction(None, s, l)
            ax2.bar(label, dof, color=color, alpha=0.7)
        
        ax1.set_xlabel('Frequency')
        ax1.set_ylabel('Effective Speed (c_eff/c)')
        ax1.set_title('Dispersion Relations')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        ax2.set_ylabel('DoF Fraction')
        ax2.set_title('Degrees of Freedom Reduction')
        ax2.set_ylim(0, 1)
        
        plt.tight_layout()
        return fig, (ax1, ax2)

# Validation function
def validate_tension_bandgap_mechanism():
    """
    Validate the tension bandgap mechanism.
    """
    mechanism = TensionInducedBandgaps()
    
    print("=== Tension-Induced Bandgaps Validation ===")
    
    # Test frequency-dependent effects
    print("\nFrequency-dependent DoF reduction:")
    print("ŝ\tλ̂\tDoF Fraction\tBandgap Present")
    
    test_cases = [(0.0, 0.0), (0.3, 0.0), (0.0, 0.3), (0.5, 0.5)]
    for s, l in test_cases:
        dof = mechanism.compute_dof_reduction(None, s, l)
        accessible = mechanism.compute_bandgap_structure(s, l)
        has_bandgap = not np.all(accessible)
        print(f"{s:.1f}\t{l:.1f}\t{dof:.3f}\t\t{has_bandgap}")
    
    # Test dispersion effects
    print("\nDispersion relation analysis:")
    for s, l in [(0.0, 0.0), (0.5, 0.0), (0.0, 0.5)]:
        freqs, speeds = mechanism.compute_dispersion_relation(s, l)
        if len(speeds) > 0:
            speed_variation = np.max(speeds) - np.min(speeds)
            print(f"ŝ={s:.1f}, λ̂={l:.1f}: Speed variation = {speed_variation:.3f}")

if __name__ == "__main__":
    validate_tension_bandgap_mechanism()
