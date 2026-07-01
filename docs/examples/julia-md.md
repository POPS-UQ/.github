<span class="lang-pill julia">Julia</span>

# Uncertainty in molecular dynamics

This example propagates model uncertainties from the [ACE example](julia-ace.md)
to molecular dynamics trajectories. We run a single MD trajectory with
[Molly.jl](https://github.com/JuliaMolSim/Molly.jl) on bulk silicon under the
*mean* potential (the ridge solution), then **reweight** the trajectory to
estimate a thermodynamic property — the radial distribution function (RDF) —
under the whole POPS posterior, without re-running the simulation.

The full script is at
[`examples/md/pops_rdf.jl`](https://github.com/POPS-UQ/POPSRegression.jl/blob/main/examples/md/pops_rdf.jl).

## Theory: Boltzmann reweighting

Suppose we have a trajectory of atomic configurations $\{q_i\}_{i=1}^N$ obtained
from MD sampling of the potential energy surface defined by the ridge parameter
$\theta_0$. We estimate the expectation of an observable $f(q)$ by the
trajectory average

$$
\hat{f}_{\theta_0,N} = \frac{1}{N} \sum_{i=1}^N f(q_i)
\xrightarrow{N \to \infty}
\frac{\int f(q)\, \mathrm{e}^{-\beta U(q;\theta_0)} \, \mathrm{d}q}
     {\int \mathrm{e}^{-\beta U(q;\theta_0)} \, \mathrm{d}q}.
$$

For any other parameter $\theta \neq \theta_0$, the identity

$$
\frac{\int f(q)\, \mathrm{e}^{-\beta U(q;\theta)} \mathrm{d}q}
     {\int \mathrm{e}^{-\beta U(q;\theta)} \mathrm{d}q}
=
\frac{\int f(q)\, \dfrac{\mathrm{e}^{-\beta U(q;\theta)}}{\mathrm{e}^{-\beta U(q;\theta_0)}}\, \mathrm{e}^{-\beta U(q;\theta_0)} \mathrm{d}q}
     {\int \dfrac{\mathrm{e}^{-\beta U(q;\theta)}}{\mathrm{e}^{-\beta U(q;\theta_0)}}\, \mathrm{e}^{-\beta U(q;\theta_0)} \mathrm{d}q}
$$

lets us reweight the *same* samples to estimate the Boltzmann average under any
$\theta$:

$$
\hat{f}_{\theta_0 \to \theta, N} = \frac{\sum_{i=1}^N w_i\, f(q_i)}{\sum_{i=1}^N w_i},
\qquad w_i = \mathrm{e}^{-\beta\,(U(q_i;\theta) - U(q_i;\theta_0))}.
$$

Drawing $\theta$ from the POPS posterior thus turns a single trajectory into a
distribution over thermodynamic averages. Here we propagate to the RDF $g(r)$ of
bulk silicon at 300 K; after binning in $r$, the reweighting applies
component-wise.

## Fit a POPS ACE potential

The fit mirrors the [ACE example](julia-ace.md): assemble the preconditioned
linear problem and fit the POPS hypercube, keeping the full `Si_tiny` dataset.

```julia
using ACEpotentials, ACEfit
using POPSRegression
using AtomsBuilder
using Molly
using Unitful
using LinearAlgebra, Random, Statistics
using CairoMakie
using ProgressMeter

data_raw, _, _ = ACEpotentials.example_dataset("Si_tiny")

Eref  = [:Si => -158.54496821]
rcut  = 4.0
model = ace1_model(; elements=[:Si], order=3, totaldegree=10, rcut=rcut, Eref=Eref)
n_basis = length(model.ps.WB) + length(model.ps.Wpair)

weights = Dict("default" => Dict("E" => 30.0, "F" => 1.0, "V" => 1.0))
datakw  = (energy_key="dft_energy", force_key="dft_force", virial_key="dft_virial")
data    = [ACEpotentials.AtomsData(s; weights=weights, v_ref=model.model.Vref, datakw...)
           for s in data_raw]

A, Y, W = ACEfit.assemble(data, model)
P  = ACEpotentials.Models.algebraic_smoothness_prior(model.model; p=4)
Ap = Diagonal(W) * (A / P)
Yp = W .* Y

pops = fit(POPSModel, Ap, Yp;
    prior_covariance=1e-4,
    leverage_percentile=0.1)

θ0_pre  = vec(pops.coef)     # coefficients in preconditioned basis
θ0_orig = P \ θ0_pre         # coefficients in native coordinates
ACEpotentials.Models.set_linear_parameters!(model, θ0_orig)
```

## Molecular dynamics trajectory

We run MD under the ridge potential: a 3×3×3 supercell of diamond silicon
(216 atoms), equilibrated for 2 ps then sampled for 20 ps with a BAOA Langevin
integrator. For each frame we record both the pair-distance histogram and the
per-basis ACE energy features — the latter let us reweight samples *without*
re-running MD.

```julia
T_md = 300.0u"K"
sys0 = bulk(:Si, cubic=true) * (3, 3, 3)   # 216 atoms
rattle!(sys0, 0.03)

sys_md = Molly.System(sys0; force_units=u"eV/Å", energy_units=u"eV")
sys_md = Molly.System(sys_md;
    general_inters=(model,),
    velocities=Molly.random_velocities(sys_md, T_md))

simulator = Langevin(dt=1.0u"fs", temperature=T_md, friction=1.0u"ps^-1")

Molly.simulate!(sys_md, simulator, 2_000)   # equilibration

function pair_histogram!(h, sys, edges)
    fill!(h, 0)
    coords, boundary = sys.coords, sys.boundary
    rmax, dx, nb, n = edges[end], step(edges), length(h), length(coords)
    @inbounds for i in 1:n-1, j in i+1:n
        r = norm(Molly.vector(coords[i], coords[j], boundary))
        r ≥ rmax && continue
        b = clamp(Int(fld(ustrip(r), ustrip(dx))) + 1, 1, nb)
        h[b] += 1
    end
    return h
end

n_frames, chunk_steps, n_bins = 200, 100, 300
r_max = 8.14u"Å"
edges = range(0.0u"Å", r_max, length=n_bins + 1)

ace_features_buf = zeros(n_basis, n_frames)
histos_buf       = zeros(Int, n_frames, n_bins)
h_buf            = zeros(Int, n_bins)

@showprogress for i in 1:n_frames
    Molly.simulate!(sys_md, simulator, chunk_steps)
    Xi = ACEpotentials.Models.potential_energy_basis(sys_md, model)
    ace_features_buf[:, i] .= ustrip.(u"eV", Xi)
    pair_histogram!(h_buf, sys_md, edges)
    histos_buf[i, :] .= h_buf
end
```

## Reweighting to the POPS posterior

For each posterior parameter sample $\theta$ from the POPS hypercube, we compute
the energy difference along the trajectory and apply the Boltzmann weight to
obtain the RDF that *would* have been sampled under $\theta$. The min/max
envelope across posterior samples gives a non-parametric uncertainty band.

```julia
function rdf_normalize(h_avg, edges, sys)
    N    = length(sys.coords)
    Vbox = ustrip(u"Å^3", Molly.volume(sys))
    e    = ustrip.(u"Å", collect(edges))
    n_pairs_ideal = N * (N - 1) / 2
    g = similar(h_avg, Float64)
    for b in eachindex(h_avg)
        shell = (4 / 3) * π * (e[b+1]^3 - e[b]^3)
        g[b]  = h_avg[b] / (n_pairs_ideal * shell / Vbox)
    end
    return g
end

n_samples = 2000
S_pre = sample(pops, n_samples; sampling_method=:sobol)
β     = ustrip(u"eV^-1", 1 / (Unitful.k * T_md))

Hf        = Float64.(histos_buf)
g_samples = zeros(n_samples, n_bins)

for s in 1:n_samples
    Δθ_orig = P \ (S_pre[:, s] .- θ0_pre)
    ΔU      = ace_features_buf' * Δθ_orig

    logw  = -β .* ΔU
    logw .-= maximum(logw)            # numerical stability
    w     = exp.(logw)
    Z     = sum(w)

    h_avg            = vec((w' * Hf) ./ Z)
    g_samples[s, :] .= rdf_normalize(h_avg, edges, sys_md)
end

g0   = rdf_normalize(vec(mean(Hf; dims=1)), edges, sys_md)
g_lo = vec(minimum(g_samples; dims=1))
g_hi = vec(maximum(g_samples; dims=1))
```

## Plotting

```julia
r_centers = ustrip.(u"Å", 0.5 .* (edges[1:end-1] .+ edges[2:end]))

fig = Figure()
ax  = Axis(fig[1, 1]; xlabel="r [Å]", ylabel="g(r)",
           title="POPS bounds on Si RDF at 300K")
band!(ax, r_centers, g_lo, g_hi; color=(:blue, 0.3),
      label="min/max bounds (POPS)")
lines!(ax, r_centers, g0; color=:black, label="ridge MLIP", linewidth=0.5)
axislegend(ax; position=:rt)
save("rdf_pops.pdf", fig)
```

**Result.** The black line is the RDF from the ridge trajectory; the blue band
is the min/max envelope over the reweighted RDF ensemble — a direct, physical
visualization of how POPS parameter uncertainty propagates to a measurable
thermodynamic quantity.
