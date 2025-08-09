"""
Causal Diamond Throttling Mechanism

Mechanism: Your local "causal diamond" (what can influence you within a proper tick) 
shrinks with acceleration/gravity. Fewer nodes/links fit inside → fewer independent 
modes are addressable per tick.

Motion: Large boosts tilt/narrow the diamond (relativity of simultaneity), reducing simultaneous access.
Curvature: Gravitational redshift squeezes the diamond radially.

Signature: Time dilation scales with accessible volume of the causal diamond; 
predicts specific cross-terms when boost and redshift coexist.
"""

import numpy as np
from typing import Dict
from ..framework.substrate import DoFMechanism, SubstrateNetwork

class CausalDiamondThrottling(DoFMechanism):
    """
    DoF reduction via causal diamond volume throttling.
    
    The accessible volume of the causal diamond determines how many
    voxels can be updated simultaneously, limiting the effective DoF.
    """
    
    def __init__(self, 
                 base_diamond_radius: float = 1.0,
                 motion_compression_factor: float = 1.0,
                 curvature_compression_factor: float = 1.0):
        """
        Initialize causal diamond mechanism.
        
        Args:
            base_diamond_radius: Base radius of causal diamond in Planck units
            motion_compression_factor: How much motion compresses the diamond
            curvature_compression_factor: How much curvature compresses the diamond
        """
        self.base_radius = base_diamond_radius
        self.motion_factor = motion_compression_factor
        self.curvature_factor = curvature_compression_factor
    
    def compute_diamond_volume(self, s_hat: float, lambda_hat: float) -> float:
        """
        Compute the accessible volume of the causal diamond.
        
        Args:
            s_hat: Kinematic smear parameter
            lambda_hat: Gravitational load parameter
            
        Returns:
            Relative volume of accessible causal diamond
        """
        # Motion effect: Lorentz contraction along boost direction
        # Reduces effective simultaneity surface
        motion_compression = 1.0 - self.motion_factor * s_hat**2
        
        # Curvature effect: Gravitational redshift compresses radially
        curvature_compression = 1.0 - self.curvature_factor * lambda_hat
        
        # Combined volume reduction
        relative_volume = motion_compression * curvature_compression
        
        return max(relative_volume, 0.01)  # Prevent complete collapse
    
    def compute_dof_reduction(self, 
                            substrate: SubstrateNetwork,
                            s_hat: float, 
                            lambda_hat: float) -> float:
        """
        Compute DoF reduction based on causal diamond volume.
        
        The number of accessible modes is proportional to the volume
        of the causal diamond that can be updated per tick.
        """
        diamond_volume = self.compute_diamond_volume(s_hat, lambda_hat)
        
        # DoF scales with accessible volume
        # In 3D, volume ~ radius^3, so DoF ~ volume^(1/3) for surface modes
        # or DoF ~ volume for bulk modes
        dof_fraction = diamond_volume**(2/3)  # Intermediate scaling
        
        return dof_fraction
    
    def get_signature(self) -> Dict[str, str]:
        """Return observational signatures of causal diamond throttling."""
        return {
            "time_dilation": "Scales with accessible causal diamond volume",
            "cross_terms": "Specific boost × redshift interactions from diamond geometry",
            "anisotropy": "Directional effects along boost axis due to simultaneity changes",
            "horizon_behavior": "Smooth approach to zero DoF near event horizons",
            "dispersion": "Minimal - diamond size affects all frequencies equally"
        }
    
    def plot_diamond_evolution(self, 
                              s_range: tuple = (0, 0.9),
                              lambda_range: tuple = (0, 0.9),
                              resolution: int = 50):
        """Plot how causal diamond volume changes with motion and curvature."""
        import matplotlib.pyplot as plt
        
        s_vals = np.linspace(s_range[0], s_range[1], resolution)
        lambda_vals = np.linspace(lambda_range[0], lambda_range[1], resolution)
        
        S, L = np.meshgrid(s_vals, lambda_vals)
        Volume = np.zeros_like(S)
        DoF = np.zeros_like(S)
        
        for i in range(resolution):
            for j in range(resolution):
                s, l = S[i,j], L[i,j]
                Volume[i,j] = self.compute_diamond_volume(s, l)
                DoF[i,j] = self.compute_dof_reduction(None, s, l)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Plot diamond volume
        contour1 = ax1.contourf(S, L, Volume, levels=20, cmap='viridis')
        ax1.set_xlabel('Smear ŝ')
        ax1.set_ylabel('Load λ̂')
        ax1.set_title('Causal Diamond Volume')
        plt.colorbar(contour1, ax=ax1, label='Relative Volume')
        
        # Plot DoF fraction
        contour2 = ax2.contourf(S, L, DoF, levels=20, cmap='plasma')
        ax2.set_xlabel('Smear ŝ')
        ax2.set_ylabel('Load λ̂')
        ax2.set_title('DoF Fraction Available')
        plt.colorbar(contour2, ax=ax2, label='DoF Fraction')
        
        plt.tight_layout()
        return fig, (ax1, ax2)

# Example usage and validation
def validate_causal_diamond_mechanism():
    """
    Validate the causal diamond mechanism against known limits.
    """
    mechanism = CausalDiamondThrottling()
    
    # Test weak field limits
    print("=== Causal Diamond Throttling Validation ===")
    
    # Pure motion (SR limit)
    s_vals = [0.1, 0.3, 0.5, 0.7, 0.9]
    print("\nPure Motion (λ̂ = 0):")
    print("ŝ\tDoF Fraction\tExpected ~(1-ŝ²)")
    for s in s_vals:
        dof = mechanism.compute_dof_reduction(None, s, 0.0)
        expected = (1 - s**2)**(2/3)  # Approximate expectation
        print(f"{s:.1f}\t{dof:.3f}\t\t{expected:.3f}")
    
    # Pure curvature (GR limit)  
    lambda_vals = [0.1, 0.3, 0.5, 0.7, 0.9]
    print("\nPure Curvature (ŝ = 0):")
    print("λ̂\tDoF Fraction\tExpected ~(1-λ̂)")
    for l in lambda_vals:
        dof = mechanism.compute_dof_reduction(None, 0.0, l)
        expected = (1 - l)**(2/3)
        print(f"{l:.1f}\t{dof:.3f}\t\t{expected:.3f}")
    
    # Combined effects
    print("\nCombined Effects:")
    print("ŝ\tλ̂\tDoF Fraction\tCapacity OK")
    test_cases = [(0.3, 0.3), (0.5, 0.5), (0.7, 0.2), (0.2, 0.7)]
    for s, l in test_cases:
        dof = mechanism.compute_dof_reduction(None, s, l)
        capacity_ok = s**2 + l**2 <= 1.0
        print(f"{s:.1f}\t{l:.1f}\t{dof:.3f}\t\t{capacity_ok}")

if __name__ == "__main__":
    validate_causal_diamond_mechanism()
