# Geodesics  
*(COMS 4770/5770 Notes)*  
**Yan-Bin Jia**  
**Dec 12, 2024**

---

Geodesics are the curves in a surface that make turns just to stay on the surface and never move sideways. A bug living in the surface and following such a curve would perceive it to be straight. A geodesic is a generalization of the notion of a “straight line’’ from a plane to a surface, on which it represents in some sense the shortest path between two points.

The term *geodesic* comes from geodesy, the science of measuring the earth’s surface. Historically, Bessel and Jacobi studied geodesic curves on ellipsoids.

Geodesics have applications in mechanics, relativity, neurology, statistics, architecture, robotics, image segmentation, and shape analysis.

---

# 1. Definition

A curve \( \gamma(t) \) on a surface \( S \) is called a geodesic if at every point \( \gamma(t) \), the acceleration \( \ddot{\gamma}(t) \) is either zero or parallel to its unit normal \( \hat{n} \).

### Example 1  
A straight line \( \gamma(t) = at + b \) is a geodesic because \( \ddot{\gamma}(t) = 0 \).  
But a reparametrization \( \delta(u) = a \tan u + b \) is *not* a geodesic since  
\[
\ddot{\delta}(u) = -\frac{2\sin u}{\cos^3 u}a \neq 0.
\]

### Mechanical Interpretation  
A particle constrained to move on a surface under a force normal to the surface follows a geodesic.

---

## Proposition 1 — A geodesic has constant speed.

**Proof:**  
\[
\frac{d}{dt} \|\dot{\gamma}\|^2 = 2 \ddot{\gamma}\cdot\dot{\gamma} = 0
\]  
since \( \ddot{\gamma} \) is normal to the surface and \( \dot{\gamma} \) is tangent.  
Thus speed is constant.

---

## Proposition 2 — A curve is a geodesic iff its geodesic curvature is zero.

For unit-speed curve:
\[
\kappa_g = \ddot{\gamma}\cdot (N \times \dot{\gamma}).
\]

Thus:
- Straight lines are geodesics.  
- Rulings of ruled surfaces (cylinders, cones) are geodesics.

### Example 2 — Great Circles  
Intersection of sphere with a plane through the center.  
Curve lies in a normal plane → geodesic curvature zero.

### Example 3 — Cylinders  
Intersection with planes perpendicular to rulings → geodesic.

---

# 2. Geodesic Equations

Surface patch:
\[
\sigma(u,v)
\]

First fundamental form:
\[
Edu^2 + 2F dudv + Gdv^2
\]

A curve \( \gamma(t) = \sigma(u(t), v(t)) \) is a geodesic iff:

\[
\frac{d}{dt}(E\dot{u} + F\dot{v}) = 
\frac{1}{2}(E_u \dot{u}^2 + 2F_u \dot{u}\dot{v} + G_u \dot{v}^2)
\tag{1}
\]

\[
\frac{d}{dt}(F\dot{u} + G\dot{v}) = 
\frac{1}{2}(E_v \dot{u}^2 + 2F_v \dot{u}\dot{v} + G_v \dot{v}^2)
\tag{2}
\]

---

## Example 4 — Geodesics on a Sphere

Spherical coordinates:
\[
\sigma(\theta,\phi) = (\cos\theta\cos\phi, \cos\theta\sin\phi, \sin\theta)
\]

First fundamental form:
\[
d\theta^2 + \cos^2\theta \, d\phi^2
\]

Unit speed condition:
\[
\dot{\theta}^2 + \cos^2\theta\dot{\phi}^2 = 1
\]

Equation (2) gives:
\[
\frac{d}{dt}(\dot{\phi}\cos^2\theta) = 0
\Rightarrow \dot{\phi}\cos^2\theta = C
\]

Thus:
- \(C = 0\): meridians  
- \(C \neq 0\): great circles  

Hence **all geodesics on a sphere are great circles**.

---

## Example 5 — Geodesics on a Circular Cylinder

Parametrization:
\[
\sigma = (a\cos\phi, a\sin\phi, z)
\]

First fundamental form:
\[
E=a^2,\quad F=0,\quad G=1
\]

Geodesics satisfy:
\[
\frac{dz}{d\phi} = D_1 \Rightarrow z = D_1\phi + D_2
\]

Thus **geodesics are helices**.

---

# Theorem 4 — Existence & Uniqueness

For any point \(p\) and tangent direction \( \hat{t} \), there exists a **unique unit-speed geodesic**.

---

# 3. Preservation of Geodesics Under Isometry

An isometry \(f: S_1 \to S_2\) preserves lengths.  
Therefore it preserves geodesics.

### Example 6 — Cylinder isometric to a strip

Flat strip:
\[
\sigma_1(u,v) = (u,v,0)
\]

Cylinder:
\[
\sigma_2(u,v) = (\cos u, \sin u, v)
\]

Both have first fundamental form \(du^2 + dv^2\).

---

# Theorem 5  
If \(f\) is an isometry, then \(f(\gamma)\) is geodesic whenever \(\gamma\) is.

### Example 7  
Lines on strip → helices on cylinder → geodesics.

---

# 4. Geodesics vs Shortest Paths

**Theorem 6:**  
Every shortest path on a surface is a geodesic.

Counterexample:  
On a sphere, two geodesic arcs between same endpoints → only shorter arc is shortest path.

### No shortest path example  
Plane with origin removed → no shortest path from (-1,0) to (1,0).

### Shortest path existence  
If surface is a *closed subset* of \( \mathbb{R}^3 \), shortest paths exist.

---

# 5. Geodesic Coordinates

Construct coordinates using geodesics.

Given a point \(p\) and a geodesic \( \gamma(v) \):  
Define \( \beta_v(u) \) as the perpendicular geodesic at each point.

Patch:
\[
\sigma(u,v) = \beta_v(u)
\]

### Example 8 — Sphere  
Latitude and longitude form geodesic coordinates.

---

# References

1. P. N. Atkar et al. *Uniform coverage of automotive surface patches*.  
2. J. McCleary. *Geometry from a Differentiable Viewpoint*.  
3. B. O’Neill. *Elementary Differential Geometry*.  
4. G. Peyré et al. *Geodesic methods in computer vision and graphics*.  
5. A. Pressley. *Elementary Differential Geometry*.
