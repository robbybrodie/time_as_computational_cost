"""
Core substrate simulation framework for time-as-computational-cost experiments.

This module implements the basic voxel/string network substrate with capacity budgets
and provides the foundation for testing different DoF mechanisms.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, Dict, List, Optional, Callable
from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class VoxelState:
    """State of a single voxel in the substrate network."""
    position: np.ndarray  # 3D position
    capacity: float       # Total capacity budget
    used_capacity: float  # Currently used capacity
    connections: List[int]  # Indices of connected voxels
    modes: np.ndarray     # Available vibrational modes
    phase: np.ndarray     # Phase information for each mode
    
    @property
    def available_capacity(self) -> float:
        return self.capacity - self.used_capacity
    
    @property
    def dof_count(self) -> int:
        """Number of accessible degrees of freedom."""
        return len(self.modes)

class SubstrateNetwork:
    """
    Base class for the discrete substrate network.
    
    Implements the fundamental capacity constraint and provides methods
    for computing smear (ŝ) and load (λ̂) parameters.
    """
    
    def __init__(self, 
                 grid_size: Tuple[int, int, int] = (10, 10, 10),
                 voxel_capacity: float = 1.0,
                 planck_length: float = 1.0):
        """
        Initialize the substrate network.
        
        Args:
            grid_size: Dimensions of the voxel grid
            voxel_capacity: Base capacity per voxel
            planck_length: Fundamental length scale
        """
        self.grid_size = grid_size
        self.voxel_capacity = voxel_capacity
        self.planck_length = planck_length
        
        # Initialize voxel grid
        self.voxels = self._initialize_voxels()
        self.total_voxels = np.prod(grid_size)
        
        # Physical parameters
        self.c = 1.0  # Speed of light (natural units)
        
    def _initialize_voxels(self) -> List[VoxelState]:
        """Initialize the voxel network with default connectivity."""
        voxels = []
        
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                for k in range(self.grid_size[2]):
                    pos = np.array([i, j, k]) * self.planck_length
                    
                    # Default: 6-connected cubic lattice
                    connections = self._get_neighbors(i, j, k)
                    
                    # Initialize with random modes (placeholder)
                    n_modes = 6  # One per connection direction
                    modes = np.random.random(n_modes)
                    phases = np.random.random(n_modes) * 2 * np.pi
                    
                    voxel = VoxelState(
                        position=pos,
                        capacity=self.voxel_capacity,
                        used_capacity=0.0,
                        connections=connections,
                        modes=modes,
                        phase=phases
                    )
                    voxels.append(voxel)
                    
        return voxels
    
    def _get_neighbors(self, i: int, j: int, k: int) -> List[int]:
        """Get indices of neighboring voxels in 6-connected lattice."""
        neighbors = []
        directions = [(-1,0,0), (1,0,0), (0,-1,0), (0,1,0), (0,0,-1), (0,0,1)]
        
        for di, dj, dk in directions:
            ni, nj, nk = i + di, j + dj, k + dk
            if (0 <= ni < self.grid_size[0] and 
                0 <= nj < self.grid_size[1] and 
                0 <= nk < self.grid_size[2]):
                idx = ni * self.grid_size[1] * self.grid_size[2] + nj * self.grid_size[2] + nk
                neighbors.append(idx)
                
        return neighbors
    
    def compute_smear(self, velocity: np.ndarray) -> float:
        """
        Compute kinematic smear parameter ŝ.
        
        Args:
            velocity: 3D velocity vector
            
        Returns:
            Smear parameter ŝ ∈ [0, 1)
        """
        v_mag = np.linalg.norm(velocity)
        return min(v_mag / self.c, 0.999)  # Prevent division by zero
    
    def compute_load(self, mass_density: np.ndarray) -> float:
        """
        Compute gravitational load parameter λ̂.
        
        Args:
            mass_density: Local mass-energy density
            
        Returns:
            Load parameter λ̂ ∈ [0, 1)
        """
        # Simplified: proportional to local curvature
        # In full theory, this would come from Einstein tensor
        total_mass = np.sum(mass_density)
        return min(total_mass / (self.total_voxels * self.voxel_capacity), 0.999)
    
    def capacity_constraint_satisfied(self, s_hat: float, lambda_hat: float) -> bool:
        """Check if capacity constraint ŝ² + λ̂² ≤ 1 is satisfied."""
        return s_hat**2 + lambda_hat**2 <= 1.0
    
    def compute_gamma(self, s_hat: float, lambda_hat: float, p: float = 1.0) -> float:
        """
        Compute the dilation factor Γ(ŝ, λ̂).
        
        Args:
            s_hat: Kinematic smear parameter
            lambda_hat: Gravitational load parameter  
            p: Exponent parameter (default 1.0)
            
        Returns:
            Dilation factor Γ
        """
        if not self.capacity_constraint_satisfied(s_hat, lambda_hat):
            raise ValueError("Capacity constraint violated")
            
        sr_factor = 1.0 / np.sqrt(1 - s_hat**2)
        
        # Lapse function N = 1 - λ̂
        N = 1.0 - lambda_hat
        gr_factor = 1.0 / (N**p)
        
        return sr_factor * gr_factor
    
    def proper_time_rate(self, s_hat: float, lambda_hat: float, p: float = 1.0) -> float:
        """Compute dτ/dt = Γ⁻¹."""
        return 1.0 / self.compute_gamma(s_hat, lambda_hat, p)

class DoFMechanism(ABC):
    """Abstract base class for degrees of freedom mechanisms."""
    
    @abstractmethod
    def compute_dof_reduction(self, 
                            substrate: SubstrateNetwork,
                            s_hat: float, 
                            lambda_hat: float) -> float:
        """
        Compute the reduction in degrees of freedom.
        
        Args:
            substrate: The substrate network
            s_hat: Kinematic smear parameter
            lambda_hat: Gravitational load parameter
            
        Returns:
            Fraction of DoF remaining (0 to 1)
        """
        pass
    
    @abstractmethod
    def get_signature(self) -> Dict[str, str]:
        """Return the observational signatures of this mechanism."""
        pass

def plot_dilation_surface(substrate: SubstrateNetwork, 
                         s_range: Tuple[float, float] = (0, 0.9),
                         lambda_range: Tuple[float, float] = (0, 0.9),
                         p: float = 1.0,
                         resolution: int = 50):
    """
    Plot the dilation factor Γ as a function of ŝ and λ̂.
    
    Args:
        substrate: SubstrateNetwork instance
        s_range: Range for ŝ parameter
        lambda_range: Range for λ̂ parameter  
        p: Exponent parameter
        resolution: Grid resolution for plotting
    """
    s_vals = np.linspace(s_range[0], s_range[1], resolution)
    lambda_vals = np.linspace(lambda_range[0], lambda_range[1], resolution)
    
    S, L = np.meshgrid(s_vals, lambda_vals)
    Gamma = np.zeros_like(S)
    
    for i in range(resolution):
        for j in range(resolution):
            s, l = S[i,j], L[i,j]
            if substrate.capacity_constraint_satisfied(s, l):
                Gamma[i,j] = substrate.compute_gamma(s, l, p)
            else:
                Gamma[i,j] = np.nan
    
    fig, ax = plt.subplots(figsize=(10, 8))
    contour = ax.contourf(S, L, Gamma, levels=20, cmap='viridis')
    ax.contour(S, L, S**2 + L**2, levels=[1.0], colors='red', linewidths=2, 
               linestyles='--', label='Capacity constraint')
    
    ax.set_xlabel('Smear ŝ')
    ax.set_ylabel('Load λ̂')
    ax.set_title(f'Dilation Factor Γ(ŝ, λ̂) with p={p}')
    
    cbar = plt.colorbar(contour)
    cbar.set_label('Γ')
    
    ax.legend()
    plt.tight_layout()
    return fig, ax
