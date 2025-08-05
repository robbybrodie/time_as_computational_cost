## 4. Arrow of Time

### Paradox:
Why does time seem to flow in one direction, even though the laws of physics are largely time-symmetric?

### Resolution in this Model:
In this computational model, the arrow of time emerges from the asymmetry in computational cost when resolving quantum systems forward versus backward. Forward evolution of quantum systems is computed incrementally through delta-based updates — one tick at a time — with each step building upon previously resolved gate states. This is efficient.

However, reversing the evolution would require computing **all possible prior states** that could have led to the current configuration — an operation that grows exponentially in gate cost as the number of entanglements and interactions increases. The system has no stored history, only present-state resolution through gate pathways. Thus, **the past cannot be recomputed without exceeding available gate bandwidth**, making time reversal infeasible.

This computational asymmetry underlies the thermodynamic and psychological arrows of time. Time appears to "move forward" because that's the direction in which compute cost grows linearly rather than exponentially.

### Example:
A cooled gas expands into a vacuum. The particles’ wavefunctions entangle and evolve as they spread, creating a large number of possible microstates from a low-entropy macrostate. Reversing this evolution would require re-entangling those particles in exactly the right configuration — a prohibitively high compute cost that renders such reversal practically impossible in this model. Thus, entropy increases because gate pathways naturally accumulate in one direction — forward.

---

### Sub-Example: Frame Mismatch and the Illusion of Retrocausality

In small, isolated quantum experiments (like entanglement or delayed-choice setups), observers sometimes record behaviors that appear to imply retrocausality. In this model, such phenomena are explained by **temporal incoherence caused by mismatched resolution frames**.

An isolated quantum system with a very low gate tick rate (e.g. under isolation from the environment) might only compute one or two quantum state transitions over a long period. When this system is later re-entangled with the external universe — whose resolution frame is many orders of magnitude denser — the few updates from the isolated system must be “slotted in” to the global causal mesh.

Because of this sparse data and the observer’s own gate limitations, **the sequence of updates may appear out of order**, giving the illusion of backwards-in-time causation. In truth, the system simply lacked the gate density to preserve consistent observable causality across frames.

This resolves many apparent paradoxes in quantum foundations by treating time-ordering as **an emergent property of gate resolution density**, not an absolute coordinate.